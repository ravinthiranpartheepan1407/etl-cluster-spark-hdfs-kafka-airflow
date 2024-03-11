start-cluster: start-airflow start-hdfs start-spark start-kafka

stop-cluster: stop-airflow stop-hdfs stop-spark stop-kafka

start-airflow:
	docker build --no-cache --progress=plain -t airflow -f ./Dockerfile .
	docker-compose -f ./airflow-compose.yml up -d

stop-airflow:
	docker-compose -f ./airflow-compose.yml down

start-hdfs:
	docker-compose -f ./hdfs-compose.yml up -d

stop-hdfs:
	docker-compose -f ./hdfs-compose.yml down

start-spark:
	docker-compose -f ./spark-compose.yml up -d

stop-spark:
	docker-compose -f ./spark-compose.yml down

start-kafka:
	docker-compose -f ./kafka-compose.yml up -d

stop-kafka:
	docker-compose -f ./kafka-compose.yml down
