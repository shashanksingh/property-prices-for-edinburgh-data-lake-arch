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
