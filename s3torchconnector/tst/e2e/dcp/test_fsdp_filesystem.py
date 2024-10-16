#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  // SPDX-License-Identifier: BSD

import pytest
import torch
import torch.distributed.checkpoint as dcp
from torch.distributed.checkpoint import CheckpointException

from s3torchconnector import S3DPWriter
from s3torchconnector.dcp.fsdp_filesystem import S3FS


def test_fsdp_filesystem_when_single_thread(image_directory):
    s3fs = S3FS(image_directory.region)

    with s3fs.create_stream(image_directory.s3_uri, "rb") as s3_reader:
        s3_reader

    pass


def test_fsdp_filesystem_when_multiple_threads(checkpoint_directory):
    s3fs = S3FS(checkpoint_directory.region)
    pass


# Inspired from https://github.com/pytorch/pytorch/blob/main/test/distributed/checkpoint/test_fsspec.py.
def test_overwrite(image_directory):
    t1, t2 = torch.randn(10), torch.randn(10)
    region = image_directory.region
    s3_uri = image_directory.s3_uri

    dcp.save(
        {"random": t1}, storage_writer=S3DPWriter(region, s3_uri, overwrite=False)
    )
    dcp.save(
        {"random": t2}, storage_writer=S3DPWriter(region, s3_uri, overwrite=True)
    )

    sd = {"random": torch.zeros(10)}
    dcp.load(sd, checkpoint_id=s3_uri)
    assert torch.allclose(sd["random"], t2) is True

    with pytest.raises(CheckpointException) as excinfo:
        dcp.save(
            {"random": t2},
            storage_writer=S3DPWriter(region, s3_uri, overwrite=False)
        )

    assert "Checkpoint already exists" in str(excinfo.value)
