import argparse

from omegaconf import DictConfig

from s3torchbenchmarking.benchmark import run_experiment


# for dataset in "${datasets[@]}"; do
#     if [[ "$dataset" == *"shards"* ]]; then
#         s3torch-benchmark -cd conf -m -cn dataloading_sharded_vit "dataset=$dataset" "dataloader=$DATALOADER"
#         s3torch-benchmark -cd conf -m -cn dataloading_sharded_ent "dataset=$dataset" "dataloader=$DATALOADER"
#     else
#         s3torch-benchmark -cd conf -m -cn dataloading_unsharded_1epochs "dataset=$dataset" "dataloader=$DATALOADER"
#         s3torch-benchmark -cd conf -m -cn dataloading_unsharded_vit_10epochs "dataset=$dataset" "dataloader=$DATALOADER"
#         s3torch-benchmark -cd conf -m -cn dataloading_unsharded_ent_10epochs "dataset=$dataset" "dataloader=$DATALOADER"
#     fi
# done

def run_dataloading_benchmarks(dataloader: str, datasets: [str]):
    for dataset in datasets:
        if "shards" in dataset:
            run_experiment()
        else:
            run_experiment()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dataloader', type=str, help='the dataloader to benchmark')
    parser.add_argument('datasets', nargs='+', type=str, help='the dataset(s) to use')

    args = parser.parse_args()
    run_dataloading_benchmarks(args.dataloader, args.datasets)
