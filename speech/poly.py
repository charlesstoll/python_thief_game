"""
Used to get an mp3 file with speech amazon poly"
Last Updated: 21 Februaruy 2019
Author: Emma Smith
"""
import boto3
from pygame import mixer
import os

def main (data):
	polly = boto3.client('polly')
	spoken_text = polly.synthesize_speech(Text = data, OutputFormat = 'mp3', VoiceId = 'Matthew')
	with open('output.mp3', 'wb') as f:
		f.write(spoken_text['AudioStream'].read())
		f.close()
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

if __name__ == '__main__':
	main("i guess i'll go left")
	


