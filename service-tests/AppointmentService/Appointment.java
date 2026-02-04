package com.appointmentservice.AppointmentService;

import java.util.Date;

/**
 *
 * @author Matthew Pool
 * @version 1.0
 */
public class Appointment {
    private static final int MAX_ID = 10;
    private static final int MAX_DESCRIPTION = 50;
    private final String id; // 10 char max; not null, not updateable
    private final Date date; // valid future Date; not null 
    private final String description; // 50 char max; not null
    
    // Validate passed appointment information
    private void validateInfo(String id, Date date, String description) {
        
        if (id == null || id.length() > MAX_ID) {
            throw new IllegalArgumentException("ID must be between 1 and 10 characters!");
        }
        
        if (date == null || date.before(new Date())) { // verifies passed date should be later than current date
            throw new IllegalArgumentException("Date must be a valid future date!");
        }
        
        if (description == null || description.length() > MAX_DESCRIPTION) {
            throw new IllegalArgumentException("Description must be between 1 and 50 characters!");
        }
    }

    // Parameterized Constructor
    public Appointment(String id, Date date, String description) {
        
        validateInfo(id, date, description);
        
        this.id = id;
        this.date = date;
        this.description = description;
    }
    
    // Getters / Accessors
    public String getId() {
        return this.id;
    }
    public Date getDate() {
        return this.date;
    }
    public String getDescription() {
        return this.description;
    }
}
