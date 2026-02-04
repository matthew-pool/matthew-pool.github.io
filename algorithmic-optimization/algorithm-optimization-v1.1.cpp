//============================================================================
// Name        :	CourseVector.cpp
// Author      :	Matthew Pool
// Version     :	1.1
// Copyright   :	Copyright © 2023
// Description :    Loads data from a CSV file (of which the user specifies) into
//                  a vector data structure. Data consists of Course information 
//                  on each line, containing number, name, and prerequisites.
//                  The user may load the data, print a list in alphanumeric
//                  order, print the name and prerequisites for a given course,
//                  or exit the program.
//============================================================================

#include <iostream>         // (std) cout, cin, cerr, clog, endl, <<, >>
#include <sstream>          // istringstream, stringstream, str
#include <fstream>          // ifstream, open, close, getline, read, eof, fail
#include <string>           // at, operator[], front, back, append, push_back, insert, erase, replace, clear, size, length, empty, resize, capacity, reserve, c_str, find, substr, compare
#include <cctype>           // toupper, tolower, isalpha, isdigit, isalnum, isspace, isupper, islower,ispunct, iscntrl, isgraph, isprint, isxdigit 
#include <vector>           // at, operator[], front, back, push_back, pop_back, insert, erase, clear, size, empty, resize, capacity, reserve, begin, end, swap
#include <stdexcept>        // logic_error, runtime_error, out_of_range, invalid_argument, length_error, overflow_error, underflow_error
#include <algorithm>        // find, find_if, binary_search, sort, stable_sort, partial_sort, reverse, rotate, shuffle, swap, count, min_element, max_element, equal_range

using namespace std;

//============================================================================
// Global definitions visible to all methods and classes
//============================================================================

// structure for each course object to be be created
struct Course {
    string number;
    string name;
    vector<string> prereqs;

    // default constructor
    Course() : number(""), name ("") {}
};

//============================================================================
// Static methods used for testing
//============================================================================

/**
 * @brief Function that loads course data from CSV to vector data structure
 * Time Complexity: O(n*m), where n is number of courses and m is number of prereqs, due to validating prereqs
 * Space Complexity: O(n*m), due to loading n courses into the courses vector
 * @param csvPath path to CSV file
 * @return courses vector constaining instances of Course
 */
vector<Course> loadDataStructure(const string& csvPath) { // passing by reference for efficiency}
    // create vectors to hold courses from CSV
    vector<Course> courses;

    // open CSV file for reading
    ifstream file(csvPath);
    // checks if CSV file was successfully opened
    if (!file.is_open()) {
        throw runtime_error ("Failed to open CSV file successfully: " + csvPath + "\n");
    }

    string line;
    while (getline(file, line)) { // while not CSV EoF
        istringstream iss(line); // reads string as stream
        Course course; // create a Course instance for every line read

        // verify at least 2 parameters for course exist, and store in course instance if so
        if (!getline(iss, course.number, ',') || !getline(iss, course.name, ',')) { // checks to see if either parameter is missing
            throw runtime_error("Requires at least 2 parameters: number, name!\n");
        }

        string prereq;
        while (getline(iss, prereq, ',')) { // additional items stored as prereqs in course
            course.prereqs.push_back(prereq); // add prereq to list of prereqs for this course
        }

        courses.push_back(course); // add course containing only number and name to list of courses

    } // all course data for each course added to courses
 
    vector<string> courseNumbers; // creates a vector of course numbers to verify prereqs exist as courses
    for (const Course& course : courses) {
        courseNumbers.push_back(course.number);
    } // course numbers added to list

    // validate prereqs exist in courseNumbers vector, else throw error
    for (const Course& course : courses) {
        for (const string& prereq : course.prereqs) {
            if (find(courseNumbers.begin(), courseNumbers.end(), prereq) == courseNumbers.end()) { // reached end without finding prereq in courseNumbers list
                throw runtime_error("Required prerequisite not listed: " + prereq + "\n");
            }
        }
    } // all prereqs validated and courses list fully loaded

    return courses;
}

/**
 * @brief Function sorts courses alphanumerically by course number, then print number, name, prereqs (if any)
 * Time Complexity: O(n^2), due to Insertion sort
 * Space Complexity: O(1)
 * @param courses vector of courses
 */
void printAllSorted(vector<Course>& courses) { // referenced to change original vector when sorting
    int n = courses.size();
    if (n == 0) { // empty list
        return;
    }

    // Insertion sort
    for (int i = 1; i < n; ++i) { // i is first element compared with j
        Course key = courses[i]; // what to search for
        int j = i - 1; // j = 1st element, located at index[0]
    
        while (j >= 0 && courses[j].number > key.number) { // compare course number alphanumerically
            courses[j+1] = courses[j]; // move courses[0..i-1] elements > key to preceding index
            j--;
        }

        courses[j+1] = key;
    }

    // print all sorted courses
    cout << "Here is a sample schedule:\n\n";
    for (const Course& course : courses) {
        cout << course.number << ", " << course.name << "\n";

        /*
        if (course.prereqs.size() > 0) {
            cout << "Prerequisites:\n";
            for (const string& prereq : course.prereqs) {
                cout << prereq + "\n";
            }
        } 
        */  
    }
    cout << "\n";

    return;
}

/**
 * @brief Function searches for an input course number, then if found prints name and prereqs (if any)
 * Time Complexity: O(n*m)
 * Space Complexity: O(1)
 * @param courses vector of courses
 * @param number course number to find
 */
void printCourseInfo(const vector<Course>& courses, string number) { // referenced for efficiency
    for (const Course& course : courses) {
        if (course.number == number) {
            cout << course.number << ", " << course.name << "\n";
            cout << "Prerequisites: "; // no new line
            if (course.prereqs.size() == 0) { // no prereqs
                cout << "None\n";
            }
            else {
                bool isFirst = true; // determines if comma is needed
                for (const string& prereq : course.prereqs) {
                    if (!isFirst) {
                        cout << ", ";
                    }
                    cout << prereq;
                    isFirst = false;
                }
                cout << "\n";
            }
            cout << "\n";
            return; // if course found and info printed, then exit function
        }
    }
    cout << "Course not found: " << number << "\n\n";
}


/**
 * @brief Main function runs with default CSV file path or specified path in terminal when executing program 
 * Time Complexity: Unknown, as its dependent on number of times user loops and which functions are called
 * Space Complexity: O(n), where n is the number of courses loaded into the courses vector
 * @param argc number of arguments passed to the program
 * @param argv array of pointers to the command line arguments
 * @return int status code
 */
int main(int argc, char* argv[]) {

    string csvPath;
    string userInput = "";
    vector<Course> courses;

    /* Testing Purposes
    // process command line arguments
    switch (argc) {
    case 2: // includes 1 extra arg in execution
        csvPath = argv[1];
        break;
    default: // includes 0 extra args in execution
        csvPath = "csvFile.csv"; // located in same directory as .cpp file
        // csvPath = "csvFile_course_error.csv";
        // csvPath = "csvFile_prereq_error.csv";
    }
    */

    cout << "Welcome to the course planner.\n\n";
    do { // until user input equals "9"
        cout << "1. Load Data Structure.\n";
        cout << "2. Print Course List.\n";
        cout << "3. Print Course.\n";
        cout << "9. Exit\n\n";
        cout << "What would you like to do? ";
        //cin.ignore(numeric_limits<streamsize>::max(), '\n');
        getline(cin, userInput); // get user input and store in userInput variable
        //cout << "\n";

        if (userInput == "1") {
            try {
                cout << "What is the CSV file name (including extension) to load?\n";
                getline(cin, csvPath);
                cout << "\n";
                courses = loadDataStructure(csvPath);
                cout << "Data loaded from CSV successfully!\n\n";
            }
            catch (const exception& e) {
                cout << e.what() << "\n";
            }
        }
        else if (userInput == "2") {
            
            int n = courses.size();
            if (n == 0) { // empty list
                continue; // acquire menu input from user again
            }
            
            try {
                printAllSorted(courses);
            }
            catch (const exception& e) {
                cout << e.what() << "\n";
            }
        }
        else if (userInput == "3") {
            
            int n = courses.size();
            if (n == 0) { // empty list
                continue; // acquire menu input from user again
            }
            
            cout << "What course do you want to know about? "; // no new line
            getline(cin, userInput);

            // ensures that the first 4 (L) Letters preceeding 3 (N) Numbers are capitalized from "LLLLNNN"
            for (int i = 0; i < 4; ++i) { // pass by reference
                userInput[i] = toupper(userInput[i]);
            }

            try {
                printCourseInfo(courses, userInput);
            }
            catch (const exception& e) {
                cout << e.what() << "\n";
            }
        }
        else if (userInput == "9") {
            break;
        }
        else {
            cout << userInput << " is not a valid option.\n\n";
        }
    } while (userInput != "9");

    cout << "Thank you for using the course planner!\n\n";
    return 0; // execution terminated without error
}
