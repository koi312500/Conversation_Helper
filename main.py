import socket
import speech_recognition as sr
import requests
import time
from pygame import mixer
from queue import PriorityQueue

import config

que = PriorityQueue()
word_list = {}

def read_file():
    with open("data.txt", 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for i in lines:
            result = i.split(' ', maxsplit = 1)
            word_list[result[0]] = result[1]

def exchange_message(message:str):
    mList = message.split()
    value = ""
    for i in mList:
        if i in word_list:
            value = value + word_list[i] + " "
        else:
            value = value + i + " "
    return value
    
def init_all():
    global conn
    HOST = ''  
    PORT = 15625 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    print('Connected by', addr)
    data = conn.recv(1024).decode()
    print(data)
    if data == "Client Hello":
        print("Hello Message was received.")
    
    mixer.pre_init(44100, 16, 2, 4096)
    mixer.init()

def main():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening to your voice : ")
            audio = r.listen(source)
        
        message = ""
        try:
            message = r.recognize_google(audio, language='ko')
        except:
            print("Recognition Error.")
        
        conn.send(bytes('0 ' + message, 'utf-8'))
        print("Message sented.")
        time.sleep(0.5)
        data = conn.recv(1024).decode()
        print("Message receive to client.")

        changed_message = exchange_message(message)
        url = "https://tts-translate.kakao.com/newtone?message=" + changed_message + "&format=wav-16k"
        music = requests.get(url)
        with open(config.audio_file_name, 'wb') as f:
            f.write(music.content)
        conn.send(bytes('1 ' + changed_message, 'utf-8'))
        mixer.music.load(config.audio_file_name)
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
        mixer.music.unload()
        

    conn.close()


if __name__ == "__main__":
    init_all()
    read_file()
    main()