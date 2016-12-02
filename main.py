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

if __name__ == '__main__':
    #TODO: redirects and option calls
    for x in departments:
        print "Department:", x
        print "\tScore:", get_department_score(x)
