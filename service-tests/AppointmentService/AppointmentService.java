package com.appointmentservice.AppointmentService;

import java.util.ArrayList;
import java.util.Date;

/**
 *
 * @author Matthew Pool
 * @version 1.0
 */
public class AppointmentService {
    
    // Create list of appointments
    private final ArrayList<Appointment> appointments = new ArrayList<Appointment>();

    // Method to create an appointment and add to list of appointments
    public void createAppointment(String id, Date date, String description) {
  
        // Verify id doesn't exist in appointments
        for (int i = 0; i < appointments.size(); ++i) {
            if (appointments.get(i).getId().equals(id)) {
                throw new IllegalArgumentException("Appointment ID already exists - cannot add!");
            }
        }
        
        // Create new Appointment instance
        Appointment appointment = new Appointment(id, date, description);
        
        // Store appointment in appointments list
        appointments.add(appointment);
    }
    
    // Method to delete an appointment from list of appointments
    public void deleteAppointment(String id) {
        
        // Delete appointment if id exists in appointments list
        for (int i = 0; i < appointments.size(); ++i) {
            if (appointments.get(i).getId().equals(id)) {
                appointments.remove(i);
                return; // exit method after deletion
            }
        }
        throw new IllegalArgumentException("Appointment ID not found - cannot remove!");
    }
    
    // Method to update an appointment from list of appointments
    public void updateAppointment(String id, Date date, String description) {
    
        // Update appointment if id exists in appointments list
        for (int i = 0; i < appointments.size(); ++i) {
            if (appointments.get(i).getId().equals(id)) {
                Appointment appointment = new Appointment(id, date, description);
                appointments.set(i, appointment);
                return;
            }
        }
        throw new IllegalArgumentException("Appointment ID not found - cannot update!");
    }
}
