package rescueAnimal;

import java.io.Serial;
import java.io.Serializable;

/**
 * RescueAnimal base class for all rescue animals.
 * 
 * <p>The RescueAnimal class is the parent class to all animals.
 * It includes name, animalType, gender, age, weight, acquisitionDate,
 * acquisitionCountry, trainingStatus, reserved, and inServiceCountry.</p>
 * 
 * @author Matthew Pool
 * @version 4.0
 * @since 2024-12-01
 * @see Dog
 * @see Monkey
 */
public class RescueAnimal implements Serializable {
	// Used for Serializable functionality
	@Serial
	private static final long serialVersionUID = 1L;

    // Attributes (instance variables)
    private String name;
    private String animalType;
    private String gender;
    private String age;
    private String weight;
    private String acquisitionDate;
    private String acquisitionCountry;
	private String trainingStatus;
    private boolean reserved;
	private String inServiceCountry;

    // Constructor
    public RescueAnimal() {}
    
    // Getters & Setters
	public String getName() { 
		return name; 
	}

	public void setName(String name) { 
		this.name = name; 
	}

	public String getAnimalType() {	
		return animalType; 
	}

	public void setAnimalType(String animalType) {
		this.animalType = animalType;
	}
		
	public String getGender() {
		return gender;
	}

	public void setGender(String gender) {
		this.gender = gender;
	}

	public String getAge() {
		return age;
	}

	public void setAge(String age) {
		this.age = age;
	}

	public String getWeight() {
		return weight;
	}

	public void setWeight(String weight) {
		this.weight = weight;
	}

	public String getAcquisitionDate() {
		return acquisitionDate;
	}

	public void setAcquisitionDate(String acquisitionDate) {
		this.acquisitionDate = acquisitionDate;
	}

	public String getAcquisitionCountry() {
		return acquisitionCountry;
	}

	public void setAcquisitionCountry(String acquisitionCountry) {
		this.acquisitionCountry = acquisitionCountry;
	}

	public String getTrainingStatus() {
		return trainingStatus;
	}

	public void setTrainingStatus(String trainingStatus) {
		this.trainingStatus = trainingStatus;
	}

	public boolean getReserved() {
		return reserved;
	}

	public void setReserved(boolean reserved) {
		this.reserved = reserved;
	}

	public String getInServiceCountry() {
		return inServiceCountry;
	}

	public void setInServiceCountry(String inServiceCountry) {
		this.inServiceCountry = inServiceCountry;
	}
}
