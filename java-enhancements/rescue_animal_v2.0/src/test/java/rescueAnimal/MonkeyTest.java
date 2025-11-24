package rescueAnimal;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Unit tests for the Monkey class.
 *
 * <p>Tests class functions and instantiations.</p>
 *
 * @author Matthew Pool
 * @version 2.0
 * @since 2024-11-14
 */
public class MonkeyTest {

    @Test
    @DisplayName("Test default constructor.")
    public void testDefaultConstructor() {
        Monkey monkey = new Monkey();
        assertEquals(null, monkey.getName());
    }

    @Test
    @DisplayName("Test parameterized constructor.")
    public void testParameterizedConstructor() {
        Monkey monkey = new Monkey("Gizmo", "guenon", "male", "3", "35.2", "02-03-2020",
                "United States", "Phase 1", false, "United States",
                "16", "22", "30");
        assertEquals("Gizmo", monkey.getName());
    }

    @Test
    @DisplayName("Test monkey setters and getters.")
    public void testMonkeyGetters() {
        Monkey monkey = new Monkey();

        // Setters
        monkey.setName("Kimchi");
        monkey.setAnimalType("monkey");
        monkey.setSpecies("capuchin");
        monkey.setGender("male");
        monkey.setAge("1");
        monkey.setWeight("25.6");
        monkey.setAcquisitionDate("05-12-2019");
        monkey.setAcquisitionCountry("United States");
        monkey.setTrainingStatus("intake");
        monkey.setReserved(false);
        monkey.setInServiceCountry("United States");
        monkey.setTailLength("32.3");
        monkey.setBodyLength("48.3");
        monkey.setHeight("20");

        // Getters
        assertEquals("Kimchi", monkey.getName());
        assertEquals("monkey", monkey.getAnimalType());
        assertEquals("capuchin", monkey.getSpecies());
        assertEquals("male", monkey.getGender());
        assertEquals("1", monkey.getAge());
        assertEquals("25.6", monkey.getWeight());
        assertEquals("05-12-2019", monkey.getAcquisitionDate());
        assertEquals("United States", monkey.getAcquisitionCountry());
        assertEquals("intake", monkey.getTrainingStatus());
        assertEquals(false, monkey.getReserved());
        assertEquals("United States", monkey.getInServiceCountry());
        assertEquals("32.3", monkey.getTailLength());
        assertEquals("48.3", monkey.getBodyLength());
        assertEquals("20", monkey.getHeight());
    }
}
