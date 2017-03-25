from flask import Flask, render_template, request, jsonify, session, redirect
import hashlib
import os
import script
import dao


app = Flask(__name__)
app.secret_key = 'aaBBccDDee'

school_names = ['mcmaster university', 'brock university', 'university of toronto', 'university of waterloo']
restaurant_names = ['lava pizza', 'boston pizza', 'tim hortons', 'taco del mar']
show_names = ['the walking dead', 'orange is the new black', 'grey\'s anatomy', 'vampire diaries']
athlete_names = ['lebron james', 'tiger woods', 'serena williams', 'tom brady']
names = {'schools': school_names, 'restaurants': restaurant_names, 'shows': show_names, 'athletes': athlete_names}


@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/test/<name>')
# def test(name):
#     session['testname'] = name
#     return testz()
#
#
# @app.route('/test')
# def testz():
#     if 'testname' in session:
#         return session['testname']
#     else:
#         return 'nothing found'


@app.route('/custom')
def custom():
    if 'username' not in session:
        return redirect('login')
    return render_template('custom.html', username=session['username'])


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('custom')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        action = request.form['action']

        if action == 'register':
            salt = os.urandom(64)
            salt = salt.encode('base64')
            m = hashlib.md5()
            m.update(password + salt)
            message = dao.create_user({'username': username, 'hashedpass': m.hexdigest(), 'salt': salt})
            return render_template('login.html', message=message)
        elif action == 'login':
            existing_user = dao.get_user(username)
            if existing_user is None:
                return render_template('login.html', message='username not found')
            else:
                m = hashlib.md5()
                m.update(password + existing_user['salt'])
                if m.hexdigest() == existing_user['hashedpass']:
                    session['username'] = username
                    return redirect('custom')
                else:
                    return render_template('login.html', message='password incorrect')

    return render_template('login.html')


@app.route('/results/<collection>')
def get_data(collection):
    data = dao.get_tweets(names[collection], collection)
    return jsonify(data)


@app.route('/load-data/<collection>')
def load_schools(collection):
    data = script.get_data(names[collection])
    dao.save_tweets(data, collection)
    return jsonify({'status': 'complete'})


@app.route('/load-custom-data/<topic>')
def load_custom_data(topic):
    if 'username' in session:
        data = script.get_data([topic])
        dao.save_custom_data(data[0], session['username'])
        return jsonify({'status': 'complete'})


@app.route('/get-custom-data')
def get_custom_data():
    if 'username' in session:
        data = dao.get_custom_data(session['username'])
        return jsonify(data)


if __name__ == "__main__":
    app.run()
    # script.get_data()
