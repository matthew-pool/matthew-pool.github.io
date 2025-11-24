package rescueAnimal;

/**
 * Dog class extends RescueAnimal.
 * 
 * <p>The Dog class provides dog-specific attribute 'breed'.</p>
 * 
 * @author Matthew Pool
 * @version 2.0
 * @since 2024-11-14
 * @see RescueAnimal
 */
public class Dog extends RescueAnimal {

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
