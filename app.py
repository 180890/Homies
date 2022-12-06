#import libraries
from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
import stripe
import time
app=Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51MBzMqSD6LAQPZyMwWpxgX03gFVt6uQ6qPOCor0oozSKsemE0CxzwNwvPub9PGvsT22qBlvEquxL1ltuPrTsrFkk00xRGmmNmH'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51MBzMqSD6LAQPZyMH1lOtYsFvPScawQIZduk6ptRX2BRBtFOBus8yaNhRffCbfEDMRUBkjvMOLoavNPw6CF9RUaI00ZdwHcW6K'
stripe.api_key = app.config['STRIPE_SECRET_KEY']


app.secret_key = "4db8b51a4017e427f3ea5c2137c450f767dce1bf"  

#code for connection
app.config['MYSQL_HOST'] = 'localhost'#hostname
app.config['MYSQL_USER'] = 'root'#username
app.config['MYSQL_PASSWORD'] = ''#password

app.config['MYSQL_DB'] = 'blogdata'#database name
mysql = MySQL(app)



@app.route('/pindex')
def pindex():

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1MC0JRSD6LAQPZyMHbmJiIWI',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('pindex', _external=True),
    )

    return render_template(
        'pindex.html', 
        checkout_session_id=session['id'], 
        checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
    )

@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1MC0JRSD6LAQPZyMHbmJiIWI',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('pindex', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}











@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/savedetails',methods=['GET', 'POST'])

def savedetails():
    if request.method == "POST":
            UN = request.form['full_name']
            EMAIL = request.form['email']
            PN=request.form['phonenumber']
            PSS = request.form['password']
            CPS = request.form['confirm_password']
            if(PSS!=CPS):
                return render_template('register.html',msg="Password doesn't matches!")
            else:
                cur = mysql.connection.cursor()
                
                
                Name = UN
                Email = EMAIL
                Password = PSS
                Phonenumber = PN
                cur.execute("INSERT INTO User(Name, Email, PhoneNumber, Password) VALUES (%s, %s, %s, %s)", (Name, Email, Phonenumber, Password))
                mysql.connection.commit()
                cur.close()
                return render_template("login.html",msg="Registered Successfully, Please Login")
    
    
    

@app.route('/logged',methods=['GET', 'POST'])

def loggedin():
    if request.method == "POST":
            EMAIL = request.form['email']
            PSS = request.form['password']
            cur = mysql.connection.cursor()

            cur.execute('SELECT * FROM user WHERE email = %s AND password = %s', (EMAIL, PSS,))
            account = cur.fetchone()
            if account:
                session['loggedin'] = True
                session['userid']=account[0]
                session['email'] = account[2]
                return redirect("/home")
            
            else:
                return  render_template('login.html',msg="Incorrect username/password!")
    

@app.route('/home')
def home():
 
    return render_template('home.html')

@app.route('/logout')  
def logout():
   session.pop('email', None)
   session.pop('userid', None)
   return render_template('index.html')


@app.route("/user/<name>")
def user(name):
    return render_template("user.html",user=name)


"""
@app.route('/srch',methods=['GET', 'POST'])
def serch():
    if request.method == "POST":
            sq = "%"+request.form['search']+"%"
            cur = mysql.connection.cursor()
            
            cur.execute("SELECT * FROM blogs where isActive='true' and blogTitle like '%s'"%(sq))
            blog = cur.fetchall()
            return render_template('home.html',blogData=blog)
"""
        

@app.route('/adds')
def adds():
    return render_template('addproperty.html')

@app.route('/addproperty',methods=['GET', 'POST'])
def addproperty():
    if request.method == "POST":
            propName = request.form['propName']
            propPrice = request.form['propPrice']
            propPhone = request.form['propPhone']
            propType = request.form['propType']
            propCity = request.form['propCity']
            propPhone = request.form['propPhone']
            occupency = request.form['occupency']
            gendOccupency = request.form['gendOccupency']
            amenities = request.form.getlist("amenities")
            propAddress = request.form['propAddress']
            propDetails = request.form['propDetails']
            propImage = request.form['propImage']
            cur = mysql.connection.cursor()
            
            

            #UserId = session['userid']
            str1 = ','.join(amenities)
            cur.execute("INSERT INTO property(propName, propPrice, propPhone, propType, propCity, occupency, gendOccupency, amenities, propAddress,propDetails, propImage) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)", (propName, propPrice, propPhone, propType, propCity, occupency, gendOccupency, str1, propAddress,propDetails, propImage))
            mysql.connection.commit()
            cur.close()
            return  render_template('index.html',msg=" Added Successfully")




app.run(debug=True)