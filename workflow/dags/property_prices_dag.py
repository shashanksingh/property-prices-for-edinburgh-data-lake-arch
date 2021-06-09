"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
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

geography_downloader = BashOperator(
    task_id='geography_downloader',
    bash_command='python geography_downloader.py',
    dag=dag)

get_rightmove_prices = BashOperator(
    task_id='get_rightmove_prices',
    bash_command='python get_rightmove_prices.py',
    dag=dag)

#need to put sensors here
silver_geography_dimension = BashOperator(
    task_id='silver_geography_dimension',
    bash_command='python silver_geography_dimension.py',
    dag=dag)


geography_downloader >> get_rightmove_prices >> silver_geography_dimension