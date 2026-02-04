package com.appointmentservice.ContactService;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;

@DisplayName("ContactService Class Test")
public class ContactServiceTest {

    private final String id = "77777";
    private final String firstName = "Freddy";
    private final String lastName = "Mercury";
    private final String phone = "5556669999";
    private final String address = "1428 Elm Street";
    
    private ContactService contactService;
    
    @BeforeEach
    public void setUp() {
        contactService = new ContactService();
    }
    
    // Test createContact method
    @Test
    @DisplayName("createContact Method Test")
    public void testCreateContact() {
        
        // Test normal case
        assertDoesNotThrow(() -> {
            contactService.createContact(id, firstName, lastName, phone, address);
        });
        
        // Test existing matching ID
        assertThrows(IllegalArgumentException.class, () -> {
            contactService.createContact(id, "Fred", "Flinstone", "1112223333", "Bedrock");
        });
    }
    
    // Test deleteContact method
    @Test
    @DisplayName("deleteContact Method Test")
    public void testDeleteContact() {
        
        contactService.createContact(id, firstName, lastName, phone, address);
        
        // Test deleting existing contact with matching ID
        assertDoesNotThrow(() -> {
            contactService.deleteContact(id);
        });
        
        // Test deleting contact with non-matching ID
        assertThrows(IllegalArgumentException.class, () -> {
            contactService.deleteContact("0123456789");
        });
     
    }
    // Test update Contact method
    @Test
    @DisplayName("updateContact Method Test")
    public void testUpdateContact() {
        
        contactService.createContact(id, firstName, lastName, phone, address);
        
        // Test updating contact with matching ID
        assertDoesNotThrow(() -> {
            contactService.updateContact(id, "Fredrick", "Fredding", "9998887777", "Fred Street");
        });
        
        // Test updating contact with non-matching ID
        assertThrows(IllegalArgumentException.class, () -> {
            contactService.updateContact("9876543210", "Fredster", "Frederico", "1119995555", "Fred Town, USA");
        });
    }
}
