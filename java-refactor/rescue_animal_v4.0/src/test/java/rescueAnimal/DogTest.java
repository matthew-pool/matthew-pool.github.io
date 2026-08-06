package rescueAnimal;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Unit tests for the Dog class.
 *
 * <p>Tests class functions and instantiations.</p>
 *
 * @author Matthew Pool
 * @version 4.0
 * @since 2024-12-01
 */
public class DogTest {

    @Test
    @DisplayName("Test default constructor.")
    public void testDefaultConstructor() {
        Dog dog = new Dog();
        assertEquals(null, dog.getName());
    }

    @Test
    @DisplayName("Test parameterized constructor.")
    public void testParameterizedConstructor() {
        Dog dog = new Dog("Crimson", "Great Dane", "male", "3", "35.2", "02-03-2020",
                "United States", "Phase 1", false, "United States");
        assertEquals("Crimson", dog.getName());
    }

    @Test
    @DisplayName("Test dog setters and getters.")
    public void testDogGettersAndSetters() {
        Dog dog = new Dog();

        // Setters
        dog.setName("Sophie");
        dog.setAnimalType("dog");
        dog.setBreed("German Shepherd");
        dog.setGender("male");
        dog.setAge("1");
        dog.setWeight("25.6");
        dog.setAcquisitionDate("05-12-2019");
        dog.setAcquisitionCountry("United States");
        dog.setTrainingStatus("intake");
        dog.setReserved(false);
        dog.setInServiceCountry("United States");

        // Getters
        assertEquals("Sophie", dog.getName());
        assertEquals("dog", dog.getAnimalType());
        assertEquals("German Shepherd", dog.getBreed());
        assertEquals("male", dog.getGender());
        assertEquals("1", dog.getAge());
        assertEquals("25.6", dog.getWeight());
        assertEquals("05-12-2019", dog.getAcquisitionDate());
        assertEquals("United States", dog.getAcquisitionCountry());
        assertEquals("intake", dog.getTrainingStatus());
        assertEquals(false, dog.getReserved());
        assertEquals("United States", dog.getInServiceCountry());
    }
}
