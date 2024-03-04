import json
from dagster import (
    AssetSelection,
    AssetKey,
    Definitions,
    asset,
    define_asset_job,
)
from dagster_airbyte import load_assets_from_airbyte_instance, AirbyteResource
from dagster_snowflake import SnowflakeResource

airbyte_instance = AirbyteResource(
    host="localhost",
    port="8000",
)

airbyte_assets = load_assets_from_airbyte_instance(
    airbyte_instance,
)

@asset(deps=[AssetKey("stargazers")])
def stargazers_file(snowflake: SnowflakeResource):
    with snowflake.get_connection() as conn:
        stargazers = conn.cursor.execute(
            "SELECT * FROM STARGAZERS"
        ).fetch_pandas_all()
    with open("stargazers.json", "w", encoding="utf8") as f:
        f.write(json.dumps(stargazers.to_json(), indent=2))

# only run the airbyte syncs necessary to materialize stargazers_file
my_upstream_job = define_asset_job(
    "my_upstream_job",
    AssetSelection.keys("stargazers_file")
    .upstream()  # all upstream assets (in this case, just the stargazers Airbyte asset)
    .required_multi_asset_neighbors(),  # all Airbyte assets linked to the same connection
)

defs = Definitions(
    jobs=[my_upstream_job],
    assets=[airbyte_assets, stargazers_file],
    resources={"snowflake": SnowflakeResource(...)},
)
