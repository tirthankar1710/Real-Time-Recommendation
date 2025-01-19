import streamlit as st
import random

st.set_page_config(page_title='E-Commerce Recommendation', layout='wide', initial_sidebar_state='collapsed')

with st.container(border=True):
    st.title("E-Commerce Simulator")

# with st.container(border=True):
#     login_button = st.button("Login")

# Initialize a session state variable to track login status

user_list = ["user_1", "user_2", "user_3"]

random_user = random.choice(user_list)
welcome_message= f"Welcome to the platform {random_user}"
st.subheader(welcome_message)

