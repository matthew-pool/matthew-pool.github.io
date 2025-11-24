package com.appbuddy.inventorybuddy;

import android.content.SharedPreferences;
import android.util.Log;

import androidx.lifecycle.LiveData;

import java.util.List;
import java.util.concurrent.Executors;

import javax.inject.Inject;
import javax.inject.Singleton;

@Singleton
public class ItemRepository {
    private final ItemDao itemDao;
    private final SharedPreferences sharedPreferences;
//==================================================================================================
//  Constructors
//==================================================================================================
    @Inject
    public ItemRepository(ItemDao itemDao, SharedPreferences sharedPreferences) {
        this.itemDao = itemDao;
        this.sharedPreferences = sharedPreferences;
    }
//==================================================================================================
//  Custom Functions
//==================================================================================================
    public Long fetchId() {
        Long userId = null;
        try {
            userId = sharedPreferences.getLong("user_id", -1L);
        } catch (Exception e) {
            Log.e("UserRepository: retrieveId: ", "getLong call: " + e);
        }
        return userId;
    }
//==================================================================================================
//  CRUD Functions
//==================================================================================================
    public void insertItem(Item item) {
        Executors.newSingleThreadExecutor().execute(() -> itemDao.insertItem(item));  //background thread
    }
    public LiveData<List<Item>> getItems() {
        return itemDao.getItems();
    }
    public void updateItem(Item item) {
        Executors.newSingleThreadExecutor().execute(() -> itemDao.updateItem(item));  //background thread
    }
    public void deleteItem(Item item) {
        Executors.newSingleThreadExecutor().execute(() -> itemDao.deleteItem(item));  //background thread
    }
//==================================================================================================
}