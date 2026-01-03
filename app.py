from flask import Flask, render_template, request, make_response, redirect, url_for
import jwt
import datetime

app = Flask(__name__)

# CONFIGURATION
# Real world mein ye "StrongPassword123!@#" hona chahiye tha.
# Lekin developer ne dictionary ka koi common word use kiya hai.
# HINT: The secret is a very common english word (lowercase).
SECRET_KEY = "secret"  

FLAG = "CREED{JWT_S1gn4tur3_Cr4ck3d_Succ3ssfully}"

@app.route('/')
def home():
    token = request.cookies.get('auth_token')
    if not token:
        return render_template('index.html')
    
    try:
        # Server token verify kar raha hai
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        if data['role'] == 'admin':
            return render_template('admin.html', flag=FLAG, user=data['user'])
        else:
            return render_template('dashboard.html', user=data['user'], role=data['role'])
            
    except jwt.ExpiredSignatureError:
        return "Token Expired! Login again."
    except jwt.InvalidTokenError:
        return "Invalid Token! Tampering detected."

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    # Koi password check nahi hai, bas login ho jao as Guest
    
    # Payload create ho raha hai
    payload = {
        'user': username,
        'role': 'guest',  # By default sab guest hain
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    
    # Token generate ho raha hai
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('auth_token', token)
    return resp

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('auth_token', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
