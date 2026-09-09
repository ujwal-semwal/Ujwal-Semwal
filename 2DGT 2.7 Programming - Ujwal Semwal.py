import random
import datetime
import tkinter as tk
from tkinter import messagebox

# Standard setup values
MAX_BOX = 25
MIN_QTY = 1
MAX_QTY = 500
DATE_HINT = "DD/MM/YYYY"

# Main data lists
hire_list = []
raffle_list = []


def calculate_boxes(qty):
    # Calculates how many boxes are needed
    return (qty + MAX_BOX - 1) // MAX_BOX


def validate_inputs(name, receipt, item, qty_str, start_date, return_date):
    # Check for empty entries or placeholders
    if not (name.strip() and receipt.strip() and item.strip() and 
            qty_str.strip() and start_date.strip() and return_date.strip()):
        return False, "All fields are required."

    if start_date == DATE_HINT or return_date == DATE_HINT:
        return False, "Please enter valid dates."

    # Name validation
    if not name.replace(" ", "").isalpha():
        return False, "Name must contain only letters."

    # Quantity validation
    try:
        qty = int(qty_str)
        if qty < MIN_QTY or qty > MAX_QTY:
            return False, f"Quantity must be between {MIN_QTY} and {MAX_QTY}."
    except ValueError:
        return False, "Quantity must be a whole number."

    # Date validation
    for d_str, label in [(start_date, "Start Date"), (return_date, "Return Date")]:
        try:
            datetime.datetime.strptime(d_str, "%d/%m/%Y")
        except ValueError:
            return False, f"Invalid {label}. Use DD/MM/YYYY format."

    return True, qty


# Placeholder functions
def add_placeholder(entry):
    entry.insert(0, DATE_HINT)
    entry.config(fg="grey")


def on_focus_in(event, entry):
    if entry.get() == DATE_HINT:
        entry.delete(0, tk.END)
        entry.config(fg="black")


def on_focus_out(event, entry):
    if not entry.get().strip():
        add_placeholder(entry)


# Button actions
def add_hire():
    name = entry_name.get()
    receipt = entry_receipt.get()
    item = entry_item.get()
    qty_str = entry_quantity.get()
    start_date = entry_start.get()
    return_date = entry_return.get()

    is_valid, result = validate_inputs(name, receipt, item, qty_str, start_date, return_date)

    if not is_valid:
        messagebox.showerror("Error", result)
        return

    qty = result
    boxes = calculate_boxes(qty)
    raffle_num = random.randint(1, 1000)

    # Store in lists
    hire_list.append([name.strip(), receipt.strip(), item.strip(), qty, start_date.strip(), return_date.strip(), boxes])
    raffle_list.append([name.strip(), raffle_num])

    update_display()
    clear_entries()
    messagebox.showinfo("Success", f"Item added! Raffle Ticket: #{raffle_num}")


def delete_hire():
    selected = listbox_hires.curselection()

    if not selected:
        messagebox.showerror("Error", "Please select an item to delete.")
        return

    index = selected[0]
    
    # Delete from BOTH lists so terminal matches GUI
    del hire_list[index]
    del raffle_list[index]

    update_display()
    messagebox.showinfo("Success", "Record deleted.")


def update_display():
    listbox_hires.delete(0, tk.END)
    for row in hire_list:
        info = f"Name: {row[0]} | Receipt: {row[1]} | Item: {row[2]} (x{row[3]}) | Out: {row[4]} | Return: {row[5]} | Boxes: {row[6]}"
        listbox_hires.insert(tk.END, info)


def print_raffle_list():
    print("\n--- JULIE'S PARTY HIRE RAFFLE LIST ---")
    if not raffle_list:
        print("No raffle entries yet.")
    else:
        for item in raffle_list:
            print(f"Customer: {item[0]} | Ticket: #{item[1]}")
    print("--------------------------------------\n")


def clear_entries():
    entry_name.delete(0, tk.END)
    entry_receipt.delete(0, tk.END)
    entry_item.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    
    entry_start.delete(0, tk.END)
    add_placeholder(entry_start)
    
    entry_return.delete(0, tk.END)
    add_placeholder(entry_return)


# GUI Setup
root = tk.Tk()
root.title("Julie's Party Hire Tracking System")
root.geometry("800x680")

# Form Inputs
tk.Label(root, text="Customer Full Name:").pack(pady=(5, 0))
entry_name = tk.Entry(root, width=40)
entry_name.pack()

tk.Label(root, text="Receipt Number:").pack(pady=(5, 0))
entry_receipt = tk.Entry(root, width=40)
entry_receipt.pack()

tk.Label(root, text="Item Hired:").pack(pady=(5, 0))
entry_item = tk.Entry(root, width=40)
entry_item.pack()

tk.Label(root, text=f"Quantity ({MIN_QTY}-{MAX_QTY}):").pack(pady=(5, 0))
entry_quantity = tk.Entry(root, width=40)
entry_quantity.pack()

tk.Label(root, text="Date Hired From:").pack(pady=(5, 0))
entry_start = tk.Entry(root, width=40)
add_placeholder(entry_start)
entry_start.bind("<FocusIn>", lambda e: on_focus_in(e, entry_start))
entry_start.bind("<FocusOut>", lambda e: on_focus_out(e, entry_start))
entry_start.pack()

tk.Label(root, text="Return Date:").pack(pady=(5, 0))
entry_return = tk.Entry(root, width=40)
add_placeholder(entry_return)
entry_return.bind("<FocusIn>", lambda e: on_focus_in(e, entry_return))
entry_return.bind("<FocusOut>", lambda e: on_focus_out(e, entry_return))
entry_return.pack()

# Add Button
btn_add = tk.Button(root, text="Add Hire Record", command=add_hire, width=20)
btn_add.pack(pady=10)

# Display Listbox Frame with Scrollbars
tk.Label(root, text="Current Hires Out:").pack()

list_frame = tk.Frame(root)
list_frame.pack(padx=10, pady=5)

v_scroll = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

h_scroll = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

listbox_hires = tk.Listbox(
    list_frame, 
    width=90, 
    height=10, 
    yscrollcommand=v_scroll.set, 
    xscrollcommand=h_scroll.set
)
listbox_hires.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

v_scroll.config(command=listbox_hires.yview)
h_scroll.config(command=listbox_hires.xview)

# Management Buttons
btn_delete = tk.Button(root, text="Delete Selected Hire", command=delete_hire, width=20)
btn_delete.pack(pady=5)

btn_print_raffle = tk.Button(root, text="Print Raffle List to Console", command=print_raffle_list, width=25)
btn_print_raffle.pack(pady=5)

if __name__ == "__main__":
    root.mainloop()