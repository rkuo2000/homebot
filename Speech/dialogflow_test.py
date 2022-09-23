### $pip3 install Dialogflow
import speech_recognition as sr
import dialogflow_v2 as dialogflow
import sys
import random

PROJECT_ID = "homedroid-228703"

random.seed(0x228703)

# Dialogflow detect intent
def detect_intent_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(response.query_result.intent.display_name, response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))

session_id = str(random.random())[2:]
text = "Hello"
sl = "en"
detect_intent_text(PROJECT_ID, session_id, text, sl)
