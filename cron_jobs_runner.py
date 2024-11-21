import schedule
import time
import asyncio

from cron_jobs.aqar_zyte_gbucket_db.zyte_aqar import main as zyte_aqar_runner
from cron_jobs.gbucket_to_db.main import main as gbucket_to_db_runner


def my_task():
    print("Running my periodic task...\n")
    print('Task 1: Scraping -> save JSON to bucket -> populate DB')
    asyncio.run(zyte_aqar_runner())
    print('-' * 50 + '\n')
    print('Task 2: Read CSV -> Populate DB')
    gbucket_to_db_runner()
    print('-' * 50 + '\n' 'Completed tasks.')


# Schedule the task to run every minute
schedule.every(1).day.do(my_task)


while True:
    print('Heartbeat...')
    # This will keep the script running and checking for the scheduled task
    schedule.run_pending()
    time.sleep(10)