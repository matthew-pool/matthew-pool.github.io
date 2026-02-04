package com.appointmentservice.AppointmentService;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.text.ParseException;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.BeforeEach;

/**
 *
 * @author Matthew Pool
 * @version 1.0
 */
@DisplayName("Appointment Class Test")
public class AppointmentTest {

    private static final String DATE_FORMAT = "MMMM d, yyyy";
    private static final SimpleDateFormat sdf = new SimpleDateFormat(DATE_FORMAT);
    
    private static final String ID = "77777";
    private static final String DESCRIPTION = "Valid appointment description.";

    private Date date;
    private Date pastDate;

    private Date createDate(String dateString) throws ParseException {
        return sdf.parse(dateString);
    }

    @BeforeEach
    public void setup() throws ParseException {
        date = createDate("December 30, 2050");
        pastDate = createDate("January 1, 2000"); // Y2K
    }
    
    @Test
    @DisplayName("Invalid Misspelled Month")
    public void testMisspelledMonth() {
        assertThrows(ParseException.class,
                () -> createDate("Febtember 22, 2050"));
    }

    @Test
    @DisplayName("Invalid Past Date")
    public void testPastDate() {
        //Date pastdate = createDate("January 1, 2000"); // Y2K
        assertThrows(IllegalArgumentException.class,
                () -> new Appointment(ID, pastDate, DESCRIPTION));
    }

    @Test
    @DisplayName("Valid Constructor")
    public void testValidConstructor() {
        assertDoesNotThrow(() -> new Appointment("123987", date, DESCRIPTION));
    }

    @Test
    @DisplayName("Invalid ID Over 10 Characters")
    public void testInvalidIdOverLimit() {
        assertThrows(IllegalArgumentException.class, () -> new Appointment("01234567890", date, DESCRIPTION));
    }

    @Test
    @DisplayName("Invalid Null ID")
    public void testInvalidNullId() {
        assertThrows(IllegalArgumentException.class, () -> new Appointment(null, date, DESCRIPTION));
    }

    @Test
    @DisplayName("Invalid Null Date")
    public void testInvalidNullDate() {
        assertThrows(IllegalArgumentException.class, () -> new Appointment(ID, null, DESCRIPTION));
    }

    @Test
    @DisplayName("Invalid Long Description")
    public void testInvalidDescriptionOverLimit() {
        assertThrows(IllegalArgumentException.class, () -> new Appointment(ID, date, "This description is extremely long and way too long."));
    }

    @Test
    @DisplayName("Invalid Null Description")
    public void testInvalidNullDescription() {
        assertThrows(IllegalArgumentException.class, () -> new Appointment(ID, date, null));
    }

    @Test
    @DisplayName("Getter/Accessor Method Tests")
    void testGetters() {
        Appointment appointment = new Appointment("7890", date, DESCRIPTION);
        
        assertTrue(appointment.getId().equals("7890"));
        assertTrue(appointment.getDate().equals(date));
        assertTrue(appointment.getDescription().equals(DESCRIPTION));
    }
}
