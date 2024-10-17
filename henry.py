import tkinter as tk
from tkinter import ttk
from tkinter import *
from HenryDAO import HenryDAO


import mysql.connector

    




# Making the initial window, adds title, and makes size
root = tk.Tk()
root.option_add('*TCombobox*Listbox.foreground', 'blue') # change dropdown colors
root.title('Henry Bookstore')
root.geometry('900x400')

# Setting up the tab control
tabControl = ttk.Notebook(root) # Making a tab control
tabControl.pack(expand=2, fill="both") # Making the tabs show up

dao = HenryDAO()




author_tab = ttk.Frame(tabControl)

class HenrySBA:
    def __init__(self, frame, dao):
        self.dao = dao
        self.frame = frame
        self.age = 0
        self.authors_list = self.dao.initAuthors()
        tabControl.add(self.frame, text="Search by Author")


        # Adding the author combo box label
        author_lab = ttk.Label(frame)
        author_lab.grid(column=3, row=5)
        author_lab['text'] = "Author Selection"

        # Adding the book combo box label
        book_lab = ttk.Label(frame)
        book_lab.grid(column=4, row=5)
        book_lab['text'] = "Book Selection"

        # Initial book list and prices for the first author
        first = self.authors_list[0]
        self.book_list = self.dao.getBooksAuthor(first.author_id)
        book_prices = []
        book_codes = []
        for book in self.book_list:
            book_prices.append(book.price)
            book_codes.append(book.book_code)
            

         # Adding the author combobox
        self.author_combo = ttk.Combobox(frame, width=20, state="readonly")
        self.author_combo.grid(column=3, row=6)
        self.author_combo['values'] = self.authors_list # Putting values in the box
        self.author_combo.current(0) # Setting the first author as the initial value
        self.author_combo.bind("<<ComboboxSelected>>", self.newAuthorCatcher)  # Bind a callback

        # Adding the books combobox
        self.book_combo = ttk.Combobox(frame, width=35, state="readonly")
        self.book_combo.grid(column=4, row=6)
        self.book_combo['values'] = self.book_list # Putting values in the box
        self.book_combo.current(0) # Setting the first book as the initial value
        self.book_combo.bind("<<ComboboxSelected>>", self.newBookCatcher) # Bind a callback

        # Setting the initial price
        self.price = ttk.Label(frame)
        self.price.grid(column=5, row=6)
        self.price['text'] = "Price: $" + str(book_prices[0])

        # Availability tree
        self.av = ttk.Treeview(frame, columns=('Branch', 'Copies'), show='headings', selectmode="extended")
        self.avlab = ttk.Label(frame)
        self.avlab.grid(column=4, row=1)
        self.avlab['text'] = "Available Copies"
        self.av.heading('Branch', text='Branch Name')
        self.av.heading('Copies', text='Copies Available')
        self.av.grid(column=4, row=2)

    def newAuthorCatcher(self, event):
        author_id = self.author_combo.current() + 1
        self.newAuthor(author_id)

    def newAuthor(self, author_id):
        self.book_list = self.dao.getBooksAuthor(author_id)
        if len(self.book_list) == 0:
            self.price['text'] = "Price: $0"
            self.book_combo.config(values = ["No Books"])
            self.book_combo.current(0)
        else:
            self.book_combo.config(values = self.book_list)
            self.book_combo.current(0)
            self.newBook(0)

    def newBookCatcher(self, event):
        book_index = self.book_combo.current()
        self.newBook(book_index)

    def newBook(self, book_index):
        self.price['text'] = "Price: $" + str(self.book_list[book_index].price)
        self.book_availability = self.dao.getBookData(self.book_list[book_index].book_code)
        for item in self.av.get_children():
            self.av.delete(item)
        for row in self.book_availability:
            self.av.insert("", "end", values=[row[0], row[1]])
        # you are tryna get da branch info from the function getBookData, which returns a tuple
        

    

a = HenrySBA(author_tab, dao)
# a.gad(2)

publisher_tab = ttk.Frame(tabControl)
class HenrySBP:
    def __init__(self, frame, dao):
        self.dao = dao
        self.frame = frame
        self.age = 0
        self.publishers_list = self.dao.initPublishers()
        tabControl.add(frame, text="Search by Publisher")
        

        # Adding the author combo box label
        publisher_lab = ttk.Label(frame)
        publisher_lab.grid(column=3, row=5)
        publisher_lab['text'] = "Publisher Selection"

        # Adding the book combo box label
        book_lab = ttk.Label(frame)
        book_lab.grid(column=4, row=5)
        book_lab['text'] = "Book Selection"


        # Initial book list and prices for the first author
        first = self.publishers_list[0]
        self.book_list = self.dao.getBooksPublisher(first.publisher_code)
        book_prices = []
        book_codes = []
        for book in self.book_list:
            book_prices.append(book.price)
            book_codes.append(book.book_code)


        # Adding the author combobox
        self.publisher_combo = ttk.Combobox(frame, width=20, state="readonly")
        self.publisher_combo.grid(column=3, row=6)
        self.publisher_combo['values'] = self.publishers_list # Putting values in the box
        self.publisher_combo.current(0) # Setting the first author as the initial value
        self.publisher_combo.bind("<<ComboboxSelected>>", self.newPublisherCatcher)  # Bind a callback

        # Adding the books combobox
        self.book_combo = ttk.Combobox(frame, width=35, state="readonly")
        self.book_combo.grid(column=4, row=6)
        self.book_combo['values'] = self.book_list # Putting values in the box

        if len(self.book_list) == 0:
            self.book_combo.config(values = ["No Books"])
            self.book_combo.current(0)

        self.book_combo.current(0) # Setting the first book as the initial value
        self.book_combo.bind("<<ComboboxSelected>>", self.newBookCatcher) # Bind a callback

        # Setting the initial price
        self.price = ttk.Label(frame)
        self.price.grid(column=5, row=6)
        if len(self.book_list) == 0:
            self.price['text'] = "Price: $0"
        else:
            self.price['text'] = "Price: $" + str(book_prices[0])

        # Availability tree
        self.av = ttk.Treeview(frame, columns=('Branch', 'Copies'), show='headings', selectmode="extended")
        self.avlab = ttk.Label(frame)
        self.avlab.grid(column=4, row=1)
        self.avlab['text'] = "Available Copies"
        self.av.heading('Branch', text='Branch Name')
        self.av.heading('Copies', text='Copies Available')
        self.av.grid(column=4, row=2)
        
        
    def newPublisherCatcher(self, event):
        publisher_id = self.publisher_combo.current()
        self.newPublisher(publisher_id)

    def newPublisher(self, publisher_id):
        publisher_code = self.publishers_list[publisher_id].publisher_code
        self.book_list = self.dao.getBooksPublisher(publisher_code)
        if len(self.book_list) == 0:
            self.price['text'] = "Price: $0"
            self.book_combo.config(values = ["No Books"])
            self.book_combo.current(0)
        else:
            self.book_combo.config(values = self.book_list)
            self.book_combo.current(0)
            self.newBook(0)

    def newBookCatcher(self, event):
        book_index = self.book_combo.current()
        self.newBook(book_index)

    def newBook(self, book_index):
        self.price['text'] = "Price: $" + str(self.book_list[book_index].price)
        self.book_availability = self.dao.getBookData(self.book_list[book_index].book_code)
        for item in self.av.get_children():
            self.av.delete(item)
        for row in self.book_availability:
            self.av.insert("", "end", values=[row[0], row[1]])
        # you are tryna get da branch info from the function getBookData, which returns a tuple


p = HenrySBP(publisher_tab, dao)


category_tab = ttk.Frame(tabControl)
class HenrySBC:
    def __init__(self, frame, dao):
        self.dao = dao
        self.frame = frame
        self.age = 0
        self.categorys_list = self.dao.initCategories()
        tabControl.add(frame, text="Search by Category")

        # Adding the author combo box label
        category_lab = ttk.Label(frame)
        category_lab.grid(column=3, row=5)
        category_lab['text'] = "Category Selection"

        # Adding the book combo box label
        book_lab = ttk.Label(frame)
        book_lab.grid(column=4, row=5)
        book_lab['text'] = "Book Selection"


        # Initial book list and prices for the first author
        first = self.categorys_list[0]
        self.book_list = self.dao.getBooksCategory(first)
        book_prices = []
        book_codes = []
        for book in self.book_list:
            book_prices.append(book.price)
            book_codes.append(book.book_code)


        # Adding the author combobox
        self.category_combo = ttk.Combobox(frame, width=20, state="readonly")
        self.category_combo.grid(column=3, row=6)
        self.category_combo['values'] = self.categorys_list # Putting values in the box
        self.category_combo.current(0) # Setting the first author as the initial value
        self.category_combo.bind("<<ComboboxSelected>>", self.newCategoryCatcher)  # Bind a callback

        # Adding the books combobox
        self.book_combo = ttk.Combobox(frame, width=35, state="readonly")
        self.book_combo.grid(column=4, row=6)
        self.book_combo['values'] = self.book_list # Putting values in the box
        
        if len(self.book_list) == 0:
            self.book_combo.config(values = ["No Books"])
            self.book_combo.current(0)

        self.book_combo.current(0) # Setting the first book as the initial value
        self.book_combo.bind("<<ComboboxSelected>>", self.newBookCatcher)

        # Setting the initial price
        self.price = ttk.Label(frame)
        self.price.grid(column=5, row=6)
        if len(self.book_list) == 0:
            self.price['text'] = "Price: $0"
        else:
            self.price['text'] = "Price: $" + str(book_prices[0])

        # Availability tree
        self.av = ttk.Treeview(frame, columns=('Branch', 'Copies'), show='headings', selectmode="extended")
        self.avlab = ttk.Label(frame)
        self.avlab.grid(column=4, row=1)
        self.avlab['text'] = "Available Copies"
        self.av.heading('Branch', text='Branch Name')
        self.av.heading('Copies', text='Copies Available')
        self.av.grid(column=4, row=2)
        
    def newCategoryCatcher(self, event):
        category = self.category_combo.current()
        self.newCategory(category)

    def newCategory(self, category):
        category = self.categorys_list[category]
        self.book_list = self.dao.getBooksCategory(category)
        if len(self.book_list) == 0:
            self.price['text'] = "Price: $0"
            self.book_combo.config(values = ["No Books"])
            self.book_combo.current(0)
        else:
            self.book_combo.config(values = self.book_list)
            self.book_combo.current(0)
            self.newBook(0)

    def newBookCatcher(self, event):
        book_index = self.book_combo.current()
        self.newBook(book_index)

    def newBook(self, book_index):
        self.price['text'] = "Price: $" + str(self.book_list[book_index].price)
        self.book_availability = self.dao.getBookData(self.book_list[book_index].book_code)
        for item in self.av.get_children():
            self.av.delete(item)
        for row in self.book_availability:
            self.av.insert("", "end", values=[row[0], row[1]])
        # you are tryna get da branch info from the function getBookData, which returns a tuple

        

c = HenrySBC(category_tab, dao)


root.mainloop()
