import argparse
import datetime
import json
import logging
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

DEFAULT_RESULT_FILENAME = "collated_results.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upload_file_to_s3(result_file: Path, bucket: str, key: str) -> None:
    s3_client = boto3.client("s3")
    try:
        logger.info(f"Uploading {result_file} to {bucket}/{key}...")
        s3_client.upload_file(result_file, bucket, key)
        logger.info(f"Uploaded {result_file} to {bucket}/{key}")
    except ClientError:
        logger.exception(f"Error uploading {result_file} to {bucket}/{key}")


def traverse_folders(local_result_folder: str, bucket: str, prefix: str) -> None:
    def extract_dataloader(file: Path) -> str:
        """Extract the dataloader name from within the JSON result file."""
        with open(file) as f:
            data = json.load(f)
            return data[0]["cfg"]["dataloader"]["kind"]

    dataloader = ""
    for result_file in Path(local_result_folder).rglob(DEFAULT_RESULT_FILENAME):
        dataloader = dataloader or extract_dataloader(result_file)
        key = f"{prefix}/{dataloader}_{result_file.parent.name}_{result_file.name}"
        upload_file_to_s3(result_file, bucket, key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script to upload benchmark result files to S3",
        epilog="Example of use: python script.py ./multirun pytorch-benchmarks-results 20240810")
    parser.add_argument('local_result_folder', type=Path, help='the local folder the results are located in')
    parser.add_argument('bucket', type=str, help='the S3 bucket to upload the results to')
    parser.add_argument('prefix', nargs='?', default=datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ"),
                        type=str, help='the S3 prefix to use')

    args = parser.parse_args()
    traverse_folders(args.local_result_folder, args.bucket, args.prefix)
