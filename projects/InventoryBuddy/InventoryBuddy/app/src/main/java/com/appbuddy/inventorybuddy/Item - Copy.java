package com.appbuddy.inventorybuddy;

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.Ignore;
import androidx.room.Index;
import androidx.room.PrimaryKey;

@Entity(tableName = "item_table",
        /*foreignKeys = @ForeignKey(  entity = User.class,
                                    parentColumns = "id",
                                    childColumns = "userId",
                                    onDelete = ForeignKey.CASCADE),  // CASCADE: deletes all associated items when User is deleted
        */
        indices = {@Index(value = {"itemId"})}) // indices improve query performance for operations involving the foreign key (userId)
public class Item {
    @PrimaryKey(autoGenerate = true)
    private Long itemId;
    /* TODO: userId foreign key to link user's items to user
    @ColumnInfo(name = "userId")
    private Long userId;  // foreign key to user_table.id column
     */
    @ColumnInfo(name = "name")
    private String name;
    @ColumnInfo(name = "quantity")
    private int quantity;
//==================================================================================================
//  Constructors
//==================================================================================================
    @Ignore
    public Item() {}

    public Item(String name, int quantity) {
        this.name = name;
        this.quantity = quantity;
    }

    @Ignore
    public Item(Long itemId, Long userId, String name, int quantity) {
        this.itemId = itemId;
        this.name = name;
        this.quantity = quantity;
    }
//==================================================================================================
//  Getters and Setters
//==================================================================================================
    public Long getItemId() {
        return itemId;
    }
    public void setItemId(Long itemId) {
        this.itemId = itemId;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public int getQuantity() {
        return quantity;
    }
    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }
//==================================================================================================
}