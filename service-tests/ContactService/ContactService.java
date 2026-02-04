package com.appointmentservice.ContactService;

// Libraries/Modules
import java.util.ArrayList;

/**
 * Service class with operations for Contact objects.
 *
 * Contact information includes a unique customer ID, first
 * and last name, phone number, and address.
 * Service operations include Create, Delete, and Update.
 *
 * @author Matthew Pool
 * @version 1.0
 */
public class ContactService {

    // TODO: use <Map> instead of <ArrayList> for better time complexity
    // ArrayList methods: .add(<Contact>), .remove(i), .get(i), .set(i, <Contact>), .clear(), .size()
    private final ArrayList<Contact> contacts = new ArrayList<Contact>();

    /**
     * Create a new Contact object.
     *
     * @param id Unique identifier for Contact to be created.
     * @param firstName Contact first name.
     * @param lastName Contact last name.
     * @param phone Contact phone number.
     * @param address Contact address.
     * @throws IllegalArgumentException If ID already exists in database.
     */
    public void createContact(String id, String firstName, String lastName, String phone, String address) {
        
        // verify id doesn't already exist in one of the Contact objects in the contacts list
        for (int i = 0; i < contacts.size(); ++i) {
            if (contacts.get(i).getId().equals(id)) {
                throw new IllegalArgumentException("Contact ID already exists - cannot add!");
            }
        }

        // create a new Contact object instance using the new contact info
        Contact contact = new Contact(id, firstName, lastName, phone, address);

        // store new Contact in list of contacts
        contacts.add(contact);
    }

    /**
     * Deletes an existing Contact object.
     *
     * @param id Unique identifier for Contact to be deleted.
     * @throws IllegalArgumentException If ID does not exist in database.
     */
    public void deleteContact(String id) {

        // delete contact if ID found
        for (int i = 0; i < contacts.size(); ++i) {
            if (contacts.get(i).getId().equals(id)) {
                contacts.remove(i);
                return; // exit method after deletion
            }
        }
        throw new IllegalArgumentException("Contact ID not found - cannot remove!");
    }

    /**
     * Updates an existing Contact object.
     *
     * @param id Unique identifier for Contact to be created.
     * @param firstName Contact first name.
     * @param lastName Contact last name.
     * @param phone Contact phone number.
     * @param address Contact address.
     * @throws IllegalArgumentException If ID does not exist in database.
     */
    public void updateContact(String id, String firstName, String lastName, String phone, String address) {
        
        // Update existing Contact object if it already exists
        for (int i = 0; i < contacts.size(); ++i) {
            if (contacts.get(i).getId().equals(id)) {
                // Updates contact with passed Contact information and add to contacts list
                Contact contact = new Contact(id, firstName, lastName, phone, address);
                contacts.set(i, contact);
                return; // exits method after adding new updating contact
            }
        }
        // If no contacts matching passed ID are found, then throw exception
        throw new IllegalArgumentException("Contact ID not found!");
    }
}
