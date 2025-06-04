import streamlit as st
import boto3
import logging
import uuid
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = boto3.client(
        'bedrock-agent-runtime', 
        'us-east-1'
)
      

agent_id = "PDAC00CSHO"
agent_alias_id = "AKMHICVSSP"

# Generate session ID on first load
if "session_id" not in st.session_state:
    #st.session_state.session_id = str(uuid.uuid4())
    st.session_state.session_id = str(uuid.uuid1())
    logger.info(f"Generated new session ID: {st.session_state.session_id}")

def invoke_bedrock_agent(user_input):
    """
    Calls AWS Bedrock agent and returns the completion.
    """
    try:
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=st.session_state.session_id,
            inputText=user_input,
        )

        completion = ""

        for event in response.get("completion", []):
            chunk = event["chunk"]
            completion += chunk["bytes"].decode()

        return completion
    except ClientError as e:
        logger.error(f"Couldn't invoke agent. {e}")
        st.error(f"Error calling AWS Bedrock Agent: {e}")
        return None


# Streamlit app setup
st.set_page_config(page_title="RANHILL POC", page_icon="💬")

st.title("💬 RANHILL Chatbot POC")


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['text'])


questions = st.chat_input('Enter you questions here...')
if questions:
    with st.chat_message('user'):
        st.markdown(questions)
    st.session_state.chat_history.append({"role":'user', "text":questions})


    response = invoke_bedrock_agent(questions)
    # st.write(response)
    #answer = response['output']['text']

    with st.chat_message('assistant'):
        st.markdown(response)
    st.session_state.chat_history.append({"role":'assistant', "text": response})