import pendulum
from airflow.models import DAG
from airflow.operators.email import EmailOperator
from libs.providers.amazon.aws.operators.ses import SESOperator

with DAG(
    "sample_send_email",
    description="Send Email with aws ses",
    start_date=pendulum.datetime(2022, 8, 14, tz="UTC"),
    schedule_interval=None,
) as dag:
    EmailOperator(
        task_id="send_email_base_operator",
        to=["test_user@test.com"],
        subject="Test Email From Airflow",
        conn_id="smtp",
        html_content="""
        <h1>HELLo!</h1>
        <p>it's from airflow email operator</p>
    """,
    )
    SESOperator(
        task_id="send_email_ses_operator",
        to=["test_user@test.com"],
        subject="Test Email From Airflow",
        conn_id="smtp",
        html_content="""
        <h1>HELLo!</h1>
        <p>it's from airflow email operator</p>
    """,
    )
