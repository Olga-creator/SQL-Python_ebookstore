# Import libraries
import sqlite3
import os

# List of new records
rows = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
        (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12),
        (3006, 'The Hobbit', 'J.R.R. Tolkien', 57),
        (3007, 'Jane Eyre', 'Charlotte Brontë', 17),
        (3008, 'David Copperfield', 'Charles Dickens', 17),
        (3009, 'Great Expectations', 'Charles Dickens', 23)]

# Error handling if a file ebookstore_db already exists
if not os.path.isfile('ebookstore_db'):
    print()

# Create a file called ebookstore_db with a SQLite3 DB
ebookstore = sqlite3.connect('ebookstore_db')
cursor = ebookstore.cursor()
ebookstore.commit()

try:
    # Create a table called books
    cursor.execute('''CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)''')

    # Insert new rows into the books table
    sqlite_insert_query = ("""INSERT INTO books
                                (id, title, author, qty) 
                                VALUES (?, ?, ?, ?);""")

    cursor.executemany(sqlite_insert_query, rows)
    ebookstore.commit()

except sqlite3.OperationalError as error:
    print()


# This function called when the user selects 'Enter book' from main menu to add a new book to the database
def enter_book():
    # ID will be automatically generated: last ID plus one
    last_id = cursor.execute("""SELECT max(id) FROM books""")
    for row in last_id:
        id_book = row[0] + 1
    id_new = id_book

    # Titles aren't copyright, unlike the content of the book itself so legally a book title can be used
    # for another book in UK. Therefore, title and author both are checked if the book already exists in the database
    title_input = input("Enter the title of a book: ")
    author_input = input("Enter author: ")
    title_exists = cursor.execute("""SELECT id, title, author, qty FROM books 
                                    WHERE title = ? AND author = ?""", (title_input, author_input))

    for row in title_exists:
        answer = row[0]
        if answer:
            print("\nWarning: The book with the same title and author already exists.\n"
                  f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, QTY: {row[3]}\n"
                  "If you would like to update quantity, please choose option 2 from main menu.\n")
            user_menu()

    while True:
        try:
            qty_input = int(input("Enter quantity: "))
            break
        except ValueError:
            print("Incorrect quantity. Try again!\n")
            continue

    sqlite_insert_query1 = ("""INSERT INTO books
                            (id, title, author, qty)
                            VALUES (?, ?, ?, ?);""")

    ebookstore.execute(sqlite_insert_query1, (id_new, title_input, author_input, qty_input))
    print(f"\nThe book has been successfully entered. ID of this book is {id_new}.\n")


# This function called when the user selects 'Update book' from main menu to update quantity
# for the book with the lowest quantity in the database
def update_book():
    print("\t\t\tTHIS BOOK HAS THE LOWEST QUANTITY:")
    print("---------------------------------------------------------------------")
    min_qty = cursor.execute("""SELECT id, title, author, min(qty) FROM books""")
    for row1 in min_qty:
        print(f'ID: {row1[0]}, Title: {row1[1]}, Author: {row1[2]}, QTY: {row1[3]}')
        old_qty = row1[3]
    print("---------------------------------------------------------------------\n")

    while True:
        update = input("Would you like to update quantity? (Yes/No) ").lower()
        if update == "yes" or update == "y":
            try:
                new_qty = int(input("Please enter new quantity: "))
                cursor.execute("""UPDATE books SET qty = ? WHERE qty = ?""", (new_qty, old_qty))
                print("\nQuantity has been successfully updated!\n")
                break
            except ValueError:
                print("Invalid quantity. Try again!\n")
                continue

        elif update == "no" or update == "n":
            break

        else:
            print("Invalid option. Try again!\n")
            continue


# This function called when the user selects 'Delete book' from main menu to delete a book
def delete_book():
    # Range of ID will be used to check a user's input
    last_id = cursor.execute("""SELECT max(id) FROM books""")
    for item in last_id:
        l_id = item[0]

    first_id = cursor.execute("""SELECT min(id) FROM books""")
    for item1 in first_id:
        f_id = item1[0]

    while True:
        try:
            book_delete = int(input("Please enter ID for the book you would like to delete: "))
            if l_id >= book_delete >= f_id:
                cursor.execute('''DELETE FROM books WHERE id = ?''', (book_delete,))
                print(f"\nThe book with ID {book_delete} has been successfully deleted!\n")
                break
            else:
                print("Invalid ID. Try again!\n")
                continue
        except ValueError:
            print("ID is a number. Try again!\n")
            continue


# This function called when the user selects 'Search book' from main menu to look for a book
def search_book():
    while True:
        # A user is given options to use different parameters to perform a book search
        search_menu = input("""\nPlease choose from the menu below: 
1 - ID
2 - Author
3 - Title
4 - Highest Quantity
0 - Exit
:""")

        if search_menu == "1":
            option1 = input("Please enter ID: ")
            book = cursor.execute("""SELECT id, title, author, qty FROM books WHERE id = ?""", (option1,))
            for row1 in book:
                print(f'ID: {row1[0]}, Title: {row1[1]}, Author: {row1[2]}, QTY: {row1[3]}')
                continue

        elif search_menu == "2":
            option2 = input("Please enter author: ")
            list_new = cursor.execute("""SELECT id, title, author, qty FROM books WHERE author = ?""", (option2,))
            for row2 in list_new:
                print(f'ID: {row2[0]}, Title: {row2[1]}, Author: {row2[2]}, QTY: {row2[3]}')
                continue

        elif search_menu == "3":
            option3 = input("Please enter title: ")
            list_new = cursor.execute("""SELECT id, title, author, qty FROM books WHERE title = ?""", (option3,))
            for row3 in list_new:
                print(f'ID: {row3[0]}, Title: {row3[1]}, Author: {row3[2]}, QTY: {row3[3]}')
                continue

        elif search_menu == "4":
            print("\t\t\tTHIS BOOK HAS THE HIGHEST QUANTITY:")
            print("-----------------------------------------------------------------------------------------")
            min_qty = cursor.execute("""SELECT id, title, author, max(qty) FROM books""")
            for row4 in min_qty:
                print(f'ID: {row4[0]}, Title: {row4[1]}, Author: {row4[2]}, QTY: {row4[3]}')
            print("-----------------------------------------------------------------------------------------\n")
            continue

        elif search_menu == "0":
            break

        else:
            print("\nThis option is not valid. Try again.\n")
            continue


# This function called when the user selects 'View all books' from main menu
def view_all():
    # Ref: https://www.pylenin.com/blogs/python-width-precision/
    cursor.execute('SELECT id, title, author, qty FROM books')
    info = cursor.fetchall()

    # Determine the longest width for each column
    header = ("id", "Title", "Author", "qty")
    widths = [len(item) for item in header]
    for row in info:
        for i, item in enumerate(row):
            widths[i] = max(len(str(item)), widths[i])

    # Construct formatted row like before
    formatted_row = ' '.join('{:%d}' % width for width in widths)
    print()
    print("------------------------------------------------------------------------")
    print(formatted_row.format(*header))
    print("------------------------------------------------------------------------")
    for row in info:
        print(formatted_row.format(*row))
    print("------------------------------------------------------------------------")
    print()


# User's menu
def user_menu():
    while True:
        menu = input("""\nSelect one of the following options below:
1 - Enter book
2 - Update book
3 - Delete book
4 - Search book
5 - View all books
0 - Exit
: """)

        if menu == "1":
            enter_book()
            continue

        elif menu == "2":
            update_book()
            continue

        elif menu == "3":
            delete_book()
            continue

        elif menu == "4":
            search_book()
            continue

        elif menu == "5":
            view_all()
            continue

        elif menu == "0":
            ebookstore.commit()
            ebookstore.close()
            print("Connection to database closed. Goodbye!!!")
            exit()

        else:
            print("\nThis option is not valid. Try again.\n")
            continue


user_menu()
