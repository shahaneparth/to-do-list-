rimport tkinter as tk
import sqlite3

def create_table():
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)''')
    conn.commit()
    conn.close()

def insert_record():
    name = name_entry.get()
    age = age_entry.get()
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute("INSERT INTO records (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()
    refresh_list()

def update_record():
    selected_item = listbox.curselection()
    if selected_item:
        selected_item = selected_item[0]
        new_name = name_entry.get()
        new_age = age_entry.get()
        conn = sqlite3.connect('records.db')
        c = conn.cursor()
        record_id = listbox.get(selected_item).split(':')[0]
        c.execute("UPDATE records SET name=?, age=? WHERE id=?", (new_name, new_age, record_id))
        conn.commit()
        conn.close()
        refresh_list()

def delete_record():
    selected_item = listbox.curselection()
    if selected_item:
        selected_item = selected_item[0]
        conn = sqlite3.connect('records.db')
        c = conn.cursor()
        record_id = listbox.get(selected_item).split(':')[0]
        c.execute("DELETE FROM records WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        refresh_list()

def refresh_list():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute("SELECT * FROM records")
    records = c.fetchall()
    for record in records:
        listbox.insert(tk.END, f"{record[0]}: {record[1]}, {record[2]} years old")
    conn.close()
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)

# Create the GUI window
root = tk.Tk()
root.title("Record Management")

# Create and set up the database
create_table()

# Create input fields and labels
name_label = tk.Label(root, text="Name:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

age_label = tk.Label(root, text="Age:")
age_label.pack()
age_entry = tk.Entry(root)
age_entry.pack()

# Create buttons
insert_button = tk.Button(root, text="Insert Record", command=insert_record)
insert_button.pack()

update_button = tk.Button(root, text="Update Record", command=update_record)
update_button.pack()

delete_button = tk.Button(root, text="Delete Record", command=delete_record)
delete_button.pack()

# Create a listbox to display records
listbox = tk.Listbox(root, selectmode=tk.SINGLE)
listbox.pack()

# Populate the listbox initially
refresh_list()

# Start the main GUI loop
root.mainloop()