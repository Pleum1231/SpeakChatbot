import speech_recognition as sr
import os
import playsound
import random
import time
from datetime import datetime
from googletrans import Translator
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from gtts import gTTS

print(str(datetime.now())+' Start')

#ตั้งชื่อ bot
chatbot = ChatBot('R2D2')

#สร้างเทรนเนอร์สอน
chatbot.set_trainer(ChatterBotCorpusTrainer)

#สอนภาษาอังกฤษ
#print(str(datetime.now())+' สอนภาษาอังกฤษ')
#chatbot.train("chatterbot.corpus.english")

#พูดออกลำโพง
def speak(word):
    #สร้างชื่อไฟล์จากเวลา
    now = datetime.now()
    timestamp = datetime.timestamp(now)

    #สร้างเสียงพูด
    tts=gTTS(text=word,lang='th')
    
    #บันทึกไฟล์เป็นmp3
    mp3 = str(timestamp) + '.mp3'
    tts.save(mp3)

    #เล่นไฟล์mp3
    playsound.playsound(mp3,True)

    #ลบไฟล์
    os.remove(mp3)

#ตัวแปรไว้แปลภาษา
translator = Translator()

#ตัวแปรไว้รับเสียง
r = sr.Recognizer()
    
check = True
speak('สวัสดีวีรภัทร')    
while check:
        #1.รอรับเสียง
        print(str(datetime.now())+' 1.รอรับเสียงพูดจากไมค์')
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration = 1)
            print('พูดได้')
            audio = r.listen(source)
                
        try:
            #2.แปลงเสียงเป็นข้อความไทย
            print(str(datetime.now())+' 2.แปลงเสียงเป็นข้อความภาษาไทย')
            said = r.recognize_google(audio,None,'th')
            print(str(datetime.now())+' ข้อความที่ได้ : ' +said)

            #3.แปลงไทยเป็นอังกฤษ
            print(str(datetime.now())+' 3.แปลงภาษาไทยเป็นภาษาอังกฤษ')
            thaiTOenglish = translator.translate(said,src='th',dest='en')
            print(str(datetime.now())+' ข้อความที่ได้ : ' + thaiTOenglish.text)

            #4.เรียก chatbot
            print(str(datetime.now())+' 4.เรียกchatbot')
            response = chatbot.get_response(thaiTOenglish.text)
            print(str(datetime.now())+' ข้อความที่ได้ : '+str(response))

            #5.แปลงอังกฤษเป็นไทย
            print(str(datetime.now())+' 5.แปลภาษาอังกฤษเป็นภาษาไทย')
            englishTOthai = translator.translate(str(response),src='en',dest='th')
            print(str(datetime.now())+' ข้อความที่ได้ : ' +englishTOthai.text)

            #6.นำข้อความแปลงเป็นเสียงออกลำโพง
            print(str(datetime.now())+' 6.นำข้อความแปลงเป็นเสียงออกลำโพง')

            speak(englishTOthai.text)
            print(str(datetime.now())+ '----------------------------------------------------')

            word=thaiTOenglish.text
            if word == 'Bye':
                check = False


        except Exception as e:
            print(str(datetime.now()) + ' Error! ' + str(e))
            break