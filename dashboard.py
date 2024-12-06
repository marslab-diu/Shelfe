import streamlit as st
import mysql.connector
import signin
import pandas as pd
# st.set_option('client.showErrorDetails', False)


def connect_to_db():
    connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="shelfiedb"
                )
    # st.success("Connected to the database successfully!")
    return connection


def app():

    st.title("Dashboard")

    if 'username' not in st.session_state:
        st.session_state.username = ''

    st.write(f"Welcome, {st.session_state.username}")

    
    def search_books(query, search_by):
        connection = connect_to_db()
        try:
            mycursor = connection.cursor()
            if search_by == "Title":
                mycursor.execute("SELECT * FROM books WHERE title LIKE %s", ('%' + query + '%',))
            elif search_by == "Author":
                mycursor.execute("SELECT * FROM books WHERE author LIKE %s", ('%' + query + '%',))
            elif search_by == "Year":
                mycursor.execute("SELECT * FROM books WHERE publication_year LIKE %s", ('%' + query + '%',))
            elif search_by == "Genre":
                mycursor.execute("SELECT * FROM books WHERE genre LIKE %s", ('%' + query + '%',))
            result = mycursor.fetchall()
            connection.close()
            return result
        finally:
            connection.close()

    def add_book(title, author, genre, publication_year, description):
        connection = connect_to_db()
        try:
            mycursor = connection.cursor()
            mycursor.execute("INSERT INTO books (title, author, genre, publication_year, description) VALUES (%s, %s,%s,%s,%s)", (title, author, genre, publication_year, description))
            connection.commit()
        finally:
            connection.close()

    def update_book(book_id, new_title, new_author, new_genre, new_publication_year, new_description):
        connection = connect_to_db()
        try:
            mycursor = connection.cursor()
            mycursor.execute("UPDATE books SET title = %s, author = %s, genre = %s, publication_year = %s, description = %s WHERE book_id = %s", (new_title, new_author, new_genre, new_publication_year, new_description, book_id))
            connection.commit()
        finally:
            connection.close()

    def remove_book(book_id):
        connection = connect_to_db()
        try:
            mycursor = connection.cursor()
            mycursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
            connection.commit()
        finally:
            connection.close()

    if 'add_book' not in st.session_state:
        st.session_state.add_book = False
    if 'update_book' not in st.session_state:
        st.session_state.update_book = False
        st.session_state.search_book = False
    if 'remove_book' not in st.session_state:
        st.session_state.remove_book = False
    if 'search_book' not in st.session_state:
        st.session_state.search_book = False

    if st.button("Add Book"):
        st.session_state.add_book = True
        st.session_state.update_book = False
        st.session_state.remove_book = False
        st.session_state.search_book = False

    if st.session_state.add_book:
        title = st.text_input("Enter book title:")
        author = st.text_input("Enter book author:")
        genre = st.text_input("Enter book genre:")
        publication_year = st.text_input("Enter book publication year:")
        description = st.text_area("Enter book description:")
        if st.button(f"Submit {book[0]}"):
            add_book(title, author, genre, publication_year, description)
            st.success("Book added successfully!")
            st.session_state.add_book = False

    if st.button("Update Book"):
        st.session_state.update_book = True
        st.session_state.add_book = False
        st.session_state.remove_book = False
        st.session_state.search_book = False

    if st.session_state.update_book:
        update_query = st.text_input("Search for a book to update:")
        if update_query:
            books = search_books(update_query, "Title")
            if books:
                for book in books:
                    st.write(f"Title: {book[1]}, Author: {book[2]}")
                    if st.button(f"Select '{book[1]}' for update", key=f"select_{book[0]}"):
                        st.session_state.selected_book = book

            # Check if a book is selected
            if "selected_book" in st.session_state:
                selected_book = st.session_state.selected_book
                st.write(f"**Updating Book:** {selected_book[1]}")

                # Input fields for updating the book
                new_title = st.text_input("Enter new title:", value=selected_book[1], key="new_title")
                new_author = st.text_input("Enter new author:", value=selected_book[2], key="new_author")
                new_genre = st.text_input("Enter new genre:", value=selected_book[3], key="new_genre")
                new_publication_year = st.text_input("Enter new publication year:", value=selected_book[4], key="new_publication_year")
                new_description = st.text_area("Enter new description:", value=selected_book[5], key="new_description")

                # Submit button for updating the book
                if st.button("Submit Update"):
                    update_book(
                        selected_book[0],
                        new_title,
                        new_author,
                        new_genre,
                        new_publication_year,
                        new_description,
                    )
                    st.success(f"Book '{selected_book[1]}' updated successfully!")

                    # Clear session state after updating
                    del st.session_state["selected_book"]
                    st.session_state.update_book = False
                    # st.experimental_rerun()
        #         else:
        #             st.info("Please select a book to update.")
        #     else:
        #         st.info("Enter a search query to find books.")
        # else:
        #     # st.info("Click 'Update Book' to start updating a book.")


    if st.button("Remove Book"):
        st.session_state.remove_book = True
        st.session_state.add_book = False
        st.session_state.update_book = False
        st.session_state.search_book = False

    if st.session_state.remove_book:
        remove_query = st.text_input("Search for a book title to remove:")
        if remove_query:
            books = search_books(remove_query, "Title")
            if books:
                for i in range(0, len(books), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(books):
                            book = books[i + j]
                            with cols[j]:
                                st.image(book[6], width=100)  # Assuming book[6] is the URL or path to the cover image
                                st.write(f"**Title:** {book[1]}")
                                st.write(f"**Author:** {book[2]}")
                                st.write(f"**Genre:** {book[3]}")
                                st.write(f"**Publication Year:** {book[4]}")
                                st.write(f"**Description:** {book[5]}")
                                if st.button(f"Remove '{book[1]}'"):
                                    remove_book(book[0])
                                    st.success("Book removed successfully!")
                                    st.session_state.remove_book = False
            else:
                st.write("No books found.")

    if st.button("Search Book"):
        st.session_state.search_book = True
        st.session_state.add_book = False
        # st.session_state.update_book = False
        # st.session_state.remove_book = False

    if st.session_state.search_book:
        search_query = st.text_input("Enter search query:")
        search_by = st.selectbox("Search by", ["Title", "Author", "Year", "Genre"])
        if st.button("Search"):
            books = search_books(search_query, search_by)
            if books:
                st.write("Search Results:")
                for i in range(0, len(books), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(books):
                            book = books[i + j]
                            with cols[j]:
                                st.image(book[6], width=100)  # Assuming book[6] is the URL or path to the cover image
                                st.write(f"**Title:** {book[1]}")
                                st.write(f"**Author:** {book[2]}")
                                st.write(f"**Genre:** {book[3]}")
                                st.write(f"**Publication Year:** {book[4]}")
                                st.write(f"**Description:** {book[5]}")
            else:
                st.write("No books found.")





