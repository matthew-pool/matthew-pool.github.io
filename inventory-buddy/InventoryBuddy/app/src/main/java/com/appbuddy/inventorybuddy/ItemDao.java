package com.appbuddy.inventorybuddy;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import java.util.List;

@Dao
public interface ItemDao {
    // execute in background thread
    @Insert
    void insertItem(Item item);

    // LiveData with Room automatically executes queries on background threads
    @Query("SELECT * FROM item_table")
    LiveData<List<Item>> getItems();

    // execute in background thread
    @Update
    void updateItem(Item item);

    // execute in background thread
    @Delete
    void deleteItem(Item item);
}
