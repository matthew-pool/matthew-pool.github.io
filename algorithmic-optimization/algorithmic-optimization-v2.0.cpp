//============================================================================
// Name        : algorithm-complexity.cpp
// Author      : Matthew Pool
// Version     : 2.0 (Optimized)
// Copyright   : Copyright © 2023
// Description : Loads data from a CSV file into a vector data structure.
//               Features a custom recursive Merge Sort implementation for 
//               O(n log n) sorting performance and specific course searching.
//============================================================================

#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

//============================================================================
// Global definitions visible to all methods and classes
//============================================================================

struct Course {
    string number;
    string name;
    vector<string> prereqs;

    Course() : number(""), name("") {}
};

//============================================================================
// Static methods used for testing
//============================================================================

/**
 * @brief Function that loads course data from CSV to vector data structure
 * Time Complexity: O(n*m), where n is number of courses and m is number of prereqs
 * Space Complexity: O(n*m), due to loading n courses into the courses vector
 * @param csvPath path to CSV file
 * @return courses vector containing instances of Course
 */
vector<Course> loadDataStructure(const string& csvPath) {
    vector<Course> courses;
    ifstream file(csvPath);

    if (!file.is_open()) {
        throw runtime_error("Failed to open CSV file successfully: " + csvPath + "\n");
    }

    string line;
    while (getline(file, line)) {
        istringstream iss(line);
        Course course;

        if (!getline(iss, course.number, ',') || !getline(iss, course.name, ',')) {
            continue; // Skip malformed lines
        }

        string prereq;
        while (getline(iss, prereq, ',')) {
            course.prereqs.push_back(prereq);
        }
        courses.push_back(course);
    }
    
    // Optional: Prerequisite validation logic would go here
    return courses;
}

/**
 * @brief Helper function to merge two subarrays of courses[]
 * Time Complexity: O(n)
 * @param courses vector of courses
 * @param left left index
 * @param mid middle index
 * @param right right index
 */
void merge(vector<Course>& courses, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    // Create temp vectors
    vector<Course> L(n1), R(n2);

    // Copy data to temp vectors L[] and R[]
    for (int i = 0; i < n1; i++)
        L[i] = courses[left + i];
    for (int j = 0; j < n2; j++)
        R[j] = courses[mid + 1 + j];

    // Merge the temp vectors back into courses[left..right]
    int i = 0; 
    int j = 0; 
    int k = left;

    while (i < n1 && j < n2) {
        // Alphanumeric comparison on course number
        if (L[i].number <= R[j].number) {
            courses[k] = L[i];
            i++;
        } else {
            courses[k] = R[j];
            j++;
        }
        k++;
    }

    // Copy the remaining elements of L[], if there are any
    while (i < n1) {
        courses[k] = L[i];
        i++;
        k++;
    }

    // Copy the remaining elements of R[], if there are any
    while (j < n2) {
        courses[k] = R[j];
        j++;
        k++;
    }
}

/**
 * @brief Recursive function that implements Merge Sort
 * Time Complexity: O(n log n)
 * @param courses vector of courses to be sorted
 * @param left left index
 * @param right right index
 */
void mergeSort(vector<Course>& courses, int left, int right) {
    if (left < right) {
        // Same as (left+right)/2, but avoids overflow for large left and right
        int mid = left + (right - left) / 2;

        // Sort first and second halves
        mergeSort(courses, left, mid);
        mergeSort(courses, mid + 1, right);

        merge(courses, left, mid, right);
    }
}

/**
 * @brief Wrapper function to call Merge Sort and print the result
 * Time Complexity: O(n log n) - Significantly faster than previous O(n^2) Insertion Sort
 * @param courses vector of courses
 */
void printAllSorted(vector<Course>& courses) {
    int n = courses.size();
    if (n == 0) return;

    // Execute recursive Merge Sort
    mergeSort(courses, 0, n - 1);

    cout << "Here is a sample schedule:\n\n";
    for (const Course& course : courses) {
        cout << course.number << ", " << course.name << "\n";
    }
    cout << "\n";
}

/**
 * @brief Function searches for an input course number
 * Time Complexity: O(n)
 * @param courses vector of courses
 * @param number course number to find
 */
void printCourseInfo(const vector<Course>& courses, string number) {
    for (const Course& course : courses) {
        if (course.number == number) {
            cout << course.number << ", " << course.name << "\n";
            cout << "Prerequisites: ";
            if (course.prereqs.empty()) {
                cout << "None\n";
            } else {
                for (size_t i = 0; i < course.prereqs.size(); ++i) {
                    cout << course.prereqs[i] << (i < course.prereqs.size() - 1 ? ", " : "");
                }
                cout << "\n";
            }
            cout << "\n";
            return;
        }
    }
    cout << "Course not found: " << number << "\n\n";
}

/**
 * @brief Main function
 */
int main(int argc, char* argv[]) {
    string csvPath;
    string userInput = "";
    vector<Course> courses;

    cout << "Welcome to the course planner.\n\n";
    do {
        cout << "1. Load Data Structure.\n";
        cout << "2. Print Course List.\n";
        cout << "3. Print Course.\n";
        cout << "9. Exit\n\n";
        cout << "What would you like to do? ";
        getline(cin, userInput);

        if (userInput == "1") {
            cout << "Enter CSV file name (try 'csvFile.csv'): ";
            getline(cin, csvPath);
            try {
                courses = loadDataStructure(csvPath);
                cout << "Data loaded successfully!\n\n";
            } catch (const exception& e) {
                cout << "Error: " << e.what() << "\n";
            }
        } else if (userInput == "2") {
            printAllSorted(courses);
        } else if (userInput == "3") {
            cout << "What course do you want to know about? ";
            getline(cin, userInput);
            // Convert input to uppercase
            transform(userInput.begin(), userInput.end(), userInput.begin(), ::toupper);
            printCourseInfo(courses, userInput);
        }
    } while (userInput != "9");

    cout << "Thank you for using the course planner!\n";
    return 0;
}