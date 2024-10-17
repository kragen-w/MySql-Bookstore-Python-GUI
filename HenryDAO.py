import mysql.connector
import pandas as pd

class HenryDAO():
    def __init__(self):
    
        self.mydb = mysql.connector.connect(
            user='root',
            passwd='kragenwild',
            database='henry',
            host='127.0.0.1',
            allow_local_infile=1)
        self.mycur = self.mydb.cursor()


    def close(self):
        self.mydb.commit()
        self.mydb.close()

    def getAuthorData(self, author_id):

        # Perform the query
        sql = f"""SELECT author_first, author_last 
                FROM henry_author 
                WHERE author_num = {author_id};"""
        self.mycur.execute(sql)

        # Display the results
        for row in self.mycur:
            first_name = row[0]
            last_name = row[1]
            return (first_name, last_name)
        
    def initAuthors(self):
        mycur = self.mydb.cursor()
        mycur.execute('SELECT * FROM henry_author')
        authors = []
        for row in mycur:
            row = Author(row[0], row[1], row[2])
            authors.append(row)
        return authors
    def getBooksAuthor(self, author_id):
        mycur = self.mydb.cursor()
        mycur.execute(f'SELECT * FROM HENRY_BOOK INNER JOIN henry_WROTE on HENRY_BOOK.book_code = HENRY_WROTE.book_code where author_num = {author_id};')
        books = []
        for row in mycur:
            row = Book(row[0], row[1], row[2], row[3], row[4], row[5])
            books.append(row)
        return books
    def getBookData(self, book_code):
        mycur = self.mydb.cursor()
        mycur.execute(f'SELECT BRANCH_NAME, ON_HAND FROM HENRY_BRANCH inner join HENRY_INVENTORY on HENRY_BRANCH.BRANCH_NUM = HENRY_INVENTORY.BRANCH_NUM where book_code = \'{str(book_code)}\';')
        branch_info = []
        for branch, copies in mycur:
            branch_info.append((branch, copies))
        return branch_info
    
    def initPublishers(self):
        mycur = self.mydb.cursor()
        mycur.execute('SELECT * FROM HENRY_PUBLISHER')
        publishers = []
        for row in mycur:
            row = Publisher(row[0], row[1])
            publishers.append(row)
        return publishers

    def getBooksPublisher(self, publisher_code):
        mycur = self.mydb.cursor()
        mycur.execute(f'SELECT * FROM HENRY_BOOK INNER JOIN HENRY_PUBLISHER on HENRY_BOOK.PUBLISHER_CODE = HENRY_PUBLISHER.PUBLISHER_CODE where HENRY_PUBLISHER.PUBLISHER_CODE = \'{publisher_code}\';')
        books = []
        for row in mycur:
            row = Book(row[0], row[1], row[2], row[3], row[4], row[5])
            books.append(row)
        return books
    
    def initCategories(self):
        mycur = self.mydb.cursor()
        mycur.execute('SELECT TYPE FROM henry.HENRY_BOOK group by type order by type')
        categories = []
        for row in mycur:
            categories.append(row[0])
        return categories
    
    def getBooksCategory(self, category):
        mycur = self.mydb.cursor()
        mycur.execute(f'SELECT * FROM HENRY_BOOK where type = \'{category}\';')
        books = []
        for row in mycur:
            row = Book(row[0], row[1], row[2], row[3], row[4], row[5])
            books.append(row)
        return books



class Author:
    def __init__(self, author_id, author_last, author_first):
        self.author_id = author_id
        self.author_first = author_first
        self.author_last = author_last
    def __str__(self):
        return f"{self.author_first} {self.author_last}"
    
class Book:
    def __init__(self, book_code, title, publisher_code, type, price, paperback):
        self.book_code = book_code
        self.title = title
        self.publisher_code = publisher_code
        self.type = type
        self.price = price
        self.paperback = paperback

    def __str__(self):
        return f"{self.title}"
    
class Publisher:
    def __init__(self, publisher_code, publisher_name):
        self.publisher_code = publisher_code
        self.publisher_name = publisher_name
    def __str__(self):
        return f"{self.publisher_name}"
    
class Category:
    def __init__(self, category):
        self.category = category
    def __str__(self):
        return f"{self.category}"