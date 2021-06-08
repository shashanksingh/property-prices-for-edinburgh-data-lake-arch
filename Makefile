dev-setup:
	$(MAKE) -C airflow dev-setup

dev-run:
	$(MAKE) -C airflow dev-run

prod-setup:
	$(MAKE) -C terraform prod-setup

tests:
	#how to run tests ?
