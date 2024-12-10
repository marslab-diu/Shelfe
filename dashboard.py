import streamlit as st
import mysql.connector
import datetime

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
    st.write("Hello " + st.session_state.username)

    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (st.session_state.username,))
    user_details = cursor.fetchone()

    if user_details:
        st.write("User ID: ", user_details['user_id'])
        st.write("Account created at: ",user_details['created_at'])
        st.session_state.user_id = user_details['user_id']
    else:
        st.write("User not found.")
    
    

    # Fetch and display user statistics
    cursor.execute("""
        SELECT 
            COUNT(CASE WHEN status = 'reading' THEN 1 END) AS reading_count,
            COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed_count,
            COUNT(CASE WHEN status = 'wishlist' THEN 1 END) AS wishlist_count
        FROM user_books
        WHERE user_id = %s;
    """, (st.session_state.user_id,))
    stats = cursor.fetchone()

    if stats:
        st.subheader("Your Book Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Books Reading", stats['reading_count'])
        col2.metric("Books Completed", stats['completed_count'])
        col3.metric("Books in Wishlist", stats['wishlist_count'])
    else:
        st.write("No statistics available.")
    

    # Fetch and display user books
    cursor.execute("""
        SELECT 
            ub.user_book_id,
            ub.book_id,
            b.title AS book_name,
            ub.status,
            ub.start_date,
            ub.end_date,
            ub.rating,
            ub.notes
        FROM user_books AS ub
        JOIN books AS b ON ub.book_id = b.book_id
        WHERE ub.user_id = %s;
    """, (st.session_state.user_id,))
    records = cursor.fetchall()


    if records:
        st.subheader("Your Books")
        for record in records:
            with st.expander(f"Book: {record['book_name']}"):
                # Fetch and display book cover
                cursor.execute("SELECT cover_image_url FROM books WHERE book_id = %s", (record['book_id'],))
                cover = cursor.fetchone()
                if cover and cover['cover_image_url']:
                    st.image(cover['cover_image_url'], caption=record['book_name'], width=100)
                st.write(f"**Status:** {record['status']}")
                st.write(f"**Start Date:** {record['start_date']}")
                st.write(f"**End Date:** {record['end_date']}")
                st.write(f"**Rating:** {record['rating']}")
                st.write(f"**Notes:** {record['notes']}")

                # Editable fields
                end_date = st.date_input(
                    "End Date", value=record['end_date'], key=f"end_date_{record['user_book_id']}"
                )
                rating = st.slider(
                    "Rating", min_value=1, max_value=5, value=record['rating'], key=f"rating_{record['user_book_id']}"
                )
                notes = st.text_area(
                    "Notes", value=record['notes'], key=f"notes_{record['user_book_id']}"
                )

                # Update button
                if st.button(f"Update Record for {record['book_name']}", key=f"update_{record['user_book_id']}"):
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute("""
                        UPDATE user_books
                        SET end_date = %s, rating = %s, notes = %s
                        WHERE user_book_id = %s;
                    """, (end_date, rating, notes, record['user_book_id']))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    st.success(f"Record for {record['book_name']} updated successfully!")
                    # st.experimental_rerun()
    else:
        st.write("No books found in your library.")
    



