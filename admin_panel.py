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
    if 'admin' not in st.session_state:
        st.session_state.admin = False
    if 'add_book' not in st.session_state:
        st.session_state.add_book = False
    if 'update_book' not in st.session_state:
        st.session_state.update_book = False
        st.session_state.search_book = False
    if 'remove_book' not in st.session_state:
        st.session_state.remove_book = False
    if 'search_book' not in st.session_state:
        st.session_state.search_book = False
    if 'requested_book' not in st.session_state:
        st.session_state.requested_book = False


    st.title("Admin Panel")


    if st.session_state.admin == False:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if username == "admin" and password == "admin":
            st.session_state.admin = True
            st.write("Logged in as Admin")
        else:
            st.warning("Please enter the correct username and password.")
            st.stop()


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

    def add_book(title, author, genre, publication_year, description,cover):
        connection = connect_to_db()
        try:
            mycursor = connection.cursor()
            mycursor.execute("INSERT INTO books (title, author, genre, publication_year, description,cover_image_url) VALUES (%s, %s,%s,%s,%s)", (title, author, genre, publication_year, description,cover))
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
            mycursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
            connection.commit()
        finally:
            connection.close()
    
    def requested_book():
        connection = connect_to_db()
        try:
            mycursor = connection.cursor()
            mycursor.execute("SELECT * FROM book_requests")
            result = mycursor.fetchall()
            connection.close()
            return result
        finally:
            connection.close()


    if st.session_state.admin:
        write = st.write("Welcome Admin")
        if st.button("Logout"):
                st.session_state.admin = False
                st.session_state.add_book = False
                st.session_state.update_book = False
                st.session_state.remove_book = False
                st.session_state.search_book = False
                st.warning("Logged out successfully!")
                st.stop()
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
            cover = st.text_input("Enter cover image URL:")
            if st.button(f"Submit '{title}'"):
                add_book(title, author, genre, publication_year, description,cover)
                st.success("Book added successfully!")
                st.session_state.add_book = False
        

        if st.button("Search Book"):
            st.session_state.search_book = True
            st.session_state.add_book = False
            # st.session_state.update_book = False
            # st.session_state.remove_book = False

        if st.session_state.search_book:
            search_by = st.selectbox("Search by", ["Title", "Author", "Year", "Genre"])
            search_query = st.text_input("Enter search query:")
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

        if st.button("Update Book"):
            st.session_state.update_book = True
            st.session_state.add_book = False
            st.session_state.remove_book = False
            st.session_state.search_book = False

        if st.session_state.update_book:
            update_query = st.text_input("Search for a book title to update:")
            if update_query:
                books = search_books(update_query, "Title")
                if books:
                    st.write("Search Results:")
                    for i in range(0, len(books), 3):
                        cols = st.columns(3)
                        for j in range(3):
                            if i + j < len(books):
                                book = books[i + j]
                                with cols[j]:
                                    st.image(book[6], width=100)  # book[6] is the URL or path to the cover image
                                    st.write(f"Title: {book[1]}")
                                    if st.button(f"Click to update", key=f"select_{book[0]}"):
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
                    for book in books:
                        st.image(book[6], width=100)  # Assuming book[6] is the URL or path to the cover image
                        st.write(f"Title: {book[1]}, Author: {book[2]}")
                        if st.button(f"Select '{book[1]}' to remove", key=f"select_{book[0]}"):
                            remove_book(book[0])
                            st.success("Book removed successfully!")
                            st.session_state.remove_book = False
                else:
                    st.write("No books found.")

        if st.button("Requested Books"):
            st.session_state.requested_book = True
            st.session_state.add_book = False
            st.session_state.update_book = False
            st.session_state.remove_book = False
            st.session_state.search_book = False
        
        if st.session_state.requested_book:
            requested_books = requested_book()
            if requested_books:
                df = pd.DataFrame(requested_books, columns=["Request ID", "User ID", "Book Title", "Request Date"])
                st.table(df.set_index("Request ID"))
            else:
                st.write("No requested books found.")

    





