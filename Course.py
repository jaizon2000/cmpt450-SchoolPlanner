import pandas as pd

class Course:
    def __init__(self, id, name, credit, desc, prereq=None):
        if prereq is None:
            prereq = []
        self.id = id
        self.name = name
        self.credit = credit
        self.desc = desc
        self.prereq = prereq

    def has_prereq(self, Student):
        # todo
        return False


cmpt103 = Course("CMPT 103", "Introduction to Computing II", 3,
                 "This course continues the overview of computing science concepts that was started in CMPT 101. Topics include representation of compound data using abstraction, programming languages, and modularity; algorithms that use these data structures; and networks with the TCP/IP model and client/server architecture. Students continue with the syntax of a high-level programming language: functions, arrays, and user-defined data types.",
                 ())
cmpt200 = Course("CMPT 200", "Data Structures and Algorithms", 3,
                 "This course continues the study of dynamic data structures (e.g., lists, stacks, queues, trees, and dictionaries) and associated algorithms (e.g., traversal, sorting, searching, element addition and removal). Recursion is covered, and some of the basic ideas of object-oriented programming, such as classes and objects, are introduced.",
                 (cmpt103,))
cmpt201 = Course("CMPT 201", "Practical Programming Methodology", 3,
                 "This course provides an introduction to the principles, methods, tools, and practices of the professional programmer. The lectures focus on best practices in software development and the fundamental principles of software engineering. The laboratories offer an intensive apprenticeship to the aspiring software developer. Students use C and the software development tools of the UNIX environment.",
                 (cmpt200,))

# list of Course classes
all = [cmpt103, cmpt200, cmpt201]

# for course in Course list


# df["id"] = [course.id for course in all]
# df.insert(1, str, ["CMPT", "AA"], True)
