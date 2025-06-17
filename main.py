import streamlit as st
from langchain_helper import get_few_shot_db_chain

st.title("GUTH T Shirts: Database Q&A 👕")

# Initialize chain once and store in session state
if 'chain' not in st.session_state:
    with st.spinner('Initializing the AI system...'):
        try:
            chain = get_few_shot_db_chain()
            st.session_state.chain = chain
            st.success('System initialized successfully!')
        except Exception as e:
            st.error(f'Failed to initialize the system: {str(e)}')
            st.session_state.chain = None

question = st.text_input("Ask a question about the t-shirt inventory:", 
                        placeholder="e.g., How many white Levi's shirts do we have?")

# Display some example questions
with st.expander("💡 Example Questions"):
    st.write("""
    - How many t-shirts do we have left for Nike in XS size and white color?
    - How much is the total price of the inventory for all S-size t-shirts?
    - If we have to sell all the Levi's T-shirts today with discounts applied, how much revenue will our store generate?
    - How many white color Levi's shirts do I have?
    - How much sales amount will be generated if we sell all large size t-shirts today in Nike brand after discounts?
    """)

# Process the question
if question and st.session_state.get('chain'):
    with st.spinner('Processing your question...'):
        try:
            response = st.session_state.chain({"question": question})
            
            st.header("Answer")
            st.write(response)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try rephrasing your question or check your database connection.")

elif question and not st.session_state.get('chain'):
    st.warning("System not initialized. Please refresh the page.")

st.markdown("---")
st.markdown("*Powered by LangChain and Google Gemini*")