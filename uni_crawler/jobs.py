from dagster import define_asset_job

uni_scrape_pipeline = define_asset_job(name='uni_scrape_pipeline', selection='*')