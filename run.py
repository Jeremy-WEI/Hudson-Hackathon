from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/test')
def test():
    return jsonify({"a": 1})

# @app.route('/about')
# def about():
#   return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
