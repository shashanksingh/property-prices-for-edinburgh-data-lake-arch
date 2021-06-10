"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.python_operator import PythonVirtualenvOperator
from datetime import datetime, timedelta

# import get_rightmove_prices
# import silver_geography_dimension

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('property_prices_dag', default_args=default_args, schedule_interval=timedelta(days=1))


def geography_downloader_run():
    print("geography_downloader_run")
    import geography_downloader
    geography_downloader.run()


geography_downloader = PythonVirtualenvOperator(
    task_id='geography_downloader',
    python_callable=geography_downloader_run,
    requirements=["requests==2.22.0", "pandas==1.2.4"],
    system_site_packages=False,
    dag=dag)
#
# get_rightmove_prices = PythonVirtualenvOperator(
#     task_id='get_rightmove_prices',
#     python_callable=get_rightmove_prices.run,
#     requirements=["rightmove-webscraper==0.4.0", "requests==2.22.0", "pandas==1.2.4"],
#     system_site_packages=False,
#     dag=dag)

# need to put sensors here
# silver_geography_dimension = PythonVirtualenvOperator(
#     task_id='silver_geography_dimension',
#     python_callable=silver_geography_dimension.run,
#     requirements=["pandas==1.2.4"],
#     system_site_packages=False,
#     dag=dag)

geography_downloader
