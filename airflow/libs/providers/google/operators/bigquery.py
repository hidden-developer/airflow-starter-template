from typing import Any, Dict, List, Optional, Sequence

from airflow.models import BaseOperator
from airflow.utils.context import Context

from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook as _BigQueryHook


class BigQueryInsertAllOperator(BaseOperator):
    template_fields: Sequence[str] = (
        "project_id",
        "dataset_id",
        "table_id",
        "rows",
        "gcp_conn_id",
        "location",
        "ignore_unknown_values",
        "skip_invalid_rows",
        "fail_on_error",
    )
    template_fields_renderers: Dict[str, str] = {"rows": "json"}

    def __init__(
        self,
        *,
        project_id: str,
        dataset_id: str,
        table_id: str,
        rows: List,
        gcp_conn_id: Optional[str] = "google_cloud_default",
        location: Optional[str] = "asia-northeast3",
        ignore_unknown_values: Optional[bool] = False,
        skip_invalid_rows: Optional[bool] = False,
        fail_on_error: Optional[bool] = False,
        chunk_size: Optional[int] = 10000,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.ignore_unknown_values = ignore_unknown_values
        self.skip_invalid_rows = skip_invalid_rows
        self.fail_on_error = fail_on_error
        self.rows = rows
        self.location = location
        self.gcp_conn_id = gcp_conn_id
        self.chunk_size = chunk_size

    def execute(self, context: Context) -> Any:
        hook = _BigQueryHook(
            gcp_conn_id=self.gcp_conn_id,
            location=self.location,
        )
        total_size = len(self.rows)
        chunk_size = self.chunk_size
        for i in range(0, total_size, chunk_size):
            hook.insert_all(
                dataset_id=self.dataset_id,
                project_id=self.project_id,
                table_id=self.table_id,
                rows=self.rows[i : i + chunk_size],
                ignore_unknown_values=self.ignore_unknown_values,
                skip_invalid_rows=self.skip_invalid_rows,
                fail_on_error=self.fail_on_error,
            )
