from flask import Flask, render_template, request, jsonify
import script
import dao

app = Flask(__name__)

school_names = ['mcmaster university', 'brock university', 'university of toronto', 'university of waterloo']
restaurant_names = ['lava pizza', 'boston pizza', 'tim hortons', 'taco del mar']
show_names = ['the walking dead', 'orange is the new black', 'grey\'s anatomy', 'vampire diaries']
athlete_names = ['lebron james', 'tiger woods', 'serena williams', 'tom brady']
names = {'schools': school_names, 'restaurants': restaurant_names, 'shows': show_names, 'athletes': athlete_names}


@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/results/universities')
# def universities():
#     data = script.get_data(['mcmaster university'])
#     return jsonify(data)


@app.route('/results/<collection>')
def get_data(collection):
    data = dao.get_tweets(names[collection], collection)
    return jsonify(data)


@app.route('/load-data/<collection>')
def load_schools(collection):
    data = script.get_data(names[collection])
    dao.save_tweets(data, collection)
    return jsonify({'status': 'complete'})


if __name__ == "__main__":
    app.run()
    # script.get_data()
