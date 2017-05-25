from flask import *
from flaskext.mysql import MySQL

app = Flask(__name__)

#Session key
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

# MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'abc123'
app.config['MYSQL_DATABASE_DB'] = 'supermarket'
app.config['MYSQL_DATABASE_HOST'] = 'app_mysql-node01_1'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/registered')
def SignUp():
    return render_template('registered.html')

@app.route('/login')
def SignIn():
    return render_template('login.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact')
def contact():
   return render_template('contact.html')

@app.route('/short-codes')
def shortcode():
  return render_template('short-codes.html')

@app.route('/faq')
def faq():
   return render_template('faq.html')

@app.route('/products')
def products():
  return render_template('products.html')
  
@app.route('/groceries')
def groceries():
  return render_template('groceries.html')

@app.route('/household')
def household():
   return render_template('household.html')

@app.route('/personalcare')
def personalcare():
  return render_template('personalcare.html')

@app.route('/packagedfoods')
def packagedfoods():
   return render_template('packagedfoods.html')

@app.route('/beverages')
def beverages():
  return render_template('beverages.html')

@app.route('/gourmet')
def gourmet():
  return render_template('gourmet.html')
  
@app.route('/offers')
def offers():
  return render_template('offers.html')
  
@app.route('/single')
def single():
  return render_template('single.html')

  
@app.route('/checkout')
def checkout():
   return render_template('checkout.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    if request.method == 'POST':
        try:
            _name = request.form['inputName']
            _username = request.form['inputEmail']
            _password = request.form['inputPassword']
    
            # validate the received values
            if _name and _username and _password:
    
                #MySQL Call
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_createUser',(_name,_username,_password))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    #return json.dumps({'message':'User created successfully !'})
                    return url_for('main')
                else:
                    return url_for('usercheck')
                    #return json.dumps({'error':str(data[0])})                
            else:
                #return json.dumps({"html": "<span>Enter the required fields</span>"})
                return url_for('checkField')
                
    
        except Exception as e:
            return json.dumps({'error':str(e)})
            cursor.close()
            conn.close()
      
@app.route('/signIn',methods = ['POST', 'GET'])
def signIn():
    if request.method == 'POST':
        
        try:
            _username = request.form['inputEmail']
            _password = request.form['inputPassword']
    
            # validate the received values
            if _username and _password:
    
                #MySQL Call
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_loginUser',(_username,_password))
                data = cursor.fetchall()
                
                if len(data) > 0:
                    conn.commit()
                    session['username'] = _username
                    return url_for('main')
                    return redirect(url_for('main'))
                    
                               
                else:
                    #abort(401)
                    return url_for('usercheck')
            else:
                #return json.dumps('Action Required: Input username and password')
                return url_for('checkField')
    
        except Exception as e:
            return json.dumps({'error':str(e)})
            cursor.close()
            conn.close()
            
@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('main'))

@app.route("/usercheck")
def usercheck():
    return 'Check User'

@app.route("/checkField")
def checkField():
    return 'checkField'

@app.route("/checkCredential")
def checkCredential():
    return 'checkCredential'


@app.route("/")
def main():
    return render_template('index2.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')