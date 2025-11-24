package com.appbuddy.inventorybuddy;

import android.content.Context;
import android.content.SharedPreferences;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;
import dagger.hilt.InstallIn;
import dagger.hilt.android.qualifiers.ApplicationContext;
import dagger.hilt.components.SingletonComponent;

@Module
@InstallIn(SingletonComponent.class)
public abstract class AppModule {

    @Provides
    @Singleton
    public static UserRepository provideUserRepository(UserDao userDao, SharedPreferences sharedPreferences) {
        return new UserRepository(userDao, sharedPreferences);
    }
    @Provides
    @Singleton
    public static ItemRepository provideItemRepository(ItemDao itemDao, SharedPreferences sharedPreferences) {
        return new ItemRepository(itemDao, sharedPreferences);
    }
    @Provides
    @Singleton
    public static SharedPreferences provideSharedPreferences(@ApplicationContext Context context) {
        return context.getSharedPreferences("UserPreferences", Context.MODE_PRIVATE);
    }
    // @Provides for other application-scoped dependencies here
}
