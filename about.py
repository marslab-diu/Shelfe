import streamlit as st

def app():
    st.title("About")

    st.markdown(
        """
        ### What is Shelfie?
        **Shelfie** is your personal book-reading manager designed to help you organize and track your reading journey with ease. 
        Whether you’re building a wishlist, currently reading, or looking back at completed books, Shelfie simplifies the process.

        #### Key Features:
        - **Discover Books:** Browse a collection of books and filter by genre, author, and more.
        - **Personalized Shelf:** Manage your own bookshelf with statuses like `Reading`, `Wishlist`, and `Completed`.
        - **Track Progress:** Update your reading status, add ratings, notes, and completion dates for each book.
        - **Request Books:** Missing a book? Send requests directly through the app.
        - **Interactive Dashboard:** Stay on top of your reading statistics and manage your entries effortlessly.

        ### Built By:
        This application is developed by **Mars Lab**, a dedicated team passionate about creating smart solutions for learning and productivity.

        ### Academic Purpose:
        Shelfie was developed as part of the **Database Management Systems (DBMS)** course project. 
        It showcases the integration of SQL databases with Python using **Streamlit**, a modern app-building framework, to create a seamless user experience.

        ---
        We hope you enjoy using Shelfie to enhance your reading experience. Happy reading!
        """
    )

    