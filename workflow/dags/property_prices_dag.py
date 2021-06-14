"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.python_operator import PythonVirtualenvOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 6, 9),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    'schedule_interval': '@daily',
    'concurrency': 1,
    'max_active_runs': 1,
}

dag = DAG('property_prices_dag', default_args=default_args)


def geography_downloader_run(execution_date, **kwargs):
    import requests
    import shutil
    import zipfile
    import os
    from pathlib import Path

    download_geography_data_url = "https://api.os.uk/downloads/v1/products/OpenNames/downloads?area=GB&format=CSV&redirect"
    zipped_file_name = "opname_csv_gb.zip"
    execution_date_path = f"{execution_date}"
    data_path = "/opt/airflow/data/bronze"
    full_dir = Path(f'{data_path}/{execution_date_path}/')
    full_dir.mkdir(parents=True, exist_ok=True)

    def download_file(url: str, file_name: str):
        with requests.get(url, stream=True) as r:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        print("download_file")

    def unzip_file(output_dir: str, file_name: str):
        with zipfile.ZipFile(file_name, "r") as zip_ref:
            zip_ref.extractall(f"{output_dir}{file_name.split('.')[0]}")

    def remove_zip_file(file_name: str):
        if os.path.isfile(file_name):
            os.remove(file_name)
        else:
            print(f"file doesnt exist {file_name}")

    download_file(download_geography_data_url, zipped_file_name)
    unzip_file(full_dir, zipped_file_name)
    remove_zip_file(zipped_file_name)


def get_rightmove_prices_run(execution_date, **kwargs):
    print(" get_rightmove_prices_run")
    from rightmove_webscraper import RightmoveData
    from pathlib import Path

    rightmove_url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94346"
    execution_date_path = f"{execution_date}"
    data_path = "data/bronze"
    table_name = "property.csv"
    full_dir = Path(f'{data_path}/{execution_date_path}/{table_name}')
    full_dir.mkdir(parents=True, exist_ok=True)

    rm = RightmoveData(rightmove_url)
    df_property_prices = rm.get_results
    df_property_prices.to_csv(f"{full_dir}")


def silver_geography_dimension_run(execution_date, **kwargs):
    execution_date_path = f"{execution_date}/"
    print(f"silver_geography_dimension {execution_date_path}")


geography_downloader = PythonVirtualenvOperator(
    task_id='geography_downloader',
    python_callable=geography_downloader_run,
    requirements=["requests==2.22.0", "pandas"],
    system_site_packages=False,
    provide_context=True,
    op_kwargs={'execution_date': '{{ execution_date }}', },
    dag=dag)

get_rightmove_prices = PythonVirtualenvOperator(
    task_id='get_rightmove_prices',
    python_callable=get_rightmove_prices_run,
    requirements=["rightmove-webscraper", "requests==2.22.0", "pandas"],
    system_site_packages=False,
    provide_context=True,
    op_kwargs={'execution_date': '{{ execution_date }}', },
    dag=dag)

# need to put sensors here
silver_geography_dimension = PythonVirtualenvOperator(
    task_id='silver_geography_dimension',
    python_callable=silver_geography_dimension_run,
    requirements=["pandas"],
    system_site_packages=False,
    provide_context=True,
    op_kwargs={'execution_date': '{{ execution_date }}', },
    dag=dag)

# check if file exists, if not download
geography_downloader.set_downstream([get_rightmove_prices, silver_geography_dimension])
