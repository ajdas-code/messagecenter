from flask import Flask, request, redirect, render_template
import sys

sys.path.insert(1,
                "PATH TO LOCAL PYTHON PACKAGES")  # OPTIONAL: Only if need to access Python packages installed on a
# local (non-global) directory
sys.path.insert(2, "PATH TO FLASK DIRECTORY")  # OPTIONAL: Only if you need to add the directory of your flask app

app = Flask(__name__)

# initialization
@app.before_request
def before_request():
    from functions.sqlquery import create_table, setup_schema
    app.logger.info('before request called..')
    setup_schema()
    app.logger.info('schema setup done..')

@app.teardown_request
def teardown_request(exception):
    app.logger.info('tear down called..')

# entrance gate
@app.route('/')
@app.route('/index')
def index():
    app.logger.info('Index page requested..')
    return render_template('index.html')


# from entrance to manage schedule life cycle
@app.route('/schedule')
def schedule():
    from functions.sqlquery import sql_query
    app.logger.info('schedule page requested..')
    msg = '''SELECT * FROM jobdetails'''
    results = sql_query(msg)
    return render_template('schedule.html', results=results, msg=msg)


# form entrance to manage subscriber life cycle
@app.route('/subscriber')
def subscriber():
    from functions.sqlquery import sql_query
    app.logger.info('subscriber page requested..')
    msg = '''SELECT * FROM subscriberdetails'''
    results = sql_query(msg)
    return render_template('subscriber.html', results=results, msg=msg)


# from entrance to subscribe and/or unsubscribe a subscription
@app.route('/subscription')
def subscription():
    from functions.sqlquery import sql_query
    app.logger.info('subscription page requested..')
    msg = '''SELECT * FROM subscriptiondetails'''
    results = sql_query(msg)
    return render_template('subscription.html', results=results, msg=msg)


# insert operation of schedule job or a subscriber
@app.route('/insert', methods=['POST', 'GET'])  # this is when user submits an insert
def sql_datainsert():
    from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'GET':
        msg = "Insert is a POST operation. Illegal access requested!"
        return render_template('5xx.html', error_msg=msg)
    elif request.method == 'POST':
        if request.form['opcode'].upper() == "SCHEDULE":
            name = request.form['name']
            creator = request.form['creator']
            isrepeat = request.form['isrepeat']
            create_date = request.form['create_date']
            start_date = request.form['start_date']
            cron_string = request.form['cron_string']
            message = request.form['message']
            r_tuple = (name, creator, isrepeat, create_date, start_date, cron_string, message)
            app.logger.debug("Input Values: %s %s %d %s %s %s %s".format(r_tuple))
            try:
                sql_edit_insert(
                    '''INSERT INTO jobdetails (name, creator, isrepeat, create_date, start_date, cron_string, message) 
                    VALUES (?,?,?,?,?,?,?) ''',
                    (name, creator, isrepeat, create_date, start_date, cron_string, message))
                msg = "Insert Successful!!!"
                results = sql_query(''' SELECT * FROM jobdetails''')
                return render_template('schedule.html', results=results, msg=msg)
            except ValueError as e:
                msg = "Insert Failed with error : {}".format(e.__str__())
                return render_template('5xx.html', error_msg=msg)
        elif request.form['opcode'] == 'SUBSCRIBER':
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            messengerid = request.form['messengerid']
            r_tuple = (name, phone, email, messengerid)
            app.logger.debug("Input Values: %s %s %s %s" % r_tuple, )
            try:
                sql_edit_insert(
                    '''INSERT INTO subscriberdetails (name, phone, email, messengerid) 
                    VALUES (?,?,?,?) ''',
                    (name, phone, email, messengerid))
                msg = "Insert Successful!!!"
                results = sql_query(''' SELECT * FROM subscriberdetails''')
                return render_template('subscriber.html', results=results, msg=msg)
            except ValueError as e:
                msg = "Insert Failed with error : {}".format(e.__str__())
                return render_template('5xx.html', error_msg=msg)
        elif request.form['opcode'] == 'SUBSCRIPTION':
            job_name = request.form['job_name']
            job_id = request.form['job_id']
            subscriber_name = request.form['subscriber_name']
            subscriber_id = request.form['subscriber_id']
            transport = request.form['transport']
            r_tuple = (job_name, job_id, subscriber_name, subscriber_id, transport)
            app.logger.debug("Input Values: %s %d %s %d %d".format(r_tuple))
            try:
                sql_edit_insert(
                    '''INSERT INTO subscriptiondetails (job_name, job_id, subscriber_name, subscriber_id, transport) 
                    VALUES (?,?,?,?,?) ''',
                    (job_name, job_id, subscriber_name, subscriber_id, transport))
                msg = "Insert Successful!!!"
                results = sql_query(''' SELECT * FROM subscriptiondetails''')
                return render_template('subscription.html', results=results, msg=msg)
            except ValueError as e:
                msg = "Insert Failed with error : {}".format(e.__str__())
                return render_template('5xx.html', error_msg=msg)
        else:
            msg = "Unknown entity. Valid entities are - Job , Subscriber and Subscription"
            return render_template('5xx.html', error_msg=msg)
    else:
        msg = "unknown Operation. Valid operations is POST."
        return render_template('5xx.html', error_msg=msg)


@app.route('/delete', methods=['POST', 'GET'])  # this is when user clicks delete link
def sql_datadelete():
    from functions.sqlquery import sql_delete, sql_query
    if request.method == 'POST':
        msg = "Delete is a GET operation. Illegal access requested!"
        return render_template('5xx.html', error_msg=msg)
    if request.args.get('opcode') == 'SCHEDULE':
        if request.method == 'GET':
            name = request.args.get('name')
            creator = request.args.get('creator')
        else:
            msg = "unknown Operation. Valid operations is POST."
            return render_template('5xx.html', error_msg=msg)
        sql_delete('''DELETE FROM jobdetails where name = ? and creator = ?''', (name, creator))
        results = sql_query(''' SELECT * FROM jobdetails''')
        msg = 'DELETE FROM jobdetails WHERE name = ' + name + ' and creator = ' + creator
        return render_template('schedule.html', results=results, msg=msg)
    elif request.args.get('opcode') == 'SUBSCRIBER':
        if request.method == 'GET':
            name = request.args.get('name')
            email = request.args.get('email')
        else:
            msg = "unknown Operation. Valid operations is POST."
            return render_template('5xx.html', error_msg=msg)
        sql_delete(''' DELETE FROM subscriberdetails where name = ? and email = ?''', (name, email))
        results = sql_query(''' SELECT * FROM subscriberdetails''')
        msg = 'DELETE FROM subscriberdetails WHERE name = ' + name + ' and email = ' + email
        return render_template('subscriber.html', results=results, msg=msg)
    elif request.args.get('opcode') == 'SUBSCRIPTION':
        if request.method == 'GET':
            job_name = request.args.get('job_name')
            subscriber_name = request.args.get('subscriber_name')
            job_id = request.args.get('job_id')
            subscriber_id = request.args.get('subscriber_id')
        else:
            msg = "unknown Operation. Valid operations is POST."
            return render_template('5xx.html', error_msg=msg)
        sql_delete('''DELETE FROM subscriptiondetails where job_name = ? and subscriber_name = ? and job_id = ? and 
        subscriber_id = ?''', (job_name, subscriber_name, job_id, subscriber_id))
        results = sql_query(''' SELECT * FROM subscriberdetails''')
        msg = 'DELETE FROM subscriberdetails WHERE job_name = ' + job_name + ' and subscriber_name = ' + \
              subscriber_name + ' and job_id = ' + job_id + ' and subscriber_id = ' + subscriber_id
        return render_template('subscription.html', results=results, msg=msg)
        pass
    else:
        msg = "Unknown entity. Valid entities are - Job , Subscriber and Subscription"
        return render_template('5xx.html', error_msg=msg)


@app.route('/query_edit', methods=['POST', 'GET'])  # this is when user clicks edit link
def sql_editlink():
    from functions.sqlquery import sql_query, sql_query2
    if request.method == 'GET':
        if request.args.get('opcode') == 'SCHEDULE':
            name = request.args.get('name')
            creator = request.args.get('creator')
            eresults = sql_query2(''' SELECT * FROM jobdetails where name = ? and creator = ?''', (name, creator))
            results = sql_query(''' SELECT * FROM jobdetails''')
            return render_template('schedule.html', eresults=eresults, results=results)
        elif request.args.get('opcode') == 'SUBSCRIBER':
            name = request.args.get('name')
            email = request.args.get('email')
            eresults = sql_query2(''' SELECT * FROM subscriberdetails where name = ? and email = ?''', (name, email))
            results = sql_query(''' SELECT * FROM subscriberdetails''')
            return render_template('subscriber.html', eresults=eresults, results=results)
        elif request.args.get('opcode') == 'SUBSCRIPTION':
            job_name = request.args.get('job_name')
            job_id = request.args.get('job_id')
            subscriber_name = request.args.get('subscriber_name')
            subscriber_id = request.args.get('subscriber_id')
            eresults = sql_query2('''SELECT * FROM subscriptiondetails where job_name = ? and job_id = ? and 
            subscriber_name = ? and subscriber_id = ?''', (job_name, job_id, subscriber_name, subscriber_id))
            results = sql_query(''' SELECT * FROM subscriptiondetails''')
            return render_template('subscription.html', eresults=eresults, results=results)
        else:
            msg = "Unknown entity. Valid entities are - Job , Subscriber and Subscription"
            return render_template('5xx.html', error_msg=msg)
    else:
        msg = "Unknown operation. Valid operation is - GET"
        return render_template('5xx.html', error_msg=msg)


@app.route('/edit', methods=['POST', 'GET'])  # this is when user submits an edit
def sql_dataedit():
    from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        if request.form['opcode'].upper() == "SCHEDULE":
            name = request.form['name']
            creator = request.form['creator']
            isrepeat = request.form['isrepeat']
            create_date = request.form['create_date']
            start_date = request.form['start_date']
            cron_string = request.form['cron_string']
            message = request.form['message']
            old_name = request.form['old_name']
            old_creator = request.form['old_creator']
            r_tuple = (name, creator, isrepeat, create_date, start_date, cron_string, message, old_name, old_creator)
            app.logger.debug("Input Values: %s %s %d %s %s %s %s %s %s".format(r_tuple))
            sql_edit_insert(
                '''UPDATE jobdetails set name=?,creator=?,isrepeat=?,create_date=?,start_date=?,cron_string=?,
                message=? WHERE name=? and creator=? ''', (name, creator, isrepeat, create_date, start_date,
                                                           cron_string, message, old_name, old_creator))
            results = sql_query(''' SELECT * FROM jobdetails''')
            msg = 'UPDATE jobdetails set name = ' + name + ', creator = ' + creator + ', isrepeat = ' \
                  + isrepeat + ', create_date = ' + create_date + ', start_date = ' + start_date + ', cron_string = ' \
                  + cron_string + ', message = ' + message + ' WHERE name = ' \
                  + old_name + ' and creator = ' + old_creator
            return render_template('schedule.html', results=results, msg=msg)
        elif request.form['opcode'].upper() == "SUBSCRIBER":
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            messengerid = request.form['messengerid']
            old_name = request.form['old_name']
            old_email = request.form['old_email']
            r_tuple = (
                name, phone, email, messengerid, old_name, old_email)
            app.logger.debug("Input Values: %s %s %s %s %s %s".format(r_tuple))
            sql_edit_insert('''UPDATE subscriberdetails set name=?,phone=?,email=?,messengerid=? WHERE name=? and 
                    email=? ''', (name, phone, email, messengerid, old_name, old_email))
            results = sql_query(''' SELECT * FROM subscriberdetails''')
            msg = 'UPDATE jobdetails set name = ' + name + ', phone = ' + phone + ', email = ' \
                  + email + ', messengerid = ' + messengerid + ' WHERE name = ' \
                  + old_name + ' and email = ' + old_email
            return render_template('subscriber.html', results=results, msg=msg)
        elif request.form['opcode'].upper() == "SUBSCRIPTION":
            job_name = request.form['job_name']
            job_id = request.form['job_id']
            subscriber_name = request.form['subscriber_name']
            subscriber_id = request.form['subscriber_id']
            transport = request.form['transport']
            old_job_name = request.form['old_job_name']
            old_job_id = request.form['old_job_id']
            old_subscriber_name = request.form['old_subscriber_name']
            old_subscriber_id = request.form['old_subscriber_id']
            r_tuple = (
                job_name, job_id, subscriber_name, subscriber_id, transport, old_job_name, old_job_id,
                old_subscriber_name, old_subscriber_id)
            app.logger.debug("Input Values: %s %d %s %d %d %s %d %s %d".format(r_tuple))
            sql_edit_insert('''UPDATE subscriptiondetails set name=?,phone=?,email=?,messengerid=? WHERE name=? and 
                        email=? ''', (
                job_name, job_id, subscriber_name, subscriber_id, transport, old_job_name, old_job_id,
                old_subscriber_name,
                old_subscriber_id))
            results = sql_query(''' SELECT * FROM subscriberdetails''')
            msg = 'UPDATE jobdetails set job_name = ' + job_name + ', job_id = ' + job_id + ', subscriber_name = ' \
                  + subscriber_name + ', subscriber_id = ' + subscriber_id + ', transport = ' + transport + \
                  ' WHERE job_name = ' + old_job_name + ' and job_id = ' + old_job_id + 'subscriber_name = ' + \
                  old_subscriber_name + ' and subscriber_id = ' + old_subscriber_id
            return render_template('subscription.html', results=results, msg=msg)
        else:
            msg = "Unknown entity. Valid entities are - Job , Subscriber and Subscription"
            return render_template('5xx.html', error_msg=msg)
    else:
        msg = "Unknown operation. Valid operation is - GET"
        return render_template('5xx.html', error_msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
