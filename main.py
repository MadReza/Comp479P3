print "Main App"

import os

scraped_root_directory = "www_roots"

#Get All Departments:
departments = [x[1] for x in os.walk(scraped_root_directory)][0]

if __name__ == '__main__':
    #for later redirects.
    print departments
