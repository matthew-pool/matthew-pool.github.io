package com.appointmentservice.TaskService;

import java.util.ArrayList;

/**
 *
 * @author Matthew Pool
 * @version 1.0
 */
public class TaskService {
    
    // Create list of tasks
    private final ArrayList<Task> tasks = new ArrayList<Task>();

    // Method to create a task and add to list of tasks
    public void createTask(String id, String name, String description) {
  
        // Verify id doesn't exist in tasks
        for (int i = 0; i < tasks.size(); ++i) {
            if (tasks.get(i).getId().equals(id)) {
                throw new IllegalArgumentException("Task ID already exists - cannot add!");
            }
        }
        
        // Create new Task instance
        Task task = new Task(id, name, description);
        
        // Store task in tasks list
        tasks.add(task);
    }
    
    // Method to delete a task from list of tasks
    public void deleteTask(String id) {
        
        // Delete task if id exists in tasks list
        for (int i = 0; i < tasks.size(); ++i) {
            if (tasks.get(i).getId().equals(id)) {
                tasks.remove(i);
                return; // exit method after deletion
            }
        }
        throw new IllegalArgumentException("Task ID not found - cannot remove!");
    }
    
    // Method to update a task from list of tasks
    public void updateTask(String id, String name, String description) {
    
        // Update task if id exists in tasks list
        for (int i = 0; i < tasks.size(); ++i) {
            if (tasks.get(i).getId().equals(id)) {
                Task task = new Task(id, name, description);
                tasks.set(i, task);
                return;
            }
        }
        throw new IllegalArgumentException("Task ID not found - cannot update!");
    }
}
