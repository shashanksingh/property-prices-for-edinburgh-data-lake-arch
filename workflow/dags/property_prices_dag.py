"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from typing import List

from airflow import DAG
from airflow.operators.python_operator import PythonVirtualenvOperator
from airflow.operators.dummy_operator import DummyOperator
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
    'schedule_after_task_execution': False,
}


def geography_downloader_run(execution_date, **kwargs):
    import requests
    import shutil
    import zipfile
    import os
    import logging
    from pathlib import Path

    download_geography_data_url = "https://api.os.uk/downloads/v1/products/OpenNames/downloads?area=GB&format=CSV&redirect"
    zipped_file_name = "opname_csv_gb.zip"
    execution_date_path = f"{execution_date}"
    data_path = "/opt/airflow/data/bronze"
    full_dir = Path(f'{data_path}/{execution_date_path}/')
    full_dir.mkdir(parents=True, exist_ok=True)

    def is_file_exists(output_dir: str, file_name: str) -> bool:
        return Path(f"{output_dir}/{file_name.split('.')[0]}").exists()

    def download_file(url: str, file_name: str):
        with requests.get(url, stream=True) as r:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        logging.info("download_file")

    def unzip_file(output_dir: str, file_name: str):
        with zipfile.ZipFile(file_name, "r") as zip_ref:
            zip_ref.extractall(f"{output_dir}/{file_name.split('.')[0]}")

    def remove_zip_file(file_name: str):
        if os.path.isfile(file_name):
            os.remove(file_name)
        else:
            logging.info(f"file doesnt exist {file_name}")

    def make_success_file(output_dir: str):
        success_file = f"{output_dir}/_SUCCESS"
        Path(success_file).touch()

    if not is_file_exists(full_dir, zipped_file_name):
        download_file(download_geography_data_url, zipped_file_name)
        unzip_file(full_dir, zipped_file_name)
        remove_zip_file(zipped_file_name)
    make_success_file(full_dir)


def get_rightmove_prices_run(execution_date, region_code, **kwargs):
    from rightmove_webscraper import RightmoveData
    from pathlib import Path
    import logging
    # region_code = kwargs['region_code']

    logging.info(" get_rightmove_prices_run")
    rightmove_url = f"https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=POSTCODE^{region_code}&radius=5.0&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords="
    execution_date_path = f"{execution_date}"
    data_path = "/opt/airflow/data/bronze"
    table_name = "property.csv"
    full_dir = Path(f'{data_path}/{execution_date_path}/')
    full_dir.mkdir(parents=True, exist_ok=True)

    rm = RightmoveData(rightmove_url)
    df_property_prices = rm.get_results
    df_property_prices.to_csv(f"{full_dir}/{table_name}")


def silver_geography_dimension_run(execution_date, **kwargs):
    from pathlib import Path
    import glob
    import os
    import pandas as pd
    import logging

    execution_date_path = f"{execution_date}/"
    logging.info(f"silver_geography_dimension {execution_date_path}")
    execution_date_path = f"{execution_date}"
    data_path = "/opt/airflow/data/silver"
    table_name = "geography_dimension.csv"
    full_dir = Path(f'{data_path}/{execution_date_path}/')
    full_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"silver_geography_dimension {full_dir}")

    columns = ["ID", "NAMES_URI", "NAME1", "NAME1_LANG", "NAME2", "NAME2_LANG", "TYPE", "LOCAL_TYPE", "GEOMETRY_X",
               "GEOMETRY_Y", "MOST_DETAIL_VIEW_RES", "LEAST_DETAIL_VIEW_RES", "MBR_XMIN", "MBR_YMIN", "MBR_XMAX",
               "MBR_YMAX",
               "POSTCODE_DISTRICT", "POSTCODE_DISTRICT_URI", "POPULATED_PLACE", "POPULATED_PLACE_URI",
               "POPULATED_PLACE_TYPE",
               "DISTRICT_BOROUGH", "DISTRICT_BOROUGH_URI", "DISTRICT_BOROUGH_TYPE", "COUNTY_UNITARY",
               "COUNTY_UNITARY_URI",
               "COUNTY_UNITARY_TYPE", "REGION", "REGION_URI", "COUNTRY", "COUNTRY_URI", "RELATED_SPATIAL_OBJECT",
               "SAME_AS_DBPEDIA",
               "SAME_AS_GEONAMES"
               ]

    files_to_read = glob.glob(
        os.path.join('', f"/opt/airflow/data/bronze/{execution_date_path}/opname_csv_gb/DATA/HP40.csv"))

    df_bronze_geography = pd.concat(map(lambda file: pd.read_csv(file, dtype={
        "ID": str,
        "NAMES_URI": str,
        "NAME1": str,
        "NAME1_LANG": str,
        "NAME2": str,
        "NAME2_LANG": str,
        "TYPE": str,
        "LOCAL_TYPE": str,
        "GEOMETRY_X": int,
        "GEOMETRY_Y": int,
        "MOST_DETAIL_VIEW_RES": 'Int64',
        "LEAST_DETAIL_VIEW_RES": 'Int64',
        "MBR_XMIN": 'Int64',
        "MBR_YMIN": 'Int64',
        "MBR_XMAX": 'Int64',
        "MBR_YMAX": 'Int64',
        "POSTCODE_DISTRICT": str,
        "POSTCODE_DISTRICT_URI": str,
        "POPULATED_PLACE": str,
        "POPULATED_PLACE_URI": str,
        "POPULATED_PLACE_TYPE": str,
        "DISTRICT_BOROUGH": str,
        "DISTRICT_BOROUGH_URI": str,
        "DISTRICT_BOROUGH_TYPE": str,
        "COUNTY_UNITARY": str,
        "COUNTY_UNITARY_URI": str,
        "COUNTY_UNITARY_TYPE": str,
        "REGION": str,
        "REGION_URI": str,
        "COUNTRY": str,
        "COUNTRY_URI": str,
        "RELATED_SPATIAL_OBJECT": str,
        "SAME_AS_DBPEDIA": str,
        "SAME_AS_GEONAMES": str
    }, names=columns), files_to_read))

    df_bronze_geography = df_bronze_geography[["ID", "NAME1", "POSTCODE_DISTRICT"]]
    df_bronze_geography = df_bronze_geography.rename(
        columns={"ID": "geography_dimension_id", "POSTCODE_DISTRICT": "postcode", "NAME1": "name"})
    df_bronze_geography.to_csv(f"{full_dir}/{table_name}")


# should be replaced with human curated data
# SCD
def all_region_code():
    return ['4080771', '4632255',
            '280682', '1475548', '280684']


# '1475549', '280685', '280686',
#            '1328515', '280687', '280688', '4106340', '280690', '1475550', '280691', '280692', '280693',
#            '280694', '1475551'

with DAG('property_prices_dag', default_args=default_args) as dag:
    start_task = DummyOperator(task_id='start')


    # geography_downloader_task = PythonVirtualenvOperator(
    #     task_id='geography_downloader',
    #     python_callable=geography_downloader_run,
    #     requirements=["requests==2.22.0", "pandas"],
    #     system_site_packages=False,
    #     provide_context=True,
    #     op_kwargs={'execution_date': '{{ execution_date }}', })

    def group(number, **kwargs):
        # load the values if needed in the command you plan to execute
        dyn_value = "{{ task_instance.xcom_pull(task_ids='push_func') }}"
        return PythonVirtualenvOperator(
            task_id='get_rightmove_prices_{}'.format(number),
            python_callable=get_rightmove_prices_run,
            requirements=["rightmove-webscraper", "requests==2.22.0", "pandas"],
            system_site_packages=False,
            provide_context=True,
            op_kwargs={'execution_date': '{{ execution_date }}', 'region_code': number}, )


    push_func = PythonVirtualenvOperator(
        task_id='push_func',
        provide_context=True,
        python_callable=all_region_code, )

    end_task = DummyOperator(task_id='end')

    start_task >> push_func

    for region_code in all_region_code():
        push_func >> group(region_code) >> end_task
