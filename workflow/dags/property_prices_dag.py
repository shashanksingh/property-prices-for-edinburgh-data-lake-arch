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
    'concurrency': 10,
    'max_active_runs': 5,
}

dag = DAG('property_prices_dag', default_args=default_args)


def geography_downloader_run(execution_date, **kwargs):
    import requests
    import shutil
    import zipfile
    import os

    download_geography_data_url = "https://api.os.uk/downloads/v1/products/OpenNames/downloads?area=GB&format=CSV&redirect"
    LOCAL_FILE_NAME = "opname_csv_gb.zip"
    EXECUTION_DATE = f"{execution_date}/"
    DATA_FOLDER = "/opt/airflow/data/bronze/"

    def download_file(url: str, file_name: str):
        with requests.get(url, stream=True) as r:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    def unzip_file(file_name: str):
        with zipfile.ZipFile(file_name, "r") as zip_ref:
            zip_ref.extractall(f"{DATA_FOLDER}{EXECUTION_DATE}{LOCAL_FILE_NAME.split('.')[0]}")

    def remove_zip_file(file_name: str):
        if os.path.isfile(file_name):
            os.remove(file_name)
        else:
            print(f"file doesnt exist {file_name}")

    try:
        download_file(download_geography_data_url, LOCAL_FILE_NAME)
        unzip_file(LOCAL_FILE_NAME)
        remove_zip_file(LOCAL_FILE_NAME)
    except requests.exceptions.RequestException as e:
        print(e)


def get_rightmove_prices_run(execution_date, **kwargs):
    print(" get_rightmove_prices_run")
    import rightmove_webscraper


    rightmove_url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94346"
    EXECUTION_DATE = f"{execution_date}/"
    DATA_FOLDER = "data/bronze/"
    TABLE_NAME = "property.csv"
    rm = rightmove_webscraper.rightmove_data(rightmove_url)
    df_property_prices = rm.get_results
    df_property_prices.to_csv(f"{DATA_FOLDER}{EXECUTION_DATE}{TABLE_NAME}")


def silver_geography_dimension_run(execution_date, **kwargs):
    print("silver_geography_dimension")
    import silver_geography_dimension
    silver_geography_dimension.run()


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

geography_downloader >> get_rightmove_prices >> silver_geography_dimension
