import pendulum
from airflow.models import DAG
from poomang.providers.https.operators.https import SimpleHttpsOperator

with DAG(
    "send_https_api",
    description="Send Https API",
    start_date=pendulum.datetime(2022, 8, 14, tz="UTC"),
    schedule_interval=None,
) as dag:

    def check(response, **kwargs):
        print(response.text, kwargs)
        return True

    SimpleHttpsOperator(
        task_id="dummy",
        endpoint="/slack_hook_channel_url",
        data={"text": "테스트 통신 from airflow"},
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
        http_conn_id="slack_hook",
        response_check=check,
    )
