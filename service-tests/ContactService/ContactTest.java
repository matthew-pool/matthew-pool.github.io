package com.appointmentservice.ContactService;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.DisplayName;

@DisplayName("Contact Class Test")
public class ContactTest {
    
    private final String id = "77777";
    private final String firstName = "Freddy";
    private final String lastName = "Mercury";
    private final String phone = "5556669999";
    private final String address = "1428 Elm Street";
    
    // Test getters
    @Test
    @DisplayName("Getter/Mutator Method Test")
    void testGetters() {
        Contact contact = new Contact(id, firstName, lastName, phone, address);
        assertTrue(contact.getId().equals(id));
        assertTrue(contact.getFirstName().equals(firstName));
        assertTrue(contact.getLastName().equals(lastName));
        assertTrue(contact.getPhone().equals(phone));
        assertTrue(contact.getAddress().equals(address));
    }
    
    // Test constructor validations
    @Test
    @DisplayName("Parameterized Constructor Test")
    public void testConstructor() {
    
        // Test normal case
        assertDoesNotThrow(() -> {
            new Contact(id, firstName, lastName, phone, address);
        });    
        
        // TODO: Use nested test methods for testing different parameters
        // Test invalid ID
        assertThrows(IllegalArgumentException.class, () -> {
            new Contact("10000000000", firstName, lastName, phone, address);
        });

        assertThrows(IllegalArgumentException.class, () -> {
            new Contact(null, firstName, lastName, phone, address);
        });
        
        assertThrows(IllegalArgumentException.class, () -> {
            new Contact("123F987", firstName, lastName, phone, address);
        });
        
        // Test invalid first name
        assertThrows(IllegalArgumentException.class, () -> {
            new Contact(id, "Bartholomew", lastName, phone, address);
        });

        assertThrows(IllegalArgumentException.class, () -> {
            new Contact(id, null, lastName, phone, address);
        });

        // Test invalid last name
        assertThrows(IllegalArgumentException.class, () -> {
            new Contact(id, firstName, "Higginbotham", phone, address);
        });

        assertThrows(IllegalArgumentException.class, () -> {
            new Contact(id, firstName, null, phone, address);
        });

        // Test invalid phone
        assertThrows(IllegalArgumentException.class, () -> {
            new Contact(id, firstName, lastName, "55566699990", address);
        });

        assertThrows(IllegalArgumentException.class, () -> {
            new Contact(id, firstName, lastName, null, address);
        });

        assertThrows(IllegalArgumentException.class, () -> {
           new Contact(id, firstName, lastName, "111222333", address); 
        });
        
        assertThrows(IllegalArgumentException.class, () -> {
            new Contact(id, firstName, lastName, "1113B35555", address);
        });
        
        // Test invalid address
        assertThrows(IllegalArgumentException.class, () -> {
            new Contact(id, firstName, lastName, phone, "Nightmare on Elm Street at 1428");
        });

        assertThrows(IllegalArgumentException.class, () -> {
            new Contact(id, firstName, lastName, phone, null);
        });
    }
}
