#import DataBuilder
import ProjectClass
from flask import Flask, render_template, jsonify, request
from collections import Counter
import pandas
import numpy
import flask
import sys
import os
import scipy
import scipy.io as sio
import pickle
import math
import json


class StateYear:
    __module__ = os.path.splitext(os.path.basename(__file__))[0]

    def __init__(self, state_name):
        self.state_name = state_name
        self.Years = dict()


class State:
    __module__ = os.path.splitext(os.path.basename(__file__))[0]

    def __init__(self, state_name):
        self.state_name = state_name
        self.total_donations = 0
        self.count_students = 0
        self.count_donors = 0
        self.count_project = 0
        self.subjects = []
        self.areas = []


class City:
    __module__ = os.path.splitext(os.path.basename(__file__))[0]

    def __init__(self, city_name):
        self.city_name = city_name
        self.total_donations = 0
        self.count_students = 0
        self.count_donors = 0
        self.count_project = 0
        self.subjects = []
        self.areas = []


class Project:
    __module__ = os.path.splitext(os.path.basename(__file__))[0]

    def __init__(self, row):
        self._projectid = row['_projectid']
        self.school_latitude = row['school_latitude']
        self.school_longitude = row['school_longitude']
        self.school_city = row['school_city']
        self.school_state = row['school_state']
        self.school_zip = row['school_zip']
        self.school_metro = row['school_metro']
        self.school_district = row['school_district']
        self.school_county = row['school_county']
        self.teacher_prefix = row['teacher_prefix']
        self.primary_focus_subject = row['primary_focus_subject']
        self.primary_focus_area = row['primary_focus_area']
        self.poverty_level = row['poverty_level']
        self.grade_level = row['grade_level']
        self.total_price_including_optional_support = row[
            'total_price_including_optional_support']
        self.students_reached = row['students_reached']
        self.total_donations = row['total_donations']
        self.num_donors = row['num_donors']
        self.funding_status = row['funding_status']
        date = str(row['date_posted'])
        year = date.split('-')[0]
        self.date_posted = int(year)
        self.date_completed = row['date_completed']


# def getdata():
#
#     city_dict_ = open('citydict.txt','rb')
#     state_dict_ = open('statedict.txt','rb')
#     state_year_dict_ = open('state_year_dict.txt','rb')
#     global city_dict
#     global state_dict
#     global state_dict
#     city_dict = pickle.load(city_dict_)
#     state_dict = pickle.load(state_dict_)
#     state_year_dict  = pickle.load(state_year_dict_)
#     return city_dict, state_dict, state_year_dict


if __name__ == "__main__":
    from DataBuilder import *
    state_year_dict_ = open('state_year_dict.txt', 'rb')
    city_dict_ = open('citydict.txt', 'rb')
    state_dict_ = open('statedict.txt', 'rb')
    global city_dict
    global state_dict
    city_dict = pickle.load(city_dict_)
    state_dict = pickle.load(state_dict_)
    state_year_dict = pickle.load(state_year_dict_)
    # print city_dict

# DataBuilder.dumpCityYearDict()
# city_dict, state_dict, state_year_dict = DataBuilder
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/chart')
def test():
    #city_dict, state_dict = DataBuilder.getdata()
    stateid = request.args.get('statename')
    areas = state_dict[stateid].areas
    areas_dict = {}
    for area in areas:
        if area in areas_dict:
            areas_dict[area] += 1
        else:
            areas_dict[area] = 1
    json_result = json.dumps(areas_dict)

    raised_money = {}
    for year in xrange(2008, 2015):
        raised_money[year] = state_year_dict[stateid].Years[year].total_donations
    json_result2 = json.dumps(raised_money)
    projects_num = {}
    for year in xrange(2008, 2015):
        projects_num[year] = state_year_dict[stateid].Years[year].count_project
    json_result3 = json.dumps(projects_num)
    return jsonify({"area": json_result, "raise": json_result2, "projects": json_result3})


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
        "popular_subjects": countSubjects[0:7],
        # "areas": stateInfo.areas
    })

@app.route('/compare')
def compare():
    result = {}
 
    firststate = request.args.get('firststate')
    secondstate = request.args.get('secondstate')
    for stateid in [firststate, secondstate]:
        areas = state_dict[stateid].areas
        areas_dict = {}
        for area in areas:
            if area in areas_dict:
                areas_dict[area] += 1
            else:
                areas_dict[area] = 1
        json_result = json.dumps(areas_dict)

        raised_money = {}
        for year in xrange(2008, 2015):
            raised_money[year] = state_year_dict[stateid].Years[year].total_donations
        json_result2 = json.dumps(raised_money)
        projects_num = {}
        for year in xrange(2008, 2015):
            projects_num[year] = state_year_dict[stateid].Years[year].count_project
        json_result3 = json.dumps(projects_num)
        result[stateid] = {"area": json_result, "raise": json_result2, "projects": json_result3}
    # print result
    # print jsonify(result)
    print json.dumps(result)
    # jsonstring =  jsonify(result)
    # print jsonstring
    # jsonstring = json.dumps(jsonstring)
    # print jsonstring
    return render_template('compare.html', jsonstring=result)
	# return jsonify({'firststate': firststate, 'secondstate': secondstate})

  

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
