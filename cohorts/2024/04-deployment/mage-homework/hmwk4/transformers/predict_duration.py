import pandas as pd
import pickle

# from hmwk4.models 

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

with open('hmwk4/models/model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    print('y_pred done')

    preds_std = y_pred.std()
    preds_mean = y_pred.mean()
    print(f"month: {kwargs.get('month')}")
    print(f"std: {preds_std}")
    print(f"mean: {preds_mean}")

    service_type = kwargs.get('service_type')
    year = kwargs.get('year')
    month = kwargs.get('month')
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predictions'] = y_pred.tolist()
    # print(f'df_result done')

    return df_result

