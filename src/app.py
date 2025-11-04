import streamlit as st
import mysql.connector
from groq import Groq
import time
def extract_schema(cursor):
    schema = ""
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        cursor.execute(f"SHOW COLUMNS FROM {table}")
        columns = [row[0] for row in cursor.fetchall()]
        schema += f"Table: {table}, Columns: {', '.join(columns)}\n"
    return schema

# Initialize Groq client
client = Groq(api_key="Your API key")  # <-- Replace with your actual key

# Database connection
def init_database(user, password, host, port, database):
    return mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )


def generate_sql(user_query, table_schema):
    """Ask Groq to generate SQL based on user input and table structure"""
    prompt = f"""
You are an expert SQL generator.
Given the database schema and the user query, generate ONLY the SQL query.If no table is specified, infer the table name when possible from the schema
write only the sql query and nothing else.do no wrap sql query in any other text,not even backticks.
Schema:
{table_schema}

User Query:
{user_query}

Return only the SQL query, no explanations.
for example:
   Question:name 10 artists
   SQL Query: SELECT Name from artists LIMIT 10;
   Question:how many faculty are there
   SQL Query:SELECT COUNT(*) AS NUMBER_OF_STUDENTS FROM STUDENTDETAILS;
Your Turn:
    """
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct", 
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip("`").strip()


def explain_results(results, user_query):
    """Ask Groq to explain SQL results in simple language"""
    prompt = f"""
    Return only the main answer in plain English, no breakdowns or explanations
Explain these SQL query results in simple language for the question: "{user_query}"

Results:
{results}
    """
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content


st.title("💬 SQL Chatbot ")
st.markdown("Ask your database anything in natural language!")

# Sidebar for DB connection
with st.sidebar:
    st.header("🔗 Database Connection")
    user = st.text_input("User")
    password = st.text_input("Password", type="password")
    host = st.text_input("Host", "localhost")
    port = st.text_input("Port", "3306")
    database = st.text_input("Database")

    if st.button("Connect"):
        try:
            st.session_state.db = init_database(user, password, host, port, database)
            st.success("✅ Connected successfully!")
        except Exception as e:
            st.error(f"❌ Connection failed: {e}")

show_modify_section = st.checkbox("Modify database records?")
if show_modify_section:
    cursor = st.session_state.db.cursor()

    # Get all tables for user to select
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    selected_table = st.selectbox("Select a table", tables)

    if selected_table:
        # Fetch columns of selected table
        cursor.execute(f"SHOW COLUMNS FROM {selected_table}")
        columns = [row[0] for row in cursor.fetchall()]

        operation = st.radio("Choose operation", ["Insert", "Update", "Delete"])

        if operation == "Insert":
            selected_columns = st.multiselect("Select columns to insert into", columns)
            if selected_columns:
                insert_columns = ", ".join(selected_columns)
                insert_values = st.text_input("Enter values (comma separated) for insertion")
                if st.button("Insert Data"):
                    try:
                        placeholders = ", ".join(["%s"] * len(selected_columns))
                        sql = f"INSERT INTO {selected_table} ({insert_columns}) VALUES ({placeholders})"
                        values = tuple(val.strip() for val in insert_values.split(","))
                        cursor.execute(sql, values)
                        st.session_state.db.commit() 
                        st.success("Record inserted successfully!")
                        time.sleep(2)
                        st.rerun()

                    except Exception as e:
                        st.error(f"Insertion failed: {e}")

        elif operation == "Update":
            key_column = st.selectbox("Select column for WHERE clause (to identify record)", columns)
            key_value = st.text_input(f"Value of {key_column} to update")
            update_column = st.selectbox("Select column to update", columns)
            new_value = st.text_input(f"New value for {update_column}")
            if st.button("Update Data"):
                try:
                    sql = f"UPDATE {selected_table} SET {update_column} = %s WHERE {key_column} = %s"
                    cursor.execute(sql, (new_value, key_value))
                    st.session_state.db.commit()
                    st.success("Record updated successfully!")
                    time.sleep(2)
                    st.rerun() 
                    
                    
                except Exception as e:
                    st.error(f"Update failed: {e}")

        elif operation == "Delete":
            key_column = st.selectbox("Select column for WHERE clause (to identify record)", columns)
            key_value = st.text_input(f"Value of {key_column} to delete")
            if st.button("Delete Data"):
                try:
                    sql = f"DELETE FROM {selected_table} WHERE {key_column} = %s"
                    cursor.execute(sql, (key_value,))
                    st.session_state.db.commit()
                    st.success("Record deleted successfully!")
                    time.sleep(2)
                    st.rerun() 
                    
                   
                except Exception as e:
                    st.error(f"Deletion failed: {e}")


# Main chat interface
if "db" in st.session_state:
    user_query = st.text_input("Type your question:")

    if st.button("Run Query"):
        try:
            cursor = st.session_state.db.cursor()

            table_schema = extract_schema(cursor)


            # Step 1: Generate SQL
            sql_query = generate_sql(user_query, table_schema)
            st.code(sql_query, language="sql")

            # Step 2: Execute SQL
            cursor.execute(sql_query)
            results = cursor.fetchall()

            # Step 3: Explain results
            explanation = explain_results(results, user_query)

            # Step 4: Display results
           
            st.write(explanation)  



        except Exception as e:
            st.error(f"❌ Error: {e}")
