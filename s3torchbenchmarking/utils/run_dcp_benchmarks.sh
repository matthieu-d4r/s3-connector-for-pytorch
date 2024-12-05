#!/usr/bin/env bash
#
# Run PyTorch’s Distributed Checkpointing (DCP) benchmarks.

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
python ./src/s3torchbenchmarking/dcp/benchmark.py -cd conf -cn dcp path=$nvme_dir

# Write (collated) benchmark results to a DynamoDB table
python ./utils/collect_and_write_to_dynamodb.py ./multirun/ "$region" "$table"
