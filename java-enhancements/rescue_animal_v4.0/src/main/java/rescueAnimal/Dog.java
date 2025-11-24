package rescueAnimal;

import java.io.Serial;
import java.io.Serializable;  // Used to integrate MapDB

/**
 * Dog class extends RescueAnimal.
 * 
 * <p>The Dog class provides dog-specific attribute 'breed'.</p>
 * 
 * @author Matthew Pool
 * @version 4.0
 * @since 2024-12-01
 * @see RescueAnimal
 */
public class Dog extends RescueAnimal implements Serializable {
    // Used for Serializable functionality
    @Serial
    private static final long serialVersionUID = 1L;

    // Attribute (instance variable)
    private String breed;

    // Constructors
    public Dog() {}

    public Dog(String name, String breed, String gender, String age, String weight, String acquisitionDate,
               String acquisitionCountry,String trainingStatus, boolean reserved, String inServiceCountry) {
        setName(name);
        setBreed(breed);
        setGender(gender);
        setAge(age);
        setWeight(weight);
        setAcquisitionDate(acquisitionDate);
        setAcquisitionCountry(acquisitionCountry);
        setTrainingStatus(trainingStatus);
        setReserved(reserved);
        setInServiceCountry(inServiceCountry);
    }

    // Accessor
    public String getBreed() {
        return breed;
    }

    // Mutator
    public void setBreed(String dogBreed) {
        breed = dogBreed;
    }
}
