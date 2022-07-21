# Project Description

In this project, we are working for a property management company renting rooms and properties for short periods of 
time on various rental platforms. We estimate the typical price for a given property based 
on the price of similar properties. The company receives new data in bulk every week. The model needs 
to be retrained with the same cadence, necessitating an end-to-end pipeline that can be reused.

The present repo builds that pipeline

# Link to pipeline records and outputs in Weights and Biases

We use the weights and biases API to store model outputs (eg mean absolute error scores for different models)

Here is the link to the public weights and biases project: [https://wandb.ai/rebeccaj/nyc_airbnb](https://wandb.ai/rebeccaj/nyc_airbnb)

# Order to run

1. Create a virtual env using our preferred specifications and activate that environment

```bash
> conda env create -f environment.yml
> conda activate nyc_airbnb_dev
```

2a. To run the full pipeline locally, run the following command in terminal (mlflow is installed via the environment.yml step)

```bash
>  mlflow run .
```

2b. To run the full pipeline using a specific release stored in the remote repo with new data, run the following command in terminal:

```bash
> mlflow run https://github.com/rebeccajohnson88/udacity_rentalpricepredict.git \
             -v {insert version number} \
             -P hydra_options={key with new data in config.yaml file}"
```

2c. To run specific steps in the pipeline, use hydra_options to specify that step. Eg if we just want to run the download or download + data_cleaning step, we can run the below. 

```bash
> mlflow run . -P steps=download
```

```bash
> mlflow run . -P steps=download,basic_cleaning
```

If running step by step, the steps should be run in the following order:

1. `download`
2. `basic_cleaning`
3. `data_check`
4. `data_split`
5. `train_[random_forest|gradient_boosting]`
6. `test_regression_model`: note that before running these steps, you need to go the Weights and Biases interface and tag one of the models with the `:prod` qualifier to indicate it's the best-performing model and should be used in production



## License

[License](LICENSE.txt)
