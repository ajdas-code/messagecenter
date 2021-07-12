# This is a Python script. This scripts runs daily and find out the jobs
# to execute
import croniter
from datetime import datetime
import sys
from functions.sqlquery import sql_query, sql_query2
import logging
import pprint

LOGFILE = '.mainlog.log'
logging.basicConfig(filename=LOGFILE, level=logging.INFO)


def getnext(cstring):
    if not croniter.is_valid(cstring):
        lprint("Invalid Cron string: {}".format(cstring), logging.ERROR)
        raise ValueError("Invalid cron string: {}".format(cstring))
    now = datetime.now()
    # Spec : https://crontab.cronhub.io/
    # sched = '1 15 1,15 * *'    # at 3:01pm on the 1st and 15th of every month
    # sched = '1 15 *  * FRI'  # at 3:01pm on the 1st and 15th of every month
    sched = cstring
    cron = croniter.croniter(sched, now)
    return cron.get_next(datetime)
    # ---------------


def getprev(cstring):
    if not croniter.is_valid(cstring):
        lprint("Invalid Cron string: {}".format(cstring), logging.ERROR)
        raise ValueError("Invalid cron string: {}".format(cstring))
    now = datetime.now()
    # Spec : https://crontab.cronhub.io/
    # sched = '1 15 1,15 * *'    # at 3:01pm on the 1st and 15th of every month
    # sched = '1 15 *  * FRI'  # at 3:01pm on the 1st and 15th of every month
    sched = cstring
    cron = croniter.croniter(sched, now)
    return cron.get_prev(datetime)
    # ---------------

def checkrange( cstring):
    now = datetime.now()
    future = getnext(cstring)
    past = getprev(cstring)
    fduration = future - now
    pduration = now - past
    fhrs = divmod(fduration.total_seconds(), 3600)[0]
    phrs = divmod(pduration.total_seconds(), 3600)[0]
    fretval = (lambda: True, lambda: False)[fhrs < 260]()
    pretval = (lambda: True, lambda: False)[phrs > -260]()
    return (fretval or pretval)

def hasstarted(then):
    duration = then - now
    hrs = divmod(duration.total_seconds(), 3600)[0]
    print("-----------HRS: {}".format(hrs))
    # return (lambda: True, lambda: False)[hrs < 0]()
    return True if hrs < 0 else False


def lprint(message, lev=logging.INFO):
    lstr = None
    if lev == logging.INFO:
        lstr = 'INFO'
        pprint.pprint("{}:{}".format(message, lstr))
        logging.info(message)
    elif lev == logging.WARN or lev == logging.WARNING:
        lstr = 'WARNING'
        pprint.pprint("{}:{}".format(message, lstr))
        logging.warn(message)
    elif lev == logging.DEBUG:
        lstr = 'DEBUG'
        pprint.pprint("{}:{}".format(message, lstr))
        logging.debug(message)
    elif lev == logging.ERROR:
        lstr = 'ERROR'
        pprint.pprint("{}:{}".format(message, lstr))
        logging.error(message)
    else:
        lstr = 'NOTSET'
        pprint.pprint("{}:{}".format(message, lstr))
        logging.error("{}:{}".format(message, lstr))


def action_execute(rec):
    pass


def process_record(rec):
    now = datetime.now()
    format_str = '%m/%d/%Y'  # The format
    expensive_query = '''SELECT	subscriberdetails.id as subscriber_id, subscriberdetails.name as subscriber_name, 
    subscriberdetails.phone as subscriber_phone, subscriberdetails.email as subscriber_email,
    subscriberdetails.messengerid as subscriber_messengerid, subscriptiondetails.transport as subscription_transport,
    jobdetails.id as job_id, jobdetails.name as job_name, jobdetails.creator as job_creator, 
    jobdetails.start_date as job_start_date,jobdetails.cron_string as job_cron_string,jobdetails.message as job_message
    FROM
    subscriberdetails	
    INNER JOIN subscriptiondetails ON subscriptiondetails.subscriber_id = subscriberdetails.id
    INNER JOIN jobdetails ON jobdetails.id = subscriptiondetails.job_id
    WHERE
	    jobdetails.id = ? and jobdetails.creator = ? '''
    try:
        # Step 0: get the values of the current record
        date_str = rec['start_date']
        job_id = rec['id']
        job_creator = rec['creator']
        cron_string = rec['cron_string']
        is_repeat = rec['isrepeat']

        ##
        ## Step 1: Check if the job is active based on the start date
        ##
        then = datetime.strptime(date_str, format_str)
        isstarted = hasstarted(then)
        if not isstarted:
            lprint("Job is in the Future in terms of start date: {}".format(rec),logging.WARNING)
            return

        ##
        ## Step 2: check if the job execution time within next 24 hrs based on cron expression
        ##
        if not checkrange(cron_string):
            lprint("This job will not be running today. will check in next run: {}".format(rec),logging.WARNING)
            return


        ##
        ## Step 3: looks like we need to process this job today based on cron string
        ##

        print("+++++++++++: {}, {}".format(job_id, job_creator))
        eresults = sql_query2(expensive_query, (job_id, job_creator))
        lprint("records returned: {}".format(len(eresults)))
        for rrec in eresults:
            vrec = dict(rrec)
            pprint.pprint("record:{}".format(vrec))
            if isinstance(vrec, dict):
                action_execute(vrec)
            else:
                lprint("Corrupted record!!", logging.ERROR)

    except RuntimeError as e:
        lprint("Error in processing rec: {}::::{}".format(e,rec), logging.ERROR)


def process_schedules():
    lprint('schedule processing requested..', logging.INFO)
    msg = '''SELECT * FROM jobdetails'''
    results = sql_query(msg)
    lprint("records returned: {}".format(len(results)))
    for rec in results:
        vrec = dict(rec)
        pprint.pprint("record:{}".format(vrec))
        if isinstance(vrec, dict):
            process_record(vrec)
        else:
            lprint("Corrupted record!!", logging.ERROR)
    lprint("Shutting down daily processor", logging.INFO)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lprint('Starting daily job', logging.INFO)
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    lprint("today's date: {}".format(date_time))
    process_schedules()
    lprint("Goodbye", logging.INFO)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
