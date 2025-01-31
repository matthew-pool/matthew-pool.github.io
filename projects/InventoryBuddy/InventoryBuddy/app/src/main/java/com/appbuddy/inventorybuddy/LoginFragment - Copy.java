// :feature:login module LoginFragment.java
// Login Architecture: Model-View-ViewModel (MVVM) with Repository pattern
package com.appbuddy.inventorybuddy;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import dagger.hilt.android.AndroidEntryPoint;
// Fragments ("Screen" View): observe data and update UI elements accordingly
@AndroidEntryPoint  // used for Activities, Fragments, Views, and Services
public class LoginFragment extends Fragment {
    private UserState userState;  // = getUserState();
    private UserViewModel userViewModel;
    private EditText editUsername, editPassword;
    // TODO: private TextView textForgotPassword, textForgotUsername;
    private String username, password;
    private Button buttonSubmit;
//==================================================================================================
//  Constructors
//==================================================================================================
    public LoginFragment() {}
//==================================================================================================
//  TextWatcher
//==================================================================================================
    // TextWatcher to enable "Submit" button when both username and password fields have text
    private final TextWatcher textWatcher = new TextWatcher() {
        @Override
        public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            // required override
        }
        @Override
        public void onTextChanged(CharSequence s, int start, int before, int count) {
            // required override
        }
        @Override
        public void afterTextChanged(Editable s) {
            // enable buttonSubmit if username and password fields both have text
            boolean usernameHasText = !editUsername.getText().toString().trim().isEmpty();  // !isEmpty ensures text is not just whitespace
            boolean passwordHasText = !editPassword.getText().toString().trim().isEmpty();
            buttonSubmit.setEnabled(usernameHasText && passwordHasText);
        }
    };
//==================================================================================================\
//  Lifecycle Functions
//==================================================================================================
    /**
     * Called when fragment is first created
     *
     * @param savedInstanceState state saved if fragment is being re-created from a previous state
     */
    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        try {
            userViewModel = new ViewModelProvider(this).get(UserViewModel.class);
        } catch (Exception e) {
            Log.e("LoginFragment", "Error in onCreate: ViewModel initialization " + e);
        }

        try {
            userState = getUserState();  // null to DEFAULT_STATE
        } catch (Exception e) {
            Log.e("LoginFragment", "Error in onCreate: getUserState call " + e);
        }
    }
//==================================================================================================
    /**
     * Called when fragment draws UI the first time
     * Inflates the fragment's layout and initializes UI view elements
     *
     * @param inflater           LayoutInflater inflates the layout defined in the XML file into the fragment's view
     * @param container          ViewGroup container returned to attach fragment UI
     * @param savedInstanceState Bundle object containing the activity's previous state if it exists
     * @return View object representing the fragment's UI
     */
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // inflate fragment layout
        View view = inflater.inflate(R.layout.fragment_login, container, false);
        // get resource reference IDs
        editUsername = view.findViewById(R.id.editUsername);
        editPassword = view.findViewById(R.id.editPassword);
        // TODO: get reference IDs for textForgotPassword, textForgotUsername
        buttonSubmit = view.findViewById(R.id.buttonSubmit);
        buttonSubmit.setEnabled(false);  // disable Submit button initially
        // text change listeners
        editUsername.addTextChangedListener(textWatcher);
        editPassword.addTextChangedListener(textWatcher);

        return view;
    }
//==================================================================================================
    /**
     * Called after onCreateView() and ensures that the fragment's view is non-null
     * Receives view hierarchy and final initialization like listeners, observations, and interaction logic
     *
     * @param view               View object representing the fragment's UI
     * @param savedInstanceState Bundle object containing the activity's previous state if it exists
     */
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

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
        // TODO: set up OnClickListeners for "Forgot Password", "Forgot Username", and "Sign Up" text views
        buttonSubmit.setOnClickListener(v -> {
            if (getContext() == null) return;  // prevents possible null pointer exception
            // TODO: regex input validation
            username = editUsername.getText().toString().trim();
            password = editPassword.getText().toString().trim();

            loginUser(username, password);

            userState = getUserState();

            if (userState == UserState.LOGIN_SUCCESS || userState == UserState.SIGNUP_SUCCESS)
                goToPermissionsFragment();
            // else stay on LoginFragment
        });
    }
//==================================================================================================
    // Called when fragment is destroyed
    public void onDestroyView() {
        super.onDestroyView();
        // remove listeners
        editUsername.removeTextChangedListener(textWatcher);
        editPassword.removeTextChangedListener(textWatcher);
        buttonSubmit.setOnClickListener(null);
        // destroy references
        editUsername = null;
        editPassword = null;
        buttonSubmit = null;
    }
//==================================================================================================
//  Custom Functions
//==================================================================================================
    public void goToPermissionsFragment() {
        try {
            requireActivity().getSupportFragmentManager().beginTransaction()
                    .replace(R.id.fragment_container, new PermissionsFragment())  // replaces LoginFragment with PermissionsFragment
                    .commit();
        } catch (Exception e) {
            Log.e("LoginFragment", "Error navigating to PermissionsFragment: " + e);
        }
    }
//==================================================================================================
    /**
     * Initiates login process
     *
     * @param username entered by user
     * @param password entered by user
     */
    public void loginUser(String username, String password) {
        try {
            userViewModel.loginUser(username, password);
        }
        catch (Exception e) {
            Log.e("LoginFragment", "userViewModel.loginUser: " + e);
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