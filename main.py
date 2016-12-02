from helper import *

if __name__ == '__main__':
    #TODO: redirects and option calls
    departments = get_all_departments(scraped_root_directory)
    for x in departments:
        print "Department:", x
        score = get_department_score(x)
        print "\tScore:", score
        print "\tClassified:", classifier(score)

    compare_positivity(departments[0], departments[1])
    compare_positivity(departments[0], departments[7])
