from helper import *

def main_options():
    while True:
        print "Please select one of the following:"
        print "'a': Add a new Department link to scrap"
        print "'s': Get all departments: score and classifier by Most Positive to Most Negative"
        print "'d': Department Specific: get all children score and classifer by Most Positive to Most Negative"
        print "'c': Compare 2 departments positivity classifier"
        print "'p': Get Most Positive Department"
        print "'n': Get Most Negative Department"
        print "'q': Quit program"
        choices = ('a', 's', 'd', 'c', 'p', 'n', 'q')
        user_choice = raw_input("Please select the letter:")
        if user_choice in choices:
            return user_choice


if __name__ == '__main__':

    while True:
        m = main_options()
        if m == 'q':
            quit()
        elif m == 'a':
            scrap_new_link()
        elif m == 's':
            print_departments_score_classifier()
        elif m == 'd':
            dep_choice = get_dep_choice()
            print_score_classifier_for(dep_choice)
        elif m == 'c':
            dep_choice1 = get_dep_choice()
            dep_choice2 = get_dep_choice()
            compare_positivity(dep_choice1, dep_choice2)
        elif m == 'p':
            name, v = get_most_positive()
            print "Most positive department:", name, "score:", v[0]
        elif m == 'n':
            name, v = get_most_negative()
            print "Most negative department:", name, "score:", v[0]
            

    departments = get_all_departments(scraped_root_directory)
    for x in departments:
        print "Department:", x
        score = get_department_score(x)
        print "\tScore:", score
        print "\tClassified:", classifier(score)

    compare_positivity(departments[0], departments[1])
    compare_positivity(departments[0], departments[7])
