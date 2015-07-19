__author__ = 'acton'
import pandas
import numpy
import flask
import sys
import os
import scipy
import scipy.io as sio
import pickle
import math


class State:
    def __init__(self,state_name):
        self.state_name = state_name
        self.total_donations = 0
        self.count_students = 0
        self.count_donors = 0
        self.count_project = 0
        self.subjects = []
        self.areas = []

class City:
    def __init__(self,city_name):
        self.city_name = city_name
        self.total_donations = 0
        self.count_students = 0
        self.count_donors = 0
        self.count_project = 0
        self.subjects = []
        self.areas = []


class Project:
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
        self.total_price_including_optional_support = row['total_price_including_optional_support']
        self.students_reached = row['students_reached']
        self.total_donations = row['total_donations']
        self.num_donors = row['num_donors']
        self.funding_status = row['funding_status']
        self.date_completed = row['date_completed']

if __name__ == "__main__":
    city_dict_ = open('/Users/acton/PycharmProjects/DonorChoose/HudsonHack/citydict.txt','rb')
    state_dict_ = open('/Users/acton/PycharmProjects/DonorChoose/HudsonHack/statedict.txt','rb')
    city_dict = pickle.load(city_dict_)
    state_dict = pickle.load(state_dict_)
    print city_dict
    print state_dict['NY'].count_students
    print city_dict['FAIRPORT'].count_students
