package rescueAnimal;

import java.nio.charset.StandardCharsets;  // For internationalization/parsing
import java.time.Year;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

/**
 * Rescue Animal Management System
 * 
 * <p>The Main class is the program entry point and helps maintain
 * a list of animals. The user can add dogs and monkeys (and related
 * attributes) to temporary storage with the option to print to console.</p>
 * 
 * @author Matthew Pool
 * @version 2.0
 * @since 2024-11-14
 */
public class Main {
    // Allowable menu options that the user can enter
    private static final List<String> ALLOWED_OPTIONS = Arrays.asList("1", "2", "3", "4", "5", "6", "q", "Q");
    // Allowable status options that the user can enter
    private static final List<String> STATUS_OPTIONS = Arrays.asList("phase 1", "phase 2", "phase 3", "phase 4", "phase 5", "intake", "in service", "farm");

    // Used when printing lists to console
    private static final String PRINT_FORMAT = "%-20s %-20s %-25s %-10s%n";

    // ANSI Escape (Color & Style) Codes
    private static final String RESET = "\u001B[0m";  // Reset text color/style to default
    private static final String UNDERLINED = "\u001B[4m";
    private static final String BLACK = "\u001B[30m";
    private static final String RED = "\u001B[31m";
    private static final String GREEN = "\u001B[32m";
    private static final String YELLOW = "\u001B[33m";
    private static final String BLUE = "\u001B[34m";
    private static final String MAGENTA = "\u001B[35m";
    private static final String CYAN = "\u001B[36m";
    private static final String GRAY = "\u001B[37m";
    private static final String BLACK_BG = "\u001B[40m";
    private static final String WHITE_BG = "\u001B[47m";
    // Example: System.out.print(STYLE + COLOR + BACKGROUND)

    // Instance variables / ArrayList initializations
    private static final ArrayList<Dog> dogList = new ArrayList<>();
    private static final ArrayList<Monkey> monkeyList = new ArrayList<>();

    /**
     * Prints menu options to console
     */
    public static void displayMenu() {
        System.out.println("\n");
        System.out.print(UNDERLINED + BLACK + WHITE_BG);
        System.out.println("\t\t\t\tRescue Animal Management System\t\t\t\t" + RESET);
        System.out.println();
        System.out.println("[1] Intake new dog");
        System.out.println("[2] Intake new monkey");
        System.out.println("[3] Reserve animal");
        System.out.println("[4] Print list of dogs");
        System.out.println("[5] Print list of monkeys");
        System.out.println("[6] Print list of non-reserved animals");
        System.out.println("[Q] Quit application");
        System.out.println();
        System.out.print(GRAY + "Enter a menu selection: " + RESET);
    }

    /**
     * Creates and adds dogs to a list for testing
     */
    public static void initializeDogList() {
        Dog dog1 = new Dog("Sophie", "German Shepherd", "male", "1", "25.6", "05-12-2019",
                "United States", "intake", false, "United States");
        Dog dog2 = new Dog("Crimson", "Great Dane", "male", "3", "35.2", "02-03-2020",
                "United States", "1", false, "United States");
        Dog dog3 = new Dog("Blueberry", "Chihuahua", "female", "4", "25.6", "12-12-2019",
                "Canada", "in service", true, "Canada");
        dogList.add(dog1);
        dogList.add(dog2);
        dogList.add(dog3);
    }

    /**
     * Creates and adds monkeys to a list for testing
     */
    public static void initializeMonkeyList() {
        Monkey monkey1 = new Monkey("Kimchi",      "capuchin",	"male", 	"1", "25.6",
                "05-12-2019", "United States", "intake", 		false,
                "United States",    "3",  "12", "11");
        Monkey monkey2 = new Monkey("Gizmo",        "guenon", 	"male", 	"3", "35.2",
                "02-03-2020", "United States", "Phase 1", 		false,
                "United States",    "16", "22", "30");
        Monkey monkey3 = new Monkey("Sweet Pea",     "macaque",	"female","4", "25.6",
                "12-12-2019", "Canada", 		"in service", 	true,
                "Canada","4",  "13", "24");
        monkeyList.add(monkey1);
        monkeyList.add(monkey2);
        monkeyList.add(monkey3);
    }

    /**
     * Helper function for the intakeNewDog and intakeNewMonkey functions
     *
     * @param scanner Used for user input
     * @return gender (male or female) as a String
     */
    public static String getGender(Scanner scanner) {
        String gender;
        System.out.print("Gender (male/female): ");
        while(true) {
            try {
                gender = scanner.nextLine().trim();
                if (gender.isEmpty()) {
                    System.out.print("Please enter a gender: ");
                } else if (!gender.equalsIgnoreCase("male") && !gender.equalsIgnoreCase("female")) {
                    System.out.print(RED + "Male or female, please: " + RESET);
                } else break;  // Exit loop if valid gender
            } catch (Exception e) {
                System.out.println(RED + "Error reading gender." + RESET);
            }
        }
        return gender;
    }

    /**
     * Helper function for the intakeNewDog and intakeNewMonkey functions
     *
     * @param scanner Used for user input
     * @return age as a String representing an int between 0 and 50
     */
    public static String getAge(Scanner scanner) {
        String age;
        System.out.print("Age: ");
        while (true) {
            try {
                age = scanner.nextLine().trim();
                if (age.isEmpty()) {
                    System.out.print(RED + "Please enter a valid age: " + RESET);
                } else {
                    // Verify age is a positive integer with 1 or more digits
                    if (!age.matches("\\d+") || Integer.parseInt(age) < 0 || Integer.parseInt(age) > 50) {
                        System.out.print(RED + "Please enter a valid age: " + RESET);
                    } else break;  // Exit loop if valid age
                }
            } catch (Exception e) {
                System.out.println(RED + "Error reading age." + RESET);
            }
        }
        return age;
    }

    /**
     * Helper function for the intakeNewDog and intakeNewMonkey functions
     *
     * @param scanner Used for user input
     * @return weight as String representing a float between 0 and 500
     */
    public static String getWeight(Scanner scanner) {
        String weight;
        System.out.print("Weight (lbs.): ");
        while (true) {
            try {
                weight = scanner.nextLine().trim();
                if (weight.isEmpty()) {
                    System.out.print(RED + "Please enter weight in pounds (lbs.): " + RESET);
                    // Verify weight is numeric with 1 or more digits before and (optionally) after the decimal
                } else if (!weight.matches("\\d+(\\.\\d+)?") || Float.parseFloat(weight) < 0 || Float.parseFloat(weight) > 500) {
                    System.out.print(RED + "Please enter a valid weight in pounds (lbs.): " + RESET);
                } else break;
            } catch (Exception e) {
                System.out.println(RED + "Error reading weight." + RESET);
            }
        }
        return weight;
    }

    /**
     * Helper function for the intakeNewDog and intakeNewMonkey functions
     *
     * @param scanner Used for user input
     * @return acquisitionDate as a String representing a date
     * in the format MM-DD-YYYY between 1975 and the current year
     */
    public static String getAcquisitionDate(Scanner scanner) {
        final List<Integer> THIRTY_DAY_MONTHS = Arrays.asList(4, 6, 9, 11);
        final List<Integer> THIRTY_ONE_DAY_MONTHS = Arrays.asList(1, 3, 5, 7, 8, 10, 12);
        String acquisitionDate;
        int month, day, year;
        final int CURRENT_YEAR = Year.now().getValue();

        System.out.print("Acquisition Date (MM-DD-YYYY): ");
        while (true) {
            try {
                acquisitionDate = scanner.nextLine().trim();
                if (acquisitionDate.isEmpty()) {
                    System.out.print(RED + "Please enter a date (MM-DD-YYYY): " + RESET);
                } else {
                    // Verify acquisitionDate is in correct format (MM-DD-YYYY)
                    if (!acquisitionDate.matches("\\d{2}-\\d{2}-\\d{4}")) {
                        System.out.print(RED + "Please enter the acquisition date (MM-DD-YYYY): " + RESET);
                    } else {
                        // NOTE: substring takes arguments start_index (inclusive) and end_index (exclusive)
                        month = Integer.parseInt(acquisitionDate.substring(0, 2));
                        day = Integer.parseInt(acquisitionDate.substring(3, 5));
                        year = Integer.parseInt(acquisitionDate.substring(6, 10));
                        if (month < 1 || month > 12 || day < 1 || day > 31
                                || year < 1975 || year > CURRENT_YEAR) {
                            System.out.print(RED + "Please enter a valid acquisition date (MM-DD-YYYY): " + RESET);
                        } else if ((day == 31) && !THIRTY_ONE_DAY_MONTHS.contains(month)) {
                            System.out.print(RED + "Please enter a valid date (MM-DD-YYYY): " + RESET);
                        } else if (day == 30 && !THIRTY_DAY_MONTHS.contains(month)) {
                            System.out.print(RED + "Please enter a valid date (MM-DD-YYYY): " + RESET);
                        } else if (month == 2) {
                            boolean isLeapYear = (year % 4 == 0);
                            if (day > 29 || (day == 29 && !isLeapYear)) {
                                System.out.println(RED + "Please enter a valid date (MM-DD-YYYY): " + RESET);
                            }
                            else break;
                        } else break;  // Valid date entered
                    }
                }
            } catch (Exception e) {
                System.out.println(RED + "Error reading acquisition date." + RESET);
            }
        }
        return acquisitionDate;
    }

    /**
     * Helper function for the intakeNewDog and intakeNewMonkey functions
     *
     * @param scanner Used for user input
     * @return acquisitionCountry as a String
     */
    public static String getAcquisitionCountry(Scanner scanner) {
        String acquisitionCountry;
        System.out.print("Acquisition Country: ");
        while (true) {
            try {
                acquisitionCountry = scanner.nextLine().trim();
                if (acquisitionCountry.isEmpty()) {
                    System.out.print(RED + "Please enter a country: " + RESET);
                } else break;
            } catch (Exception e) {
                System.out.println(RED + "Error reading acquisition country." + RESET);
            }
        }
        return acquisitionCountry;
    }

    /**
     * Helper function for the intakeNewDog and intakeNewMonkey functions
     *
     * @param scanner Used for user input
     * @return trainingStatus as a String with the value Phase #, intake, in service, or farm
     */
    public static String getTrainingStatus(Scanner scanner) {
        String trainingStatus;
        System.out.print("Training Status (phase number, intake, in service, or farm): ");
        while (true) {
            try {
                trainingStatus = scanner.nextLine().trim().toLowerCase();
                if (trainingStatus.isEmpty()) {
                    System.out.print(RED + "Please enter status (phase number, intake, in service, or farm): " + RESET);
                } else if (!STATUS_OPTIONS.contains(trainingStatus)) {
                    System.out.print(RED + "Please enter status (examples: 'Phase 1', 'intake', 'in service', farm): " + RESET);
                } else break;
            } catch (Exception e) {
                System.out.println(RED + "Error reading training status." + RESET);
            }
        }
        return trainingStatus;
    }

    /**
     * Helper function for the intakeNewDog and intakeNewMonkey functions
     *
     * @param scanner Used for user input
     * @return isReserved as a boolean with value true or false
     */
    public static boolean getReserved(Scanner scanner) {
        String reservedChoice;
        boolean isReserved;

        System.out.print("Reserved (true or false): ");
        while (true) {
            try {
                reservedChoice = scanner.nextLine().trim().toLowerCase();
                if (reservedChoice.isEmpty()) {
                    System.out.print(RED + "Please enter true or false: " + RESET);
                } else if (!reservedChoice.equals("true") && !reservedChoice.equals("false")) {
                    System.out.print(RED + "Please enter true or false: " + RESET);
                } else {
                    // Convert to boolean
                    isReserved = Boolean.parseBoolean(reservedChoice);
                    break;
                }
            } catch (Exception e) {
                System.out.println(RED + "Error reading reserved status." + RESET);
            }
        }
        return isReserved;
    }

    /**
     * Helper function for the intakeNewDog and intakeNewMonkey functions
     *
     * @param scanner Used for user input
     * @return inServiceCountry as a String
     */
    public static String getInServiceCountry(Scanner scanner) {
        String inServiceCountry;
        System.out.print("In Service Country: ");
        while (true) {
            try {
                inServiceCountry = scanner.nextLine().trim();
                if (inServiceCountry.isEmpty()) {
                    System.out.print(RED + "Enter the in service country: " + RESET);
                } else break;
            } catch (Exception e) {
                System.out.println(RED + "Error reading in service country." + RESET);
            }
        }
        return inServiceCountry;
    }

    /**
     * Option 1: Passes user input, and adds dog if dog name does not exist
     *
     * @param scanner Used for user input
     */
    public static void intakeNewDog(Scanner scanner) {
        String name, breed, gender, age, weight, acquisitionDate,
                acquisitionCountry, trainingStatus, inServiceCountry;
        boolean reserved;

        // Name
        System.out.print("Dog Name: ");
        while (true) {
            try {
                name = scanner.nextLine().trim();
                if (name.isEmpty()) {
                    System.out.print(RED + "Please enter a valid name: " + RESET);
                } else break;  // Exit inner loop if valid name
            } catch (Exception e) {
                System.out.println(RED + "Error reading dog name." + RESET);
            }
        }

        try {
            // Verify dog isn't already in system
            for (Dog dog : dogList) {
                if (dog.getName() != null && dog.getName().equalsIgnoreCase(name)) {
                    System.out.println(RED + "This dog already exists in the system." + RESET);
                    return;  // Exit method and return to menu
                }
            }
        } catch (Exception e) {
            System.out.println(RED + "Error looking up dog name."+ RESET);
            return;
        }

        // Breed
        System.out.print("Breed: ");
        while (true) {
            try {
                breed = scanner.nextLine().trim();
                if (breed.trim().isEmpty()) {
                    System.out.print(RED + "Please enter a dog breed: " + RESET);
                } else break;
            } catch (Exception e) {
                System.out.println(RED + "Error reading dog breed." + RESET);
            }
        }

        gender = getGender(scanner);

        age = getAge(scanner);

        weight = getWeight(scanner);

        acquisitionDate = getAcquisitionDate(scanner);

        acquisitionCountry = getAcquisitionCountry(scanner);

        trainingStatus = getTrainingStatus(scanner);

        reserved = getReserved(scanner);

        if (trainingStatus.equalsIgnoreCase("in service"))
            inServiceCountry = getInServiceCountry(scanner);
        else inServiceCountry = "n/a";

        // Instantiate a new dog and add to list upon user confirmation
        String userChoice;
        System.out.print(YELLOW + "\nWould you like to add this dog (Y or N): " + RESET);
        while (true) {
            try {
                userChoice = scanner.nextLine().trim();
                if (userChoice.isEmpty() || (!userChoice.equalsIgnoreCase("y") && !userChoice.equalsIgnoreCase("n"))) {
                    System.out.print(YELLOW + "Would you like to add this dog (Y or N): " + RESET);
                } else if (userChoice.equalsIgnoreCase("y")) {
                    Dog dog = new Dog(name, breed, gender, age, weight, acquisitionDate,
                            acquisitionCountry, trainingStatus, reserved, inServiceCountry);
                    dogList.add(dog);
                    System.out.println(CYAN + "\nSuccessfully added!" + RESET);
                    return;
                } else if (userChoice.equalsIgnoreCase("n")) return;
            } catch (Exception e) {
                System.out.println("Error reading add dog prompt input.");
            }
        }
    }  // End of intakeNewDog method

    /**
     * Option 2: Passes user input, and adds monkey if monkey name does not exist
     *
     * @param scanner Used for user input
     */
    public static void intakeNewMonkey(Scanner scanner) {
        String name, species, gender, age, weight, acquisitionDate, acquisitionCountry,
                trainingStatus, inServiceCountry, tailLength, height, bodyLength;
        boolean reserved;

        // Name
        System.out.print("Monkey Name: ");
        while (true) {
            try {
                name = scanner.nextLine().trim();
                if (name.isEmpty()) {
                    System.out.print(RED + "Please enter a valid name: " + RESET);
                } else break;  // Exit inner loop if valid name
            } catch (Exception e) {
                System.out.print(RED + "Error reading monkey name. Please try again: " + RESET);
            }
        }

        try {
            // Verify monkey isn't already in system
            for (Monkey monkey : monkeyList) {
                if (monkey.getName() != null && monkey.getName().equalsIgnoreCase(name)) {
                    System.out.println(RED + "This monkey already exists in the system." + RESET);
                    return;  // Exit method and return to menu
                }
            }
        } catch (Exception e) {
            System.out.println(RED + "Error looking up monkey name." + RESET);
            return;
        }


        // Species
        final List<String> SPECIES = Arrays.asList("capuchin", "guenon", "macaque", "marmoset", "squirrel monkey", "tamarin");
        System.out.print("Species: ");
        while (true) {
            try {
                species = scanner.nextLine().trim().toLowerCase();
                if (species.isEmpty()) {
                    System.out.print(RED + "Only allowed species are capuchin, guenon, macaque, marmoset, squirrel monkey, or tamarin: " + RESET);
                } else if (!SPECIES.contains(species)) {
                    System.out.println(RED + "\nThis species is not allowed." + RESET);
                    return;
                } else break;
            } catch (Exception e) {
                System.out.println(RED + "Error reading monkey species." + RESET);
            }
        }

        gender = getGender(scanner);

        age = getAge(scanner);

        weight = getWeight(scanner);

        acquisitionDate = getAcquisitionDate(scanner);

        acquisitionCountry = getAcquisitionCountry(scanner);

        trainingStatus = getTrainingStatus(scanner);

        reserved = getReserved(scanner);

        if (trainingStatus.equalsIgnoreCase("in service"))
            inServiceCountry = getInServiceCountry(scanner);
        else inServiceCountry = "n/a";

        // Tail Length
        System.out.print("Tail Length (in.): ");
        while (true) {
            try {
                tailLength = scanner.nextLine().trim();
                if (tailLength.isEmpty()) {
                    System.out.print(RED + "Please enter the tail length in inches: " + RESET);
                    // Verify tailLength is numeric with 1 or more digits before and (optionally) after the decimal
                } else if (!tailLength.matches("\\d+(\\.\\d+)?")) {
                    System.out.print(RED + "Please enter a valid tail length in inches: " + RESET);
                } else break;
            } catch (Exception e) {
                System.out.println(RED + "Error reading monkey tail length." + RESET);
            }
        }

        // Height
        System.out.print("Height (in.): ");
        while (true) {
            try {
                height = scanner.nextLine().trim();
                if (height.isEmpty()) {
                    System.out.print(RED + "Please enter the height in inches (in.): " + RESET);
                    // Verify height is numeric with 1 or more digits before and (optionally) after the decimal
                } else if (!height.matches("\\d+(\\.\\d+)?")) {
                    System.out.print(RED + "Please enter a valid height in inches (in.): " + RESET);
                } else break;
            } catch (Exception e) {
                System.out.println(RED + "Error reading monkey height." + RESET);
            }
        }
        // Body Length
        System.out.print("Body Length (in.): ");
        while (true) {
            try {
                bodyLength = scanner.nextLine().trim();
                if (bodyLength.isEmpty()) {
                    System.out.print(RED + "Please enter the body length in inches: " + RESET);
                    // Verify bodyLength is numeric with 1 or more digits before and (optionally) after the decimal
                } else if (!bodyLength.matches("\\d+(\\.\\d+)?")) {
                    System.out.print(RED + "Please enter a valid body length in inches: " + RESET);
                } else break;
            } catch (Exception e) {
                System.out.println(RED + "Error reading monkey body length." + RESET);
            }
        }

        // Instantiate a new monkey and add to appropriate list
        String userChoice;
        System.out.print(YELLOW + "\nWould you like to add this monkey (Y or N): " + RESET);
        while (true) {
            try {
                userChoice = scanner.nextLine().trim();
                if (userChoice.isEmpty() || (!userChoice.equalsIgnoreCase("y") && !userChoice.equalsIgnoreCase("n"))) {
                    System.out.print(YELLOW + "Would you like to add this monkey (Y or N): " + RESET);
                } else if (userChoice.equalsIgnoreCase("y")) {
                    Monkey monkey = new Monkey(name, species, gender, age, weight, acquisitionDate, acquisitionCountry,
                            trainingStatus, reserved, inServiceCountry, tailLength, height, bodyLength);
                    monkeyList.add(monkey);
                    System.out.println(CYAN + "\nSuccessfully added!" + RESET);
                    return;
                } else if (userChoice.equalsIgnoreCase("n")) return;
            } catch (Exception e) {
                System.out.println(RED + "Error reading add monkey prompt input." + RESET);
            }
        }
    }  // End of intakeNewDog method

    /**
     * Option 3: Finds animal by animal type and in service country
     * 
     * @param scanner Scanner object to receive user input
     */
    public static void reserveAnimal(Scanner scanner) {
        String animalType, inServiceCountry;

        // Animal Type
        System.out.print("Animal type to reserve (dog or monkey): ");
        while (true) {
            try {
                animalType = scanner.nextLine().trim();
                if (animalType.isEmpty()) {
                    System.out.print(RED + "Please enter a valid animal type (dog or monkey): " + RESET);
                } else if (!animalType.equalsIgnoreCase("dog") && !animalType.equalsIgnoreCase("monkey")) {
                    System.out.print(RED + "Please enter a valid animal type (dog or monkey): " + RESET);
                } else break;  // Exit inner loop if valid animal type
            } catch (Exception e) {
                System.out.println(RED + "Error reading animal type." + RESET);
            }
        }

        // In Service Country
        System.out.print("What country is the service needed: ");
        while (true) {
            try {
                inServiceCountry = scanner.nextLine();
                if (inServiceCountry.trim().isEmpty()) {
                    System.out.print(RED + "Please enter a valid country: " + RESET);
                } else break;  // Exit inner loop if valid String
            } catch (Exception e) {
                System.out.println(RED + "Error reading in service country needed." + RESET);
            }
        }

        System.out.print(YELLOW + "\nWould you like to reserve this animal if available here (Y or N): " + RESET);
        String userChoice;
        while (true) {
            try {
                userChoice = scanner.nextLine().trim();
                if (userChoice.isEmpty() || (!userChoice.equalsIgnoreCase("y") && !userChoice.equalsIgnoreCase("n"))) {
                    System.out.print(YELLOW + "\nWould you like to reserve this animal if available here (Y or N): " + RESET);
                } else break;
            } catch (Exception e) {
                System.out.println("Error confirming reservation.");
            }
        }

        if (userChoice.equalsIgnoreCase("n")) return;
        else if (userChoice.equalsIgnoreCase("y")) {
            // Reserve in service dog if available
            if (animalType.equalsIgnoreCase("dog")) {
                try {
                    for (Dog dog : dogList) {
                        if (!dog.getInServiceCountry().equalsIgnoreCase(inServiceCountry)) {
                            System.out.println(RED + "\nNo in service dogs for this country!" + RESET);
                        } else {
                            dog.setReserved(true);
                            System.out.println(CYAN + "\nReserved successfully!" + RESET);
                        }
                        return;
                    }
                } catch (Exception e) {
                    System.out.println(RED + "Error reserving dog." + RESET);
                    return;
                }
            }
            // Reserve in service monkey if available
            else if (animalType.equalsIgnoreCase("monkey")) {
                try {
                    for (Monkey monkey : monkeyList) {
                        if (monkey.getInServiceCountry().equalsIgnoreCase(inServiceCountry)) {
                            monkey.setReserved(true);
                            System.out.println(CYAN + "\nReserved successfully!" + RESET);
                        } else {
                            System.out.println(RED + "\nNo in service monkeys for this country!" + RESET);
                        }
                        return;  // Return to system menu
                    }
                } catch (Exception e) {
                    System.out.println(RED + "Error reserving monkey." + RESET);
                    return;
                }
            }
            // If user did not enter 'dog' or 'monkey'
            else {
                System.out.print(RED + "\nPlease enter either 'dog' or 'monkey': " + RESET);
                return;
            }
        } else return;
    }
    
    /**
     * Helper function to print the header used in the print methods
     */
    public static void printHeader() {
        System.out.println();
        System.out.print(UNDERLINED + BLACK + WHITE_BG);  // TEXT_STYLE + TEXT_COLOR + BACKGROUND_COLOR
        System.out.printf(
            PRINT_FORMAT,
            "Name",
            "Training Status",
            "In Service Locations",
            "Reserved"
        );
        System.out.println(RESET);
    }

    /**
     * Option 4: Prints list of dogs
     */
    public static void printDogs() {        
        printHeader();

        try {
            for (Dog dog : dogList) {
                System.out.printf(
                        PRINT_FORMAT,
                        dog.getName(),
                        dog.getTrainingStatus(),
                        dog.getInServiceCountry(),
                        dog.getReserved() ? "Yes" : "No"
                );
            }
        } catch (Exception e) {
            System.out.println(RED + "Error printing dogs." + RESET);
        }
    }

    /**
     * Option 5: Prints list of monkeys
     */
    public static void printMonkeys() {
        printHeader();

        try {
            for (Monkey monkey: monkeyList) {
                System.out.printf(
                    PRINT_FORMAT,
                    monkey.getName(),
                    monkey.getTrainingStatus(),
                    monkey.getInServiceCountry(),
                    monkey.getReserved() ? "Yes" : "No"
                );
            }
        } catch (Exception e) {
            System.out.println(RED + "Error printing monkeys." + RESET);
        }
    }

    /**
     * Option 6: Prints all available in service animals
     */
    public static void printNonreserved() {
        printHeader();

        try {
            for (Dog dog: dogList) {
                if (!dog.getInServiceCountry().isEmpty() && !dog.getReserved() ) {
                    System.out.printf(
                        PRINT_FORMAT,
                        dog.getName(),
                        dog.getTrainingStatus(),
                        dog.getInServiceCountry(),
                        dog.getReserved() ? "Yes" : "No"
                    );
                }
            }
        } catch (Exception e) {
            System.out.println(RED + "Error printing non-reserved dogs." + RESET);
        }

        try {
            for (Monkey monkey: monkeyList) {
                if (!monkey.getInServiceCountry().isEmpty() && !monkey.getReserved() ) {
                    System.out.printf(
                        PRINT_FORMAT,
                        monkey.getName(),
                        monkey.getTrainingStatus(),
                        monkey.getInServiceCountry(),
                        monkey.getReserved() ? "Yes" : "No"
                    );
                }
            }
        } catch (Exception e) {
            System.out.println(RED + "Error printing non-reserved monkeys." + RESET);
        }
     
    }        


    /**
     * Rescue Animal Management System entry point
     * 
     * <p>Initializes system, loads animals, outputs a user menu, and accepts user input.</p>
     * 
     * @param args Command-line arguments not used in this program
     */
    public static void main(String[] args) {
    	String userOption;

        // Create Scanner object to get user input (UTF_8 for internationalization)
    	Scanner scanner = new Scanner(System.in, StandardCharsets.UTF_8);
    	
    	// Initializations of sample animals
        initializeDogList();
        initializeMonkeyList();

        // Loop until user enters 'q' or 'Q'
        do {
        	// Display user options
        	displayMenu();

        	// Get user input
            while (true) {
                try {
                    userOption = scanner.nextLine().trim();
                    if (userOption.length() != 1 || !ALLOWED_OPTIONS.contains(userOption)) {
                        System.out.print(RED + "Please enter a menu option number: " + RESET);
                    }
                    else break;  // Exit inner loop if valid option entered
                } catch (Exception e) {
                    System.out.println("Error reading user input in system menu.");
                }
            }

        	// User option actions
        	switch(userOption) {
            	case "1":
            		intakeNewDog(scanner);
            		break;
        	    case "2":
        		    intakeNewMonkey(scanner);
        		    break;
        	    case "3":
        		    reserveAnimal(scanner);
        		    break;
        	    case "4":
        		    printDogs();
        		    break;
        	    case "5":
        		    printMonkeys();
        		    break;
        	    case "6":
        		    printNonreserved();
        		    break;
                // "q" or "Q" to quit
                case "q":
        	    case "Q":
        		    System.out.println(BLUE + "\nQuitting system" + RESET);
        		    System.exit(0);  // Exit program with no errors
        		    break;
                default:
                    System.out.println(RED + "Please try again." + RESET);
                    break;
        	}

        } while (!userOption.equalsIgnoreCase("q"));

        scanner.close();
    }
}
