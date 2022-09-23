### $pip3 install SpeechRecognition
### $pip3 install PyAudio
### $pip3 install Dialogflow
import speech_recognition as sr
import dialogflow_v2 as dialogflow
import sys
import random

sl = sys.argv[1]
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# defines for Dialogflow
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
    print('Query text: {}\n'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(response.query_result.intent.display_name, response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))

def speech2text():
    print("Speak:")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language=sl)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio!")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
			
if __name__ == "__main__":
    while True:
        text  = speech2text()
        session_id = str(random.random())[2:]
        detect_intent_text(PROJECT_ID, session_id, text, sl)
        print("--------------------------------------------")
