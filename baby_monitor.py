#Importing required Libraries
import time, conf
import sounddevice as sd
import soundfile as sf
import pyloudnorm as pyln
from scipy.io.wavfile import write
from boltiot import Bolt

#Setup
count = 1 #counter
fs = 44100 #Sample Rate
seconds = 4 #Recording time
mybolt = Bolt(conf.BOLT_API_KEY, conf.DEVICE_ID) #


# Function for recording and saving audio
def record_and_save_audio():
	try:
		print('Recording Started')
		recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2) # Recording audio
		sd.wait() #Waiting till the recording is finished
		write('output.wav', fs, recording) #Saving the recorded audio in .wav format
		print('Recording ended')

	except KeyboardInterrupt:
		print("Recording ended")
		pass


# Function for measuring loudness of audio file
# Using LUFS (Loudness units relative to Full Scale) to measure loudness
def get_loudness():
	data, rate = sf.read("output.wav") #Reading the saved file
	meter = pyln.Meter(rate) #Making a meter (Required in LUFS)
	loud = meter.integrated_loudness(data) #Measuring Loudness
	return loud


# Function for buzzing according to previous and current values of loudness
def buzz(previous_loudness, current_loudness):
	if current_loudness >= previous_loudness + 8 or current_loudness > -38:
		print("Baby awake....Alerting")
		mybolt.digitalWrite('0', 'HIGH')
		time.sleep(3)
		mybolt.digitalWrite('0', 'LOW')


while True:
	record_and_save_audio()

	# For the 1st recording
	if count == 1:
		current_loudness = get_loudness()
		previous_loudness = current_loudness
		count = 0

	# For other recordings
	else:
		previous_loudness = current_loudness
		current_loudness = get_loudness()

	buzz(previous_loudness, current_loudness)
	time.sleep(3)