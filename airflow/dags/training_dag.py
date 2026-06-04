from datetime import datetime

from airflow import DAG

from airflow.operators.bash import BashOperator


default_args = {

    "owner": "voyage-analytics",

    "start_date": datetime(
        2025,
        1,
        1
    )
}


with DAG(

    dag_id="flight_price_training_pipeline",

    default_args=default_args,

    schedule="@daily",

    catchup=False

) as dag:

    train_pipeline = BashOperator(

        task_id="run_training_pipeline",

        bash_command="""
        cd /opt/airflow/project &&
        python run_training_pipeline.py
        """
    )