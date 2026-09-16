import datetime
import tkinter as tk
from tkinter import messagebox

# These numbers and text limits stay the same so the gui runs according to the requirements
MIN_QTY = 1
MAX_QTY = 500
DATE_HINT = "DD/MM/YYYY"

# This main list holds all the saved hire records in one place as a 2D list
hire_list = []

def validate_inputs(name, receipt, item, qty_text, start_date, return_date):
    # this function checks the validity of inputs to make sure no fields are left blank
    if not name or not receipt or not item or not qty_text or not start_date or not return_date:
        return False, "All fields must be filled in."

    # this function checks the validity of date fields to make sure default placeholders are replaced
    if start_date == DATE_HINT or return_date == DATE_HINT:
        return False, "Please enter actual dates, not placeholders."

    # this function checks the validity of the customer name so it only contains letters and spaces
    if not name.replace(" ", "").isalpha():
        return False, "Customer name can only contain letters."

    # this function checks the validity of the receipt number so it only contains numbers
    if not receipt.isdigit():
        return False, "Receipt number must be numbers only."

    # this function checks the validity of the quantity so it is a whole number within limits
    if not qty_text.isdigit():
        return False, "Quantity must be a valid whole number."

    quantity = int(qty_text)
    if quantity < MIN_QTY or quantity > MAX_QTY:
        return False, f"Quantity must be between {MIN_QTY} and {MAX_QTY}."

    # this function checks the validity of dates for correct format and logical timeline order
    try:
        start_dt = datetime.datetime.strptime(start_date, "%d/%m/%Y")
        return_dt = datetime.datetime.strptime(return_date, "%d/%m/%Y")
    except ValueError:
        return False, "Dates must follow DD/MM/YYYY format."

    # this function checks the validity of the return date so it is not before the hire date
    if return_dt < start_dt:
        return False, "Return date cannot be before hire start date."

    return True, quantity


def set_placeholder(entry_box):
    # this function puts the default placeholder text inside the date entry box in grey
    entry_box.insert(0, DATE_HINT)
    entry_box.config(fg="grey")


def clear_placeholder(event, entry_box):
    # this function clears the placeholder text when the user clicks inside the entry box
    if entry_box.get() == DATE_HINT:
        entry_box.delete(0, tk.END)
        entry_box.config(fg="black")


def restore_placeholder(event, entry_box):
    # this function brings back the placeholder text if the entry box is left empty
    if not entry_box.get().strip():
        set_placeholder(entry_box)


def add_hire_record():
    # this function gets all string values entered into the gui entry boxes
    name = entry_name.get().strip()
    receipt = entry_receipt.get().strip()
    item = entry_item.get().strip()
    qty_text = entry_quantity.get().strip()
    start_date = entry_start.get().strip()
    return_date = entry_return.get().strip()

    # this function runs the validation subroutine and checks if inputs passed validity
    is_valid, result = validate_inputs(name, receipt, item, qty_text, start_date, return_date)

    if not is_valid:
        messagebox.showerror("Input Error", result)
        return

    quantity = result

    # this function appends a new list item into the main 2D hire list collection
    hire_list.append([name, receipt, item, quantity, start_date, return_date])

    # this function updates the listbox output and clears the input form
    refresh_display()
    clear_form()
    messagebox.showinfo("Success", "Hire record added successfully!")


def delete_hire_record():
    # this function gets the selected index from listbox and removes it from the 2D hire list
    selected = listbox_hires.curselection()

    if not selected:
        messagebox.showerror("Selection Error", "Please select a record from the list to delete.")
        return

    index = selected[0]
    del hire_list[index]

    # this function refreshes the listbox display after removing the selected item
    refresh_display()
    messagebox.showinfo("Success", "Record deleted successfully.")


def refresh_display():
    # this function clears the listbox and loops through the 2D hire list to display formatted records
    listbox_hires.delete(0, tk.END)
    for row in hire_list:
        display_string = f"Name: {row[0]} | Receipt #: {row[1]} | Item: {row[2]} | Qty: {row[3]} | Start: {row[4]} | Return: {row[5]}"
        listbox_hires.insert(tk.END, display_string)


def clear_form():
    # this function resets all text entry boxes back to blank or default placeholders
    entry_name.delete(0, tk.END)
    entry_receipt.delete(0, tk.END)
    entry_item.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)

    entry_start.delete(0, tk.END)
    set_placeholder(entry_start)

    entry_return.delete(0, tk.END)
    set_placeholder(entry_return)


def close_application():
    # this function closes and destroys the main tkinter window
    root.destroy()

# this sets up the main tkinter GUI window size and background colour
root = tk.Tk()
root.title("Julie's Party Hire Tracking System")
root.geometry("800x620")
root.configure(bg="#eef2f5")

# this creates the top main heading label with custom text size and colors
lbl_title = tk.Label(root, text="Julie's Party Hire Tracking System", font=("Helvetica", 18, "bold"), bg="#eef2f5", fg="#2c3e50")
lbl_title.pack(pady=10)

# this creates the label and text entry box for the customer full name
tk.Label(root, text="Customer Full Name:", font=("Helvetica", 10, "bold"), bg="#eef2f5").pack(pady=(4, 0))
entry_name = tk.Entry(root, width=40)
entry_name.pack(pady=2)

# this creates the label and text entry box for the receipt number
tk.Label(root, text="Receipt Number:", font=("Helvetica", 10, "bold"), bg="#eef2f5").pack(pady=(4, 0))
entry_receipt = tk.Entry(root, width=40)
entry_receipt.pack(pady=2)

# this creates the label and text entry box for the hired item name
tk.Label(root, text="Item Hired:", font=("Helvetica", 10, "bold"), bg="#eef2f5").pack(pady=(4, 0))
entry_item = tk.Entry(root, width=40)
entry_item.pack(pady=2)

# this creates the label and text entry box for quantity with boundary values shown
tk.Label(root, text=f"Quantity ({MIN_QTY}-{MAX_QTY}):", font=("Helvetica", 10, "bold"), bg="#eef2f5").pack(pady=(4, 0))
entry_quantity = tk.Entry(root, width=40)
entry_quantity.pack(pady=2)

# this creates the start date box and listens for when the customer clicks it
tk.Label(root, text="Date Hired From:", font=("Helvetica", 10, "bold"), bg="#eef2f5").pack(pady=(4, 0))
entry_start = tk.Entry(root, width=40)
set_placeholder(entry_start)
entry_start.bind("<FocusIn>", lambda event: clear_placeholder(event, entry_start))
entry_start.bind("<FocusOut>", lambda event: restore_placeholder(event, entry_start))
entry_start.pack(pady=2)

# this creates the return date entry field and listens for when the customer clicks it
tk.Label(root, text="Return Date:", font=("Helvetica", 10, "bold"), bg="#eef2f5").pack(pady=(4, 0))
entry_return = tk.Entry(root, width=40)
set_placeholder(entry_return)
entry_return.bind("<FocusIn>", lambda event: clear_placeholder(event, entry_return))
entry_return.bind("<FocusOut>", lambda event: restore_placeholder(event, entry_return))
entry_return.pack(pady=2)

# this creates the button that triggers the add record function when clicked
btn_add = tk.Button(root, text="Add Hire Record", command=add_hire_record, bg="#27ae60", fg="white", font=("Helvetica", 10, "bold"), width=22)
btn_add.pack(pady=10)

# this creates the section label for the saved items output display
tk.Label(root, text="Current Hires Out:", font=("Helvetica", 11, "bold"), bg="#eef2f5").pack()

# this creates a container frame to hold the listbox and its scrollbars together
list_frame = tk.Frame(root, bg="#eef2f5")
list_frame.pack(padx=10, pady=5)

# this creates vertical and horizontal scrollbars for navigating long data entries
v_scroll = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

h_scroll = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

# this creates the listbox widget where saved hire records are displayed
listbox_hires = tk.Listbox(list_frame, width=85, height=6, font=("Courier", 9), yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
listbox_hires.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# this links the scrollbars directly to the listbox view
v_scroll.config(command=listbox_hires.yview)
h_scroll.config(command=listbox_hires.xview)

# this creates the button that deletes the selected row from the listbox
btn_delete = tk.Button(root, text="Delete Selected Hire", command=delete_hire_record, bg="#e67e22", fg="white", font=("Helvetica", 10, "bold"), width=22)
btn_delete.pack(pady=4)

# this creates the exit button to close down the application
btn_exit = tk.Button(root, text="Exit / Close", command=close_application, bg="#7f8c8d", fg="white", font=("Helvetica", 10, "bold"), width=22)
btn_exit.pack(pady=4)

# this starts the main tkinter event loop to keep the gui running and listening for user actions
root.mainloop() 
