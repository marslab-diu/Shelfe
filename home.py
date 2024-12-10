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


    st.image(hero, use_container_width=True)
    st.image(all_books, use_container_width=True)

    #here add the code for showing all books in 3 columns, and option to filter by genre, author, etc.
    #also add the option to search for a book
    #the books cover should be clickable and should lead to the book details popup
    #the book details popup should have the option to add the book to the user's shelf
    # if user is not logged in , then cant be addded to user's shelf





    st.image(request, use_container_width=True)
    st.image(features, use_container_width=True)
    st.image(faq, use_container_width=True)
    st.image(footer, use_container_width=True)



    

    