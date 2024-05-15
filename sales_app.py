from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import pandas as pd
import streamlit as st
import os
import sqlite3

import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    response=cur
    # for row in rows:
    #     print(row)
    df = pd.DataFrame(response.fetchall(),columns = [desc[0] for desc in cur.description]) 
    print(df)

    conn.commit()
    conn.close()
    return df

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name Sales and has 4 following tables- customers, items, orders, sales.\n
    customers table has the following 2 columns- customer_id, age where customer_id is the primary key 
    sales table has the following 2 columns- sales_id, customer_id where sales_id is primary key and customer_id is foreign key reference to customers table 
    items table has the following 2 columns- item_id, item_name where item_id is the primary key 
    orders table has the following 4 columns- order_id, sales_id, item_id, quantity where order_id is primary key and item_id and sales_id are foreign key reference to items and sales table respectively.\n

    SECTION \n\nFor example,\nExample 1 - give the list of sales id, item id, order id and quantity where only 2 items are purchased for a single sale
    the SQL command will be something like this-
    SELECT * FROM orders o where o.sales_id in (select o1.sales_id from orders o1 group by o1.sales_id having count(o1.quantity) = 2)
    and o.quantity is not NUll;\n
    do not add ``` or sql in the start of the query 
    """
]

## Streamlit App
st.set_page_config(page_title="SQL query Retriever")
st.header("Smart Database Assistant")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"D:\Python Projects\TEXT_TO_SQL\Sales.db")
    st.subheader("Result:")
    # for row in response:
    #     print(row)
    st.dataframe(response, hide_index=True)
 