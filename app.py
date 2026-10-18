import streamlit as st
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv(r'D:\Learning\TuteDude2026\Python\Assignments\.env')
import wikipedia
wikipedia.set_user_agent("myproject/1.0 (contact: abhishek0465@gmail.com)")
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


st.sidebar.title("My First AI-Agent")
st.sidebar.subheader("Use it for Wiki Search, Google Search or Simple Calculations.")
model_selection = st.sidebar.selectbox("Select Your Model",['openai','groq'])
if model_selection=='openai':
   openai_api_key = st.sidebar.text_input("Provide you OpenAI API Key",type='password')
   if openai_api_key:
      llm=ChatOpenAI(model='gpt-4o',api_key=openai_api_key)
else:
   llm=ChatGroq(model='openai/gpt-oss-20b')
@tool
def addition(a:int,b:int)->int:
    """ Adds 2 numbers """
    return a+b
@tool
def multiplication(a:int,b:int)->int:
    """ Multiplies 2 numbers """
    return a*b
search_tool = DuckDuckGoSearchResults()
wiki_wrapper = WikipediaAPIWrapper()
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)

def generate_response(query):
   result = agent.invoke({'messages':[
      {'role':'user','content':query}
   ]})
   return result['messages'][-1].content
if model_selection=='groq' or (model_selection=='openai' and openai_api_key):
    agent = create_agent(model=llm,tools=[addition,multiplication,search_tool,wiki_tool],
                     system_prompt="""You are a helpful assistant. Use your tools when necessary to
                                                      find accurate information.""")

# Initialize chat history in session state
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

prompt = st.chat_input("Say something...")

# Action triggered on submit
if prompt:
  # 1. Save and display the user's message
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # 2. Run an action for the assistant response
  response_text = generate_response(prompt)

  # 3. Save and display the assistant's message
  st.session_state.messages.append(
      {"role": "assistant", "content": response_text}
  )
  with st.chat_message("assistant"):
    st.markdown(response_text)
