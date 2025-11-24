// :core:data module UserDao.java
package com.appbuddy.inventorybuddy;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;

//==================================================================================================
// DAO (Data Access Object) interfaces with database(s)/table(s)
// CRUD database methods: Create (Insert), Read (Query), Update, Delete
// must be run on a background thread to prevent locking the UI and possible ANR
@Dao
public interface UserDao {

    // @Insert returns id of new row (or number less than 0 if user already exists)
    @Insert(onConflict = OnConflictStrategy.IGNORE) // IGNORE: returns -1L or -1 if username already exists
    Long insertUser(User user);  // array<long> (long[]) for bulk insert return type returns all ids of new rows; otherwise -1L or -1 if username already exists

    // @Query returns null if record not found; otherwise returns id > 0 for matching row
    @Query("SELECT id FROM user_table WHERE username = :username AND password = :password")  // TODO: change to hashed password
    Long getUserId(String username, String password);
//==================================================================================================
    // @Transaction: prevents issues with data integrity by creating an atomic operation
    // @Relation: allows fetching data from multiple tables without using JOIN
    // @RawQuery: used for complex queries that cannot be handled by Room
}
