// :core:datastore module AppDatabase.java
package com.appbuddy.inventorybuddy;

import android.content.Context;
import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;
// Data Source: obtains data from Room database
// can be a single database, file, network source, etc.
// Room: Library for SQLite database operations
// abstracts database creation and version management
// inherently protects against SQL injection attacks
// uses DAOs to define database interactions
//==================================================================================================
// Database class for Room
@Database(entities = {User.class, Item.class}, version = 1)  // version used for modified schema (e.g., adding/removing tables)
public abstract class AppDatabase extends RoomDatabase {
    public abstract UserDao userDao();  // returns instance of UserDao
    public abstract ItemDao itemDao();  // returns instance of ItemDao
    private static volatile AppDatabase INSTANCE;  // Singleton instance
    // Singleton method to get the instance of AppDatabase
    public static AppDatabase getDatabase(final Context context) {
        if (INSTANCE == null) {
            synchronized (AppDatabase.class) {
                if (INSTANCE == null) {
                    // Create database
                    // Application Context is global to entire application's lifecycle
                    // and safer for context that lives beyond current activity (or when creating singletons)
                    INSTANCE = Room.databaseBuilder(context.getApplicationContext(),
                            AppDatabase.class, "db")
                            .fallbackToDestructiveMigration()  // Strategy for migration; consider customizing
                            .build();
                }
            }
        }
        return INSTANCE;
    }

    // more DAOs can be added here

//==================================================================================================
//  TODO: SQLCipher with Room for database security (AES)
//  TODO: Migration to new schema version
//==================================================================================================
    /*
    Room.databaseBuilder(context.getApplicationContext(), AppDatabase.class, "inventory_database")
        .addMigrations(MIGRATION_1_2, MIGRATION_2_3)  // Example migrations between versions
        .build();
    */
//==================================================================================================
}