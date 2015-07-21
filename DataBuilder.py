__author__ = 'acton'
import ProjectClass
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

class StateYear:
    def __init__(self,state_name):
        self.state_name = state_name
        self.Years = dict()

def cityBuilder(city_list,projectList):
    city_dict = dict()
    for city_name in city_list:
        city_dict[city_name] = ProjectClass.City(city_name)
    for proj in projectList:
        city_name = proj.school_city.upper()
        city_class = city_dict[city_name]
        if isinstance( proj.total_donations , float ) or isinstance( proj.total_donations , int ):
            city_class.total_donations += proj.total_donations
        if isinstance( proj.num_donors , float ) or isinstance( proj.num_donors , int ):
            city_class.count_donors += proj.num_donors
        city_class.count_project += 1
        if isinstance( proj.students_reached , float ) or isinstance( proj.students_reached , int ) :
            if not math.isnan(proj.students_reached):
                city_class.count_students += int(proj.students_reached)
        city_class.subjects.append(proj.primary_focus_subject)
        city_class.areas.append(proj.primary_focus_area)
    return city_dict

def stateBuilder(state_list,projectList):
    state_dict = dict()
    for state_name in state_list:
        state_dict[state_name] = ProjectClass.State(state_name)
    for proj in projectList:
        state_name = proj.school_state.upper()
        state_class = state_dict[state_name]
        if isinstance( proj.total_donations , float ) or isinstance( proj.total_donations , int ):
            state_class.total_donations += proj.total_donations
        if isinstance( proj.num_donors , float ) or isinstance( proj.num_donors , int ):
            state_class.count_donors += proj.num_donors
        state_class.count_project += 1
        if isinstance( proj.students_reached , float ) or isinstance( proj.students_reached , int ) :
            if not math.isnan(proj.students_reached):
                state_class.count_students += int( proj.students_reached)
        state_class.subjects.append(proj.primary_focus_subject)
        state_class.areas.append(proj.primary_focus_area)
    return state_dict

def StatetYearBuilder():
    state_list = ["AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID", "IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY", "OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"]
    state_proj_dict = dict()
    project_list_ = open('project_list_dict.txt','rb')
    projectList = pickle.load(project_list_)
    year_list = range(2000,2015)
    state_year_dict = dict()
    for state in state_list:
        state_proj_dict[state] = []
        for proj in projectList:
            if proj.school_state == state:
                state_proj_dict[state].append(proj)
    for state in state_list:
        state_year_class = StateYear(state)
        for year in year_list:
                state_year_class.Years[year] = State(state)
        for proj in state_proj_dict[state]:
            for year in year_list:
                if int(proj.date_posted) == year:
                    state_year_class.Years[year].total_donations += int(proj.total_donations)
                    if  not math.isnan(proj.students_reached):
                        state_year_class.Years[year].count_students += int(proj.students_reached )
                    state_year_class.Years[year].count_donors  += int(proj.num_donors)
                    state_year_class.Years[year].count_project += 1
                    state_year_class.Years[year].subjects.append( proj.primary_focus_subject)
                    state_year_class.Years[year].areas.append( proj.primary_focus_area )
        state_year_dict[state] = state_year_class
        return state_year_dict



def dataDump(city_list,project_list):
    citylist_file = open('citylist.txt', 'wb')
    projectlist_file = open('projectlist.txt','wb')
    pickle.dump(project_list, projectlist_file)
    pickle.dump(city_list, citylist_file)
    projectlist_file.close()
    citylist_file.close()


def dataDump2(city_dict,state_dict):
    citydict_file = open('citydict.txt', 'wb')
    statedict_file = open('statedict.txt','wb')
    pickle.dump(state_dict, statedict_file)
    pickle.dump(city_dict, citydict_file)
    citydict_file.close()
    statedict_file.close()

def dataDump3(state_year_dict):
    state_year_dict_file = open('state_year_dict.txt', 'wb')
    pickle.dump(state_year_dict,state_year_dict_file)
    state_year_dict_file.close()


def dataDump4(state_city_dict):
    state_city_dict_file = open('state_city_dict.txt', 'wb')
    pickle.dump(state_city_dict,state_city_dict_file)
    state_city_dict_file.close()


def projectCrush(PATH):
    data = pandas.read_csv(PATH)
    city_list= cityList(data)
    projectList = []
    for index, row in data.iterrows():
        aProj = ProjectClass.Project(row)
        projectList.append(aProj)
    return projectList, city_list


def cityList(data):
    city_list = []
    for city in data['school_city']:
        if city.upper() not in city_list:
            city_list.append(city.upper())
    return city_list



if __name__ == "__main__":
    print "Use methods to build your data structure"


