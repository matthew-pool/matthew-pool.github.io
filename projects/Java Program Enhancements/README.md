## Project Summary
This project involved choosing a previously written program and enhancing it in various ways. I chose a program I wrote a couple of years ago at SNHU. I knew this program (v1.0) needed lots of work in order to provide a better user experience and a more secure, robust application. I ended up making quite a few changes in the areas of software engineering and design, run-time optimization, database implementation, and modularization. I go into more detail in my [Code Review Video](https://www.youtube.com/watch?v=heo30ZFu5Eg&ab_channel=alienhead) on YouTube. You should check it out!

### Rescue Animal Management System (Java)
This is a simple text-based program written in Java that keeps track of rescue animals. 
The user can add new dogs and monkeys (and their attributes) to temporary storage. 
The user can also print out a list of dogs or monkeys or a list of all non-reserved animals.<br>

![System menu](images/new11.png)<br>

### Program Enhancements (latest version: v4.0):
Added documentation with JavaDocs:<br>
![Main class JavaDoc](images/new19.png)<br>
![Helper function JavaDoc](images/new20.png)<br>

Added Error-Handling and Input Validation:<br>
![Error-handling & input validation](images/new9.png)<br>

Converted to Maven Framework:<br>
![Maven project architecture](images/new2.png)<br>
![Maven pom.xml file](images/new4.png)<br>

Implemented JUnit Unit Testing:<br>
![JUnit test coverage with 83% of lines and 75% of branches covered](images/new1.png)<br>
![20 JUnit tests run with 0 failures](images/new3.png)<br>

Added Custom Text Colors and Styles:<br>
![ANSI escape code declarations in Java](images/new6.png)<br>
![Various formatting applied to text](images/new10.png)<br>
![Prompting user and receiving user input for system responses](images/new13.png)<br>
![Quitting system shown in custom colored text](images/new14.png)<br>

Added Persistent Storage:<br>
![MapDB imports](images/new18.png)<br>
![MapDB and HTreeMap implementation](images/new7.png)<br>

Optimized from O(n) down to O(log n) worst-case time complexity:<br>
![LinkedHashMap declarations](images/new5.png)<br>
![Writing to the hash map](images/new17.png)<br>

### NOTE
All versions of the software are included in the "rescue_animal.zip" file