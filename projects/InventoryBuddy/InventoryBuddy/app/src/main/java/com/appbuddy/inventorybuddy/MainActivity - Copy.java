/**
 * Inventory Buddy v0.7: An app to help you keep track of your inventory
 * Author: AppBuddy (Matthew Pool)
 * Architecture: MVVM (Model-View-ViewModel) with Repository pattern
 * Database: Room
 * Initializes the app and sets the content view to the layout in activity_main.xml
 * Adds a new LoginFragment instance to the container
 * Avoids adding fragment again after config changes like screen rotation
 * Hilt annotation to enable dependency injection
 */
// :app module MainActivity.java
package com.appbuddy.inventorybuddy;

import android.os.Bundle;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.lifecycle.ViewModelProvider;

import java.util.Objects;

import dagger.hilt.android.AndroidEntryPoint;

// sets content view to the layout in activity_main.xml
// always loads LoginFragment into the fragment
@AndroidEntryPoint  // Hilt annotation to enable dependency injection
public class MainActivity extends AppCompatActivity {  // allows device compatibility
    private UserViewModel userViewModel;
//==================================================================================================
//  Lifecycle Functions
//==================================================================================================
    @Override  // overrides abstract class functions
    protected void onCreate(Bundle savedInstanceState) {  // called when activity is starting
        super.onCreate(savedInstanceState);  // initializes activity

        try {
            userViewModel = new ViewModelProvider(this).get(UserViewModel.class);
        } catch (Exception e) {
            Log.e("LoginFragment", "Error in onCreate: ViewModel initialization " + e);
        }

        try {
            userViewModel.setUserState(UserState.DEFAULT_STATE);
        } catch (Exception e) {
            Log.e("LoginFragment", "Error in onCreate: setUserState call " + e);
        }
    //==================================================================================================
    //  UI Layout
    //==================================================================================================
        // sets content view to layout in activity_main.xml
        setContentView(R.layout.activity_main);

        // Toolbar at top of all fragments
        Toolbar toolbar = findViewById(R.id.custom_toolbar);
        setSupportActionBar(toolbar);
        Objects.requireNonNull(getSupportActionBar()).setDisplayShowTitleEnabled(false);
    //==================================================================================================
    //  Preferences & Navigation
    //==================================================================================================
        // avoids adding fragment again after config changes like screen rotation
        if (savedInstanceState == null) {  // initial creation (not a screen rotation)
            // TODO: switch to Android Navigation Component

            // observers (none)

            // Initial navigation logic
            if ("allowed".equals(userViewModel.fetchSmsPermission())) {
                userViewModel.saveSmsPermission("allowed");
                goToInventoryFragment();  // user has logged in and accepted sms permission request

            } else if ("denied".equals(userViewModel.fetchSmsPermission())) {
                userViewModel.saveSmsPermission("denied");
                goToInventoryFragment();  // user has logged in but rejected (or touched outside) sms permission request

            } else {  // user has not yet responded to sms permission request
                goToLoginFragment();  // user must log in and accept/reject sms permission request
            }
        }
    }
//==================================================================================================
//  Custom Functions
//==================================================================================================
    /**
     * Adds a new LoginFragment instance to the container
     */
    private void goToLoginFragment() {
        try {
            getSupportFragmentManager().beginTransaction()
                    .replace(R.id.fragment_container, new LoginFragment())
                    .commit();
        } catch (Exception e) {
            Log.e("MainActivity.goToLoginFragment", "Error in goToLoginFragment: " + e);
        }
    }
//==================================================================================================
    /**
     * Adds a new InventoryFragment instance to the container
     */
    private void goToInventoryFragment() {
        try {
            getSupportFragmentManager().beginTransaction()
                    .replace(R.id.fragment_container, new InventoryFragment())
                    .commit();
        } catch (Exception e) {
            Log.e("MainActivity.goToInventoryFragment", "Error in goToInventoryFragment: " + e);
        }
    }
//==================================================================================================
}