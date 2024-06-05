# 3.1 Data preparation: ETL and feature engineering

## Ingestion

Our demo `mlops` project utilises sub-projects `unit_0*` .. `unit_5*` to build up our orchestration from initial setup to deployment. See [Resources](#resources) for documentation on **Multiverse-projects**.

The sub-projects are isolated environments (since we can only `register` one project at a time to be `active`). So unit_2 has no visibility of unit_3 files.

### 3.1.1 Creating a new Mage project

[![](https://markdown-videos-api.jorgenkh.no/youtube/7hKrQmoARD8)](https://youtu.be/7hKrQmoARD8&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=2)


1. Opening a text editor:

   - Go to the command center (At the top)
   - Instructor (Tommy) uses MacOS (I presume), so shortcut key is `CMD+period`. On Windows, the equivalent is `CTRL+WIN+period`
   - Type "text editor"

1. Right click at the top level `mlops` Main project and select `New Mage Project`.

1. In the dialog, input `unit_1_data_preparation`, click `Create Project` and close the Text Editor. Outcome is new folder in the Explorer Tree and new line in the **Projects list** drop down.

1. Register this project:

   - Go to the top level `mlops` Mage project
   - Click Settings. Breadcrumb should now show `mlops > unit_1_data_preparation > Settings`
   - Click on `+ Register` button on the right. This would generate a randomly named project. 
   - Edit this name to the one we created, input a **Description** if desired
   - When you enable this as the `Currently selected project`, any previous active projects would be unselected.
   - Click on `Save Settings` button and return to Project's Overview screen.


### 3.1.2 Data preparation - Ingestion

[![](https://markdown-videos-api.jorgenkh.no/youtube/1lSOdTpoRug)](https://youtu.be/1lSOdTpoRug&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=3)


1. Copy code from:

   - [`ingest.py`](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/data_loaders/ingest.py)

1. This first ingest block pulls in raw data from the Yellow service taxi file for the first 2 months of 2024. 
   - *note*: URI is to Mage's dataset's repo, not NYC taxi website; 
   - adjust accordingly for homework

1. Click on the play button (or `CMD/CTRL+Enter`) to run the block. 

1. You can also run blocks from the Tree view when you right-click on them.


### 3.1.3 Utility helper functions

We'll be utilising helper functions so we follow DRY (Don't Repeat Yourself) guidelines. 

> [!CAUTION]
> 
> There only need be ONE `mlops/utils`; not individual `mlops/unit_#_sub_project/utils`

1. Copy code from:

- [`cleaning.py`](https://github.com/mage-ai/mlops/blob/master/mlops/utils/data_preparation/cleaning.py)
- [`feature_engineering.py`](https://github.com/mage-ai/mlops/blob/master/mlops/utils/data_preparation/feature_engineering.py)
- [`feature_selector.py`](https://github.com/mage-ai/mlops/blob/master/mlops/utils/data_preparation/feature_selector.py)
- [`splitters.py`](https://github.com/mage-ai/mlops/blob/master/mlops/utils/data_preparation/splitters.py)


[![](https://markdown-videos-api.jorgenkh.no/youtube/FBh3P19lXj4)](https://youtu.be/FBh3P19lXj4&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=4)

Back in our `data_preparation` pipeline,

1. Create a time series chart.
   - Choose a date time column.
   - Do a count of each row per pickup date.

1. Add a few more pre-templated charts.
   - See the missing values.
   - See the unique values.
   - See the most frequent values.

1. Input these `global variables` in the Pipeline --> Edit screen, don't forget to press ENTER so the vars turn green to show it has been save since there's no SAVE button

   - split_on_feature: lpep_pickup_datetime
   - split_on_feature_value: 2024-02-01
   - target: duration


## Data Preparation

### 3.1.4 Data preparation block

[![](https://markdown-videos-api.jorgenkh.no/youtube/TcTMVn3BxeY)](https://youtu.be/TcTMVn3BxeY&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=5)

Before we add a Transform Block, we'll add some more utility functions to help us perform these steps:

- clean our dataset:
  - set datetime from `str` to `pd.datetime`
  - calculate `duration` in minutes by taking the timedelta of dropoff and pickup
  - remove the outliers
  - make the `PULocationID` and `DOLocationID` as categorical data types
- feature-engineer the `PULocationID` and `DOLocationID` into `PU_DO`
- split our dataset into train and val according to the `split_on_feature_value` = `2024-02-01` set in Global Variables
- set our target for predictions as the `duration` column


### 3.1.5 Visualize prepared data

[![](https://markdown-videos-api.jorgenkh.no/youtube/j0Hfaoc5wRY)](https://youtu.be/j0Hfaoc5wRY&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=6)

Mage has some built-in EDA features from `Add Charts` button. 

- create a Time Series Bar chart, use code added as per [FAQ](https://docs.google.com/document/d/12TlBfhIiKtyBv8RnsoJR6F72bkPDGEvPOItJIxaEzE0/edit#heading=h.uhb09q64puph)

  > import numpy as np
  >
  > df['lpep_pickup_epoch'] = df['lpep_pickup_datetime'].astype(np.int64) // 10**9

- create various other charts from the drop down as per video, use the `custom histogram code` linked below

### Code

-  [`prepare.py`](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/transformers/prepare.py)
-  [`custom histogram code`](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/charts/prepare_histogram_u9.py)

---

## Build training sets


### 3.1.6 Encoding functions
[![](https://markdown-videos-api.jorgenkh.no/youtube/z8erMV-6joY)](https://youtu.be/z8erMV-6joY&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=7)

- using DictVectorizer to encode our categorical feature-engineered `PU_DO` into a sparse matrix, just like in module-01 Intro.

### 3.1.7 Training set block

[![](https://markdown-videos-api.jorgenkh.no/youtube/qSzcfSHjJoY)](https://youtu.be/qSzcfSHjJoY&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=8)

- in this `build` Data Exporter block, we are finally vectorizing our selected features using DictVectorizer and splitting into `_train`,  `_val`, for the `X` and `y` datasets 
- in the next pipeline we will train with sklearn using Linear Regression.

### Code

-   [`encoders.py`](https://github.com/mage-ai/mlops/blob/master/mlops/utils/data_preparation/encoders.py)
-   [`build.py`](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/data_exporters/build.py)

---

## Data validations using built-in testing framework


### 3.1.8 Writing data validations
[![](https://markdown-videos-api.jorgenkh.no/youtube/tYPAl4Q8kpw)](https://youtu.be/tYPAl4Q8kpw&list=PL_ItKjYd0DsiUpEzPQqYM04O6jQTkCjTN&index=9)

- we can also write unit tests in our blocks
- in this demo, the logic is using hardcoded values to validate the expected shape of our returned datasets ie the number of rows and columns

### Code

-   [`build.py`](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/data_exporters/build.py)

---

## Code

1. [Complete code solution](https://github.com/mage-ai/mlops)
1. [Pipeline configuration](https://github.com/mage-ai/mlops/blob/master/mlops/unit_3_observability/pipelines/data_preparation/metadata.yaml)

---

## Resources

1. [Multiverse Projects](https://docs.mage.ai/platform/projects/management)

1. [Global Data Products](https://docs.mage.ai/orchestration/global-data-products/overview)

1. [Data validations using built-in testing framework](https://docs.mage.ai/development/data-validation)

1. [Data quality checks with Great Expectations integration](https://docs.mage.ai/development/testing/great-expectations)

1. [Unit tests](https://docs.mage.ai/development/testing/unit-tests)

1. [Feature encoding](https://www.mage.ai/blog/qualitative-data)
