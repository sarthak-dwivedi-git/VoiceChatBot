from tkinter import *
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
import pyttsx3
import speech_recognition
import threading

bot=ChatBot('Bot')
trainer=ListTrainer(bot)
for files in os.listdir('data/Conversation'):
    data=open('data/Conversation/'+files,'r',encoding='utf-8').readlines()
    trainer.train(data)


def botReply():
    question=questionField.get()
    question=question.capitalize()
    answer=bot.get_response(question)
    textArea.insert(END,'You: '+question+'\n\n')
    textArea.insert(END,'Bot: '+str(answer)+ '\n\n')

    engine = pyttsx3.init()
    rate = 150
    engine.setProperty('rate', rate)

    engine.say(answer)
    engine.runAndWait()
    questionField.delete(0,END)



def audioToText():
    sr = speech_recognition.Recognizer()
    while True:
        try:
            with speech_recognition.Microphone()as m:
                sr.adjust_for_ambient_noise(m,duration=0.2)
                audio=sr.listen(m)
                query=sr.recognize_google(audio)

                questionField.delete(0,END)
                questionField.insert(0,query)
                botReply()

        except Exception as e:
            print(e)

def listen_to_speech():
    t = threading.Timer(0, audioToText)
    t.daemon = True
    t.start()


root = Tk()

root.geometry('500x570+100+30')
root.title('Chatbot created by V.O.I.D.')
root.config(bg='LightSkyBlue2')


logoPic=PhotoImage(file='pic.png')
logoPicLabel=Label(root,image=logoPic,bg='LightSkyBlue2')
logoPicLabel.pack(pady=5)


centerFrame=Frame(root)
centerFrame.pack()



scrollBar=Scrollbar(centerFrame)
scrollBar.pack(side=RIGHT)


textArea=Text(centerFrame,font=('times new roman','15'),height=10,yscrollcommand=scrollBar.set,wrap='word')
textArea.pack(side=LEFT)
scrollBar.config(command=textArea.yview)


questionField=Entry(root,font=('arial','15'))
questionField.pack(pady=15,fill=X)

askPic=PhotoImage(file='ask.png')
askButton=Button(root,image=askPic,command=botReply)
askButton.pack()

def click(event):
    askButton.invoke()


root.bind('<Return>',click)

thread = threading.Thread(target=listen_to_speech)
thread.daemon = True
thread.start()

root.mainloop()

