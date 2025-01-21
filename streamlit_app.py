import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title='E-Commerce Recommendation', layout='wide', initial_sidebar_state='collapsed')

with st.container(border=True):
    st.title("E-Commerce Simulator! 🛍️",)

# Sample data
data = {
    'product_id': ['P001', 'P002', 'P003', 'P004', 'P005'],
    'product_name': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
    # 'price': [10.99, 12.99, 9.99, 15.99, 8.99],
    'rating': [4.5, 4.0, 4.8, 3.9, 4.2]
}

user_list = ["user_1", "user_2", "user_3"]
random_user = random.choice(user_list)
welcome_message= f"Welcome to the platform: {random_user}"
st.subheader(welcome_message)

st.button("Generate recommendations")
# Create DataFrame
df = pd.DataFrame(data)
# Display DataFrame in Streamlit
st.write("Sample Product Data")
st.dataframe(df, use_container_width=True, hide_index=True)

products = [
    {"id": "P001", "name": "Product A"},
    {"id": "P002", "name": "Product B"},
    {"id": "P003", "name": "Product C"},
    {"id": "P004", "name": "Product D"},
    {"id": "P005", "name": "Product E"},
]

ratings = {}
counter=0
print("NEW SESSION")
# Display products with sliders for ratings

with st.container(border=True):
    col1, col2= st.columns(2)
    with col1:
        st.subheader("Please provide your reviews:")
        for product in products:
            counter+=1
            st.write(f"**{product['name']}** (ID: {product['id']})")
            feedback = st.feedback("stars", key={f"counter_{counter}"})
            # print("******")
            # print(f"counter: {product['name']}, feedback: {feedback+1}")
            # st.write("---")
    with col2:
        st.subheader("Would you buy this product?")
        for product in products:
            counter+=1
            st.write(f"**{product['name']}** (ID: {product['id']})")
            button = st.button("Add to Cart", key={f"counter_{counter}"}, icon="🛒")

st.button("Submit")
