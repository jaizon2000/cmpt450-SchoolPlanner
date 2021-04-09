import numpy as np
import pandas as pd
from Course import *


class Student:
    def __init__(self, name="John Doe", id=0):
        self.name = name
        self.id = id

        self.df = pd.read_csv('cmpt-courses-cleaned.csv')
        self.df_dict = self.df.to_dict('records')
        self.course_class_list = [Course(c['id'], c['name'], c['credit'], c['description'], c['prereq']) for c in
                                  self.df_dict]

        self.my_courses = self.df.copy().iloc[0:0]  # erase all rows but keep cols: https://bit.ly/2PCF5Xi

    def add(self, course, status):
        # find course to add in course database
        other = self.df[self.df['id'] == course.upper()]

        if len(other) == 0:
            # course doesn't exist in database
            return f"{course.upper()} doesn't exist the database"

        # add to my courses, remove duplicates, reset index numbering
        self.my_courses = pd.concat([self.my_courses, other], sort=True).drop_duplicates(subset=['id'], keep='last')

        # add/change status col of given course
        self.my_courses.loc[self.my_courses['id'] == course.upper(), 'status'] = status.upper()
        # print(self)
        return self.my_courses

    def remove(self, course):
        i = self.my_courses[self.my_courses.id == course.upper()].index
        self.my_courses = self.my_courses.drop(i)
        # print(self)
        return self.my_courses

    def set(self, new_df):
        # set courses from a new df
        new_dtypes = {"Course ID": object, "Course Name": object, "Credits": int, "Prerequisites": object,
                      "Status": object}

        # new_df.astype(new_dtypes)   # change dtypes
        #
        # self.my_courses = self.my_courses.copy().iloc[0:0]  # erase all rows but keep cols names: https://bit.ly/2PCF5Xi
        # print(self)
        try:
            print(new_df['id'])
            key = 'id'
        except:
            print("Column name isn't the one given or doesn't exist. Trying 'Course ID'...")
            # print(new_df['Course ID'])
            key = 'Course ID'

        for course in new_df[key]:
            # getting the value of cell: https://bit.ly/3fS2ZJm
            status = new_df[new_df[key] == course]['Status'].values[0]
            self.add(course, status)
        return self.my_courses

    def getdf(self, sort=True):
        if sort:
            return self.my_courses.sort_values(by='id')

        else:
            return self.my_courses

    def getdf_dict(self):
        return self.my_courses.to_dict('records')

    def idExists(self, c_id):
        return c_id.upper() in [c.id for c in self.course_class_list]

    def findClass(self, c_id):
        for c in self.course_class_list:
            if c.id == c_id.upper:
                return c

    def __len__(self):
        return len(self.my_courses.index)

    def __repr__(self):
        return f"{self.my_courses}"


stud1 = Student()
stud1.add("CMPT 201", "WIP")
stud1.add("CMPT 201", "Planned")
stud1.add("CMPT 101", "Planned")

stud1.add("CMPT 200", "Planned")
stud1.remove("CMPT 201")
test = pd.read_csv("Data.csv")

# stud1.add("CMPT 200", "Completed")
#
# stud1.add("CMPT 305", "Planned")
# # stud1.add("CMPT 200", "Completed")
# print(stud)
