# coding: UTF-8
from crontab import CronTab

if __name__ == '__main__':
    cron = CronTab()
    job  = cron.new(command="python3 mf.py")

    job.setall("0 1 * * *")
    cron.write("./crontab")

    for result in cron.run_scheduler():
        print(result)
