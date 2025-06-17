from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from few_shots import few_shots
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_few_shot_db_chain():
    try:
        st.write("🔗 Connecting to database...")
        # Database connection
        db_user = "root"
        db_password = "root"
        db_host = "localhost"
        db_name = "atliq_tshirts"
        db = SQLDatabase.from_uri(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
            sample_rows_in_table_info=3
        )
        st.write("✅ Database connected!")
        
        st.write("🤖 Initializing LLM...")
        # Initialize the LLM
        llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.environ["GOOGLE_API_KEY"],
            temperature=0.1
        )
        st.write("✅ LLM initialized!")
        
        st.write("🧠 Loading embeddings model (this may take a moment)...")
        embeddings = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-MiniLM-L6-v2',
            model_kwargs={'device': 'cpu'}
        )
        st.write("✅ Embeddings loaded!")
        
        st.write("📚 Creating FAISS vector store...")
        # Create FAISS vectorstore for few-shot examples
        to_vectorize = [" ".join(example.values()) for example in few_shots]
        vectorstore = FAISS.from_texts(
            texts=to_vectorize, 
            embedding=embeddings, 
            metadatas=few_shots
        )
        st.write("✅ FAISS vector store created!")
        
        st.write("🎯 Setting up example selector...")
        example_selector = SemanticSimilarityExampleSelector(
            vectorstore=vectorstore,
            k=2,
        )
        st.write("✅ Example selector ready!")
        
        # MySQL prompt template with clear instructions
        mysql_prompt = """You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run.

IMPORTANT INSTRUCTIONS:
- When providing the SQLQuery, return ONLY the SQL query without any prefixes
- Do not include "SQLQuery:" or any other labels in the actual query
- Query for at most {top_k} results using LIMIT clause when needed
- Never query for all columns, only columns needed to answer the question  
- Wrap column names in backticks (`) when needed
- Use only column names that exist in the tables
- Use CURDATE() for current date if needed

Here are some examples of the expected format:
"""
        
        example_prompt = PromptTemplate(
            input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
            template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
        )
        
        # Few-shot prompt template
        few_shot_prompt = FewShotPromptTemplate(
            example_selector=example_selector,
            example_prompt=example_prompt,
            prefix=mysql_prompt,
            suffix="Only use the following tables:\n{table_info}\n\nQuestion: {input}\nSQLQuery:",
            input_variables=["input", "table_info", "top_k"],
        )
        
        st.write("🔧 Finalizing chain setup...")
        
        # Function to clean SQL query from LLM output
        def clean_sql_query(query_text):
            """Clean the SQL query by removing format prefixes and extra whitespace"""
            prefixes_to_remove = [
                "SQLQuery:",
                "SQL Query:",
                "Query:",
                "SQL:",
            ]
            
            cleaned_query = query_text.strip()

            for prefix in prefixes_to_remove:
                if cleaned_query.startswith(prefix):
                    cleaned_query = cleaned_query[len(prefix):].strip()
            
            # Handle multi-line queries and extract just the SQL part
            lines = cleaned_query.split('\n')
            sql_lines = []
            
            for line in lines:
                line = line.strip()
                if line and not any(indicator in line.lower() for indicator in ['sqlresult:', 'answer:', 'question:']):
                    sql_lines.append(line)
            
            # Join all SQL lines
            cleaned_query = ' '.join(sql_lines)
            
            cleaned_query = cleaned_query.rstrip(';').strip()
            if cleaned_query and not cleaned_query.endswith(';'):
                cleaned_query += ';'
            
            return cleaned_query
        
        # Simple approach - just return a function that handles everything
        def simple_chain(inputs):
            question = inputs["question"]
            
            # Generate SQL query using few-shot prompting
            sql_chain = create_sql_query_chain(llm, db, prompt=few_shot_prompt)
            raw_query = sql_chain.invoke({"question": question})
            
            # Clean the query to remove format prefixes
            query = clean_sql_query(raw_query)
            
            st.write(f"🔍 Generated SQL: {query}")
            
            # Execute query
            try:
                result = db.run(query)
                st.write(f"📊 Query result: {result}")
            except Exception as e:
                result = f"Error executing query: {str(e)}"
                st.error(f"❌ SQL Error: {result}")
            
            # Generate final answer
            answer_prompt = f"""Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
            
            response = llm.invoke(answer_prompt)
            return response
        
        st.write("🎉 Chain ready!")
        return simple_chain
        
    except Exception as e:
        st.error(f"Error at step: {str(e)}")
        raise e