import argparse
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="A script to prepare datasets, run benchmarks, and upload the results to S3",
        epilog="Example of use: python script.py ./multirun pytorch-benchmarks-results 20240810")
    parser.add_argument('dataloader', type=str, help="the dataloader to benchmark")
    parser.add_argument('datasets_path', type=Path, help="the path to the datasets")
    parser.add_argument('bucket', type=str, help="the bucket to upload the datasets to")
    parser.add_argument('region', type=str, help="the region to upload the datasets to")
    parser.add_argument('results_bucket', type=str, help="the bucket to upload the results to")
    parser.add_argument('results_region', type=str, help="the region to upload the results to")
    parser.add_argument('results_prefix', type=str, help="the prefix to upload the results to")
