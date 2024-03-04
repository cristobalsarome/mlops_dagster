from setuptools import find_packages, setup
import os
DAGSTER_VERSION=os.getenv('DAGSTER_VERSION', '1.5.6')
DAGSTER_LIBS_VERSION=os.getenv('DAGSTER_LIBS_VERSION', '0.21.6')
MLFLOW_VERSION=os.getenv('MLFLOW_VERSION', '2.8.0')

setup(
    name="mlops_dagster",
    packages=find_packages(exclude=["mlops_dagster_tests"]),
    install_requires=[
        f"dagster=={DAGSTER_VERSION}",
        f"dagit=={DAGSTER_VERSION}",
        f"dagster-gcp=={DAGSTER_LIBS_VERSION}",
        f"dagster-mlflow=={DAGSTER_LIBS_VERSION}",
        f"mlflow=={MLFLOW_VERSION}",
        f"dagster-airbyte",
        f"dagster-dbt==0.21.6",
        f"pendulum<3.0",
        f"dbt-postgres",

    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "jupyter"], "tests": ["mypy", "pylint", "pytest"]},
)
