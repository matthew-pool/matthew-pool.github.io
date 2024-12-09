package com.appbuddy.inventorybuddy;

import android.Manifest;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import dagger.hilt.android.AndroidEntryPoint;
//==================================================================================================
@AndroidEntryPoint
public class PermissionsFragment extends Fragment {
    private UserViewModel userViewModel;
    private ActivityResultLauncher<String> requestPermissionLauncher;
    private Button buttonNext;

//==================================================================================================
//  Constructors
//==================================================================================================
    public PermissionsFragment() {}
//==================================================================================================
//  Lifecycle Functions
//==================================================================================================
    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        try {
            userViewModel = new ViewModelProvider(this).get(UserViewModel.class);
        } catch (Exception e) {
            Log.e("PermissionsFragment", "Error in onCreate: ViewModel initialization " + e);
        }
        try {
            // request permission launcher initialization
            requestPermissionLauncher =
                    registerForActivityResult(new ActivityResultContracts.RequestPermission(), isGranted -> {
                        if (isGranted) {
                            setUserState(UserState.ACCEPTED_SMS);
                            userViewModel.saveSmsPermission("allowed");
                        } else {
                            setUserState(UserState.REJECTED_SMS);
                            userViewModel.saveSmsPermission("denied");
                        }
                        goToInventoryFragment();
                    });
        } catch (Exception e) {
            Log.e("PermissionsFragment", "Error in onCreate: requestPermissionLauncher initialization " + e);
        }
    }
//==================================================================================================
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // inflate fragment layout
        View view = inflater.inflate(R.layout.fragment_permissions, container, false);
        // get resource reference ids
        buttonNext = view.findViewById(R.id.buttonNext);

        return view;
    }
//==================================================================================================
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        // TODO: implement wrapper for LiveData to handle one-time events like toasts
        // LiveData observers
        userViewModel.getToastMessage().observe(getViewLifecycleOwner(), message -> {
            if (message == null) return;
            // show toast message
            Toast toast = Toast.makeText(getContext(), message, Toast.LENGTH_SHORT);
            // moves toast message up a little from default
            toast.setGravity(0, 0, 0);  // gravity: (center (0, 0), x offset, y offset)
            toast.show();
        });

        // listeners
        buttonNext.setOnClickListener(v -> {
            if (getContext() == null) return;  // prevents possible null pointer exception
            requestPermissionLauncher.launch(Manifest.permission.SEND_SMS);
        });
    }
//==================================================================================================
    /**
     * Called when fragment is destroyed
     */
    public void onDestroyView() {
        super.onDestroyView();
        // remove listeners
        buttonNext.setOnClickListener(null);
        // destroy references
        buttonNext = null;
    }
    //==================================================================================================
    public void goToInventoryFragment() {
        try {
            requireActivity().getSupportFragmentManager().beginTransaction()
                    .replace(R.id.fragment_container, new InventoryFragment())  // replaces LoginFragment with InventoryFragment
                    .commit();
        } catch (Exception e) {
            Log.e("PermissionsFragment", "Error navigating to InventoryFragment: " + e);
        }
    }
//==================================================================================================
//  Getters & Setters
//==================================================================================================
    public UserState getUserState() {
        return userViewModel.getUserState();
    }
    public void setUserState(UserState userState) {
            userViewModel.setUserState(userState);
    }
//==================================================================================================
}