import streamlit as st
import mysql.connector


def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="shelfiedb"
    )
    return connection

def app():
    hero = "UI\I1.png"
    all_books = "UI\I2.png"
    request = "UI\I3.png"
    features = "UI\I4.png"
    faq = "UI\I5.png"
    footer = "UI\I6.png"

    def show_book_details(book):
        st.markdown(f"### {book['title']}")
        st.write(f"**Author:** {book['author']}")
        st.write(f"**Genre:** {book['genre']}")
        st.write(f"**Published Year:** {book['publication_year']}")
        st.write(f"**Description:** {book['description']}")


    st.image(hero, use_container_width=True)
    st.image(all_books, use_container_width=True)
    # st.text(st.session_state.user_id)


    # Database connection
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    

    # Add filtering and searching options
    st.markdown("### Explore All Books")
    search_query = st.text_input("Search for a book by title:")
    genre_filter = st.selectbox("Filter by genre:", ["All", "Fiction","Non-Fiction","Science Fiction","Fantasy","Mystery","Romance","Thriller","Biography","Historical Fiction", "Adventure"])
    author_filter = st.text_input("Filter by author:")

    # Query to fetch books based on filters
    query = "SELECT * FROM books WHERE 1=1"
    params = []

    if search_query:
        query += " AND title LIKE %s"
        params.append(f"%{search_query}%")
    if genre_filter != "All":
        query += " AND genre = %s"
        params.append(genre_filter)
    if author_filter:
        query += " AND author LIKE %s"
        params.append(f"%{author_filter}%")

    cursor.execute(query, tuple(params))
    books = cursor.fetchall()

    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    user_signed_in = st.session_state.user_id is not None

    # Display books in 3 columns
    cols = st.columns(2)

    for index, book in enumerate(books):
        with cols[index % 2]:
               # Wrap image and caption in a center-aligned div
            st.markdown(
                f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="{book['cover_image_url']}" style="width: 120px; height: 180px; object-fit: cover; margin-bottom: 10px;" alt="Book Cover">
                <div style="font-size: 14px; font-weight: bold; margin-bottom: 10px;">{book['title']}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
            # st.image(book['cover_image_url'], width=100, caption=book['title'])
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"View Details: {book['book_id']}", key=f"details_{book['book_id']}"):
                    st.session_state.selected_book = book
                    show_book_details(book)
            with col2:
                if st.button(f"Add to Shelf ", key=f"add_{book['book_id']}"):
                    if not user_signed_in:
                        st.toast('Please Sign in to add book to shelf', icon='❗')
                    else:
                        try:
                            cursor.execute(
                                "INSERT INTO user_books (user_id, book_id, status) VALUES (%s, %s, %s)",
                                (st.session_state.user_id, book['book_id'], 'wishlist')
                            )
                        except mysql.connector.IntegrityError as e:
                            st.error(f"An error occurred: {e}")

    st.image(request, use_container_width=True)
    # st.markdown("### Request a Book")
    requested_book = st.text_input("Enter the name of the book you want to request:")

    if st.button("Submit Request"):
        if not user_signed_in:
            st.toast('Please Sign in to request a book', icon='❗')
        elif requested_book:
            try:
                cursor.execute(
                    "INSERT INTO book_requests (user_id, book_name) VALUES (%s, %s)",
                    (st.session_state.user_id, requested_book)
                )
                connection.commit()
                st.success("Your request has been submitted successfully!")
            except mysql.connector.Error as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a book name.")

    cursor.close()
    connection.close()


    st.image(features, use_container_width=True)
    st.image(faq, use_container_width=True)
    st.image(footer, use_container_width=True)

    



    

    