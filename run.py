from flask import Flask, render_template, jsonify, request
import DataBuilder, ProjectClass

city_dict, state_dict = DataBuilder.getdata()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/test')
def test():
	#city_dict, state_dict = DataBuilder.getdata()
	stateid = request.args.get('statename')
	print stateid
	print state_dict[stateid]
	if stateid == "NY":
		return jsonify({"a": 2})
	else:
		return jsonify({"a": 1})

# @app.route('/about')
# def about():
#   return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
