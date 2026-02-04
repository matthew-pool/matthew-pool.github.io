package com.appointmentservice.AppointmentService;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import java.util.Date;
import java.text.SimpleDateFormat;
import java.text.ParseException;

/**
 *
 * @author Matthew Pool
 * @version 1.0
 */
@DisplayName("AppointmentService Class Test")
public class AppointmentServiceTest {
    private static final String DATE_FORMAT = "MMMM d, yyyy";
    private static final SimpleDateFormat sdf = new SimpleDateFormat(DATE_FORMAT);
    
    private static final String ID = "77777";
    private static final String DESCRIPTION = "Valid DESCRIPTION.";
    
    private com.appointmentservice.AppointmentService.AppointmentService appointmentService;
    private Date date;
    private Date pastDate;
    
    // create valid future Date
    public Date createDate(String dateString) {
        try {
            return sdf.parse(dateString);
        } catch (ParseException e) {
            fail("Failed date parsing of dateString");
            return null;
        }
    }
    
    @BeforeEach
    public void setup() {
        // create valid future Date called 'date'
        date = createDate("December 30, 2050");
        // verify returned date is not null
        assertNotNull(date);

        pastDate = createDate("January 1, 2000"); // Y2K
        assertNotNull(pastDate);
        
        appointmentService = new AppointmentService();
        assertNotNull(appointmentService);
    }
    
    @Test
    @DisplayName("Invalid Past Date")
    public void testPastDate() {
        assertThrows(IllegalArgumentException.class, () -> {
            appointmentService.createAppointment("2222", pastDate, DESCRIPTION);
        });
    }
    
    // Test createAppointment method
    @Test
    @DisplayName("createAppointment Method Test")
    public void testCreateAppointment() {
        
        // Test valid Normal Case
        assertDoesNotThrow(() -> {
            appointmentService.createAppointment(ID, date, DESCRIPTION);
        });
        
        // Test valid multiple appointments in list
        assertDoesNotThrow(() -> {
            date = createDate("January 22, 2051");    
        });

        assertDoesNotThrow(() -> {
            appointmentService.createAppointment("99", date, "Testing for multiple appointments.");
        });
        
        // Test invalid creation of Appointment via existing ID
        assertThrows(IllegalArgumentException.class, () -> {
            appointmentService.createAppointment(ID, date, "Some Appointment Description.");
        });
    }

    // Test deleteAppointment method
    @Test
    @DisplayName("deleteAppointment Method Test")
    public void testDeleteAppointment() {

        appointmentService.createAppointment(ID, date, DESCRIPTION);

        // Test valid Normal Case deletion via existing ID
        assertDoesNotThrow(() -> {
            appointmentService.deleteAppointment(ID);
        });

        // Test invalid deletion via nonexisting ID
        assertThrows(IllegalArgumentException.class, () -> {
            appointmentService.deleteAppointment("12345");
        });
    }

    // Test updateAppointment method
    @Test
    @DisplayName("updateAppointment Method Test")
    public void testUpdateAppointment() {

        appointmentService.createAppointment(ID, date, DESCRIPTION);

        // Test valid Normal Case update via matching ID
        assertDoesNotThrow(() -> {
            appointmentService.updateAppointment(ID, date, "New DESCRIPTION.");
        });
      
        // Test invalid update via non-matching ID
        assertThrows(IllegalArgumentException.class, () -> {
            appointmentService.updateAppointment("00000", date, "Some other DESCRIPTION.");
        });
    }
}
