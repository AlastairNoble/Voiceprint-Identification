from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import os
import shutil
from playsound import playsound


def clear_audio(path):
    """
    Empties a specified directory
    Args:
        path: str
            specified directory

    Returns: NULL

    """

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def separate_words(sound_file_name):
    """
    Separates an audio into constituent words and places them into splitAudio folder
    Args:
        sound_file_name: str
            Name of the audio file

    Returns:
        out_files: list
             list of files created (str)

    """
    sound_file = AudioSegment.from_wav(sound_file_name)
    # min_silence_len=time in milliseconds, silence_thresh=what the comp classifies as silence in dB
    audio_chunks = split_on_silence(sound_file, min_silence_len=50, silence_thresh=(int(sound_file.dBFS) - 10))

    clear_audio("./splitAudio")
    out_files = []
    for i, chunk in enumerate(audio_chunks):
        if chunk.dBFS > -70: # only write file if volume is above silence threshold
            out_file = f"./splitAudio//chunk{i}.wav"
            out_files.append(out_file)
            # print("Exporting", out_file) # Check to see exporting
            chunk.export(out_file, format="wav")
    # print(f"Exported {numWords} .wav files")
    # CONVERT AUDIO TO TEXT -------------
    # initialize the recognizer

    """
    r = sr.Recognizer()

    # open the file
    with sr.AudioFile(sound_file_name) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)
    """
    # print("Start")
    # playsound(sound_file_name)
    # print("End")

    return out_files