import datetime
import pendulum


from libs.providers.google.operators.bigquery import BigQueryInsertAllOperator
from libs.providers.mysql.operators.mysql import MySqlReadOperator

from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyTableOperator,
)
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.models import DAG, TaskInstance


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

with DAG(
    "sample_transfer",
    description="sample DAG for transferring MySQL to Bigquery",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    end_date=pendulum.datetime(2023, 2, 1, tz="UTC"),
    schedule_interval="0 * * * *",
    default_args={
        "depends_on_past": True,
        "retries": 3,
        "retry_delay": datetime.timedelta(minutes=3),
    },
    render_template_as_native_obj=True,
    catchup=True,
    tags=["sample", "transfer"],
) as dag:

    # Get since and until
    def get_since_and_until_func(date: datetime.datetime):
        since = date - datetime.timedelta(hours=1)
        until = date
        return {
            "since": since.strftime(TIME_FORMAT),
            "until": until.strftime(TIME_FORMAT),
        }

    get_since_and_until = PythonOperator(
        task_id="get_since_and_until",
        python_callable=get_since_and_until_func,
        op_args=["{{ execution_date }}"],
    )
    
    # Load from MySQL
    get_users = MySqlReadOperator(
        task_id="get_users",
        sql="""
            select
                id,
                name
            from sample_table
            where date_joined between %(since)s and %(until)s
        """,
        mysql_conn_id="my_service_db",
        parameters={
            "since": "{{ task_instance.xcom_pull('get_since_and_until').get('since') }}",
            "until": "{{ task_instance.xcom_pull('get_since_and_until').get('until') }}",
        },
    )

    def get_table_name_func(since: str):
        date = datetime.datetime.strptime(since, TIME_FORMAT)
        formatted = date.strftime("%Y%m%d")
        return f"users_{formatted}"

    # Make table name
    get_table_name = PythonOperator(
        task_id="get_table_name",
        python_callable=get_table_name_func,
        op_kwargs={
            "since": "{{ task_instance.xcom_pull('get_since_and_until').get('since') }}"
        },
    )

    # Upsert empty table
    create_table = BigQueryCreateEmptyTableOperator(
        task_id="create_table",
        project_id="bigquery_project_id",
        dataset_id="bigquery_dataset_id",
        table_id="{{ task_instance.xcom_pull(task_ids='get_table_name') }}",
        gcp_conn_id="google_cloud_default",
        schema_fields=[
            {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "name", "type": "STRING", "mode": "NULLABLE"}
        ],
        location="asia-northeast3",
        # upsert option
        exists_ok=True,
    )

    # Transform
    def convert_to(ti: TaskInstance):
        array = ti.xcom_pull("get_users", [])
        data = [
            {
                "id": item[0],
                "name": item[1],
            }
            for item in array
        ]
        ti.xcom_push("transformed", data)
        return data
    transform = PythonOperator(task_id="transform", python_callable=convert_to)

    # Insert all data
    upload_to_bigquery = BigQueryInsertAllOperator(
        task_id="upload_to_bigquery",
        project_id="bigquery_project_id",
        dataset_id="bigquery_dataset_id",
        table_id="{{ task_instance.xcom_pull(task_ids='get_table_name') }}",
        rows="{{ task_instance.xcom_pull(task_ids='transform') }}",
        fail_on_error=True,
        skip_invalid_rows=True,
    )

    def upload_condition(ti):
        xcom_value = len(ti.xcom_pull(task_ids="transform"))
        if xcom_value < 1:
            return None
        return "upload_to_bigquery"

    # If uplodable data is empty skip task
    branch_op = BranchPythonOperator(
        task_id="upload_condition", python_callable=upload_condition
    )

    # pipeline as code
    get_since_and_until >> get_table_name >> create_table >> upload_to_bigquery
    get_since_and_until >> get_users >> transform >> branch_op >> upload_to_bigquery
