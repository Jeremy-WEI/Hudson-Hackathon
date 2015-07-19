import DataBuilder
import ProjectClass
from flask import Flask, render_template, jsonify, request
from collections import Counter

city_dict, state_dict = DataBuilder.getdata()
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/stateInfo')
def getStateInfo():
    state = request.args.get('state')
    stateInfo = state_dict[state]
    countSubjects = Counter(stateInfo.subjects).items()
    countSubjects = sorted(countSubjects, key=lambda subject: subject[1])
    countSubjects.reverse()
    # print countSubjects
    # print stateInfo.state_name
    # print stateInfo.count_students
    # print stateInfo.count_donors
    # print stateInfo.count_project
    # print type(stateInfo.subjects)
    # print stateInfo.areas
    return jsonify({
        "state_name": stateInfo.state_name,
        "total_donations": stateInfo.total_donations,
        "count_students": stateInfo.count_students,
        "count_donars": stateInfo.count_donors,
        "count_project": stateInfo.count_project,
        "popular_subjects": countSubjects[0:5],
        # "areas": stateInfo.areas
    })

# @app.route('/about')
# def about():
#   return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
