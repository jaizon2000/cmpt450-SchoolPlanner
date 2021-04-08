# TUT LINK: https://realpython.com/beautiful-soup-web-scraper-python/#scraping-the-monster-job-site
# https://realpython.com/python-requests/

# Jan 18, 2021
# Jehdi Aizon

# Import packages for data cleaning
import numpy as np
import pandas as pd
import re  # For finding specific strings in the text

# Import for web scraping
import requests
from bs4 import BeautifulSoup

# networkx: https://bit.ly/3f3OGkC
import networkx as nx

from Course import *

G = nx.Graph()


# print(df)


# https://docs.python.org/3/library/pprint.html


def response_status_eg():
    response = requests.get('https://api.github.com')

    if response.status_code == 200:  # or just response
        print("200: Success!")
    elif response.status_code == 404:
        print("404: Not Found.")
    elif response.status_code == 204:
        print("204: No Content.")
    elif response.status_code == 304:
        print("304: Not Modified.")
    else:
        # If the response was successful, no Exception will be raised
        response.raise_for_status()


def get_prereqs(string):
    # todo make it get a list of prerequisites
    prereqs = []

    found = False
    string = string.replace("Prerequisites", "").replace("Prerequisite", "").replace(":", "").strip()

    # using any() method: https://bit.ly/311XgrZ
    if string.lower().find("consent of the department") != -1:
        prereqs.append("Consent of the department")
    # print(f"isFound: {string}")

    string_list = string.split(" ")
    for elem in string_list:
        elem = elem.replace("\xa0", " ")

        # find courses
        for tag in ["CMPT", "MATH", "ENGL", "STAT", "PSYC", "300-level", "200-level", "100-level", "and", "or"]:
            if elem.find(tag) != -1:
                found = True

        if found:
            prereqs.append(elem)
            # print(f"isFound: {elem}")
            found = False

    print(prereqs)

    cleaned = []

    # prep cleaned list
    for elem in prereqs:
        if elem in ["or", "and"]:
            cleaned.append([])
    # return all index of found: https://bit.ly/3c8msn0
    indexes = [i for i, x in enumerate(prereqs) if x in ["or", "and"]]
    # print(indexes)
    # print(cleaned)

    return tuple(prereqs)


def print_course(course_elems):
    for course_elem in course_elems:
        # Course code, title, and credits
        course = course_elem.find(class_='courseblocktitle')
        course = course.text.split("\n")

        # ID
        course_id = course[0].replace("\xa0", " ")  # replace weird escape code
        # Title
        course_title = course[1]
        # Credits
        course_credits = int(course[2].replace(" Credits", ""))

        # Course description
        course_desc = course_elem.find(class_='courseblockdesc')

        # Course pre-requisites
        course_prereq_data = course_elem.find(class_='courseblockextra')

        # Print
        # print(course_id)
        # print(course_title)
        # print(course_credits)
        # print(course_desc.text)
        prereqs = ()
        if course_prereq_data is not None:
            print(course_prereq_data.text)
            course_prereq = course_prereq_data.text \
                .replace('.', '') \
                .replace(',', '') \
                .replace("'", '') \
                .strip()
            prereqs = get_prereqs(course_prereq)

            # print(course_prereq)
            # print(course_prereq_data.text)
        print(prereqs)

        course_id_list.append(Course(course_id, course_title, course_credits, course_desc.text, prereqs))
        # todo create a Course class when parameters all known
        print()


def init_df(list_of_courses):
    """
    take the given list of Courses classes and convert into a pandas dataframe
    :param list_of_courses: list of Course classes
    :return: pandas dataframe
    """

    # for every course
    return pd.DataFrame(
        {
            "id": [course.id for course in list_of_courses],
            "name": [course.name for course in list_of_courses],
            "credit": [course.credit for course in list_of_courses],
            "description": [course.desc for course in list_of_courses],
            "prereq": [course.prereq for course in list_of_courses]
            # todo get it to return a string e.g "CMPT 101, CMPT 103"
        }
    )


# Page URL
URL = 'https://calendar.macewan.ca/course-descriptions/cmpt/'
page = requests.get(URL)  # request for page content (beautifulsoup)
soup = BeautifulSoup(page.content, 'html.parser')  # get html content

courses = soup.find(id='textcontainer')  # find id
course_elems = courses.find_all(class_='courseblock')  # find all elements with given class

course_id_list = []  # list of Course classes
print_course(course_elems)
df = init_df(course_id_list)
df.to_csv('cmpt-courses.csv', index=False, quoting=None)
