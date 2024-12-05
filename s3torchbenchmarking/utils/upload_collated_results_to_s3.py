#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  // SPDX-License-Identifier: BSD

import argparse
import logging
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

COLLATED_RESULTS_FILENAME = "collated_results.json"

logger = logging.getLogger()
s3_client = boto3.client("s3")


def upload_results(results_dir: str, bucket: str, prefix: str) -> None:
    for file in Path(results_dir).glob(f"**/{COLLATED_RESULTS_FILENAME}"):
        key = f"{prefix}/{file.parent}"
        upload_file_to_s3(file, bucket, key)


def upload_file_to_s3(filename: str, bucket: str, key: str) -> None:
    try:
        logger.info("Uploading %s to %s/%s...", filename, bucket, key)
        s3_client.upload_file(filename, bucket, key)
        logger.info("Uploaded %s to %s/%s successfully", filename, bucket, key)
    except ClientError:
        logger.error("Failed to upload %s to %s/%s", filename, bucket, key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("results_dir", help="directory where the results are stored")
    parser.add_argument("bucket", help="S3 bucket where to upload the results")
    parser.add_argument(
        "prefix", help="S3 prefix to use (i.e., the scenario the results are from)"
    )

    args = parser.parse_args()

    upload_results(args.results_dir, args.bucket, args.prefix)
