# 🧠 Natural Language to SQL Query App

An intelligent application built using **LangChain**, **Gemini API**, and **FAISS**, powered by a **Streamlit interface**. This app allows users to ask human-like questions, which are automatically translated into SQL queries, executed on a connected SQL database, and returned with precise answers.

---

## 🚀 Features

- 💬 Converts **natural language questions** into SQL queries
- ⚙️ Executes queries directly on a connected **SQL database**
- 🧠 Uses **Gemini API** and **LangChain** for language understanding and query generation
- 📦 Optimized with **few-shot prompting**, converted into embeddings
- 🔍 Performs **semantic similarity search** using **FAISS vector database**
- 🖥️ Easy-to-use **Streamlit UI** for interactive querying

---

## 🛠️ Tech Stack

- **LLM Framework**: LangChain
- **LLM API**: Gemini API (Google's large language model)
- **Vector Store**: FAISS (for embedding-based retrieval)
- **Frontend**: Streamlit
- **Database**: Any SQL-compatible database (e.g., PostgreSQL, MySQL)

---

## 🧠 How It Works

1. **User Input**: A user types a natural language question into the Streamlit interface.
2. **Prompt Engineering**: The system uses **few-shot prompting examples** stored as embeddings in FAISS.
3. **Similarity Search**: FAISS retrieves the most relevant prompt examples.
4. **Query Generation**: LangChain + Gemini use those examples to generate an accurate SQL query.
5. **Execution**: The SQL query is run against the connected database.
6. **Response**: The final answer is displayed to the user.

---

## 📦 Status

- Core functionality complete ✅  
- Few-shot prompting with FAISS working ✅  
- SQL execution integrated ✅  
- UI live on Streamlit (local) ✅  
- Deployment options in progress 🚧

---

## 📌 Notes

- The system is easily extendable to support new schemas and database structures.
- Ideal for business analysts, internal dashboards, or non-technical users querying data.




![image](https://github.com/user-attachments/assets/9873e06e-7b12-40fb-8762-a3ee28a8b013)
