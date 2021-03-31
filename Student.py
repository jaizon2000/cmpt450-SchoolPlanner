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
        self.my_courses.loc[self.my_courses['id'] == course.upper(), 'status'] = status
        # print(self)
        return self.my_courses

    def delete(self, course):
        i = self.my_courses[self.my_courses.id == course.upper()].index
        self.my_courses = self.my_courses.drop(i)
        # print(self)
        return self.my_courses

    def getdf(self, sort=True):
        if sort:
            return self.my_courses.sort_values(by='id')

        else:
            return self.my_courses

    def __repr__(self):
        return f"{self.my_courses}"


stud1 = Student()
stud1.add("CMPT 201", "WIP")
stud1.add("CMPT 201", "Planned")
stud1.add("CMPT 101", "Planned")

stud1.add("CMPT 200", "Planned")
stud1.delete("CMPT 201")

# stud1.add("CMPT 200", "Completed")
#
# stud1.add("CMPT 305", "Planned")
# # stud1.add("CMPT 200", "Completed")
# print(stud)
