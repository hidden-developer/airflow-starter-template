from typing import Optional, Sequence, Union
from airflow.models import BaseOperator
from airflow.utils.context import Context
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


class S3DownloadFileOperator(BaseOperator):

    template_fields: Sequence[str] = (
        "source_bucket_key",
        "source_bucket_name",
        "local_path",
        "aws_conn_id",
        "verify",
    )

    def __init__(
        self,
        *,
        source_bucket_key: str,
        source_bucket_name: Optional[str] = None,
        local_path: Optional[str] = None,
        aws_conn_id: str = "aws_default",
        verify: Optional[Union[str, bool]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.source_bucket_key = source_bucket_key
        self.source_bucket_name = source_bucket_name
        self.local_path = local_path
        self.aws_conn_id = aws_conn_id
        self.verify = verify

    def execute(self, context: "Context"):
        s3_hook = S3Hook(aws_conn_id=self.aws_conn_id, verify=self.verify)
        return s3_hook.download_file(
            self.source_bucket_key,
            self.source_bucket_name,
            self.local_path,
        )
