import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    service_type = kwargs.get('service_type')
    year = kwargs.get('year')
    month = kwargs.get('month')
    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{service_type}_tripdata_{year:04d}-{month:02d}.parquet'
    df = pd.read_parquet(input_file)

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'