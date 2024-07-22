from flask import Flask, render_template, request, session, url_for, redirect
from DBcm import UseDatabase
from checker import ucheck_logged_in, adcheck_logged_in, check_logged_out
from datetime import datetime, date

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'root',
                          'password': '',
                          'database': 'bloodbank'}


def log_udetails(req: 'flask request') -> None:
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into userprofile(username,email,password,dob) values(%s,%s,%s,%s)"""
        cursor.execute(_SQL, (req.form['uname'],
                              req.form['email'],
                              req.form['pswd'],
                              req.form['dob']))


def log_donordetails(req: 'flask request') -> None:
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select email,dob from userprofile where username=%s"""
        cursor.execute(_SQL, (session['username'],))
        contents = cursor.fetchone()
        email = contents[0]
        dob = contents[1]
        _SQL = """insert into donordirectory(username,name,gender,phoneno,email,dob,city,bloodgroup,healthissues) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(_SQL, (session['username'],
                              req.form['dname'],
                              req.form['dgender'],
                              req.form['dphno'],
                              email,
                              dob,
                              req.form['dcity'],
                              req.form['dbloodgroup'],
                              req.form['hissues'] or None))


def log_donationhistory(req: 'flask request'):
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select bloodgroup from donordirectory where username=%s"""
        cursor.execute(_SQL, (session['username'],))
        contents = cursor.fetchone()
        bloodgroup = contents[0]
        _SQL = """insert into donationhistory(donorusername,datedonated,donatedatcity,bloodgroupdonated) values(%s,%s,%s,%s)"""
        cursor.execute(_SQL, (session['username'],
                              req.form['ddate'],
                              req.form['dcity'] or None,
                              bloodgroup))


def select_recentdate():
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select donorusername, max(datedonated) from donationhistory where donorusername=%s group by donorusername"""
        cursor.execute(_SQL, (session['username'],))
        contents = cursor.fetchone()
        if contents == None:
            return None
        lastdate = contents[1]
        return lastdate


def update_ldate(lastdate):
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """update donordirectory set lastdonateddate=%s where username=%s"""
        cursor.execute(_SQL, (lastdate, session['username']))


def log_patientdetails(req: 'flask request') -> None:
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into patientregister(patientname,gender,dob,phno,email,city,bloodgroup) values(%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(_SQL, (req.form['pname'],
                              req.form['pgender'],
                              req.form['pdob'],
                              req.form['pphno'],
                              req.form['pemail'],
                              req.form['pcity'],
                              req.form['pbloodgroup']))


def log_donorupdates(req: 'flask request') -> str:
    with UseDatabase(app.config['dbconfig']) as cursor:

        _SQL = """update donordirectory set phoneno=%s,city=%s,healthissues=%s,availability=%s where username=%s"""
        cursor.execute(_SQL, (req.form['dphno'],
                              req.form['dcity'],
                              req.form['hissues'] or None,
                              req.form['avail'],
                              session['username']))
        if cursor.rowcount == 1:
            return 'yes'
        else:
            return 'no'


def log_patientupdates(req: 'flask request') -> str:
    with UseDatabase(app.config['dbconfig']) as cursor:

        _SQL = """update patientregister set phno=%s,email=%s,city=%s where patientid=%s"""
        cursor.execute(_SQL, (req.form['pphno'],
                              req.form['pemail'],
                              req.form['pcity'],
                              req.form['pid']))
        if cursor.rowcount == 1:
            return 'yes'
        else:
            return 'no'


def delete_donationhistory(req: 'flask request'):
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """delete from donationhistory where donorusername=%s and donationno=%s"""
        cursor.execute(_SQL, (session['username'], req.form['dno']))
        if cursor.rowcount == 0:
            return 0
        return 1


def delete_donordetails(req: 'flask request'):
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """delete from userprofile where username=%s"""
        cursor.execute(_SQL, (req.form['duname'],))
        return cursor.rowcount


def delete_patientdetails(req: 'flask request'):
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """delete from patientregister where patientid=%s"""
        cursor.execute(_SQL, (req.form['pid'],))
        return cursor.rowcount


def delete_donoraccount():
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """delete from userprofile where username=%s"""
        cursor.execute(_SQL, (session['username'],))


def isusernameunique(req):
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select * from userprofile where username=%s"""
        cursor.execute(_SQL, (req.form['uname'],))
        contents = cursor.fetchall()
        if contents == []:
            return True
        return False


def isemailunique(req):
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select * from userprofile where email=%s"""
        cursor.execute(_SQL, (req.form['email'],))
        contents = cursor.fetchall()
        if contents == []:
            return True
        return False


@app.route('/')
def home_page() -> 'html':
    return render_template('homepage.html')


@app.route('/signup')
def show_signup() -> 'html':
    return render_template('signup.html')


@app.route('/userlogin')
@check_logged_out
def user_login() -> 'html':
    return render_template('ulogin.html')


@app.route('/adminlogin')
@check_logged_out
def admin_login() -> 'html':
    return render_template('adlogin.html')


@app.route('/ulogout')
@ucheck_logged_in
def u_logout() -> 'html':
    session.pop('logged_in')
    session.pop('username')
    return render_template('homepage.html',
                           the_title1='you are now logged out')


@app.route('/adlogout')
@adcheck_logged_in
def ad_logout() -> 'html':
    session.pop('logged_in')
    session.pop('admin')
    return render_template('homepage.html',
                           the_title1='you are now logged out')


@app.route('/mainmenu1')
@ucheck_logged_in
def main_menu1() -> 'html':
    return render_template('userdashboard.html',
                           the_title1='You are now logged in as "donor". Your username is ',
                           the_title2=session['username'])


@app.route('/mainmenu2')
@adcheck_logged_in
def main_menu2() -> 'html':
    return render_template('admindashboard.html',
                           the_title1='You are now logged in as "admin". Your username is ',
                           the_title2=session['admin'])


@app.route('/receivesignup', methods=['POST'])
def get_signup() -> 'html':
    f1 = isusernameunique(request)
    f2 = isemailunique(request)
    if (not f1 and not f2):
        return render_template('signup.html',
                               the_title='user name and email already taken')
    elif (not f1):
        return render_template('signup.html',
                               the_title='user name already taken')
    elif (not f2):
        return render_template('signup.html',
                               the_title='email already taken')
    else:
        try:
            log_udetails(request)
            title = 'signup successful'

        except Exception as err:
            msg = "****logging failed with this error: " + str(err)
            print(msg)
            title = 'error'
    return render_template('goback.html',
                           the_title=title)


@app.route('/ucheck', methods=['POST'])
@check_logged_out
def user_check() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select * from userprofile where username=%s and password=%s"""
        cursor.execute(_SQL, (request.form['uname'], request.form['passwd']))
        contents = cursor.fetchall()
        if contents == []:
            return render_template('ulogin.html',
                                   heading='invalid details')
        else:
            session['logged_in'] = True
            session['username'] = request.form['uname']
            return render_template('userdashboard.html',
                                   the_title1='You are now logged in as "donor". Your username is ',
                                   the_title2=session['username'])


@app.route('/adcheck', methods=['POST'])
@check_logged_out
def admin_check() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select * from adminprofile where username=%s and password=%s"""
        cursor.execute(_SQL, (request.form['uname'], request.form['passwd']))
        contents = cursor.fetchall()
        if contents == []:
            return render_template('adlogin.html',
                                   heading='invalid details')
        else:
            session['logged_in'] = True
            session['admin'] = request.form['uname']
            return render_template('admindashboard.html',
                                   the_title1='You are now logged in as "admin". Your username is ',
                                   the_title2=session['admin'])


@app.route('/adddonordetails')
@ucheck_logged_in
def add_donordetails() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select * from donordirectory where username=%s"""
        cursor.execute(_SQL, (session['username'],))
        contents = cursor.fetchall()
        if contents == []:
            return render_template('donorprofile.html')
        else:
            return render_template('goback1.html',
                                   the_title='profile already added')


@app.route('/adddonationhistory')
@ucheck_logged_in
def add_donationhistory() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select * from donordirectory where username=%s"""
        cursor.execute(_SQL, (session['username'],))
        contents = cursor.fetchall()
        if contents == []:
            return render_template('goback1.html',
                                   the_title='first add profile and then add donation history')
        return render_template('donationhistory.html')


@app.route('/addpatientdetails')
@adcheck_logged_in
def add_patientdetails() -> 'html':
    return render_template('patientregister.html')


@app.route('/receivedonordetails', methods=['POST'])
@ucheck_logged_in
def insert_donordetails() -> 'html':
    try:
        log_donordetails(request)
        return render_template('goback1.html',
                               the_title='donor details added to database')
    except Exception as err:
        msg = "****logging failed with this error: " + str(err)
        print(msg)
        return render_template('goback1.html',
                               the_title='error')


@app.route('/receivedonationhistory', methods=['POST'])
@ucheck_logged_in
def insert_donationhistory() -> 'html':
    try:
        log_donationhistory(request)

    except Exception as err:
        msg = "****logging failed with this error: " + str(err)
        print(msg)
        return render_template('goback1.html',
                               the_title='error')

    ldate = select_recentdate()
    try:
        update_ldate(ldate)

    except Exception as err:
        msg = "****logging failed with this error: " + str(err)
        print(msg)
        return render_template('goback1.html',
                               the_title='error')
    return render_template('goback1.html',
                           the_title='donation history added to database')


@app.route('/receivepatientdetails', methods=['POST'])
@adcheck_logged_in
def insert_patientdetails() -> 'html':
    try:
        log_patientdetails(request)
        return render_template('goback2.html',
                               the_title='patient details added to database')
    except Exception as err:
        msg = "****logging failed with this error: " + str(err)
        print(msg)
        return render_template('goback2.html',
                               the_title='error')


@app.route('/searchblooddonor')
@adcheck_logged_in
def search_donor() -> 'html':
    return render_template('donorsearch.html')


@app.route('/receivedonorsearch', methods=['POST'])
@adcheck_logged_in
def find_donor() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select bloodgroup,city from patientregister where patientid=%s"""
        cursor.execute(_SQL, (request.form['pid'],))
        contents = cursor.fetchone()
        if contents == None:
            return render_template('goback2.html',
                                   the_title='invalid patient id')
        bloodgroup = contents[0]
        city = contents[1]
        _SQL = """select username,bloodgroup,city,availability,timestampdiff(day,lastdonateddate,curdate()) from donordirectory where bloodgroup=%s and city=%s"""
        cursor.execute(_SQL, (bloodgroup, city))
        contents = cursor.fetchall()

        titles = ('username', 'bloodgroup', 'current city', 'availability', 'days since last donation', 'eligibility')
        return render_template('eligibledonors.html',
                               the_titles=titles,
                               the_data=contents)


@app.route('/userdetails/<username>')
@adcheck_logged_in
def view_userdetails(username) -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select username,name,gender,phoneno,email,timestampdiff(year,dob,curdate()),healthissues,lastdonateddate from donordirectory where username=%s"""
        cursor.execute(_SQL, (username,))
        contents = cursor.fetchone()
        titles = (
        'name', 'gender', 'phone no', 'email', 'age', 'health issues', 'last donated date', 'donation history')
        return render_template('viewuserdetails.html',
                               the_title='view donor details',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/userdetails/donationhistory/<username>')
@adcheck_logged_in
def view_history(username) -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select donationno,datedonated,donatedatcity from donationhistory where donorusername=%s"""
        cursor.execute(_SQL, (username,))
        contents = cursor.fetchall()
        titles = ('donation no.', 'date donated', 'donated at city')
        return render_template('viewhistory.html',
                               the_title='view donation history',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/search1blooddonor')
@adcheck_logged_in
def search1_donor() -> 'html':
    return render_template('donorsearch1.html')


@app.route('/receivedonorsearch1', methods=['POST'])
@adcheck_logged_in
def find_donor1() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        bloodgroup = request.form['pbloodgroup']
        city = request.form['pcity']
        _SQL = """select username,bloodgroup,city,availability,timestampdiff(day,lastdonateddate,curdate()) from donordirectory where bloodgroup=%s and city=%s"""
        cursor.execute(_SQL, (bloodgroup, city))
        contents = cursor.fetchall()

        titles = ('username', 'bloodgroup', 'current city', 'availability', 'days since last donation', 'eligibility')
        return render_template('eligibledonors.html',
                               the_titles=titles,
                               the_data=contents)


@app.route('/search2blooddonor')
@adcheck_logged_in
def search2_donor() -> 'html':
    return render_template('donorsearch2.html')


@app.route('/receivedonorsearch2', methods=['POST'])
@adcheck_logged_in
def find_donor2() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        city = request.form['dcity']
        _SQL = """select username,bloodgroup,city,availability,timestampdiff(day,lastdonateddate,curdate()) from donordirectory where city=%s"""
        cursor.execute(_SQL, (city,))
        contents = cursor.fetchall()

        titles = ('username', 'bloodgroup', 'current city', 'availability', 'days since last donation', 'eligibility')
        return render_template('eligibledonors.html',
                               the_titles=titles,
                               the_data=contents)


@app.route('/updatedonordetails')
@ucheck_logged_in
def update_donordetails() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select phoneno,healthissues from donordirectory where username=%s"""
        cursor.execute(_SQL, (session['username'],))
        contents = cursor.fetchone()
        if contents == None:
            return render_template('goback1.html',
                                   the_title='first add profile and then update')
        ph = contents[0]
        his = contents[1]
        if his == None:
            his = ''
        return render_template('updateprofile.html',
                               phone=ph,
                               health=his)


@app.route('/receiveupdates', methods=['POST'])
@ucheck_logged_in
def update_donor() -> 'html':
    try:
        flag = log_donorupdates(request)
        if flag == 'yes':
            title = 'updation successful'
        else:
            title = 'no updation done'

        return render_template('goback1.html',
                               the_title=title)
    except Exception as err:
        msg = "****logging failed with this error: " + str(err)
        print(msg)
        return render_template('goback1.html',
                               the_title='error')


@app.route('/updatepatientdetails')
@adcheck_logged_in
def update_patientdetails() -> 'html':
    return render_template('updatepatient.html')


@app.route('/receivepatientupdate', methods=['POST'])
@adcheck_logged_in
def update_patient() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select patientname,phno,email from patientregister where patientid=%s"""
        cursor.execute(_SQL, (request.form['pid'],))
        contents = cursor.fetchall()
        if contents == []:
            return render_template('goback2.html',
                                   the_title='invalid patient id')
        else:
            pname = contents[0][0]
            phno = contents[0][1]
            email1 = contents[0][2]

            return render_template('patientupdate.html',
                                   name=pname,
                                   phone=phno,
                                   email=email1,
                                   ptid=request.form['pid'])


@app.route('/receiveptupdate', methods=['POST'])
@adcheck_logged_in
def update_pt() -> 'html':
    try:
        flag = log_patientupdates(request)
        if flag == 'yes':
            title = 'updation successful'
        else:
            title = 'no updation done'

        return render_template('goback2.html',
                               the_title=title)
    except Exception as err:
        msg = "****logging failed with this error: " + str(err)
        print(msg)
        return render_template('goback2.html',
                               the_title='error')


@app.route('/viewdonordetails')
@ucheck_logged_in
def view_donordetails() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select name,gender,phoneno,email,timestampdiff(year,dob,curdate()),city,bloodgroup,healthissues,lastdonateddate,availability,timestampdiff(day,lastdonateddate,curdate()) from donordirectory where username=%s"""
        cursor.execute(_SQL, (session['username'],))
        contents = cursor.fetchone()
        if contents == None:
            return render_template('goback1.html',
                                   the_title='profile not added')
        titles = ('name', 'gender', 'phone no', 'email', 'age', 'current city', 'blood group', 'health issues',
                  'last donated date', 'availability', 'eligibility')
        return render_template('viewdonordetails.html',
                               the_title='view donor details',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/viewdonationhistory')
@ucheck_logged_in
def view_donationhistory() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select donationno,datedonated,donatedatcity,bloodgroupdonated from donationhistory where donorusername=%s"""
        cursor.execute(_SQL, (session['username'],))
        contents = cursor.fetchall()
        titles = ('donation no', 'date donated', 'donated at city', 'blood group donated')
        return render_template('viewdonationhistory.html',
                               the_title='view donation history',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/deldonationhistory')
@ucheck_logged_in
def del_donationhistory() -> 'html':
    return render_template('deldonationhistory.html')


@app.route('/receivedelhistory', methods=['POST'])
@ucheck_logged_in
def del_history() -> 'html':
    try:
        flag = delete_donationhistory(request)
        if flag == 0:
            return render_template('goback1.html',
                                   the_title='invalid donation no.')
    except Exception as err:
        msg = "****deletion failed with this error: " + str(err)
        print(msg)
        return render_template('goback1.html',
                               the_title='error')

    ldate = select_recentdate()
    try:
        update_ldate(ldate)

    except Exception as err:
        msg = "****updation of last date failed with this error: " + str(err)
        print(msg)
        return render_template('goback1.html',
                               the_title='error')
    return render_template('goback1.html',
                           the_title='donation deleted from history')


@app.route('/viewuserlogin')
@adcheck_logged_in
def view_userlogin() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select * from userprofile"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        titles = ('user name', 'email', 'password', 'date of birth', 'date of registration')
        return render_template('viewuserlogin.html',
                               the_title='view donor login details',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/viewalldonordetails')
@adcheck_logged_in
def view_alldonordetails() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select username,name,gender,phoneno,email,timestampdiff(year,dob,curdate()),city,bloodgroup,healthissues,lastdonateddate,availability from donordirectory"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        titles = (
        'user name', 'name', 'gender', 'phone no.', 'email', 'age', 'current city', 'blood group', 'health issues',
        'last donated date', 'availability')
        return render_template('viewalldonordetails.html',
                               the_title='view donor profile details',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/viewalldonationhistory')
@adcheck_logged_in
def view_alldonationhistory() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select donationno,donorusername,datedonated,donatedatcity,bloodgroupdonated from donationhistory"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        titles = ('donation no', 'donor username', 'date donated', 'donated at city', 'blood group')
        return render_template('viewalldonationhistory.html',
                               the_title='view all donation history',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/viewallpatientdetails')
@adcheck_logged_in
def view_allpatientdetails() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select patientid,patientname,gender,timestampdiff(year,dob,curdate()),phno,email,city,bloodgroup from patientregister"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        titles = ('patient id', 'patient name', 'gender', 'age', 'phone no.', 'email', 'current city', 'blood group')
        return render_template('viewallpatientdetails.html',
                               the_title='view all patientdetails',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/deletealldonordetails')
@adcheck_logged_in
def del_alldonordetails() -> 'html':
    return render_template('deldonordetails.html')


@app.route('/admindashboard', methods=['GET', 'POST'])
@adcheck_logged_in
def admindashboard() -> 'html':
    search_query = request.form.get('search', '')

    with UseDatabase(app.config['dbconfig']) as cursor:
        # Fetch total counts
        cursor.execute("SELECT COUNT(*) FROM patientregister")
        total_patients = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM donordirectory")
        total_donors = cursor.fetchone()[0]

        # Fetch patient details based on search
        if search_query:
            cursor.execute("""
                SELECT patientid, patientname, gender, TIMESTAMPDIFF(year, dob, CURDATE()), 
                       phno, email, city, bloodgroup 
                FROM patientregister
                WHERE patientname LIKE %s OR phno LIKE %s OR email LIKE %s
            """, (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
        else:
            cursor.execute("""
                SELECT patientid, patientname, gender, TIMESTAMPDIFF(year, dob, CURDATE()), 
                       phno, email, city, bloodgroup 
                FROM patientregister
            """)
        patient_data = cursor.fetchall()

        # Column titles for patients table
        row_titles = (
        'Patient ID', 'Patient Name', 'Gender', 'Age', 'Phone No.', 'Email', 'Current City', 'Blood Group')

    return render_template(
        'admindashboard.html',
        total_patients=total_patients,
        total_donors=total_donors,
        the_row_titles=row_titles,
        the_data=patient_data,
        search_query=search_query,
        the_title2=session['admin']
    )


@app.route('/find_donor/<int:patient_id>', methods=['GET'], endpoint='find_donor_route')
@adcheck_logged_in
def find_donor(patient_id) -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        # Fetch patient details
        cursor.execute("""
            SELECT city, bloodgroup 
            FROM patientregister
            WHERE patientid = %s
        """, (patient_id,))
        patient = cursor.fetchone()

        if patient:
            city, bloodgroup = patient

            # Find donors matching the patient's city and blood group
            cursor.execute("""
                SELECT username, city, bloodgroup 
                FROM donordirectory
                WHERE city = %s AND bloodgroup = %s AND availability = "Available"
            """, (city, bloodgroup))
            donors = cursor.fetchall()

            # Column titles for donors table
            donor_row_titles = ('Donor Name', 'City', 'Blood Group')
        else:
            donors = []
            donor_row_titles = ()

    return render_template(
        'find_donor.html',
        patient_id=patient_id,
        the_row_titles=donor_row_titles,
        the_data=donors,
        the_title2=session['admin']
    )


@app.route('/editpatient/<int:patient_id>', methods=['GET', 'POST'])
@adcheck_logged_in
def editpatient(patient_id):
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dob']
        phno = request.form['phno']
        email = request.form['email']
        city = request.form['city']
        bloodgroup = request.form['bloodgroup']

        # Update patient details in the database
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """
                UPDATE patientregister 
                SET patientname=%s, gender=%s, dob=%s, phno=%s, email=%s, city=%s, bloodgroup=%s 
                WHERE patientid=%s
            """
            cursor.execute(_SQL, (name, gender, dob, phno, email, city, bloodgroup, patient_id))
        return redirect(url_for('admindashboard'))

    # Fetch patient details for the form
    with UseDatabase(app.config['dbconfig']) as cursor:
        cursor.execute(
            "SELECT patientid, patientname, gender, dob, phno, email, city, bloodgroup FROM patientregister WHERE patientid=%s",
            (patient_id,))
        patient = cursor.fetchone()

    return render_template('editpatient.html', patient=patient)


@app.route('/deletepatient/<int:patient_id>', methods=['POST'])
@adcheck_logged_in
def deletepatient(patient_id):
    # Delete patient from the database
    with UseDatabase(app.config['dbconfig']) as cursor:
        cursor.execute("DELETE FROM patientregister WHERE patientid=%s", (patient_id,))
    return redirect(url_for('admindashboard'))


# -----------------------------------------------------------------------------------------------------
@app.route('/admindonorboard', methods=['GET', 'POST'])
@adcheck_logged_in
def admindonorboard() -> 'html':
    search_query = ""
    donor_data = []

    with UseDatabase(app.config['dbconfig']) as cursor:
        # Fetch total counts
        cursor.execute("SELECT COUNT(*) FROM patientregister")
        total_patients = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM donordirectory")
        total_donors = cursor.fetchone()[0]

        if request.method == 'POST':
            search_query = request.form['search']
            # Search for donors by username, name, email, or phone number
            search_sql = """
                SELECT username, name, gender, phoneno, email, TIMESTAMPDIFF(year, dob, CURDATE()), 
                       city, bloodgroup, healthissues, lastdonateddate, availability 
                FROM donordirectory
                WHERE username LIKE %s OR name LIKE %s OR email LIKE %s OR phoneno LIKE %s OR city LIKE %s OR bloodgroup LIKE %s
            """
            cursor.execute(search_sql, (
            f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%",
            f"%{search_query}%"))
            donor_data = cursor.fetchall()
        else:
            # Fetch donor details
            cursor.execute("""
                SELECT username, name, gender, phoneno, email, TIMESTAMPDIFF(year, dob, CURDATE()), 
                       city, bloodgroup, healthissues, lastdonateddate, availability 
                FROM donordirectory
            """)
            donor_data = cursor.fetchall()

    # Column titles for donors table
    row_titles = ('Username', 'Name', 'Gender', 'Phone No.', 'Email', 'Age', 'City', 'Blood Group', 'Health Issues',
                  'Last Donated Date', 'Availability')

    return render_template(
        'admindonorboard.html',
        total_patients=total_patients,
        total_donors=total_donors,
        the_row_titles=row_titles,
        the_data=donor_data,
        search_query=search_query,
        the_title2=session['admin']
    )


@app.route('/deletedonor/<username>', methods=['POST'])
@adcheck_logged_in
def deletedonor(username):
    # Delete donor from the database using username
    with UseDatabase(app.config['dbconfig']) as cursor:
        cursor.execute("DELETE FROM donordirectory WHERE username=%s", (username,))
    return redirect(url_for('admindonorboard'))


# ----------------------------------------------
# @app.route('/userdashboard')
# @ucheck_logged_in
# def userdashboard():
#     username = session['username']
#     with UseDatabase(app.config['dbconfig']) as cursor:
#         # Fetch total donation count for the logged-in user
#         cursor.execute("SELECT COUNT(*) FROM donationhistory WHERE donorusername = %s", (username,))
#         total_donations = cursor.fetchone()[0]
#
#         # Fetch donation history for the logged-in user
#         _SQL = """select donationno,datedonated,donatedatcity,bloodgroupdonated from donationhistory where donorusername=%s"""
#         cursor.execute(_SQL, (session['username'],))
#         donation_history = cursor.fetchall()
#
#     return render_template('userdashboard.html',
#                            total_donations=total_donations,
#                            donation_history=donation_history,
#                            the_title2=session['username'])

# ----------------------------------------------


#
@app.route('/userdashboard')
@ucheck_logged_in
def userdashboard():
    username = session['username']
    with UseDatabase(app.config['dbconfig']) as cursor:
        cursor.execute("SELECT MAX(datedonated) FROM donationhistory WHERE donorusername = %s", (username,))
        last_donation_date = cursor.fetchone()[0]

        # Fetch total donation count for the logged-in user
        cursor.execute("SELECT COUNT(*) FROM donationhistory WHERE donorusername = %s", (username,))
        total_donations = cursor.fetchone()[0]

        _SQL = "SELECT donationno, datedonated, donatedatcity FROM donationhistory WHERE donorusername = %s"
        cursor.execute(_SQL, (username,))
        donation_history = cursor.fetchall()

        if last_donation_date:
            days_since_last_donation = (datetime.now().date() - last_donation_date).days
        else:
            days_since_last_donation = None

    return render_template('userdashboard.html',
                           last_donation_date=last_donation_date,
                           total_donations=total_donations,
                           donation_history=donation_history,
                           days_since_last_donation=days_since_last_donation,
                           username=username)


@app.route('/edit_user_profile', methods=['GET', 'POST'])
@ucheck_logged_in
def edit_user_profile():
    username = session['username']
    if request.method == 'POST':
        new_username = request.form['username']
        email = request.form['email']
        dob = request.form['dob']
        password = request.form['password']
        with UseDatabase(app.config['dbconfig']) as cursor:
            cursor.execute(
                "UPDATE userprofile SET username = %s, email = %s, dob = %s, password = %s WHERE username = %s",
                (new_username, email, dob, password, username))
            session['username'] = new_username
        return redirect(url_for('userdashboard'))
    else:
        with UseDatabase(app.config['dbconfig']) as cursor:
            cursor.execute("SELECT username, email, dob, password FROM userprofile WHERE username = %s", (username,))
            user_profile = cursor.fetchone()
        return render_template('edit_user_profile.html', user_profile=user_profile)


from datetime import datetime


@app.route('/edit_donor_profile', methods=['GET', 'POST'])
@ucheck_logged_in
def edit_donor_profile():
    username = session['username']
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        dob = request.form['dob']
        current_city = request.form['current_city']
        blood_group = request.form['blood_group']
        health_issues = request.form['health_issues']
        availability = request.form['availability']
        last_donated_date = request.form['last_donated_date']

        with UseDatabase(app.config['dbconfig']) as cursor:
            cursor.execute("""
                UPDATE donordirectory SET name = %s, gender = %s, phoneno = %s, email = %s, dob = %s, city = %s, 
                bloodgroup = %s, healthissues = %s, availability = %s, lastdonateddate = %s
                WHERE username = %s
            """, (
            name, gender, phone, email, dob, current_city, blood_group, health_issues, availability, last_donated_date,
            username))
        return redirect(url_for('userdashboard'))
    else:
        with UseDatabase(app.config['dbconfig']) as cursor:
            cursor.execute("""
                SELECT name, gender, phoneno, email, dob, city, bloodgroup, healthissues, lastdonateddate, availability 
                FROM donordirectory WHERE username = %s
            """, (username,))
            donor_profile = cursor.fetchone()

        # Calculate days since last donation
        last_donated_date = donor_profile[8]
        if last_donated_date:
            days_since_last_donation = (datetime.now().date() - last_donated_date).days
        else:
            days_since_last_donation = None

        return render_template('edit_donor_profile.html', donor_profile=donor_profile,
                               days_since_last_donation=days_since_last_donation)


# -----------------------------------------------------------------------------------


@app.route('/deldonationhistory1/<int:donation_id>', methods=['POST'])
def delete_donation_history(donation_id):
    with UseDatabase(app.config['dbconfig']) as cursor:
        cursor.execute("DELETE FROM donationhistory WHERE donationno = %s", (donation_id,))
    return redirect(url_for('userdashboard'))


@app.route('/receivedeletedonor', methods=['POST'])
@adcheck_logged_in
def del_donor() -> 'html':
    try:
        flag = delete_donordetails(request)

    except Exception as err:
        msg = "****deletion failed with this error: " + str(err)
        print(msg)
        return render_template('goback2.html',
                               the_title='error')

    if flag == 0:
        title = 'invalid donor username'
    else:
        title = 'deletion successful'
    return render_template('goback2.html',
                           the_title=title)


@app.route('/deletepatientdetails')
@adcheck_logged_in
def del_patientdetails() -> 'html':
    return render_template('delpatientdetails.html')


@app.route('/receivedeletepatient', methods=['POST'])
@adcheck_logged_in
def del_patient() -> 'html':
    try:
        flag = delete_patientdetails(request)

    except Exception as err:
        msg = "****deletion failed with this error: " + str(err)
        print(msg)
        return render_template('goback2.html',
                               the_title='error')

    if flag == 0:
        title = 'invalid patient id'
    else:
        title = 'deletion successful'
    return render_template('goback2.html',
                           the_title=title)


@app.route('/searchdonor')
@adcheck_logged_in
def search_donordir() -> 'html':
    return render_template('searchdonor.html')


@app.route('/receivedsearch', methods=['POST'])
@adcheck_logged_in
def find_donordetails() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select username,name,gender,phoneno,email,timestampdiff(year,dob,curdate()),city,bloodgroup,healthissues,lastdonateddate,availability from donordirectory where username=%s"""
        cursor.execute(_SQL, (request.form['duname'],))
        contents = cursor.fetchall()
        titles = (
        'user name', 'name', 'gender', 'phone no.', 'email', 'age', 'current city', 'blood group', 'health issues',
        'last donated date', 'availability', 'login details', 'donation history')
        return render_template('donor.html',
                               the_title='search results',
                               the_titles=titles,
                               log_row=contents)


@app.route('/searchdonorname')
@adcheck_logged_in
def search_donorname() -> 'html':
    return render_template('searchdonorname.html')


@app.route('/receivednamesearch', methods=['POST'])
@adcheck_logged_in
def find_donorname() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select username,name,gender,phoneno,email,timestampdiff(year,dob,curdate()),city,bloodgroup,healthissues,lastdonateddate,availability from donordirectory where name like %s"""
        cursor.execute(_SQL, ('%' + request.form['dname'] + '%',))
        contents = cursor.fetchall()
        titles = (
        'user name', 'name', 'gender', 'phone no.', 'email', 'age', 'current city', 'blood group', 'health issues',
        'last donated date', 'availability', 'login details', 'donation history')
        return render_template('donor.html',
                               the_title='search results',
                               the_titles=titles,
                               log_row=contents)


@app.route('/searchdonorphno')
@adcheck_logged_in
def search_donorphno() -> 'html':
    return render_template('searchdonorphno.html')


@app.route('/receivedphnosearch', methods=['POST'])
@adcheck_logged_in
def find_donorphno() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select username,name,gender,phoneno,email,timestampdiff(year,dob,curdate()),city,bloodgroup,healthissues,lastdonateddate,availability from donordirectory where phoneno=%s"""
        cursor.execute(_SQL, (request.form['dphno'],))
        contents = cursor.fetchall()
        titles = (
        'user name', 'name', 'gender', 'phone no.', 'email', 'age', 'current city', 'blood group', 'health issues',
        'last donated date', 'availability', 'login details', 'donation history')
        return render_template('donor.html',
                               the_title='search results',
                               the_titles=titles,
                               log_row=contents)


@app.route('/searchdonoremail')
@adcheck_logged_in
def search_donoremail() -> 'html':
    return render_template('searchdonoremail.html')


@app.route('/receivedemailsearch', methods=['POST'])
@adcheck_logged_in
def find_donoremail() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select username,name,gender,phoneno,email,timestampdiff(year,dob,curdate()),city,bloodgroup,healthissues,lastdonateddate,availability from donordirectory where email=%s"""
        cursor.execute(_SQL, (request.form['demail'],))
        contents = cursor.fetchall()
        titles = (
        'user name', 'name', 'gender', 'phone no.', 'email', 'age', 'current city', 'blood group', 'health issues',
        'last donated date', 'availability', 'login details', 'donation history')
        return render_template('donor.html',
                               the_title='search results',
                               the_titles=titles,
                               log_row=contents)


@app.route('/searchpatientname')
@adcheck_logged_in
def search_patientname() -> 'html':
    return render_template('searchpatientname.html')


@app.route('/receivepnamesearch', methods=['POST'])
@adcheck_logged_in
def find_patientname() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select patientid,patientname,gender,timestampdiff(year,dob,curdate()),phno,email,city,bloodgroup from patientregister where patientname like %s"""
        cursor.execute(_SQL, ('%' + request.form['pname'] + '%',))
        contents = cursor.fetchall()
        titles = ('patient id', 'patient name', 'gender', 'age', 'phone no.', 'email', 'current city', 'blood group')
        return render_template('viewallpatientdetails.html',
                               the_title='search results',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/searchpatientgender')
@adcheck_logged_in
def search_patientgender() -> 'html':
    return render_template('searchpatientgender.html')


@app.route('/receivepgendersearch', methods=['POST'])
@adcheck_logged_in
def find_patientgender() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select patientid,patientname,gender,timestampdiff(year,dob,curdate()),phno,email,city,bloodgroup from patientregister where gender=%s"""
        cursor.execute(_SQL, (request.form['pgender'],))
        contents = cursor.fetchall()
        titles = ('patient id', 'patient name', 'gender', 'age', 'phone no.', 'email', 'current city', 'blood group')
        return render_template('viewallpatientdetails.html',
                               the_title='search results',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/searchpatientcity')
@adcheck_logged_in
def search_patientcity() -> 'html':
    return render_template('searchpatientcity.html')


@app.route('/receivepcitysearch', methods=['POST'])
@adcheck_logged_in
def find_patientcity() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select patientid,patientname,gender,timestampdiff(year,dob,curdate()),phno,email,city,bloodgroup from patientregister where city=%s"""
        cursor.execute(_SQL, (request.form['pcity'],))
        contents = cursor.fetchall()
        titles = ('patient id', 'patient name', 'gender', 'age', 'phone no.', 'email', 'current city', 'blood group')
        return render_template('viewallpatientdetails.html',
                               the_title='search results',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/searchpatientdisease')
@adcheck_logged_in
def search_patientdisease() -> 'html':
    return render_template('searchpatientdisease.html')


@app.route('/receivepdiseasesearch', methods=['POST'])
@adcheck_logged_in
def find_patientdisease() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select name,gender,timestampdiff(year,dob,curdate()),phoneno,email,city,bloodgroup,healthissues from donordirectory where healthissues like %s"""
        cursor.execute(_SQL, ('%' + request.form['pdisease'] + '%',))
        contents = cursor.fetchall()
        titles = ('patient name', 'gender', 'age', 'phone no.', 'email', 'current city', 'blood group', 'healthissues')
        return render_template('viewallpatientdetails.html',
                               the_title='search results',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/logindetails/<username>')
@adcheck_logged_in
def view_logindetails(username) -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select * from userprofile where username=%s"""
        cursor.execute(_SQL, (username,))
        contents = cursor.fetchone()
        titles = ('user name', 'email', 'password', 'date of birth', 'date of registration')
        return render_template('viewlogindetails.html',
                               the_title='view login details',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/dhistory/<username>')
@adcheck_logged_in
def view_dhistory(username) -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select donationno,datedonated,donatedatcity from donationhistory where donorusername=%s"""
        cursor.execute(_SQL, (username,))
        contents = cursor.fetchall()
        titles = ('donation no.', 'date donated', 'donated at city')
        return render_template('viewdhistory.html',
                               the_title='view donation history',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/viewdonorlogindetails')
@ucheck_logged_in
def view_donorlogin() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select * from userprofile where username=%s"""
        cursor.execute(_SQL, (session['username'],))
        contents = cursor.fetchone()
        titles = ('user name', 'email', 'password', 'date of birth', 'date of registration')
        return render_template('viewdonorlogin.html',
                               the_title='view donor login details',
                               the_row_titles=titles,
                               the_data=contents)


@app.route('/delaccount')
@ucheck_logged_in
def del_account() -> 'html':
    return render_template('delaccount.html')


@app.route('/deleteaccount')
@ucheck_logged_in
def delete_account() -> 'html':
    try:
        delete_donoraccount()

    except Exception as err:
        msg = "****deletion failed with this error: " + str(err)
        print(msg)
        return render_template('goback1.html',
                               the_title='error')

    session.pop('logged_in')
    session.pop('username')
    return render_template('homepage.html',
                           the_title1='account deleted')


app.secret_key = 'youwillneverguess'

if __name__ == '__main__':
    app.run()
