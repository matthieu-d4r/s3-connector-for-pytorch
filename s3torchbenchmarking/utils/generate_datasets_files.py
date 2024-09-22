import argparse
from pathlib import Path

import yaml


def build_yaml_files(path_to_datasets: Path, bucket: str, region: str, datasets: [str]):
    for dataset in datasets:
        data = {
            "prefix_uri": f"s3://{bucket}/{dataset}",
            "region": region,
            "sharding": "TAR" if "shards" in dataset else "null",
        }
        yaml.dump(data, path_to_datasets / f'{dataset}.yaml')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_datasets', type=Path, help='the path to the YAML dataset files')
    parser.add_argument('bucket', type=str, help='the S3 bucket')
    parser.add_argument('region', type=str, help='the S3 region')
    parser.add_argument('datasets', nargs='+', type=str, help='the list of datasets')

    args = parser.parse_args()
    build_yaml_files(args.datasets_path, args.bucket, args.region, args.datasets)
