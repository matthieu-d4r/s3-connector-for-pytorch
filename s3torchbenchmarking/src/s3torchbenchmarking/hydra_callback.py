#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  // SPDX-License-Identifier: BSD

import json
import logging
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any, Union, Optional

import requests
import torch
from hydra.experimental.callback import Callback
from omegaconf import DictConfig

import s3torchconnector
from s3torchbenchmarking.constants import (
    JOB_RESULT_FILENAME,
    COLLATED_RESULTS_FILENAME,
    Run,
    EC2Metadata,
)

logger = logging.getLogger(__name__)


class ResultCollatingCallback(Callback):
    """Hydra callback.

    Defines some routines to execute when a benchmark run is finished: namely, to merge all job results
    ("results.json" files) in one place ("collated_results.json" file).
    """

    def __init__(self) -> None:
        self._multirun_dir: Optional[Path] = None
        self._begin = 0

    def on_multirun_start(self, config: DictConfig, **kwargs: Any) -> None:
        self._begin = perf_counter()

    def on_job_start(self, config: DictConfig, **kwargs: Any) -> None:
        if not self._multirun_dir:
            # Hydra variables like `hydra.runtime.output_dir` are not available inside `on_multirun_end`, so we collect
            # the information here and refer to it later.
            self._multirun_dir = Path(config.hydra.runtime.output_dir).parent

    def on_multirun_end(self, config: DictConfig, **kwargs: Any) -> None:
        run_elapsed_time = perf_counter() - self._begin

        collated_results = self._collate_results(config, run_elapsed_time)
        collated_results_path = self._multirun_dir / COLLATED_RESULTS_FILENAME

        logger.info("Saving collated results to: %s", collated_results_path)
        with open(collated_results_path, "w") as f:
            json.dump(collated_results, f, ensure_ascii=False, indent=2)
        logger.info("Collated results saved successfully")

    def _collate_results(self, config: DictConfig, run_elapsed_time: float) -> Run:
        collated_results = []
        for file in self._multirun_dir.glob(f"**/{JOB_RESULT_FILENAME}"):
            collated_results.append(json.loads(file.read_text()))

        logger.info("Collated %i result files", len(collated_results))
        return {
            "run_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).timestamp(),
            "scenario": config.hydra.job.name,
            "versions": {
                "python": sys.version,
                "pytorch": torch.__version__,
                "hydra": config.hydra.runtime.version,
                "s3torchconnector": s3torchconnector.__version__,
            },
            "ec2_metadata": _get_ec2_metadata(),
            "run_elapsed_time_s": run_elapsed_time,
            "number_of_jobs": len(collated_results),
            "collated_results": collated_results,
        }


def _get_ec2_metadata() -> Union[EC2Metadata, None]:
    """Get some EC2 metadata.

    See also https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html#instancedata-inside-access.
    """
    r = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")

    if r.status_code == 200:
        payload = r.json()
        return {
            "architecture": payload["architecture"],
            "image_id": payload["imageId"],
            "instance_type": payload["instanceType"],
            "region": payload["region"],
        }
    return None
