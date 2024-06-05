# 3.2 Training: sklearn and XGBoost models


## Training pipeline for sklearn models

### 3.2.1 Reusable training set

[![](https://markdown-videos-api.jorgenkh.no/youtube/KP68DuJnk4Q)](https://youtu.be/KP68DuJnk4Q&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=10)

- utilising the Global Data Products to re-run `data_preparation` pipeline if training data is older than 10 minutes (600 seconds)
- from the breadcrumb `mlops > unit_2_training > Pipelines`, click on the Global Data Products item with following input:
  - UUID = Training set
  - Object type = Pipeline
  - Object UUID = data_preparation
- the above step can get fiddly, we can also simply copy+paste the `global_data_products.yaml` file from `unit_3_observability` but change the following lines:

    ```
    project: unit_2_training
    repo_path: /home/src/mlops/unit_2_training
    settings:
    build:
        partitions: 1
    ```

### 3.2.2 Create sklearn Pipeline

[![](https://markdown-videos-api.jorgenkh.no/youtube/CbHaZcq_uGo)](https://youtu.be/CbHaZcq_uGo&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=11)

- create new Pipeline = `sklearn training`
- create our first block to add the above GDP


### 3.2.3 Load models

[![](https://markdown-videos-api.jorgenkh.no/youtube/zsMHFq2C978)](https://youtu.be/zsMHFq2C978&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=12)

- create a `Custom` block and set it to dynamic as it can variable create 2 models or 6 models
- make it `Dynamic` from the `more actions` menu
- don't forget to add notes if necessary using Markdown blocks


### 3.2.4 Utility helper functions

[![](https://markdown-videos-api.jorgenkh.no/youtube/fZnxDhtPxYo)](https://youtu.be/fZnxDhtPxYo&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=13)

- create a Transformer block, name it `hyperparameter_tuning/sklearn`
- before we can run this block however, it depends on some utilities, let's create those first
- in `mlops/utils`, copy+paste the following code blocks / files

### Code

> [!TIP]
>
> Any code in `mlops/utils` that is in a subfolder need an empty `__init__.py` file so the code is picked up by `import` statements

-   [`utils/hyperparameters/shared.py`](https://github.com/mage-ai/mlops/blob/master/mlops/utils/hyperparameters/shared.py)
-   [`utils/models/sklearn.py`](https://github.com/mage-ai/mlops/blob/master/mlops/utils/models/sklearn.py)

### 3.2.5 Hyperparameter tuning

[![](https://markdown-videos-api.jorgenkh.no/youtube/zfBB4KoZ7TM)](https://youtu.be/zfBB4KoZ7TM&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=14)

- copy+paste the Transformer code block
- connect to the 2 blocks we have before, make sure you connect it in the same sequence so that the positional arguments are set as follows. Since they are *positional arguments*, the sequence in the code matters.

    ```python
    @transformer

    def transform(data, data_2):

        data → training_set
        data_2 → load_models
    ```
- add `Variables` into the Block's Global Variable panel (3rd button down from the top, below the Tree icon)
  - max_evaluations = 50 

    1. *set to 1 first for initial testing out the setups*; 
    1. *edit it to 50 later when all is good*
  - random_state = 7
- make sure to press `ENTER` so the variable names turn `Green` which indicates the vars are now Saved, since there's no explicit Save button in this panel. In this image, `random_state` has been saved, but `max_evaluations` wasn't yet.
![](../../images/3.2.5%20global%20vars%20panel.png)

- at the end of this video, the Tree looks like
![](../../images/3.2.5%20transformer%20connections.png)


### Code

-   [`transformers/hyperparameter_tuning/sklearn.py`](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/transformers/hyperparameter_tuning/sklearn.py)

### 3.2.6 Train sklearn model

[![](https://markdown-videos-api.jorgenkh.no/youtube/P7PtegUFk3k)](https://youtu.be/P7PtegUFk3k&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=14)

### Code

-   [`custom/load_models.py` block](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/custom/load_models.py): load sklearn models dynamically

-   [`data_exporters/sklearn.py`](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/data_exporters/sklearn.py)


---

## Training pipeline for XGBoost model

### Videos

1. [Hyperparameter tuning](https://youtu.be/K_Z2Lm1Cyu4)
1. [Train XGBoost model](https://youtu.be/Y2B-ivm7Mug)

### Code

-   [`utils/models/xgboost.py`](https://github.com/mage-ai/mlops/blob/master/mlops/utils/models/xgboost.py)
-   [`transformers/hyperparameter_tuning/xgboost.py`](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/transformers/hyperparameter_tuning/xgboost.py)
-   [`data_exporters/xgboost.py`](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/data_exporters/xgboost.py)
-   [`hyperparameters/shared.py`](https://github.com/mage-ai/mlops/blob/master/mlops/utils/hyperparameters/shared.py)

---

## Code

1. [Complete code solution](https://github.com/mage-ai/mlops)
1. [sklearn training pipeline configuration](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/pipelines/sklearn_training/metadata.yaml)
1. [XGBoost training pipeline configuration](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/pipelines/xgboost_training/metadata.yaml)

---

## Resources

1. [Accuracy, precision, recall](https://www.mage.ai/blog/definitive-guide-to-accuracy-precision-recall-for-product-developers)

1. [Regression model performance metrics](https://www.mage.ai/blog/product-developers-guide-to-ml-regression-model-metrics)
