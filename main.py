import socket
import speech_recognition as sr
import requests
import time
from pygame import mixer
from queue import PriorityQueue
from queue import Queue

import config
import Get_word_dictionary as gwd

wordTestQueue = PriorityQueue()
wordList = Queue()
word_list = {}

def read_file():
    with open("data.txt", 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for i in lines:
            result = i.split(' ', maxsplit = 1)
            word_list[result[0]] = result[1][:-1]

def exchange_message(message:str):
    mList = message.split()
    value = ""
    for i in mList:
        if i in word_list:
            value = value + word_list[i] + " "
            wordTestQueue.put((time.time(), (300, i)))
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
        if wordTestQueue.empty() is False:
            while True: 
                if wordTestQueue.empty() is True:
                    break
                tmp = wordTestQueue.get()
                if time.time() > tmp[0]:
                    gwd.Get_Need_Content(tmp[1][1])
                    conn.send(bytes('2 ' + tmp[1][1], 'utf-8'))
                    time.sleep(0.5)
                    conn.send(bytes('3 ' + gwd.meaning_of_word, 'utf-8'))
                    wordTestQueue.put((tmp[0] + tmp[1][0] * 10, (tmp[1][0] * 10, tmp[1][1])))
                    print_message = f"{tmp[1][1]}의 의미는 {gwd.meaning_of_word} 입니다."
                    url = "https://tts-translate.kakao.com/newtone?message=" + print_message + "&format=wav-16k"
                    music = requests.get(url)
                    with open(config.audio_file_name, 'wb') as f:
                        f.write(music.content)
                    mixer.music.load(config.audio_file_name)
                    mixer.music.play()
                    while mixer.music.get_busy():  # wait for music to finish playing
                        time.sleep(1)
                    mixer.music.unload()
                else:
                    wordTestQueue.put(tmp)
                    break
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening to your voice : ")
            audio = r.listen(source)
        
        message = ""
        try:
            message = r.recognize_google(audio, language='ko')
        except:
            print("Recognition Error.")
            continue
        
        conn.send(bytes('0 ' + message, 'utf-8'))
        time.sleep(0.5)

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
        time.sleep(0.5)
        

    conn.close()


if __name__ == "__main__":
    init_all()
    read_file()
    main()