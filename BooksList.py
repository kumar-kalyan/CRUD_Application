from tkinter import Tk,Button, Label, Scrollbar,Listbox,StringVar,Entry,W,S,E,N,END
from tkinter import ttk
from tkinter import messagebox
from sql_server_config import dbconfig #from sql_server_configfile fetching dictionary
import pypyodbc as pyodbc

con = pyodbc.connect(**dbconfig) #** means passing the content from dictionary
#print(con)

#ceating a cursor object
cursor =con.cursor()



class Bookdb :

    def __init__(self):
        #super(Bookdb, self).__init__()
        self.con = pyodbc.connect(**dbconfig)
        self.cursor = con.cursor()
        print("You have connected to the server successfully")
        print(con)
    def __del__(self)    :
        self.con.close()

    def view(self):
        self.cursor.execute("SELECT * from books")
        rows = self.cursor.fetchall()
        return rows
#adding books to the database
    def insert(self, title, author, isbn) :
        sql = ("INSERT INTO books(title, author, isbn)VALUES (?, ?, ?) ")
        values= [title, author, isbn]

        self.cursor.execute(sql, values)
        #con.comit()
        #self.con.comit()
        messagebox.showinfo(title="Books Database", message="New book added to the Database")

#updating books data into the database
    def update(self, id, title, author, isbn):
        tsql = 'UPDATE  books SET title = ?, author = ?, isbn = ? Where id=?'
        self.cursor.execute(tsql, [title, author, isbn, id])
        self.con.comit()
        messagebox.showinfo(title="Books Database", message="Book Updated to the Database")

#deleting records from Database
    def delete (self, id) :
        delquery = 'DELETE FROM books WHERE id = ?'
        self.cursor.execute(delquery, [id])
        self.con.comit()
        messagebox.showinfo(title="Books Database", message="Book Deleted")

#database object
dataBase = Bookdb()

def get_selected_row(event):
    global selected_tuple
    index = list_bx.curselection()[0]
    selected_tuple = list_bx.get(index)
    title_entry.delete(0, 'end')
    title_entry,insert('end', selected_tuple[1])
    author_entry.delete(0, 'end')
    author_entry,insert('end', selected_tuple[2])
    isbn_entry.delete(0, 'end')
    isbn_entry.insert('end', selected_tuple[3])

def view_record() :
    list_bx.delete(0, 'end')
    for row in dataBase.view():
        list_bx.insert('end', row)

def add_book():
    print(title_text.get())
    dataBase.insert(title_text.get(), author_text.get(), isbn_text.get())
    list_bx.delete(0, 'end')
    list_bx.insert('end', (title_text.get(), author.get(), isbn.get() ))
    title_entry.delete(0, 'end') #clearing nput after inserting them
    author_entry.delete(0, 'end')
    isbn_entry.delete(0, 'end')
    con.comit()

def delete_record():
    dataBase.delete(selected_tuple[0])
    con.commit()

def clear_screen():
    list_bx.delete(0, 'end')
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0, 'end')


def update_records():
    if messagebox.askokcancel("Quit", "Do you really want to Quit") :
        dataBase.update(selected_tuple[0], title_text.get(), author.get(), isbn.get())
        title_entry.delete(0, 'end')
        author_entry.delete(0, 'end')
        isbn_entry.delete(0, 'end')
    con.comit()

def On_exit():
    dd=dataBase
    root.destroy()
    del dd




root = Tk()
#App GUI
root.title("Books i have Progressed till now")
root.configure(background="Turquoise")
root.geometry("1000x500")
root.resizable(width='True', height='False')

#Title input box
title_lable = ttk.Label(root, text= "Title", background= "Turquoise",font=("TkDefaultFont", 16))
title_lable.grid(row=0,column=0,sticky=W)
title_text = StringVar()
title_entry = ttk.Entry(root, width=24,textvariable=title_text)
title_entry.grid(row=0, column=1, sticky=W)

#Author input box
author_lable = ttk.Label(root, text= "Author", background= "Turquoise",font=("TkDefaultFont", 14))
author_lable.grid(row=0,column=2,sticky=W)
author_text = StringVar()
author_entry = ttk.Entry(root, width=24,textvariable=author_text)
author_entry.grid(row=0, column=3, sticky=W)

#detail input box
isbn_lable = ttk.Label(root, text= "Details", background= "Turquoise",font=("TkDefaultFont", 12))
isbn_lable.grid(row=0,column=4,sticky=W)
isbn_text = StringVar()
isbn_entry = ttk.Entry(root, width=24,textvariable=isbn_text)
isbn_entry.grid(row=0, column=5, sticky=W)

#Add Books Button
add_btn = Button(root , text = "Add Books", bg="Blue", fg="white", command=add_book)
add_btn.grid(row =0 , column=8, sticky=W)

#listbox creation
list_bx = Listbox(root, height = 16, width=60, bg="light blue")
list_bx.grid(row=3, column=1, columnspan = 12, sticky = W+E, pady=40,padx=15)

scroll_bar =Scrollbar(root)
scroll_bar.grid(row=1,column=10,rowspan=13,sticky = W)

list_bx.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_bx.yview)
list_bx.bind('<<ListboxSelect>>', get_selected_row)



#Modify button
modify_btn = Button(root, text="Modify Record" ,bg="blue", fg="white", command=update_records)
modify_btn.grid(row=15,column=4)

#View button
view_btn = Button(root, text="View Record" ,bg="blue", fg="white", command=view_record)
view_btn.grid(row=15,column=1)

#Delete button
delete_btn = Button(root, text="Delete Record" ,bg="blue", fg="white", command=delete_record)
delete_btn.grid(row=15,column=3)

#Clear button
clear_btn = Button(root, text="Clear Record" ,bg="blue", fg="white", command=clear_screen)
clear_btn.grid(row=15,column=2)

#Exit button
exit_btn = Button(root, text="Exit Application" ,bg="blue", fg="white", command=root.destroy)
exit_btn.grid(row=15,column=5)

root.mainloop()
