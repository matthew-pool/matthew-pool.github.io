package com.appbuddy.inventorybuddy;
// TODO: switch to Kotlin sealed classes for type-safe state management
public enum UserState {
    DEFAULT_STATE,
    LOGIN_FAILURE,
    SIGNUP_FAILURE,
    SIGNUP_SUCCESS,
    LOGIN_SUCCESS,
    ACCEPTED_SMS,
    REJECTED_SMS,
    ITEM_ADDED,
    ITEM_DELETED,
    ITEM_UPDATED,
    ERROR_STATE,
}
