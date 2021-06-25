# coding: UTF-8
from crontab import CronTab

if __name__ == '__main__':
    _cron = CronTab()
    _job  = _cron.new(command="python3 mf.py")

    _job.setall("0 1 * * *")
    _cron.write("./crontab")

    for _result in _cron.run_scheduler():
        print(_result)
