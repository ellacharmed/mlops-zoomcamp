import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    service_type = kwargs.get('service_type')
    year = kwargs.get('year')
    month = kwargs.get('month')
    output_file = f'/home/src/hmwk4/data/{service_type}_{year:04d}-{month:02d}.parquet'

    data.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

    print(f'output file saved to {output_file}')
