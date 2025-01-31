// :feature:login module UserViewModel.java
package com.appbuddy.inventorybuddy;

import android.util.Log;

import androidx.annotation.NonNull;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import java.util.List;

import javax.inject.Inject;

import dagger.hilt.android.lifecycle.HiltViewModel;

// ViewModels: use LiveData, Flow, or RxJava to expose data to View (Screen)
// constructs/retain data/states across configuration changes (e.g., screen rotations)
// handle UI logic and calls Repository methods to update data
// should interact with repository through dependency injection (Hilt)
// lifecycle aware and best for data observing and data-reactive UI
//==================================================================================================
@HiltViewModel  // Hilt annotation to enable ViewModel injection
public class UserViewModel extends ViewModel {
    private final UserRepository userRepository;  // injected into ViewModel by Hilt
    private final ItemRepository itemRepository;  // injected into ViewModel by Hilt
    private UserState userState;// = getUserState(); // initial user state
    // LiveData: Lifecycle aware and best for data observing and data-reactive UI (asynchronous background thread)
    // Mutable data cannot be observed, but can be changed/updated
    private final MutableLiveData<String> toastMessage = new MutableLiveData<>();
    String message;
    private String smsPermission;
    private LiveData<List<Item>> items;
//==================================================================================================
//  Constructors
//==================================================================================================
    // default constructor unnecessary since using @HiltViewModel annotation for Hilt
    @Inject
    public UserViewModel(UserRepository userRepository, ItemRepository itemRepository) {
        this.userRepository = userRepository;
        this.itemRepository = itemRepository;
        items = itemRepository.getItems();
    }
//==================================================================================================
//  Custom Functions
//==================================================================================================
public void loginUser(String username, String password) {
    try {
        userRepository.loginUser(username, password);
        userState = getUserState();

        if (userState == UserState.LOGIN_FAILURE) {
            try {
                signUpUser(username, password);  // attempt to create new account

            } catch (Exception e) {
                Log.e("UserRepository: loginUser: ", "signUpUser call: " + e);
            }
        }
    } catch (Exception e) {
        Log.e("UserViewModel", "userRepository.loginUser: " + e.getMessage());
    }

    try {
        userState = getUserState();

    } catch (Exception e) {
        Log.e("UserViewModel: loginUser", "getUserState: " + e.getMessage());
    }

    try {
        setToast(userState);

    } catch (Exception e) {
        Log.e("UserViewModel: loginUser", "reactToUserState: " + e.getMessage());
    }
}
//==================================================================================================
    public void signUpUser(String username, String password) {
        try {
            userRepository.signUpUser(username, password);

        } catch (Exception e) {
            Log.e("UserViewModel", "userRepository.signUpUser: " + e.getMessage());
        }

        try {
            setToast(getUserState());

        } catch (Exception e) {
            Log.e("UserViewModel", "reactToUserState: " + e.getMessage());
        }
    }
//==================================================================================================
    void setToast(@NonNull UserState userState) {
        // set toast message based on user state
        switch (userState) {
            case DEFAULT_STATE:
                // no message to set
                break;
            case LOGIN_FAILURE:
                message = "Account not found. Creating account.";
                break;
            case SIGNUP_FAILURE:
                message = "Signup failed. Please try again.";
                break;
            case SIGNUP_SUCCESS:
                message = "Account created. Logging in.";
                break;
            case LOGIN_SUCCESS:
                message = "Account found. Logging in.";
                break;
            case ACCEPTED_SMS:
                message = "SMS permission accepted.";
                break;
            case REJECTED_SMS:
                message = "SMS permission denied.";
                break;
            case ITEM_ADDED:
                message = "Item added.";
                break;
            case ITEM_DELETED:
                message = "Item removed.";
                break;
            case ITEM_UPDATED:
                message = "Item updated.";
                break;
            case ERROR_STATE:
                message = "Please try again.";
                break;
            default:
                // unexpected state
                Log.e("UserViewModel: setToast: " + userState, "Unexpected UserState userState");
                break;
        }

        // set toast message
        try {
            toastMessage.postValue(message);

        } catch (Exception e) {
            Log.e("UserViewModel: reactToUserState: setToastMessage: " + userState, message + e.getMessage());
        }
    }
//==================================================================================================
//  Getters and Setters
//==================================================================================================
    public UserState getUserState() {
        return userRepository.getUserState();
    }
    public void setUserState(UserState userState) {
        this.userState = userState;
        userRepository.setUserState(userState);
    }
    public String fetchSmsPermission() {
        smsPermission = userRepository.fetchSmsPermission();
        return smsPermission;
    }
    public void saveSmsPermission(String smsPermission) {
        userRepository.saveSmsPermission(smsPermission);
        this.smsPermission = smsPermission;  // update LiveData to notify observers
    }
    public Long fetchId() {
        return userRepository.fetchId();
    }
    public void saveId(Long id) {
        userRepository.saveId(id);
    }
    public LiveData<String> getToastMessage() {
        return toastMessage;
    }  // UI reacts to LiveData by observing changes that occur to the LiveData
    public void setToastMessage(String message) {
        toastMessage.setValue(message);
    }
//==================================================================================================
//  CRUD functions
//==================================================================================================
    public void insertItem(Item item) {
        itemRepository.insertItem(item);
    }
    public LiveData<List<Item>> getItems() {
        items = itemRepository.getItems();
        return items;
    }
    public void editItem(Item item) {
        itemRepository.updateItem(item);
    }
    public void deleteItem(Item item) {
        itemRepository.deleteItem(item);
    }
//==================================================================================================
}