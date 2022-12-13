#Importing required Libraries
import time, conf
import sounddevice as sd
import soundfile as sf
import pyloudnorm as pyln
from scipy.io.wavfile import write
from boltiot import Bolt

#Setup
i = 1
fs = 44100
seconds = 4
mybolt = Bolt(conf.BOLT_API_KEY, conf.DEVICE_ID)


# Function for recording and saving audio
def record_and_save_audio():
	try:
		print('Recording Started')
		recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
		sd.wait()
		write('output.wav', fs, recording)
		print('Recording ended')

	except KeyboardInterrupt:
		print("Recording ended")
		pass


# Function for measuring loudness of audio file
# Using LUFS (Loudness units relative to Full Scale) to measure loudness
def get_loudness():
	data, rate = sf.read("output.wav")
	meter = pyln.Meter(rate)
	loud = meter.integrated_loudness(data)
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
	if i == 1:
		current_loudness = get_loudness()
		previous_loudness = current_loudness
		i = 0

	# For other recordings
	else:
		previous_loudness = current_loudness
		current_loudness = get_loudness()

	buzz(previous_loudness, current_loudness)
	time.sleep(3)