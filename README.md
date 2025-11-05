# SQL Chatbot:
  An interactive AI-powered SQL Chatbot built using Streamlit, MySQL, and Groq API.
  This project allows users to interact with a connected MySQL database using natural language queries — no need to write SQL manually!
  The chatbot intelligently generates, executes, and displays results for SQL queries while providing insights into database structure.

# Features:
   * AI-Powered Query Generation — Converts user questions into valid SQL queries using Groq API.
   * Database Schema Extraction — Automatically fetches tables and column details from a connected MySQL database.
   * Dynamic Data Interaction — Insert, update, and delete data directly from the chatbot interface.
   * Streamlit UI — Clean and simple web interface for seamless user experience.
   * Secure Connection — Credentials and queries handled safely to prevent injection risks.

# Tech Stack:
| Component       | Technology   |
| --------------- | ------------ |
| Frontend/UI     | Streamlit    |
| Backend         | Python       |
| Database        | MySQL        |
| AI Engine       | Groq API     |
| Version Control | Git + GitHub |

# Project Structure:
``` bash
SQL-chatboat/
│
├── src/
│   └── app.py              # Main Streamlit app (UI + logic)
│
├── db.sql                  # Database schema file
│
├── data_inserted/          # Folder storing inserted/exported data
│
├── .git/                   # Git version control directory
└── README.md               # Project documentation
```
# Installation & Setup : 
  * Install Dependencies:
          ```
     pip install streamlit mysql-connector-python groq
         ```
  * Run the Application
     ```streamlit run app.py```
   ,Then open the local URL (e.g., http://localhost:8501) in your browser.
# How It Works:
  * User connects to a MySQL database by entering connection details in the sidebar.
  * The app extracts the database schema (tables and columns) using SQL commands.
  * User types a natural language question (e.g., “Show all students”).
  * The question and schema are sent to the Groq API, which generates the corresponding SQL query.
  * The generated SQL query is executed on the connected database.
  * Query results are fetched and displayed in the Streamlit interface.
  * Groq API also provides a simple explanation of the results in plain English.
  * Optional section allows users to Insert, Update, or Delete records directly from the interface.
  * After each modification, the page refreshes automatically to show updated data.
# Future Enhancements
   * Data visualization for query results
   * Query history tracking
   * Authentication system for multi-user access  
