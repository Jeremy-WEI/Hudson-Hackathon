__author__ = 'acton'
import ProjectClass
import pandas
import numpy
import flask
import sys
import os
import scipy

#pandas.DataFrame.from_csv();


state_list = ["AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID", "IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY", "OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"]
state_dict = dict()
projectList = []

data = pandas.read_csv('~/PycharmProjects/opendata_projects.csv')

#print(data.columns)
#print type(data)
#print data.shape
#print data.index
#print data.iloc[1]

for index, row in data.iterrows():
    aProj = ProjectClass.Project(row)
    projectList.append(aProj)

# print len(projectList)
# print type(projectList[1000].total_donations)

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
    if proj.students_reached:
        state_class.count_students += proj.students_reached
    state_class.subjects.append(proj.primary_focus_subject)
    state_class.areas.append(proj.primary_focus_area)



        # self.total_donations = 0
        # self.count_students = 0
        # self.count_donors = 0
        # self.count_project = 0
        # self.subjects = []
        #
        #
        # self._projectid = row['_projectid']
        # self.school_latitude = row['school_latitude']
        # self.school_longitude = row['school_longitude']
        # self.school_city = row['school_city']
        # self.school_state = row['school_state']
        # self.school_zip = row['school_zip']
        # self.school_metro = row['school_metro']
        # self.school_district = row['school_district']
        # self.school_county = row['school_county']
        # self.teacher_prefix = row['teacher_prefix']
        # self.primary_focus_subject = row['primary_focus_subject']
        # self.primary_focus_area = row['primary_focus_area']
        # self.poverty_level = row['poverty_level']
        # self.grade_level = row['grade_level']
        # self.total_price_including_optional_support = row['total_price_including_optional_support']
        # self.students_reached = row['students_reached']
        # self.total_donations = row['total_donations']
        # self.num_donors = row['num_donors']
        # self.funding_status = row['funding_status']
        # self.date_completed = row['date_completed']


# state_dict = dict()
# for state_name in state_list:
#     state_dict[state_name] = State(state_name)
