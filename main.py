import time
import streamlit as st
import time
import os
import requests
import json

PROJECT_ID = os.environ['PROJECT_ID']
ENDPOINT_RESPONSES = os.environ['ENDPOINT_RESPONSES']
if 'page_title' not in os.environ:
    os.environ['page_title'] = 'Bagel Bot'

from app_logger import AppLogger
logger_name = f'{PROJECT_ID}-client-streamlit-logger'
logger = AppLogger(logger_name)
logger.log_text(f'Initialized logger: {logger_name} PROJECT_ID: {PROJECT_ID}')

def get_session_id() -> str:
    return hash(str(time.time()).replace('.', ''))

def create_response_item(prefix: str, text: str):
  return f'{prefix} {text}'

def main():

    # Generate a unique user ID if it hasn't been created yet
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = get_session_id()

    user_id = st.session_state['user_id']

    # create a storage for the conversation thread
    if 'convo_thread' not in st.session_state:
        st.session_state['convo_thread'] = []

    st.title(os.environ['page_title'])
    text_input = st.text_input('Ask me a question about bagels!')

    if st.button('Submit'):
        # build url
        url = f'{ENDPOINT_RESPONSES}?user_id={user_id}&query_str={text_input}'

        # request url
        try:
            with st.spinner("Sending..."):
              res = requests.get(url).json()
              time.sleep(1)
        except Exception as e:
            msg = f'{PROJECT_ID}: error requesting {url}: {e}'
            st.write(msg)
            print(msg)
            raise e
        else:
          st.session_state['convo_thread'].insert(0, create_response_item('A: ', res["response"],))
          st.session_state['convo_thread'].insert(0, create_response_item('Q: ', text_input,))
          print(st.session_state['convo_thread'])
          for qa in st.session_state['convo_thread']:
            st.write(qa)
    
if __name__ == "__main__":
    logger.log_text('Starting streamlit app')
    main()
