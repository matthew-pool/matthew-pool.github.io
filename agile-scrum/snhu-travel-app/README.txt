To convert .JAVA source code into a runnable .JAR file:
------------------------------------------------------


0) Install Java Development Kit (JDK) latest LTS version

* Open Terminal in .JAVA file directory:

1) Ensure JDK is installed with "javac -version" (should return version number)

2) "javac app_name.java"

* Ensure "C:\Program Files\Java\jdk-version_number\bin is included in System PATH (environmental variables)
- replace "version_number" with actual folder version number

3) "jar cfe app_name.jar app_name *.class resources"

4) Run JAR file

