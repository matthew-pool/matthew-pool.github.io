package com.appointmentservice.TaskService;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.DisplayName;

/**
 *
 * @author Matthew Pool
 * @version 1.0
 */
@DisplayName("Task Class Test")
public class TaskTest {
    private final String id = "77777";
    private final String name = "Valid Task Name";
    private final String description = "Valid task description.";
    
    // Test Getters
    @Test
    @DisplayName("Getter/Accessor Method Test")
    void testGetters() {
        Task task = new Task(id, name, description);
        
        assertTrue(task.getId().equals(id));
        assertTrue(task.getName().equals(name));
        assertTrue(task.getDescription().equals(description));
    }
    
    // Test Constructor validators
    @Test
    @DisplayName("Parameterized Constructor Test")
    public void testConstructor() {

        // Test valid Normal Case
        assertDoesNotThrow(() -> {
            new Task(id, name, description);
        });
        
        // Test invalid id over 10 characters
        assertThrows(IllegalArgumentException.class, () -> {
            new Task("01234567890", name, description);
        });
        
        // Test invalid id that is null
        assertThrows(IllegalArgumentException.class, () -> {
            new Task(null, name, description);
        });
        
        // Test invalid name that is over 20 characters
        assertThrows(IllegalArgumentException.class, () -> {
            new Task(id, "This Name Is Way Too Long", description);
        });
        
        // Test invalid name that is null
        assertThrows(IllegalArgumentException.class, () -> {
            new Task(id, null, description);
        });
        
        // Test invalid description that is over 50 characters
        assertThrows(IllegalArgumentException.class, () -> {
            new Task(id, name, "This description is extremely long and way too long.");
        });
        
        // Test invalid description that is null
        assertThrows(IllegalArgumentException.class, () -> {
            new Task(id, name, null);
        });
        
    }
    
}
