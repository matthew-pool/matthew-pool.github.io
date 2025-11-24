package com.appbuddy.inventorybuddy;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

// Adapters/ViewHolders manage data for views (RecyclerView) and binds data to these views
public class ItemAdapter extends RecyclerView.Adapter<ItemAdapter.ItemViewHolder> {
    private final List<Item> items;
    private final OnItemDeleteClickListener deleteClickListener;
    private final OnItemEditClickListener editClickListener;

    // Constructor
    public ItemAdapter(List<Item> items, OnItemDeleteClickListener deleteClickListener, OnItemEditClickListener editClickListener) {
        this.items = items;
        this.deleteClickListener = deleteClickListener;
        this.editClickListener = editClickListener;
    }

    @NonNull
    @Override
    public ItemViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.item, parent, false);
        return new ItemViewHolder(itemView);
    }

    // binds item data to UI elements for automatic UI updates when data changes
    @Override
    public void onBindViewHolder(@NonNull ItemViewHolder holder, int position) {
        Item item = items.get(holder.getBindingAdapterPosition());
        // binds data to Views
        holder.textName.setText(item.getName());
        holder.textQuantity.setText(String.valueOf(item.getQuantity()));
        holder.buttonDelete.setOnClickListener(v -> {
            int adapterPosition = holder.getBindingAdapterPosition();
            if (deleteClickListener != null && adapterPosition != RecyclerView.NO_POSITION) {
                deleteClickListener.onItemDeleteClicked(adapterPosition);
            }
        });
        holder.buttonEdit.setOnClickListener(v -> {
            int adapterPosition = holder.getBindingAdapterPosition();
            if (editClickListener != null && adapterPosition != RecyclerView.NO_POSITION) {
                editClickListener.onItemEditClicked(adapterPosition);
            }
        });
    }

    @Override
    public int getItemCount() {
        return items.size();
    }

    public static class ItemViewHolder extends RecyclerView.ViewHolder {
        private final TextView textName;
        private final TextView textQuantity;
        private final Button buttonDelete;
        private final Button buttonEdit;

        public ItemViewHolder(@NonNull View itemView) {
            super(itemView);
            textName = itemView.findViewById(R.id.textName);
            textQuantity = itemView.findViewById(R.id.textQuantity);
            buttonDelete = itemView.findViewById(R.id.buttonDelete);
            buttonEdit = itemView.findViewById(R.id.buttonEdit);
        }
    }
    public interface OnItemDeleteClickListener {
        void onItemDeleteClicked(int position);
    }
    public interface OnItemEditClickListener {
        void onItemEditClicked(int position);
    }
}