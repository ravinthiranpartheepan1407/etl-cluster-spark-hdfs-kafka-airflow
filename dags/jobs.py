import json
from datetime import datetime
import hdfs
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from hdfs import InsecureClient
from airflow import DAG

with (DAG(
    'big_data_cluster_communication',
    description="ETL pipeline from HDFS to Spark",
    schedule_interval=None,
    start_date=datetime(2024,03,13),
    catchup=False
) as dag):
    dataset="/opt/airflow/data/exchange_rate.json"
    with open(dataset, "r") as json_dat:
        metadata = json.load(json_dat)

        def send_to_hdfs():
            client = hdfs.InsecureClient("http://namenode:9870")
            client.upload("./data/exchange_rate.json", "/opt/airflow/data/exchange_rate.json", overwrite=True)

        create_spark_cluster = EmptyOperator(
            task_id = "create_spark_cluster"
        )

        create_hdfs_cluster = EmptyOperator(
            task_id= "create_hdfs_cluster"
        )

        create_kafka_cluster= EmptyOperator(
            task_id= "create_kafka_cluster"
        )

        transfer_to_hdfs = PythonOperator(
            task_id="send_data-to_hdfs",
            python_callable=send_to_hdfs
        )

        spark_tasks = SparkSubmitOperator(
            task_id="spark_task",
            conn_id="spark_default",
            packages="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0",
            application_args=["--metadata", json.dumps(metadata), "--kafka_broker", "kafka:9092", "--hdfs_host", "namenode", "--hdfs_port", "9000"],
        )

        stop_spark = EmptyOperator(
            task_id="stopped_spark_cluster"
        )

        stop_hdfs = EmptyOperator(
            task_id="stopped_hdfs_cluster"
        )

        stop_kafka = EmptyOperator(
            task_id="stopped_kafka_cluster"
        )

        [create_hdfs_cluster, create_spark_cluster, create_kafka_cluster] >> transfer_to_hdfs >> spark_tasks
        spark_tasks >> [stop_spark, stop_hdfs, stop_kafka]