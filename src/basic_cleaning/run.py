#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd 


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    logger.info("Downloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_local_path = artifact.file()
    df = pd.read_csv(artifact_local_path)

    # Clean artifact
    # Drop outliers
    logger.info("Cleaning features")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Write cleaned version
    logger.info("Logging artifact")
    filename = args.output_artifact
    df.to_csv(filename, index=False)

    # Save cleaned artifact
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
    )
    artifact.add_file(filename)
    run.log_artifact(artifact)

    os.remove(filename)
    logger.info("Finished logging artifact")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Cleaning the data")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )

    parser.add_argument(
        "--output_artifact", 
        type=str, 
        help="Name for the produced artifact", 
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
         help="Type for the artifact", 
         required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Min price",
        required=True,
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Max price",
        required=True,
    )

    args = parser.parse_args()

    go(args)
