package com.appbuddy.inventorybuddy;

import android.content.Context;

import androidx.room.Room;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;
import dagger.hilt.InstallIn;
import dagger.hilt.android.qualifiers.ApplicationContext;
import dagger.hilt.components.SingletonComponent;

@Module
@InstallIn(SingletonComponent.class) // specifies that this module is installed in the SingletonComponent, meaning the provided instances are application-scoped singletons
public class DatabaseModule {

    @Provides  // AppDatabase instance
    @Singleton // marks the provided instance as a singleton within the scope of the SingletonComponent (application scope)
    public AppDatabase provideAppDatabase(@ApplicationContext Context context) { // @ApplicationContext ensures that the application context is used, preventing potential memory leaks
        return Room.databaseBuilder(context.getApplicationContext(), AppDatabase.class, "db")
                .fallbackToDestructiveMigration() // handles migrations properly in a real app
                .build();
    }
    @Provides  // UserDao instance
    public UserDao provideUserDao(AppDatabase db) { // provides UserDao instances from the AppDatabase instance
        return db.userDao();
    }
    @Provides  // ItemDao instance
    public ItemDao provideItemDao(AppDatabase db) { return db.itemDao();
    }
    // @Provides other DAO providers as needed
}
