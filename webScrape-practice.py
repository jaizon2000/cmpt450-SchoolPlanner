# TUT LINK: https://realpython.com/beautiful-soup-web-scraper-python/#scraping-the-monster-job-site
# https://realpython.com/python-requests/

# Jan 18, 2021
# Jehdi Aizon

import requests
from bs4 import BeautifulSoup


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


def print_course_description(course_elems):
    for course_elem in course_elems:
        # Course code, title, and credits
        course = course_elem.find(class_='courseblocktitle')
        course = course.text.split("\n")

        course_code = course[0].replace("\xa0", " ")
        course_title = course[1]
        course_credits = course[2]

        # Couurse description
        course_desc = course_elem.find(class_='courseblockdesc')

        # Course pre-requisites
        course_prereq = course_elem.find(class_='courseblockextra')

        # Print
        print(course_code)
        print(course_title)
        print(course_credits)
        print(course_desc.text)
        if course_prereq is not None:
            print(course_prereq.text)

        print()

def main():
    # Page URL
    URL = 'https://calendar.macewan.ca/course-descriptions/cmpt/'
    page = requests.get(URL)  # request for page content (beautifulsoup)
    soup = BeautifulSoup(page.content, 'html.parser')  # get html content

    courses = soup.find(id='textcontainer')  # find id
    course_elems = courses.find_all(class_='courseblock')  # find all elements with given class
    print_course_description(course_elems)


main()
