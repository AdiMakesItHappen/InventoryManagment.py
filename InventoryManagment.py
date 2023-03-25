from tkinter import *
from tkinter import ttk
import mysql.connector
from PIL import ImageTk, Image
from tkinter import messagebox
import re

root = Tk()
root.title('Yvc Simulation Center Inventory management')
College_Logo = PhotoImage(file="CollegeLogo.png")
root.iconphoto(False, College_Logo)
root.configure(bg="light green")
root.resizable(width=False, height=False)


# func to show frame
def show_frame(frame):
    frame.tkraise()


parent_items_frame = Frame(root, bg="light green")
Login_Page = Frame(root, background='light green')

for frame in (
        Login_Page, parent_items_frame):
    frame.grid(row=0, column=0, sticky='nsew')


def check_logout():
    response = messagebox.askyesno("Logout?", "Do you want to Logout?")
    if response == 1:
        show_frame(Login_Page)
    else:
        return


# logout Menu
my_menu = Menu(root)
root.config(menu=my_menu)
logout_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="logout", menu=logout_menu)
logout_menu.add_command(label="logout", command=check_logout)

# Login Page -----------------------------------------------------------------------------------------------------------

show_frame(Login_Page)
my_canvas = Canvas(Login_Page, bd=0, highlightthickness=0)
my_canvas.pack(fill="both", expand=True)
global my_img
my_img = ImageTk.PhotoImage(Image.open("CollegeLogo.png"))

open_img = Image.open("green-bg4.jpg")
bg_resize_img = open_img.resize((900, 800), Image.ANTIALIAS)
bg = ImageTk.PhotoImage(bg_resize_img)

my_canvas.create_image(0, 0, image=bg, anchor='nw')
my_canvas.create_image(300, 100, image=my_img, anchor='nw')

my_canvas.create_text(430, 270, text='Yvc Simulation Center Inventory management', font=("Helvetica", 20), fill="black")
my_canvas.create_text(330, 350, text='User Name:', font=("Helvetica", 17), fill="black")
un_entry = Entry(Login_Page, font=(17), width=14, fg="#336d92", bd=0)
un_window = my_canvas.create_window(410, 340, anchor="nw", window=un_entry)
my_canvas.create_text(330, 400, text='Password:', font=("Helvetica", 17), fill="black")
pw_entry = Entry(Login_Page, font=(17), width=14, fg="#336d92", bd=0, show='*')
pw_window = my_canvas.create_window(410, 385, anchor="nw", window=pw_entry)


def validate_username_password():
    c.execute("SELECT * FROM users WHERE user_name = %s and password = %s ", (un_entry.get(), pw_entry.get()))
    result = c.fetchall()
    if (result != []):
        show_frame(parent_items_frame)
    else:
        messagebox.showerror("error entering", "Your username or Your password isn't correct")
    un_entry.delete(0, END)
    pw_entry.delete(0, END)


login_btn = Button(Login_Page, text='Login', font=(17), width=10, fg="#336d92", command=validate_username_password)
login_btn_window = my_canvas.create_window(380, 450, anchor="nw", window=login_btn)


def retrieve_items():
    # clear the Treeview
    for record in items_table.get_children():
        items_table.delete(record)

    conn = mysql.connector.connect(

        host='localhost',
        user="root",
        password='adi12345@4$!',
        database='items',

    )

    # Create cursor
    c = conn.cursor()
    c.execute("SELECT * FROM item")
    records = c.fetchall()

    #  Data From mysql
    global count
    count = 0
    for record in records:
        items_table.insert(parent='', index='end', iid=count, text="",
                           values=(record[0], record[1], record[2], record[3], record[4]))
        count += 1


def search_items():
    lookup_items = search_entry.get()

    # clear the Treeview
    for record in items_table.get_children():
        items_table.delete(record)

    conn = mysql.connector.connect(

        host='localhost',
        user="root",
        password='adi12345@4$!',
        database='items',

    )

    # Create cursor
    c = conn.cursor()
    if (re.search("\d", lookup_items)):
        c.execute("SELECT * FROM item WHERE item_id like %s %s ", (lookup_items, '%'))
    else:
        c.execute("SELECT * FROM item WHERE item_name like %s %s", (lookup_items, '%'))

    records = c.fetchall()

    if records:
        global count
        count = 0
        for record in records:
            items_table.insert(parent='', index='end', iid=count, text="",
                               values=(record[0], record[1], record[2], record[3], record[4]))
            count += 1

        conn.commit()
        c.close()

    else:
        messagebox.showerror("error search", "you are inserting wrong Item Name or Id")

    search_entry.delete(0, END)


my_label_image = Label(parent_items_frame, image=my_img, bg="light green")
my_label_image.pack(pady=(5, 0))

# Add some style
style = ttk.Style()

# Pick a theme
style.theme_use("clam")

# Configure our treeview colors
style.configure('Treeview', rowheight=30,
                background="#E0FFFF",
                fieldbackground="E0FFFF"
                )
# Change selected color
style.map('Treeview', background=[('selected', 'teal')])

# Search Frame
search_frame = Frame(parent_items_frame, background='light green')
search_frame.pack()

# Create Treeview Frame
items_frame = Frame(parent_items_frame, background='light green')
items_frame.pack()
# Search Label
search_item = LabelFrame(search_frame, text="Item Id/Item Name", bg="light green")
search_item.grid(row=0, column=0, padx=5, pady=5)

# Add Button
search_btn = Button(search_item, text="Search Item", command=search_items)
search_btn.grid(row=0, column=0, padx=5)

# Add entry box
global search_entry
search_entry = Entry(search_item, font=("Helventica", 18))
search_entry.grid(row=0, column=1, pady=5, padx=(0, 5))

search_btn = Button(search_item, text="Retrieve All Items", command=retrieve_items)
search_btn.grid(row=0, column=2, padx=5)

# Treeview Scrollbar
items_scroll = Scrollbar(items_frame)
items_scroll.pack(side=RIGHT, fill=Y)

# Create Treeview
global items_table
items_table = ttk.Treeview(items_frame, yscrollcommand=items_scroll.set)

# pack to screen
items_table.pack(pady=5)

# Configure the Scrollbar
items_scroll.config(command=items_table.yview)

# Define Our Columns
items_table['columns'] = ("Item ID", "Item Name", "Item Location", "Item description", "Item quantity")

# Formate Our Columns
# my_tree.column("#0", width=120, minwidth=25)

items_table.column("#0", width=0, stretch=NO)
items_table.column("Item ID", anchor=W, width=120)
items_table.column("Item Name", anchor=W, width=120)
items_table.column("Item Location", anchor=W, width=120)
items_table.column("Item description", anchor=W, width=300)
items_table.column("Item quantity", anchor=W, width=120)

# Creat Headings
items_table.heading("#0", text="", anchor=W)
items_table.heading("Item ID", text="Item ID", anchor=W)
items_table.heading("Item Name", text="Item Name", anchor=W)
items_table.heading("Item Location", text="Item Location", anchor=W)
items_table.heading("Item description", text="Item description", anchor=W)
items_table.heading("Item quantity", text="Item quantity", anchor=W)

conn = mysql.connector.connect(

    host='localhost',
    user="root",
    password='adi12345@4$!',
    database='items',

)

# Create cursor
c = conn.cursor()
c.execute("SELECT * FROM item")
records = c.fetchall()

#  Data From mysql
global count
count = 0
for record in records:
    items_table.insert(parent='', index='end', iid=count, text="",
                       values=(record[0], record[1], record[2], record[3], record[4]))
    count += 1

add_frame = Frame(parent_items_frame, bg="light green")
add_frame.pack(pady=10)


# Add Item Func
def add_item():
    if item_id_box.get() == "" and item_name_box.get() == "":
        messagebox.showerror("error", "you haven't entered: Item ID and Item Name")

    conn = mysql.connector.connect(

        host='localhost',
        user="root",
        password='adi12345@4$!',
        database='items',
    )

    # Create cursor
    c = conn.cursor()

    # check if item exist
    searched = item_id_box.get()
    LookUp_for = "SELECT * FROM item WHERE item_id = %s"
    data = (searched,)
    c.execute(LookUp_for, data)

    result_search_item = c.fetchone()

    if result_search_item:
        messagebox.showerror("error Item ID", "Item ID Already Exists")
        # clear boxes
        item_id_box.delete(0, END)
        item_name_box.delete(0, END)
        item_location_box.delete(0, END)
        item_description_box.delete(0, END)
        item_quantity_box.delete(0, END)
    else:
        # adding item to database
        insert_new_item = ('INSERT INTO item (item_id,item_name,item_location,item_description,quantity)'
                           'VALUES (%s, %s, %s, %s,%s)'
                           )
        data = (item_id_box.get(), item_name_box.get(), item_location_box.get(), item_description_box.get(),
                item_quantity_box.get())
        c.execute(insert_new_item, data)
        conn.commit()
        messagebox.showinfo("Add Item", "Item has been Added Successfully")
        c.close()

        global count
        items_table.insert(parent='', index='end', iid=count, text="", values=(
            item_id_box.get(), item_name_box.get(), item_location_box.get(), item_description_box.get(),
            item_quantity_box.get()))
        count += 1

        # clear boxes
        item_id_box.delete(0, END)
        item_name_box.delete(0, END)
        item_location_box.delete(0, END)
        item_description_box.delete(0, END)
        item_quantity_box.delete(0, END)


def delete_item_selected():
    conn = mysql.connector.connect(

        host='localhost',
        user="root",
        password='adi12345@4$!',
        database='items',
    )

    # Create cursor
    c = conn.cursor()

    item_selected = items_table.selection()
    item_selected_tree = items_table.item(item_selected[0])['values'][0]

    response = messagebox.askyesno("Delete Item ID", "Do You want to delete Item?")
    if response == 1:
        item_id_to_delete = "DELETE FROM item WHERE item_id = " + str(item_selected_tree)
        c.execute(item_id_to_delete)
        messagebox.showinfo("Item ID Deleted", "Item has been deleted")

    conn.commit()
    c.close()

    items_table.delete(item_selected)


def select_item():
    # clear boxes

    item_id_box.config(state='normal')

    item_id_box.delete(0, END)
    item_name_box.delete(0, END)
    item_location_box.delete(0, END)
    item_description_box.delete("1.0", "end")
    item_quantity_box.delete(0, END)

    # grab record number
    selected = items_table.focus()
    # Grab record values
    values = items_table.item(selected, 'values')

    # output to entry boxes

    item_id_box.insert(0, values[0])
    item_name_box.insert(0, values[1])
    item_location_box.insert(0, values[2])
    item_description_box.insert("1.0", values[3])
    item_quantity_box.insert(0, values[4])

    item_id_box.config(state='disabled')


def update_item():
    conn = mysql.connector.connect(

        host='localhost',
        user="root",
        password='adi12345@4$!',
        database='items',

    )

    # Create cursor
    c = conn.cursor()

    item_id = item_id_box.get()
    update_in_sql = "Update item SET item_id = %s, item_name =%s, item_location = %s, item_description = %s, quantity = %s WHERE item_id = " \
                    + item_id
    data = (
        item_id_box.get(), item_name_box.get(), item_location_box.get(), item_description_box.get(),
        item_quantity_box.get())

    c.execute(update_in_sql, data)
    conn.commit()

    # Grab record number
    selected = items_table.focus()
    # save new data
    items_table.item(selected, text='', values=(
        item_id_box.get(), item_name_box.get(), item_location_box.get(), item_description_box.get(),
        item_quantity_box.get()))

    # clear boxes
    item_id_box.config(state='normal')
    item_id_box.delete(0, END)
    item_name_box.delete(0, END)
    item_location_box.delete(0, END)
    item_description_box.delete(0, END)
    item_quantity_box.delete(0, END)

    messagebox.showinfo("Update Item", "Item has been updated Successfully")

    c.close()


def show_item_quantity_name():
    conn = mysql.connector.connect(

        host='localhost',
        user="root",
        password='adi12345@4$!',
        database='items',
    )

    # Create cursor
    c = conn.cursor()

    c.execute("SELECT quantity,item_name FROM item WHERE item_id = " + Item_Id_quantity_box.get())

    global result_quantity
    result_quantity = c.fetchone()
    c.close()


def calculate():
    conn = mysql.connector.connect(

        host='localhost',
        user="root",
        password='adi12345@4$!',
        database='items',
    )

    # Create cursor
    c = conn.cursor()

    global quantity_value
    quantity_value = items_table.item(selected_item, 'values')[4]

    global new_quantity
    selected = drop.get()
    if selected == 'choose to calculate':
        messagebox.showerror("error", "Hey! You forgot to pick a drop down selection")
    elif selected == 'add quantity':
        new_quantity = int(Item_Quantity_box.get()) + int(quantity_value)
    elif selected == 'subtract quantity':
        new_quantity = int(quantity_value) - int(Item_Quantity_box.get())

    update_quantity_in_sql = "Update item SET quantity = %s WHERE item_id = " \
                             + Id_value
    data = (new_quantity,)
    c.execute(update_quantity_in_sql, data)
    conn.commit()

    messagebox.showinfo("Update Item Quantity ", "Item Quantity has been Updated Successfully")

    global item_name_value
    item_name_value = items_table.item(selected_item, 'values')[1]
    global item_location_value
    item_location_value = items_table.item(selected_item, 'values')[2]
    global item_description_value

    item_description_value = items_table.item(selected_item, 'values')[3]

    items_table.item(selected_item, text='', values=(
        Id_value, item_name_value, item_location_value, item_description_value,
        new_quantity))

    c.close()


def clear():
    Item_Id_quantity_box.delete(0, END)
    Item_Quantity_box.delete(0, END)


def ckeck_selected_item():
    global selected_item
    selected_item = items_table.focus()

    if not selected_item:
        messagebox.showerror("error ", "Item not selected")
    else:
        item_quantity_page()


def item_quantity_page():
    quantity_page = Toplevel()
    College_Logo = PhotoImage(file="CollegeLogo.png")
    quantity_page.iconphoto(False, College_Logo)
    quantity_page.title('Update Item')
    quantity_page.geometry("600x500")
    quantity_page.configure(bg="light green")

    global quantity_frame
    quantity_frame = Frame(quantity_page)
    quantity_frame.pack(pady=5)
    quantity_frame.configure(bg="light green")

    my_label_image = Label(quantity_frame, image=my_img, bg="light green")
    my_label_image.grid(row=0, columnspan=4)

    First_title = Label(quantity_frame, text="Yvc Simulation Center Inventory management",
                        bg="light green",
                        font=('Times New Roman', 17, 'bold'), justify=CENTER, pady=20)
    First_title.grid(row=1, columnspan=4)

    Second_title = Label(quantity_frame, text="manage item quantity", bg="light green",
                         font=('Times New Roman', 17, 'underline'), pady=20)
    Second_title.grid(row=2, columnspan=4)

    Item_Id_label = Label(quantity_frame, text="Enter Item Id:", bg="light green",
                          font=('Times New Roman', 17), pady=10)
    Item_Id_label.grid(row=3, columnspan=2)

    Item_quantity_label = Label(quantity_frame, text="Enter Quantity:", bg="light green",
                                font=('Times New Roman', 17), pady=10)
    Item_quantity_label.grid(row=3, column=3)

    global Item_Id_quantity_box
    Item_Id_quantity_box = Entry(quantity_frame, width=20)
    Item_Id_quantity_box.grid(row=4, columnspan=2)

    global Item_Quantity_box
    quantity = IntVar()
    Item_Quantity_box = Entry(quantity_frame, textvariable=quantity, width=20)
    Item_Quantity_box.grid(row=4, column=3)

    global drop
    drop = ttk.Combobox(quantity_frame,
                        values=["choose to calculate", "add quantity", "subtract quantity"])
    drop.current(0)
    drop.grid(row=5, column=3, pady=(10, 0))

    Calculate_Save_btn = Button(quantity_frame, text='calculate and save',
                                command=calculate, fg="blue")
    Calculate_Save_btn.grid(row=6, column=3, pady=(10, 5))

    Back_btn = Button(quantity_frame, text='Back', command=quantity_page.destroy, fg="blue")
    Back_btn.grid(row=7, columnspan=4, ipadx=50, pady=10)

    global Id_value
    Id_value = items_table.item(selected_item, 'values')[0]
    Item_Id_quantity_box.insert(0, Id_value)

    Item_Id_quantity_box.config(state='disabled')

    quantity_page.mainloop()


# Labels
item_id_label = Label(add_frame, text="Item Id", bg="light green")
item_id_label.grid(row=0, column=0)

item_name_label = Label(add_frame, text="Item Name", bg="light green")
item_name_label.grid(row=0, column=1)

item_location_label = Label(add_frame, text="Item Location", bg="light green")
item_location_label.grid(row=0, column=2)

item_description_label = Label(add_frame, text="Item Description", bg="light green")
item_description_label.grid(row=2, column=0, pady=(10, 0))

item_quantity_label = Label(add_frame, text="Item Quantity", bg="light green")
item_quantity_label.grid(row=0, column=3)

# Entry Boxes
global item_id_box
item_id_box = Entry(add_frame)
item_id_box.grid(row=1, column=0)

global item_name_box
item_name_box = Entry(add_frame)
item_name_box.grid(row=1, column=1)

global item_location_box
item_location_box = Entry(add_frame)
item_location_box.grid(row=1, column=2)

global item_quantity_box
item_quantity_box = Entry(add_frame)
item_quantity_box.grid(row=1, column=3)
global item_description_box
item_description_box = Text(add_frame, height=5, width=30, font=17)
item_description_box.grid(row=2, column=1, columnspan=2, pady=(10, 0))

# Buttons

# add item
add_item_btn = Button(add_frame, text="Add Item", command=add_item)
add_item_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=5, ipadx=20)

# Update Item
update_item_btn = Button(add_frame, text="select Item to update", command=select_item)
update_item_btn.grid(row=3, column=1, columnspan=2, pady=10, padx=5)

# save update Item
save_updated_item = Button(add_frame, text="save Item updates ", command=update_item)
save_updated_item.grid(row=3, column=2, columnspan=2, pady=10, padx=5)

# delete Item

delete_item_btn = Button(add_frame, text="Delete Item Selected", command=delete_item_selected)
delete_item_btn.grid(row=4, column=2, columnspan=2, pady=10, padx=20)
delete_item_btn.configure(fg="red")
# button1.configure(bg="red", fg="yellow")

# Item quantity management
Item_quantity_management_btn = Button(add_frame, text='manage item quantity', command=ckeck_selected_item)
Item_quantity_management_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=20)
Item_quantity_management_btn.configure(fg="green")

root.mainloop()
