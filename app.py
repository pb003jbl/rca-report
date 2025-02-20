import streamlit as st
import dspy
import pandas as pd
import workers as wrk
import time as t


# Streamlit App Title
st.title("RCA AI Assistant")

doc = """
    Root Cause Analysis
    Overview
    Problem Statement
    Incident Details
    Root Cause Identification
    Analysis of Causes
    Corrective Actions and Preventive Measures
    Impact Analysis
    Lessons Learned and Continuous Improvement
    Documentation and Communication
    Appendices
    """
master_dataset = None
report= None
# chatMode = None
# with st.sidebar:
#         option = st.selectbox(
#             "Select Mode?",
#             ("Chat", "Report"),index=0
#         )
#         chatMode=option
#         st.write("Agent Mode :", option)
        
with st.sidebar:
    # File Uploader
    uploaded_file = st.file_uploader("Upload your dataset", type=["xlsx", "csv"])
    if uploaded_file:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
      
        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        st.write("### Preview of Uploaded Dataset:")
        st.dataframe(df.head())
        master_dataset=df

with st.sidebar:
    #Report Template
    doc = st.text_area('Report Template')
    st.markdown("Current report template : ")
    st.markdown(doc)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def genReport(prompt):
    result = wrk.genReport(master_dataset,doc,prompt)
    return result




# React to user input
st.chat_message("assistant").markdown(f"Hi, I am a helpful assistant. I can generate report on a dataset using provided template.")
if prompt := st.chat_input("Enter a report topic"):
    # Display user message in chat message container
    #Generate report on dataset
    # st.button('Generate Report on the dataset',key='reportButton',on_click=genReport())

    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # if chatMode == 'Chat':
    #     response = wrk.invokeAssistant(prompt)
    #     with st.chat_message("assistant"):
    #         st.markdown(f"{response.get('answer')}")
    # elif chatMode == 'Report':
    #     response = ag.invokeEditor(prompt)
    #     with st.chat_message("assistant"):
    #         st.markdown(f"{response.get('report')}")

    # Display assistant response in chat message container
    
    
    response = genReport(prompt=prompt)
    with st.chat_message("assistant"):
            st.markdown(f"{response.title}")
            for content in response.sections:
                st.markdown(f"{content}")
                
        
    # Add assistant response to chat history
    # st.session_state.messages.append({"role": "assistant", "content": response.title})
    # st.session_state.messages.append({"role": "assistant", "content": response.sections})
