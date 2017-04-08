from flask import Flask, render_template, request, jsonify, session, redirect
import hashlib
import os
import script
import dao
import re


app = Flask(__name__)
app.secret_key = 'aaBBccDDee'

# preset topics
school_names = ['mcmaster university', 'brock university', 'university of toronto', 'university of waterloo']
restaurant_names = ['lava pizza', 'boston pizza', 'tim hortons', 'taco del mar']
show_names = ['the walking dead', 'orange is the new black', 'grey\'s anatomy', 'vampire diaries']
athlete_names = ['lebron james', 'tiger woods', 'serena williams', 'tom brady']
names = {'schools': school_names, 'restaurants': restaurant_names, 'shows': show_names, 'athletes': athlete_names}


@app.route('/')
def home():
    return render_template('index.html')


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
        # make new account
        if action == 'register':
            # generate salt and hash for password
            salt = os.urandom(64)
            salt = salt.encode('base64')
            m = hashlib.md5()
            m.update(password + salt)
            # store user in database
            message = dao.create_user({'username': username, 'hashedpass': m.hexdigest(), 'salt': salt})
            return render_template('login.html', message=message)
        # login
        elif action == 'login':
            # see if user exists
            existing_user = dao.get_user(username)
            if existing_user is None:
                return render_template('login.html', message='username not found')
            else:
                # see if hash of entered password matches what's stored
                m = hashlib.md5()
                m.update(password + existing_user['salt'])
                if m.hexdigest() == existing_user['hashedpass']:
                    session['username'] = username
                    return redirect('custom')
                else:
                    return render_template('login.html', message='password incorrect')

    return render_template('login.html')


# get saved data for presets in json
@app.route('/results/<collection>')
def get_data(collection):
    data = dao.get_tweets(names[collection], collection)
    return jsonify(data)


# run script to fetch new data for presets
@app.route('/load-data/<collection>')
def load_schools(collection):
    data = script.get_data(names[collection])
    dao.save_tweets(data, collection)
    return jsonify({'status': 'complete'})


# run script to fetch new data for given topic
@app.route('/load-custom-data/<topic>')
def load_custom_data(topic):
    # only run if a user is logged in
    if 'username' in session:
        # sanitize input
        topic = re.sub('[^0-9a-zA-Z -]+', '', topic)
        data = script.get_data([topic])
        dao.save_custom_data(data[0], session['username'])
        return jsonify({'status': 'complete'})


# get the saved data for a custom topic
@app.route('/get-custom-data')
def get_custom_data():
    if 'username' in session:
        data = dao.get_custom_data(session['username'])
        return jsonify(data)


if __name__ == "__main__":
    app.run()
    # script.get_data()
