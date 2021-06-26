from datetime import datetime
import croniter

TotalSecondsInADay = 57600

class Util:
    def __init__(self):
        pass

    @staticmethod
    def getNextRuntime(sched):
        if (len(sched) < 1 ):
            return None
        now = datetime.now()
        # Spec : https://crontab.cronhub.io/
        # sched = '1 15 1,15 * *'    # at 3:01pm on the 1st and 15th of every month
        # sched = '1 15 *  * FRI'  # at 3:01pm on the 1st and 15th of every month
        cron = croniter.croniter(sched, now)
        """
        for i in range(40):
            nextdate = cron.get_next(datetime.datetime)
            print(nextdate)
        """
        try:
            return cron.get_next(datetime.datetime)
        except:
            return None

    @staticmethod
    def isThisDueToday ( then) :

        now = datetime.now()

        if (now - then).total_seconds() > TotalSecondsInADay:
            # do something
            return True
        else:
            return False



