package com.appointmentservice.ContactService;

public class Contact {
    // "final" ensures each private variable is immutable for each Contact object reference once assigned
    private static final int MAX_10 = 10;
    private static final int MAX_30 = 30;
    private final String id;        // 10 characters max; not NULL; not updateable
    private final String firstName; // 10 characters max; not NULL
    private final String lastName;  // 10 characters max; not NULL
    private final String phone;     // exactly 10 digits; not NULL
    private final String address;   // 30 characters max; not NULL
    
    /*
    // Default Constructor: not needed with "final" attributes
    public Contact() {
        this.id = "";
        this.firstName = "";
        this.lastName = "";
        this.phone = "";
        this.address = "";
    }
    */
    
    // Helper function to validate passed Contact information when creating a new Contact object instance
    private void validateInfo(String id, String firstName, String lastName, String phone, String address) {

        if (id == null || !id.matches("\\d{1,10}")) {
            throw new IllegalArgumentException("ID must be between 1 and 10 digits.");
        }
        if (firstName == null || firstName.length() > MAX_10) {
            throw new IllegalArgumentException("First name length should be less than or equal to 10 characters.");
        }
        if (lastName == null || lastName.length() > MAX_10) {
            throw new IllegalArgumentException("Last name length should be less than or equal to 10 characters.");
        }
        if (phone == null || !phone.matches("\\d{10}")) {
            throw new IllegalArgumentException("Phone number must be exactly 10 digits.");
        }
        if (address == null || address.length() > MAX_30) {
            throw new IllegalArgumentException("Address length should be less than or equal to 30 characters.");
        }
    }
    
    // Parameterized Constructor
    public Contact(String id, String firstName, String lastName, String phone, String address) {

        validateInfo(id, firstName, lastName, phone, address);

        // this. ensures Contact object instance has its values set to the passed parameters
        this.id = id;
        this.firstName = firstName;
        this.lastName = lastName;
        this.phone = phone;
        this.address = address;
    }

    // Getters/Accessors
    public String getId() {
        return this.id;
    }
    public String getFirstName() {
        return this.firstName;
    }
    public String getLastName() {
        return this.lastName;
    }
    public String getPhone() {
        return this.phone;
    }
    public String getAddress() {
        return this.address;
    }
    
}
