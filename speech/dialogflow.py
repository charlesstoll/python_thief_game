import dialogflow_v2 as dialogflow
import os
import boto3
import sys
from pygame import mixer
project_id = "gameplay-32385"

def detect_intent_audio(project_id, session_id, audio_file_path,
                        language_code):
    """
    Returns response to audio file
    """
	
    session_client = dialogflow.SessionsClient()

    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 44100

    session = session_client.session_path(project_id, session_id)

    with open(audio_file_path, 'rb') as audio_file:
        input_audio = audio_file.read()

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)
    query_input = dialogflow.types.QueryInput(audio_config=audio_config)

    response = session_client.detect_intent(
        session=session, query_input=query_input,
        input_audio=input_audio)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
			response.query_result.intent.display_name,
			response.query_result.intent_detection_confidence))

    print ("Response should be: ", response.query_result.fulfillment_text, "\n")
    reply = response.query_result.fulfillment_text + "\n"
    with open('intent_output.txt', 'w') as f:
      f.write('{}'.format(response.query_result.intent.display_name))
      f.close()

    return response.query_result.fulfillment_text
	
	
def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
			response.query_result.intent.display_name,
			response.query_result.intent_detection_confidence))

        print('Response should be: ')
        print(response.query_result.fulfillment_text)
        print('\n')
        speak(response.query_result.fulfillment_text)
    return response.query_result.intent.display_name

def record(seconds, filename):
    command = "arecord -f S16_LE -c1 -r44100 -d " + str(seconds) + " " + filename
    os.system(command)

def speak (data):
    polly = boto3.client('polly')
    spoken_text = polly.synthesize_speech(Text = data, OutputFormat = 'mp3', VoiceId = 'Matthew')
    with open('output.mp3', 'wb') as f:
        f.write(spoken_text['AudioStream'].read())
        f.close()
    command = "mpg321 output.mp3"
    os.system(command)

# Will not work on my linux distributable
"""
	mixer.init()
	mixer.music.load('output.mp3')
	mixer.music.play()
	
	while mixer.music.get_busy() == True:
		pass
	mixer.quit()
	os.remove('output.mp3')
"""
if len(sys.argv) <= 1:
  print("not enough arguments present")

if sys.argv[1] == "example":
  current_directory = os.getcwd()
  credentials = os.path.join(current_directory, 'gameplay-32385-fdc504fdecef.json')
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
  result = detect_intent_texts(project_id, "1-1-1-1-1", ["go right"], 'en-US')
  print(str(result))

if sys.argv[1] == "speak":
  text = ""
  i = 2
  while i < len(sys.argv):
    text = text + sys.argv[i]
    if not i == len(sys.argv) - 1:
      text = text + " "
    i = i + 1
  print("the text I got was: " + text)
  speak(text)

if sys.argv[1] == "record":
  seconds = int(sys.argv[2])
  filename = sys.argv[3]
  record(seconds, filename)
  current_directory = os.getcwd()
  credentials = os.path.join(current_directory, 'gameplay-32385-fdc504fdecef.json')
  audio_path = os.path.join(current_directory, filename)
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
  result = detect_intent_audio(project_id, "1-1-1-1-1", audio_path, 'en-US')







