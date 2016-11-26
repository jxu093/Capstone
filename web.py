from flask import Flask, render_template, request, jsonify
import script

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/results/universities')
def universities():
    data = script.get_data()
    return jsonify(data)


if __name__ == "__main__":
    app.run()
    # script.get_data()
