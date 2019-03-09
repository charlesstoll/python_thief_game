import dialogflow_v2 as dialogflow
import os
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
    return response.query_result.fulfillment_text



current_directory = os.getcwd()
credentials = os.path.join(current_directory, 'gameplay-32385-fdc504fdecef.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
result = detect_intent_texts(project_id, "1-1-1-1-1", ["go right"], 'en-US')
print result
