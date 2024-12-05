#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  // SPDX-License-Identifier: BSD

from typing import TypedDict, Union, Any, List

JOB_RESULT_FILENAME = "results.json"
COLLATED_RESULTS_FILENAME = "collated_results.json"


class Versions(TypedDict):
    python: str
    pytorch: str
    hydra: str
    s3torchconnector: str


class EC2Metadata(TypedDict):
    architecture: str
    image_id: str
    instance_type: str
    region: str


class Run(TypedDict):
    run_id: str
    timestamp: float
    scenario: str
    versions: Versions
    ec2_metadata: Union[EC2Metadata, None]
    run_elapsed_time_s: float
    number_of_jobs: int
    collated_results: List[Any]
