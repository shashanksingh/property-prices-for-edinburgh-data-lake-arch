mac-setup:
	brew install docker-compose

dev-setup:
	#curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.1.0/docker-compose.yaml'
	mkdir -p ./logs ./plugins
	echo "AIRFLOW_UID=$(shell id -u)\nAIRFLOW_GID=0" > .env
	docker-compose up airflow-init

dev-run:
	docker-compose up

airflow-info:
	docker-compose run airflow-worker airflow info

dev-destroy:
	docker-compose down --volumes --rmi all

clean:
	 docker-compose run airflow-worker airflow dags delete property_prices_dag

backfill:
	docker-compose run airflow-worker airflow dags backfill property_prices_dag -s 2021-06-08 -e 2021-06-12