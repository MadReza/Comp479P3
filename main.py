print "Main App"

import os
from glob import glob

scraped_root_directory = "www_roots"

#Get All Departments:
departments = [x[1] for x in os.walk(scraped_root_directory)][0]

def get_all_txt_files_in(path):
    """Returns all text files in all folders and sub-folders found"""
    return [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.txt'))]

def get_score(data):
    """Get score for file"""
    #TODO: remove link from scorer ? if required ?
    return len(data)#TODO, return score for that content

def get_text_from(file_path):
    """Retrieve text from file"""
    with open(file_path, 'r') as file:
        return file.read()

def get_department_score(department):
    """Gets the total score for that department"""
    path = scraped_root_directory + "/" + department
    score = 0

    for file_path in get_all_txt_files_in(path):
        file_content = get_text_from(file_path)
        score = score + get_score(file_content)
    return score

def classifier(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    return "Neutral"

def compare_positivity(department_a, department_b):
    score_a = get_department_score(department_a)
    score_b = get_department_score(department_b)

    if score_a > score_b:
        print department_a, "is more positive than", department_b
    elif score_a < score_b:
        print department_b, "is more positive than", department_b
    else:
        print "Both department:", department_a, "and", department_b, "have same positivity score"

if __name__ == '__main__':
    #TODO: redirects and option calls
    for x in departments:
        print "Department:", x
        score = get_department_score(x)
        print "\tScore:", score
        print "\tClassified:", classifier(score)

    compare_positivity(departments[0], departments[1])
    compare_positivity(departments[0], departments[7])
