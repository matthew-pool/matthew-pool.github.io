package com.appointmentservice.TaskService;

/**
 *
 * @author Matthew Pool
 * @version 1.0
 */
public class Task {
    private static final int MAX_ID = 10;
    private static final int MAX_NAME = 20;
    private static final int MAX_DESCRIPTION = 50;
    private final String id; // 10 char max; not null, not updateable
    private final String name; // 20 char max; not null 
    private final String description; // 50 char max; not null
    
    // Validate passed task information
    private void validateInfo(String id, String name, String description) {
        
        if (id == null || id.length() > MAX_ID) {
            throw new IllegalArgumentException("ID must be between 1 and 10 characters!");
        }
        
        if (name == null || name.length() > MAX_NAME) {
            throw new IllegalArgumentException("Name must be between 1 and 20 characters!");
        }
        
        if (description == null || description.length() > MAX_DESCRIPTION) {
            throw new IllegalArgumentException("Description must be between 1 and 50 characters!");
        }
    }

    // Parameterized Constructor
    public Task(String id, String name, String description) {
        
        validateInfo(id, name, description);
        
        this.id = id;
        this.name = name;
        this.description = description;
    }
    
    // Getters / Accessors
    public String getId() {
        return this.id;
    }
    public String getName() {
        return this.name;
    }
    public String getDescription() {
        return this.description;
    }
}
