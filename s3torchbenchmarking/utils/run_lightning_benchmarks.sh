#!/usr/bin/env bash
#
# Run PyTorch Lightning Checkpointing benchmarks.

set -euo pipefail

if [[ $# -lt 2 ]]; then
    echo 'Minimum number of arguments (2) not provided'
    exit 1
fi

region=$1
table=$2
nvme_dir="./nvme/" # local path for saving checkpoints

# Prepare NVMe drive mount (if required)
./utils/prepare_nvme.sh $nvme_dir

# Run benchmarks
python ./src/s3torchbenchmarking/lightning_checkpointing/benchmark.py -cd conf -cn lightning_checkpointing path=$nvme_dir

# Write (collated) benchmark results to a DynamoDB table
python ./utils/collect_and_write_to_dynamodb.py ./multirun/ "$region" "$table"
