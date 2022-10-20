from turtle import st
from warnings import catch_warnings
from flask import Flask, render_template, request
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=./DigiCertGlobalRootCA.crt;UID=bzv34237;PWD=8wV6VLP4EjMOwA15",'','')
app = Flask(__name__)
@app.route('/')
def home():
  return render_template('home copy.html')

@app.route('/login')
def new_student():
  return render_template('login.html')

@app.route('/about')
def ne():
  return render_template('about.html')
@app.route('/signup')
def student():
  return render_template('signup.html')

@app.route('/addre',methods = ['POST', 'GET'])
def addre():
  if request.method == 'POST':

    email = request.form['email']
    name = request.form['name']
    password1 = request.form['password1']
    password2 = request.form['password2']

    sql = "SELECT * FROM register WHERE name =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('login.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO register VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, email)
      ibm_db.bind_param(prep_stmt, 2,name )
      ibm_db.bind_param(prep_stmt, 3, password1)
      ibm_db.bind_param(prep_stmt, 4, password2)
      ibm_db.execute(prep_stmt)
    return render_template('home copy.html', msg="Student Data saved successfuly..")

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
  if request.method == 'POST':

    name = request.form['name']
    password = request.form['pass']

    sql = "SELECT name,password1 FROM register WHERE name =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    try:
      if account['PASSWORD1']==password and account['NAME']==name :
        return render_template('base.html')
      else:
        return render_template('login.html')
    except:
      return "<h1><center>Please enter valid credentials<center></h1>"

if __name__ == '__main__':
   app.run(debug = True)