package com.appbuddy.inventorybuddy;

import android.app.AlertDialog;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.text.InputType;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.floatingactionbutton.ExtendedFloatingActionButton;

import java.util.ArrayList;
import java.util.List;

import dagger.hilt.android.AndroidEntryPoint;
@AndroidEntryPoint
public class InventoryFragment extends Fragment {
    // InventoryAdapters provide ViewHolders to hold View references and data (items) to the RecyclerView recycler_view
    private List<Item> items;
    private UserViewModel userViewModel;
    private ItemAdapter adapter;
    private RecyclerView recyclerView;
    private UserState userState;
    private ExtendedFloatingActionButton fabAdd;
    private String phoneNumber;
    private String itemName;
    private TextView textHint;
//==================================================================================================
//  Default Constructor
//==================================================================================================
    public InventoryFragment() {}
//==================================================================================================
//  Lifecycle Functions
//==================================================================================================
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        try {
            userViewModel = new ViewModelProvider(this).get(UserViewModel.class);
            items = new ArrayList<>();  // or List<Item> items = new ArrayList<>();
        } catch (Exception e) {
            Log.e("InventoryFragment: onCreate: ", "ViewModelProvider: " + e);
        }

        try {
            userState = UserState.DEFAULT_STATE;
            setUserState(UserState.DEFAULT_STATE);
        } catch (Exception e) {
            Log.e("LoginFragment", "Error in onCreate: setUserState call " + e);
        }
    }
//==================================================================================================
    /**
     * Called when fragment draws UI the first time
     *
     * @param inflater LayoutInflater inflates the layout defined in the XML file into the fragment's view
     * @param container ViewGroup container returned to attach fragment UI
     * @param savedInstanceState Bundle object containing the activity's previous state if it exists
     * @return View object representing the fragment's UI
     */
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // inflate fragment layout
        View view = inflater.inflate(R.layout.fragment_inventory, container, false);

        // find reference IDs
        fabAdd          = view.findViewById(R.id.fabAdd);
        textHint        = view.findViewById(R.id.textHint);
        recyclerView    = view.findViewById(R.id.recycler_view);

        return view;
    }
//==================================================================================================
    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        setupItemAdapter();

        // set recyclerView layout manager and adapter
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerView.setAdapter(adapter);
        // add divider between items
        recyclerView.addItemDecoration(new DividerItemDecoration(recyclerView.getContext(), DividerItemDecoration.VERTICAL));

        // LiveData observers
        userViewModel.getItems().observe(getViewLifecycleOwner(), items -> {
            if (items == null) return;
            this.items.clear();
            this.items.addAll(items);
            adapter.notifyDataSetChanged();  // replace with notifyItemInserted(), notifyItemRemoved(), or notifyItemChanged()
            textHint.setVisibility(items.isEmpty() ? View.VISIBLE : View.GONE);
        });

        userViewModel.getToastMessage().observe(getViewLifecycleOwner(), message -> {
            if (message == null) return;
            // show toast message
            Toast toast = Toast.makeText(getContext(), message, Toast.LENGTH_SHORT);
            // moves toast message up a little from default
            toast.setGravity(0, 0, 0);  // gravity: (center (0, 0), x offset, y offset)
            toast.show();
        });

        // listeners
        fabAdd.setOnClickListener(v -> insertItem());
    }
//==================================================================================================
// Custom Functions
//==================================================================================================
    public void setupItemAdapter() {
        adapter = new ItemAdapter(
                items,
                this::deleteItem,
                this::editItem
        );
    }
//==================================================================================================
    private void sendSmsMessage(String phoneNumber, String itemName) {
        try {
            //noinspection deprecation
            SmsManager smsManager = SmsManager.getDefault();  // .getDefault() deprecated and does not support multiple SIM cards
            String textMessage = itemName + " is low! Only 1 left!";
            smsManager.sendTextMessage(phoneNumber, null, textMessage, null, null);
            // TODO: update state to ACCEPTED_SMS with ViewModel LiveData or Repository method call, and observe in InventoryFragment
            Toast.makeText(getContext(), "SMS sent successfully", Toast.LENGTH_SHORT).show(); // SMS_SENT
        } catch (Exception e) {
            Toast.makeText(getContext(), "SMS failed to send", Toast.LENGTH_SHORT).show();
            Log.e("InventoryFragment: sendSmsMessage: ", "SMS failed to send"); // SMS_FAILED
        }
    }
//==================================================================================================
    public void insertItem() {
        Log.d("InventoryFragment", "insertItem() called");

        if (getContext() == null) return;

        AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
        builder.setTitle("Add Item");

        EditText editName = new EditText(getContext());
        editName.setHint("Item Name");
        editName.setInputType(InputType.TYPE_CLASS_TEXT);
        editName.setOnFocusChangeListener((v, hasFocus) -> {
            if (hasFocus) editName.selectAll();
        });

        EditText editQuantity = new EditText(getContext());
        editQuantity.setHint("Item Quantity");
        editQuantity.setInputType(InputType.TYPE_CLASS_NUMBER);
        editQuantity.setOnFocusChangeListener((v, hasFocus) -> {
            if (hasFocus) editQuantity.selectAll();
        });

        LinearLayout layout = new LinearLayout(getContext());
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.addView(editName);
        layout.addView(editQuantity);
        builder.setView(layout);

        builder.setPositiveButton("Add", (dialog, which) -> {
            String name = editName.getText().toString().trim();
            String quantityString = editQuantity.getText().toString().trim();
            if (name.isEmpty()) {
                Toast.makeText(getContext(), "Name is required!", Toast.LENGTH_SHORT).show();
                return;
            }
            if (quantityString.isEmpty()) {
                Toast.makeText(getContext(), "Quantity is required!", Toast.LENGTH_SHORT).show();
                return;
            }
            try {
                int quantity = Integer.parseInt(quantityString);
                Item item = new Item(name, quantity);
                userViewModel.insertItem(item);
                items.add(0, item);
                adapter.notifyItemInserted(0);
                recyclerView.smoothScrollToPosition(0);
                userState = UserState.ITEM_ADDED;
                userViewModel.setUserState(userState);
                userViewModel.setToastMessage("Item added.");
                textHint.setVisibility(items.isEmpty() ? View.VISIBLE : View.GONE);
            } catch (NumberFormatException e) {
                Toast.makeText(getContext(), "Invalid quantity!", Toast.LENGTH_SHORT).show();
            }
        });

        builder.setNegativeButton("Cancel", (dialog, which) -> dialog.cancel());
        builder.create().show();
    }
//==================================================================================================
    public void deleteItem(int adapterPosition) {
        Log.d("InventoryFragment", "deleteItem() called");

        if (getContext() == null) return;  // Prevents possible null pointer exception

        // Get the item name for confirmation message
        String itemName = items.get(adapterPosition).getName();

        // Create AlertDialog builder instance with current context
        AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
        builder.setTitle("Delete Item");
        // Confirmation message
        builder.setMessage("Are you sure you want to delete \"" + itemName + "\"?");

        // "Delete" button for confirmation
        builder.setPositiveButton("Delete", (dialog, which) -> {
            // Remove item from list
            items.remove(adapterPosition);
            // Notify adapter that item removed at position
            adapter.notifyItemRemoved(adapterPosition);
            // Show toast confirmation message
            userState = UserState.ITEM_DELETED;
            userViewModel.setUserState(userState);
            userViewModel.setToastMessage("Item deleted.");
        });

        // "Cancel" button to dismiss dialog
        builder.setNegativeButton("Cancel", (dialog, which) -> dialog.cancel());

        // Create and show AlertDialog
        builder.create().show();
    }
//==================================================================================================
    public void editItem(int adapterPosition) {
        // confirm editItem() called
        Log.d("InventoryFragment", "editItem() called");

        if (getContext() == null) return;  // prevents possible null pointer exception

        // create AlertDialog builder instance with current context
        AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
        builder.setTitle("Edit Item");

        // Item Name
        EditText editName = new EditText(getContext());
        editName.setHint("Item Name");
        editName.setInputType(InputType.TYPE_CLASS_TEXT);
        // set editName to existing item name
        editName.setText(items.get(adapterPosition).getName());
        // when editName is clicked, select all text
        editName.setOnFocusChangeListener((v, hasFocus) -> {
            if (hasFocus) editName.selectAll();
        });

        // Item Quantity
        EditText editQuantity = new EditText(getContext());
        editQuantity.setHint("Item Quantity");
        editQuantity.setInputType(InputType.TYPE_CLASS_NUMBER);
        // set editQuantity to existing item quantity
        editQuantity.setText(String.valueOf(items.get(adapterPosition).getQuantity()));

        // LinearLayout
        LinearLayout layout = new LinearLayout(getContext());
        layout.setOrientation(LinearLayout.VERTICAL);
        // add views to layout
        layout.addView(editName);
        layout.addView(editQuantity);
        // set layout to builder's view
        builder.setView(layout);

        // select text when one of the EditTexts is selected (and show keyboard)
        View.OnFocusChangeListener focusChangeListener = (v, hasFocus) -> {
            if (hasFocus) {
                EditText editText = (EditText) v;  // cast View to EditText
                // select all text after 200ms so keyboard is shown to prevent focus issues
                editText.postDelayed(editText::selectAll, 200);
            }
        };
        editName.setOnFocusChangeListener(focusChangeListener);
        editQuantity.setOnFocusChangeListener(focusChangeListener);

        // "Edit" button
        builder.setPositiveButton("Save", ((dialog, which) -> {
            String name = editName.getText().toString().trim();
            String quantityString = editQuantity.getText().toString().trim();
            if (!name.isEmpty() && !quantityString.isEmpty()) {
                try {
                    // convert String value to integer
                    int quantity = Integer.parseInt(quantityString);

                    // update item
                    items.get(adapterPosition).setName(name);
                    items.get(adapterPosition).setQuantity(quantity);
                    // notify adapter that item updated at position
                    adapter.notifyItemChanged(adapterPosition);
                    // show toast confirmation message
                    userState = UserState.ITEM_UPDATED;
                    userViewModel.setUserState(userState);
                    userViewModel.setToastMessage("Item updated.");  // TODO: change to LiveData in ViewModel

                    // check if item quantity is low (1 left) and send SMS if so if user allowed
                    if (quantity == 1) {
                        String smsPermission = userViewModel.fetchSmsPermission();
                        if ("allowed".equals(smsPermission)) {
                            phoneNumber = "(650) 555-1212"; // FIXME: getUserPhoneNumber()
                            itemName = items.get(adapterPosition).getName();
                            sendSmsMessage(phoneNumber, itemName);
                        }
                    }

                } catch (NumberFormatException e) {
                    Toast.makeText(getContext(), "Invalid quantity!", Toast.LENGTH_SHORT).show();
                }
            } else {
                Toast.makeText(getContext(), "Both fields required!", Toast.LENGTH_SHORT).show();
            }
        }));

        // "Cancel" button
        builder.setNegativeButton("Cancel", ((dialog, which) -> dialog.cancel())
        );

        // create and show AlertDialog
        builder.create().show();
    }
//==================================================================================================
    public UserState getUserState() {
        return userViewModel.getUserState();
    }
    public void setUserState(UserState userState) {
        userViewModel.setUserState(userState);
    }
//==================================================================================================
}