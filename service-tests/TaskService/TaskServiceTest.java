package com.appointmentservice.TaskService;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;

/**
 *
 * @author Matthew Pool
 * @version 1.0
 */
@DisplayName("TaskService Class Test")
public class TaskServiceTest {
    private final String id = "77777";
    private final String name = "Valid Name";
    private final String description = "Valid description.";
    
    private TaskService taskService;
    
    @BeforeEach
    public void setUp() {
        taskService = new TaskService();
    }

    // Test createTask method
    @Test
    @DisplayName("createTask Method Test")
    public void testCreateTask() {
        
        // Test valid Normal Case
        assertDoesNotThrow(() -> {
            taskService.createTask(id, name, description);
        });
        
        // Test valid multiple tasks in list
        assertDoesNotThrow(() -> {
            taskService.createTask("99", "Another Task", "Testing for multiple tasks.");
        });
        
        // Test invalid creation of Task via existing id
        assertThrows(IllegalArgumentException.class, () -> {
            taskService.createTask(id, "Some Task", "Some Task Description.");
        });
    } 
    // Test deleteTask method
    @Test
    @DisplayName("deleteTask Method Test")
    public void testDeleteTask() {

        taskService.createTask(id, name, description);

        // Test valid Normal Case deletion via existing id
        assertDoesNotThrow(() -> {
            taskService.deleteTask(id);
        });

        // Test invalid deletion via existing id
        assertThrows(IllegalArgumentException.class, () -> {
            taskService.deleteTask("12345");
        });
    }

    // Test updateTask method
    @Test
    @DisplayName("updateTask Method Test")
    public void testUpdateTask() {

        taskService.createTask(id, name, description);

        // Test valid Normal Case update via matching id
        assertDoesNotThrow(() -> {
            taskService.updateTask(id, "New Name", "New description.");
        });

        // Test invalid update via non-matching id
        assertThrows(IllegalArgumentException.class, () -> {
            taskService.updateTask("00000", "Some Other Name", "Some other description.");
        });
    }
}
