package rescueAnimal;

import java.util.ArrayList;
import java.util.Scanner;

public class Driver {
    
	// Instance variables / ArrayList initializations
	private static ArrayList<Dog> dogList = new ArrayList<Dog>();
    private static ArrayList<Monkey> monkeyList = new ArrayList<Monkey>();
    
    public static void main(String[] args) {
    	
    	char option = '0';
    	
    	Scanner scanner = new Scanner(System.in);  // creates Scanner object named scanner for user input
    	
    	// Optional: test animals (no actual animal-testing was done)
        initializeDogList();
        initializeMonkeyList();

        // loop that displays the menu, accepts the users input, and takes the appropriate action.
        do {
        	
        	// Display user options
        	displayMenu();  
        	
        	// user option input
        	option = scanner.nextLine().charAt(0);
        	
        	// user option actions
        	switch(option)
        	{
        	case '1':
        		intakeNewDog(scanner);
        		break; // return; or break;
        	case '2':
        		intakeNewMonkey(scanner);
        		break;
        	case '3':
        		reserveAnimal(scanner);
        		break;
        	case '4':
        		printAnimals('4'); // dog
        		break;
        	case '5':
        		printAnimals('5'); // monkey
        		break;
        	case '6':
        		printAnimals('6'); // all non-reserved ("available") animals
        		break;
        	case 'q':
        	case 'Q':
        		System.out.println("Quitting system");
        		System.exit(0);  // exits program with exit_code 0 (no errors)
        		break;
        	default:
        		System.out.println("Incorrect option entered.");
        		break;
        	}
        } while (option != 'q' && option != 'Q');        
    }

    // This method prints the menu options
    public static void displayMenu() {
        System.out.println("\n\n");
        System.out.println("\t\t\t\tRescue Animal System Menu");
        System.out.println("[1] Intake a new dog");
        System.out.println("[2] Intake a new monkey");
        System.out.println("[3] Reserve an animal");
        System.out.println("[4] Print a list of all dogs");
        System.out.println("[5] Print a list of all monkeys");
        System.out.println("[6] Print a list of all animals that are not reserved");
        System.out.println("[Q] Quit application");
        System.out.println();
        System.out.println("Enter a menu selection");
    }


    // Adds dogs to a list for testing
    public static void initializeDogList() {
        Dog dog1 = new Dog("Spot",	"German Shepherd", 	"male", 	"1", "25.6", "05-12-2019", "United States", "intake",		false, 	"United States");
        Dog dog2 = new Dog("Rex", 	"Great Dane", 		"male", 	"3", "35.2", "02-03-2020", "United States", "Phase I",		false, 	"United States");
        Dog dog3 = new Dog("Bella", "Chihuahua",		"female", 	"4", "25.6", "12-12-2019", "Canada", 		"in service",	true, 	"Canada");
       
        dogList.add(dog1);
        dogList.add(dog2);
        dogList.add(dog3);
    }

    // Adds monkeys to a list for testing
    public static void initializeMonkeyList() {
    	Monkey monkey1 = new Monkey("Squirts",	"Capuchin",	"male", 	"1", "25.6", "05-12-2019", "United States", "intake", 		false, 	"United States","3 in",	 "12 in", "11 in");
        Monkey monkey2 = new Monkey("George", 	"Guenon", 	"male", 	"3", "35.2", "02-03-2020", "United States", "Phase I", 		false, 	"United States","16 in", "22 in", "30 in");
        Monkey monkey3 = new Monkey("Rover",	"Macaque",	"female", 	"4", "25.6", "12-12-2019", "Canada", 		"in service", 	true, 	"Canada", 		"4 in",  "13 in", "24 in");

        monkeyList.add(monkey1);
        monkeyList.add(monkey2);
        monkeyList.add(monkey3);
    }

    public static void intakeNewDog(Scanner scanner) {
        
    	System.out.print("Dogs Name: ");
        String name = scanner.nextLine();

        // verify dog isn't already in system
        for(Dog dog : dogList) {
        
        	if(dog.getName().equalsIgnoreCase(name)) {
            
        		System.out.println("\n\nThis dog is already in our system\n\n");
                return; //returns to menu
            }
        }

        // Questions for new Dog
        System.out.print("Breed: ");
        String breed = scanner.nextLine();
        
        System.out.print("Gender: ");
        String gender = scanner.nextLine();
        
        System.out.print("Age: ");
        String age = scanner.nextLine();
        
        System.out.print("Weight: ");
        String weight = scanner.nextLine();
        
        System.out.print("Acquisition Date: ");
        String acquisitionDate = scanner.nextLine();
        
        System.out.print("Acquisition Country: ");
        String acquisitionCountry = scanner.nextLine();
        
        System.out.print("Training Status <options> 1, 2, 3, 4, 5, \'in service\', or \'farm\': ");
        String trainingStatus = scanner.nextLine();
        
        System.out.print("In Service Country (leave blank if not applicable): ");
        String inServiceCountry = scanner.nextLine();
        
        if (inServiceCountry.equals("")) {
        	inServiceCountry = "n/a";
        }
        	
        System.out.print("Reserved <options> \'true\' or \'false\': ");
        boolean reserved = scanner.nextBoolean();
        scanner.nextLine();
        
        // code to instantiate a new dog and add it to the appropriate list
        Dog newDog = new Dog(name, breed, gender, age, weight, acquisitionDate, acquisitionCountry, trainingStatus, reserved, inServiceCountry);
        
        dogList.add(newDog);
        System.out.println("\nSuccessfully added!");
        return;
        
    }
    
		// make sure monkey doesn't already exist and species type is allowed
        public static void intakeNewMonkey(Scanner scanner) {
            
        	System.out.print("Monkey Name: ");
            String name = scanner.nextLine();
    
            for(Monkey monkey : monkeyList) {
             
            	if(monkey.getName().equalsIgnoreCase(name)) {
                
            		System.out.println("\n\nThis monkey is already in our system\n\n");
                    return; //returns to menu
                }
            }

            // Questions for new monkey
            System.out.print("Species: ");
            String species = scanner.nextLine();
            
            // verify species is allowed
            switch (species)
            {
            case "Capuchin":
            case "Guenon":
            case "Macaque":
            case "Marmoset":
            case "Squirrel monkey":
            case "Tamarin":
            	break;	
            	
            default:
            	System.out.println("\nWe do not allow these type of monkeys!");
            	return;
            }
            
            System.out.print("Gender: ");
            String gender = scanner.nextLine();
            
            System.out.print("Age: ");
            String age = scanner.nextLine();
            
            System.out.print("Weight: ");
            String weight = scanner.nextLine();
            
            System.out.print("Acquisition Date: ");
            String acquisitionDate = scanner.nextLine();
            
            System.out.print("Acquisition Country: ");
            String acquisitionCountry = scanner.nextLine();
            
            System.out.print("Training Status <options> 1, 2, 3, 4, 5, \'in service\', or \'farm\': ");
            String trainingStatus = scanner.nextLine();
            
            System.out.print("In Service Country (leave blank if not applicable): ");
            String inServiceCountry = scanner.nextLine();
            
            if (inServiceCountry.equals("")) {
            	inServiceCountry = "n/a";
            }
            
            System.out.print("Reserved <options> \'true\' or \'false\': ");
            boolean reserved = scanner.nextBoolean();
            scanner.nextLine();
            
            System.out.print("Tail Length: ");
            String tailLength = scanner.nextLine();
            
            System.out.print("Height: ");
            String height = scanner.nextLine();
            
            System.out.print("Body Length: ");
            String bodyLength = scanner.nextLine();
            
            // code to instantiate a new monkey and add it to the appropriate list
            Monkey newMonkey = new Monkey(name, species, gender, age, weight, acquisitionDate, acquisitionCountry, trainingStatus, reserved, inServiceCountry, tailLength, height, bodyLength);
            
            monkeyList.add(newMonkey);
            System.out.println("\nSuccessfully added!");
            return;
        }

        //Find the animal by animal type and in service country
        public static void reserveAnimal(Scanner scanner) {
            
            System.out.print("Animal Type: ");
            String animalType = scanner.nextLine();
            
            System.out.print("Service Country: ");
            String inServiceCountry = scanner.nextLine();
            
            if (animalType.equalsIgnoreCase("dog")) {

            	for (int i = 0; i < dogList.size(); i++) {
            		if (dogList.get(i).getInServiceLocation().equals(inServiceCountry)) {
            			
            			dogList.get(i).setReserved(true);
            			
            			System.out.println("\nReserved successfully!\n");
            			break;
            		}
            	}
            }
            
            else if (animalType.equalsIgnoreCase("monkey")) {
            	
            	for (int i = 0; i < monkeyList.size(); i++) {
            	
            		if (monkeyList.get(i).getInServiceLocation().equals(inServiceCountry)) {
            			
            			monkeyList.get(i).setReserved(true);
            			
            			System.out.println("\nReserved successfully!\n");
            			break;
            		}
            	}
            }
            
            else {
            	System.out.println("\nOnly \'monkey\' or \'dog\' are accepted.");
            }      
            
            return;
        }
        
        
        // Include animal name, status, acquisition country and if the animal is reserved.
        // This method connects to three different menu items.
        
        // The printAnimals() method has three different outputs based on the listType parameter
        	// dog - prints the list of dogs
        	// monkey - prints the list of monkeys
        // available - prints a combined list of all animals that are fully trained ("in service") but not reserved

    public static void printAnimals(char option) {

        //dog data output format
        String format = "%-20s %-20s %-25s %-10s%n";

        //header text used when printing data
        System.out.printf(	format,
                            "Name",
                            "Training Status",
                            "In Service Locations",
                            "Reserved"
                            );

        switch(option) {

        case '4': //dog

            for (Dog dog : dogList) {
                System.out.printf(	format,
                                    dog.getName(),
                                    dog.getTrainingStatus(),
                                    dog.getInServiceLocation(),
                                    dog.getReserved() ? "Yes" : "No"
                                    );
            }

            break;

        case '5': //monkey

            for (Monkey monkey : monkeyList) {
                System.out.printf(	format,
                                    monkey.getName(),
                                    monkey.getTrainingStatus(),
                                    monkey.getInServiceLocation(),
                                    monkey.getReserved() ? "Yes" : "No"
                                    );
            }

            break;

        case '6': //all "in service" (fully-trained) "non-reserved" animals

            for (Dog dog : dogList) {
                if (!dog.getInServiceLocation().isEmpty() && !dog.getReserved() ) {
                    System.out.printf(	format,
                                        dog.getName(),
                                        dog.getTrainingStatus(),
                                        dog.getInServiceLocation(),
                                        dog.getReserved() ? "Yes" : "No"
                                        );
                }
            }

            for (Monkey monkey : monkeyList) {
                if (!monkey.getInServiceLocation().isEmpty() && !monkey.getReserved() ) {
                    System.out.printf(	format,
                                        monkey.getName(),
                                        monkey.getTrainingStatus(),
                                        monkey.getInServiceLocation(),
                                        monkey.getReserved() ? "Yes" : "No"
                                        );
                }
            }

            break;
        }  //end switch

        return;
    }
        
}
