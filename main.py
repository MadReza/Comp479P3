print "Main App"

import os
from glob import glob

scraped_root_directory = "www_roots"

#Get All Departments:
departments = [x[1] for x in os.walk(scraped_root_directory)][0]

def get_all_txt_files_in(path):
    """Returns all text files in all folders and sub-folders found"""
    return [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.txt'))]

if __name__ == '__main__':
    #for later redirects.
    for x in departments:
        print "Department: ", x
        path = scraped_root_directory + "/" + x
        for y in get_all_txt_files_in(path):
            print "\t", y
