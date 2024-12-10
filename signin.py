import streamlit as st
import mysql.connector

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
    st.title("Account Signin or Signup ⚡")

    if 'user_id' not in st.session_state:
        st.session_state.user_id = ''
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'password' not in st.session_state:
        st.session_state.password = ''


  
    def login(username, password):
        connection = connect_to_db()
        try:
            mycursor = connection.cursor()
            mycursor.execute("""SELECT username FROM users WHERE username = %s AND password = %s""", (username,password))
            result = mycursor.fetchone()
            if result:
                st.success(f"Signed in successfully! Welcome, {result[0]}")
                st.session_state.username = username
                st.session_state.password = password
                st.session_state.name = result[0]
                st.session_state.signed_out = True
                st.session_state.sign_out = True

            else:
                st.error("Invalid Username or Password")

        finally:
            connection.close()
    
    def create_account(username, password):
        connection = connect_to_db()
        try:
            mycursor = connection.cursor()
            mycursor.execute("""INSERT INTO users (username, password) VALUES (%s, %s)""", (username, password))
            connection.commit()
            st.success("Account created successfully")
            st.write("You can now signin to your account")
            st.balloons()
        except:
            st.warning('Error in creating account')
        finally:
            connection.close()

    def sign_out():
        st.session_state.signed_out = False
        st.session_state.sign_out = False
        st.session_state.username = ''
        st.session_state.password = ''
        # st.success("Signed out successfully")


    if 'signed_out' not in st.session_state:
        st.session_state.signed_out = False
    if 'sign_out' not in st.session_state:
        st.session_state.sign_out = False


    # if user is not logged in then the options will show to login or signup
    if not st.session_state.signed_out:
        choice = st.selectbox('Signin/Signup', ['Signin', 'Signup'])
        username = st.text_input("Username")
        password = st.text_input("Password")


        if choice == 'Signup':
            # st.write("Signup for a new account")
            # password = st.text_input("Password", type='password')
            conf_password = st.text_input("Confirm Password")

            if password != conf_password:
                st.write("Passwords do not match")
            else:
                if st.button("Signup"):
                    create_account(username, password)
        # that is log in
        else:
            if st.button("Signin"):
                login(username, password)
            # st.button('Login',on_click=login(username, password))
            
    if st.session_state.sign_out:
        # st.text('User ID ' + st.session_state.user_id)
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (st.session_state.username,))
        user_details = cursor.fetchone()
        if user_details:
            st.write("User ID: ", user_details['user_id'])
            st.session_state.user_id = user_details['user_id']
            st.write('Username: ', st.session_state.username)
        
        st.button('Sign out', on_click=sign_out)
        
        
            