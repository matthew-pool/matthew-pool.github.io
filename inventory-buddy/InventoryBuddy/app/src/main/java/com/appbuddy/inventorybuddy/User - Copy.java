// :core:datastore module User.java
// optionally: other data sources like Firebase, REST API, etc. can be used for other Repository/DAOs
package com.appbuddy.inventorybuddy;

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.Ignore;
import androidx.room.Index;
import androidx.room.PrimaryKey;

// Model (Data Store): data structure/table for Room database
// User entity class for Room database
 // @Entity: specifies that this class is a Room entity
 // @tableName: specifies the name of the table in the database
 // @PrimaryKey: specifies the primary key for the table
 // @ColumnInfo: specifies the name of the column in the table
 // @Ignore: Room ignores the annotated element
 // @Index: used to create an index for a column to speed up queries
 // indices enforce a unique constraint on the column so that the column (username) is unique
@Entity(tableName = "user_table",
        indices = {@Index(value = {"username"}, unique = true)})
public class User {
    @PrimaryKey(autoGenerate = true)
    private Long id;

    @ColumnInfo(name = "username")
    private String username;

    @ColumnInfo(name = "password")
    private String password;  // TODO: change to hashed password

    // TODO: @ColumnInfo public String email;
//==================================================================================================
//  Constructors
//==================================================================================================
    @Ignore  // Room ignores this constructor
    public User() {}

    public User(String username, String password) {
        this.username = username;
        this.password = password;
    }

    @Ignore  // Room ignores this constructor
    public User(Long id, String username, String password) {
        this.id = id;  // default value is 0L
        this.username = username;
        this.password = password;
    }
//==================================================================================================
//  Getters and Setters (for unit testing)
//==================================================================================================
    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }
    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }
    public String getPassword() {
        return password;
    }
    public void setPassword(String password) {
        this.password = password;
    }
}