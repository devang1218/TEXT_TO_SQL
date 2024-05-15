import streamlit as st
import os
import sqlite3

import openai

## Configure OpenAI Key
openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
## Function to generate SQL query using OpenAI
def get_openai_response(question, prompt):
  response = openai.chat.Completion.create(
      engine="text-davinci-003",
      prompt=prompt + question,
      max_tokens=150,  # Adjust maximum response length as needed
      n=1,  # Generate only 1 response
      stop=None  # Don't specify a stop sequence for flexibility
  )
  return response.choices[0].text.strip()

## Function to retrieve data from the database
def read_sql_query(sql, db):
  conn = sqlite3.connect(db)
  cur = conn.cursor()
  cur.execute(sql)
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return rows

## Define your prompt
prompt = """
You are an expert in converting English questions to SQL query!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION 
\n\nFor example,
Example 1 - How many entries of records are present?, 
the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
\nExample 2 - Tell me all the students studying in Data Science class?, 
the SQL command will be something like this SELECT * FROM STUDENT 
where CLASS="Data Science"; 
also the sql code should not have ``` in beginning or end and sql word in output
If someone asks about the marks related query look into marks column in the table
"""

## Streamlit App
st.set_page_config(page_title="SQL query Retriever")
st.header("Text2SQL")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# If submit is clicked
if submit:
  response = get_openai_response(question, prompt)
  print(response)
  rows = read_sql_query(response, "student.db")
  st.subheader("Result:")
  for row in rows:
    print(row)
    st.write(row) 