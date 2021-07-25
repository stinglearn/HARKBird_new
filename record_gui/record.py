import PySimpleGUI as sg
import subprocess
import os
import time
import signal
import pyaudio
import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound

def getaudiodevices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        return(p.get_device_info_by_index(i).get('name'))

layout = [
            [sg.Text("Directory", size=(15, 1)), sg.FolderBrowse()],
            [sg.Text("Filename"),sg.InputText(size =(10,2)),sg.Text("time"),sg.InputText(size=(8,2)),sg.Text("rate"),sg.InputText(size=(8,2))],
            [sg.Button("Check Device"),],
            [sg.Button('Record'),sg.Button("Exit"),sg.Button("play")]
         ]

window = sg.Window('Record', layout,size=[500,200])

while True:             # Event Loop
    event, values = window.read()
    dir = values["Browse"]
    wavname =values[0]
    if values[1]:
        time = int(values[1])
    if values[2]:
        fs = int(values[2])
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event =="Check Device" :
        sg.popup_scrolled(getaudiodevices())
    if event == 'Record' :
        myrecording = sd.rec(int(time * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write(dir+"/"+wavname, fs, myrecording)
    if event =="play" :
        play_file =sg.popup_get_file("choose a file to play")
        playsound(play_file)

window.close()
