from __future__ import annotations

import re
from typing import Any, Dict, List

from app.config import settings
from app.models.observation import Observation


def _valid_identifier(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_]+", value))


class BigQueryService:
    def __init__(self) -> None:
        self.project_id = self._resolve_project_id()
        self.dataset_id = settings.BIGQUERY_DATASET
        self.table_id = settings.BIGQUERY_OBSERVATIONS_TABLE

    @staticmethod
    def _resolve_project_id() -> str:
        project = settings.GOOGLE_CLOUD_PROJECT.strip()
        if project and project != "your-gcp-project-id":
            return project
        fallback = settings.GCP_PROJECT_ID.strip()
        if fallback and fallback != "your-gcp-project-id":
            return fallback
        return ""

    def is_configured(self) -> bool:
        return bool(
            self.project_id
            and _valid_identifier(self.dataset_id)
            and _valid_identifier(self.table_id)
        )

    def _client(self):
        from google.cloud import bigquery

        return bigquery.Client(project=self.project_id or None)

    def _table_ref(self) -> str:
        if not self.is_configured():
            raise RuntimeError("BigQuery is not configured")
        return f"{self.project_id}.{self.dataset_id}.{self.table_id}"

    @staticmethod
    def _schema():
        from google.cloud import bigquery

        return [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("latitude", "FLOAT64", mode="REQUIRED"),
            bigquery.SchemaField("longitude", "FLOAT64", mode="REQUIRED"),
            bigquery.SchemaField("source_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("source_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("city", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("corridor", "STRING"),
            bigquery.SchemaField("aqi", "FLOAT64", mode="REQUIRED"),
            bigquery.SchemaField("pm25", "FLOAT64"),
            bigquery.SchemaField("pm10", "FLOAT64"),
            bigquery.SchemaField("no2", "FLOAT64"),
            bigquery.SchemaField("so2", "FLOAT64"),
            bigquery.SchemaField("co", "FLOAT64"),
            bigquery.SchemaField("o3", "FLOAT64"),
            bigquery.SchemaField("wind_speed_kmh", "FLOAT64"),
            bigquery.SchemaField("wind_direction_deg", "FLOAT64"),
            bigquery.SchemaField("weather_condition", "STRING"),
            bigquery.SchemaField("confidence", "FLOAT64"),
            bigquery.SchemaField("data_quality_flag", "BOOL"),
        ]

    def ensure_table(self) -> Dict[str, Any]:
        if not self.is_configured():
            return {"status": "not_configured"}

        from google.cloud import bigquery

        client = self._client()
        dataset_ref = f"{self.project_id}.{self.dataset_id}"
        table_ref = self._table_ref()

        try:
            client.get_dataset(dataset_ref)
        except Exception:
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = settings.GOOGLE_CLOUD_LOCATION
            client.create_dataset(dataset, exists_ok=True)

        table = bigquery.Table(table_ref, schema=self._schema())
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="timestamp",
        )
        client.create_table(table, exists_ok=True)
        return {"status": "ready", "table": table_ref}

    @staticmethod
    def _row(observation: Observation) -> Dict[str, Any]:
        return {
            "id": observation.id,
            "timestamp": observation.timestamp.isoformat(),
            "latitude": observation.latitude,
            "longitude": observation.longitude,
            "source_type": observation.source_type.value,
            "source_id": observation.source_id,
            "city": observation.city,
            "corridor": observation.corridor,
            "aqi": observation.aqi,
            "pm25": observation.pm25,
            "pm10": observation.pm10,
            "no2": observation.no2,
            "so2": observation.so2,
            "co": observation.co,
            "o3": observation.o3,
            "wind_speed_kmh": observation.wind_speed_kmh,
            "wind_direction_deg": observation.wind_direction_deg,
            "weather_condition": observation.weather_condition,
            "confidence": observation.confidence,
            "data_quality_flag": observation.data_quality_flag,
        }

    def sync_observations(self, observations: List[Observation]) -> Dict[str, Any]:
        ready = self.ensure_table()
        if ready.get("status") != "ready":
            return ready

        client = self._client()
        rows = [self._row(obs) for obs in observations]
        if not rows:
            return {"status": "ready", "inserted": 0, "errors": []}

        errors = client.insert_rows_json(self._table_ref(), rows, row_ids=[row["id"] for row in rows])
        return {
            "status": "ready" if not errors else "partial_failure",
            "inserted": len(rows) - len(errors),
            "errors": errors,
        }

    def query_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        ready = self.ensure_table()
        if ready.get("status") != "ready":
            raise RuntimeError("BigQuery table is not ready")

        limit = max(1, min(int(limit), 500))
        query = f"""
        SELECT *
        FROM `{self._table_ref()}`
        ORDER BY timestamp DESC
        LIMIT {limit}
        """
        rows = self._client().query(query).result()
        return [dict(row) for row in rows]
