from dagster import EnvVar
from dagster_airbyte import AirbyteResource
import os
from dagster_airbyte import load_assets_from_airbyte_instance
from dagster import AssetExecutionContext, Definitions
from dagster_dbt import DbtCliResource, dbt_assets, get_asset_key_for_model
from typing import Any, Mapping
from dagster import AssetKey, AssetExecutionContext
from dagster_dbt import DagsterDbtTranslator
from .mlflow import check_and_update_model
from dagster import asset

# cargo variables de entorno
def load_vars_from_file(file_path):
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):  # Ignore empty lines and comments
                var, value = line.split("=", 1)
                os.environ[var.strip()] = value.strip()


load_vars_from_file("/home/cristobal/environments/local")

# airbyte
airbyte_instance = AirbyteResource(
    host="localhost",
    port="8000",
    # If using basic auth, include username and password:
    username="airbyte",
    password=os.environ["AIRBYTE_PASS"],
)


# Use the airbyte_instance resource we defined above
airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance)


# not used
class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
        return super().get_asset_key(dbt_resource_props).with_prefix("dbt")

# dbt
dbt_manifest_path = "/home/cristobal/mlops_dbt/target/manifest.json"

@dbt_assets(manifest=dbt_manifest_path)
def dbt_project_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

# mlflow
@asset(
    deps=get_asset_key_for_model([dbt_project_assets], "scores_users_movies"),
)
def train_model() -> None:
    check_and_update_model()