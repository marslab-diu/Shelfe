import streamlit as st
import mysql.connector

from streamlit_option_menu import option_menu

import about,account,home,dashboard
st.set_page_config(
    page_title="Shelfie",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)


# connection = mysql.connector.connect(
#                 host="localhost",
#                 user="root",
#                 password="",
#                 database="noticedb"
#             )

# mycursor = connection.cursor()
# st.warning("Connected to the database successfully!")


class MultiApp:

    def __init__(self):
        self.apps = []
    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })
    def run():

        with st.sidebar:
            #st.title("")
            app = option_menu(
                menu_title='Shelfie',
                options=["Home", "Account", "Dashboard", "About"],
                icons=["🏠", "👤","📚", "📚"],
                menu_icon="📚",
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},}
                )
            
        if app == "Home":
            home.app()
        if app == "Account":
            account.app()
        if app == "Dashboard":
            dashboard.app()
        if app == "About":
            about.app()
    
    
    run()
            