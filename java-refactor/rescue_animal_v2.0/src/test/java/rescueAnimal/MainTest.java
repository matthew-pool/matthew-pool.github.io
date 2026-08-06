package rescueAnimal;

import org.junit.jupiter.api.*;

import java.util.Scanner;
import java.io.InputStream;
import java.io.ByteArrayInputStream;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Unit tests for the Main class.
 *
 * <p>Tests class functions and instantiations.</p>
 *
 * @author Matthew Pool
 * @version 2.0
 * @since 2024-11-14
 */
public class MainTest {

    private Scanner scanner;
    private InputStream originalSystemIn;

    @BeforeAll
    public static void setUpAll() {
        Main.initializeDogList();
        Main.initializeMonkeyList();
    }

    @BeforeEach
    public void setUpEach() {
        // Original state
        originalSystemIn = System.in;
    }

    @AfterEach
    public void tearDown() {
        // Restore state
        System.setIn(originalSystemIn);
        if (scanner != null) scanner.close();
    }

    @AfterAll
    public static void finalTearDown() {
        System.out.println("\n\nAll tests complete!");
    }

    @Test
    @DisplayName("Test display menu.")
    public void testMenu() {
        Main.displayMenu();
    }

    @Test
    @DisplayName("Test empty input, then incorrect input, and then quit the application.")
    public void testEmptyInput() {
        String simulateEmpty = "\nX\n Q \n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateEmpty.getBytes()));
        scanner = new Scanner(System.in);
    }

    @Test
    @DisplayName("Test getGender.")
    public void testGetGender() {
        String gender;

        // Valid input
        String simulateValidInput = "male";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateValidInput.getBytes()));
        scanner = new Scanner(System.in);
        gender = Main.getGender(scanner);
        assertEquals("male", gender);

        // Invalid input, followed by valid input
        String simulateInvalidInput = "\nm\n8\n98.4\n//\n female \n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateInvalidInput.getBytes()));
        scanner = new Scanner(System.in);
        gender = Main.getGender(scanner);
        assertEquals("female", gender);
    }

    @Test
    @DisplayName("Test getAge.")
    public void testGetAge() {
        String age;

        // Valid input
        String simulateValidInput = "3\n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateValidInput.getBytes()));
        scanner = new Scanner(System.in);
        age = Main.getAge(scanner);
        assertEquals("3", age);

        // Invalid input, followed by valid input
        String simulateInvalidInput = "\nk\n//\n600\n-1\n 1 \n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateInvalidInput.getBytes()));
        scanner = new Scanner(System.in);
        age = Main.getAge(scanner);
        assertEquals("1", age);
    }

    @Test
    @DisplayName("Test getWeight.")
    public void testGetWeight() {
        String weight;

        // Valid input
        String simulateValidInput = "3\n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateValidInput.getBytes()));
        scanner = new Scanner(System.in);
        weight = Main.getWeight(scanner);
        assertEquals("3", weight);

        // Invalid input, followed by valid input
        String simulateInvalidInput = "\nk\n//\n600\n-1\n 1.2 \n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateInvalidInput.getBytes()));
        scanner = new Scanner(System.in);
        weight = Main.getWeight(scanner);
        assertEquals("1.2", weight);
    }

    @Test
    @DisplayName("Test getAcquisitionDate.")
    public void testGetAcquisitionDate() {
        String acquisitionDate;

        // Valid input
        String simulateValidInput = " 12-15-1981 \n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateValidInput.getBytes()));
        scanner = new Scanner(System.in);
        acquisitionDate = Main.getAcquisitionDate(scanner);
        assertEquals("12-15-1981", acquisitionDate);

        // Invalid input, followed by valid input
        String simulateInvalidInput = "\n//\n3-44/8\nXX-DD-1981\n12-15-2025\n12-15-1333\n1x-5i-jj22\n02-30-2020\n11-31-2020\n02-29-2023\n12-00-2020\n 02-29-2024 \n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateInvalidInput.getBytes()));
        scanner = new Scanner(System.in);
        acquisitionDate = Main.getAcquisitionDate(scanner);
        assertEquals("02-29-2024", acquisitionDate);
    }

    @Test
    @DisplayName("Test getAcquisitionCountry.")
    public void testGetAcquisitionCountry() {
        String acquisitionCountry;

        // Valid input
        String simulateValidInput = "United States\n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateValidInput.getBytes()));
        scanner = new Scanner(System.in);
        acquisitionCountry = Main.getAcquisitionCountry(scanner);
        assertEquals("United States", acquisitionCountry);
    }

    @Test
    @DisplayName("Test getTrainingStatus.")
    public void testGetTrainingStatus() {
        String trainingStatus;  // 'Phase 1'...'Phase 5", 'intake', 'in service', farm
        String simulateValidInput;

        // Valid input
        simulateValidInput = "in service\n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateValidInput.getBytes()));
        scanner = new Scanner(System.in);
        trainingStatus = Main.getTrainingStatus(scanner);
        assertEquals("in service", trainingStatus);

        // Invalid input, followed by valid input
        String simulateInvalidInput = "\n//\n3-44/8\n3\n23.4\n farm \n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateInvalidInput.getBytes()));
        scanner = new Scanner(System.in);
        trainingStatus = Main.getTrainingStatus(scanner);
        assertEquals("farm", trainingStatus);
    }

    @Test
    @DisplayName("Test getReserved.")
    public void testGetReserved() {
        boolean isReserved;

        // Valid input
        String simulateValidInput = "true\n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateValidInput.getBytes()));
        scanner = new Scanner(System.in);
        isReserved = Main.getReserved(scanner);
        assertEquals(true, isReserved);

        // Invalid input, followed by valid input
        String simulateInvalidInput = "\nk\n//\n600\n-1\n false \n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateInvalidInput.getBytes()));
        scanner = new Scanner(System.in);
        isReserved = Main.getReserved(scanner);
        assertEquals(false, isReserved);
    }

    @Test
    @DisplayName("Test getInServiceCountry.")
    public void testGetInServiceCountry() {
        String inServiceCountry;

        // Empty string, followed by valid input
        String simulateInvalidInput = "\n United States \n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateInvalidInput.getBytes()));
        scanner = new Scanner(System.in);
        inServiceCountry = Main.getInServiceCountry(scanner);
        assertEquals("United States", inServiceCountry);
    }

    @Test
    @DisplayName("Test intakeNewDog.")
    public void testIntakeNewDog() {
        // name, breed, gender, age, weight, acquisitionDate, acquisitionCountry, trainingStatus, isReserved, inServiceCountry -> Y
        String simulateDog = "\nKit Kat\n\nDoberman\n\nmale\n\nWRONG-TYPE\n\nWRONG-TYPE\n3\n\nWRONG-TYPE\n35.2\n\nWRONG-TYPE\n02-03-2020\n\nUnited States\n\nWRONG-TYPE\nin service\n\nWRONG-TYPE\ntrue\n\nUnited States\n\nX\nY\n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateDog.getBytes()));
        scanner = new Scanner(System.in);
        // Call method with simulated input
        Main.intakeNewDog(scanner);

        // Existing name
        String simulateExistingDog = "Kit Kat\n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateExistingDog.getBytes()));
        scanner = new Scanner(System.in);
        // Call method with simulated input
        Main.intakeNewDog(scanner);

        // Do not add dog
        simulateDog = "Peanut\nWeiner\nmale\n2\n23\n02-03-2020\nUnited States\nin service\nfalse\nUnited States\nn\n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateDog.getBytes()));
        scanner = new Scanner(System.in);
        // Call method with simulated input
        Main.intakeNewDog(scanner);

        // name, breed, gender, age, weight, acquisitionDate, acquisitionCountry, trainingStatus, isReserved, inServiceCountry -> Y
        String simulateInputNewDog = "\n Rover \n Doberman \n male \n 3 \n 23.3 \n 12-01-2020 \n United States \n farm \n true \n Y \n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateInputNewDog.getBytes()));
        scanner = new Scanner(System.in);
        // Call method with simulated input
        Main.intakeNewDog(scanner);
    }

    @Test
    @DisplayName("Test intakeNewMonkey.")
    public void testIntakeNewMonkey() {
        // name, species, gender, age, weight, acquisitionDate, acquisitionCountry, trainingStatus, isReserved, inServiceCountry, tailLength, height, bodyLength -> Y
        String simulateMonkey = "\nJack\n\ncapuchin\n\nWRONG-TYPE\nfemale\n\nWRONG-TYPE\n4\n\nWRONG-TYPE\n25.6\n\nWRONG-TYPE\n02-03-2020\n\nUnited States\n\nWRONG-TYPE\nin service\n\nWRONG-TYPE\nfalse\n\nUnited States\n\nWRONG-TYPE\n4\n\nWRONG-TYPE\n13\n\nWRONG-TYPE\n24\n\nWRONG-TYPE\nY\n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateMonkey.getBytes()));
        scanner = new Scanner(System.in);
        // Call method with simulated input
        Main.intakeNewMonkey(scanner);

        // Existing name
        String simulateExistingMonkey = "Jack\n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateExistingMonkey.getBytes()));
        scanner = new Scanner(System.in);
        // Call method with simulated input
        Main.intakeNewMonkey(scanner);

        // Do not add monkey
        simulateMonkey = "George\ncapuchin\nfemale\n4\n25.6\n02-03-2020\nUnited States\nin service\nfalse\nUnited States\n4\n13\n24\nn\n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateMonkey.getBytes()));
        scanner = new Scanner(System.in);
        // Call method with simulated input
        Main.intakeNewMonkey(scanner);

        // name, species, gender, age, weight, acquisitionDate, acquisitionCountry, trainingStatus, isReserved, inServiceCountry, tailLength, height, bodyLength -> Y
        String simulateInputNewMonkey = "\n Rover \n Guenon \n female \n 3 \n 23.3 \n 12-01-2020 \n United States \n farm \n true \n 13 \n 23.3 \n 24 \n Y \n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateInputNewMonkey.getBytes()));
        scanner = new Scanner(System.in);
        // Call method with simulated input
        Main.intakeNewMonkey(scanner);
    }

    @Test
    @DisplayName("Test reserveAnimal.")
    public void testReserveAnimal() {
        String simulateReservation = "\n dog \n \n United States \n\n Y \n";
        // Simulate user input
        System.setIn(new ByteArrayInputStream(simulateReservation.getBytes()));
        scanner = new Scanner(System.in);
        // Call method with simulated input
        Main.reserveAnimal(scanner);
    }

    @Test
    @DisplayName("Test options 4, 5, 6, q.")
    public void testOptions456Q() {
        Main.printDogs();           // Option 4
        Main.printMonkeys();        // Option 5
        Main.printNonreserved();    // Option 6

        // Simulate user input
        String simulateEmpty = " q  \n";  // Option "q"
        System.setIn(new ByteArrayInputStream(simulateEmpty.getBytes()));
        scanner = new Scanner(System.in);
    }
}