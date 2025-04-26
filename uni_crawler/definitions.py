from dagster import Definitions, load_assets_from_modules
from uni_crawler import assets, jobs, schedules  # noqa: TID252

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    jobs=[jobs.uni_scrape_pipeline],
    schedules=[schedules.uni_scrape_schedule],
)