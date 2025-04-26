from dagster import ScheduleDefinition
from uni_crawler import jobs

uni_scrape_schedule = ScheduleDefinition(
    job = jobs.uni_scrape_pipeline,
    cron_schedule='0 0 1 * *', # SCHEDUULE: 1st day of each month at 12:00 AM
)