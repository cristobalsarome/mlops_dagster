from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource, dbt_assets

from . import assets

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "dbt": DbtCliResource(project_dir="/home/cristobal/mlops_dbt"),
    },
)