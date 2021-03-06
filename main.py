import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication

import re
import webbrowser
import speech_recognition
import os
import pyttsx3
import datetime
from translate import Translator
from num2words import num2words

import speech_recognition as sr
from speech_recognition import Recognizer

mic = sr.Microphone(device_index=1)

tts = pyttsx3.init()  # запуск инициализации озвучки
RU_VOICE_ID = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
# установка голоса из (windows)
tts.setProperty('voice', RU_VOICE_ID)  # выбор озвучки


class Window(QMainWindow):  # создание класса для приложения(удобнее, можно использовать вне класса)
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('Голосовой асистент ДАНИЛА')  # создание окна с надписью
        self.setGeometry(800, 200, 400, 100)  # установка размеров окна
        self.setFixedSize(400, 100)  # фиксированный размер окна

        self.main_text = QtWidgets.QLabel(self)  # добавление изменяющегося текста
        self.main_text.setText('Привет я голосовой асистент ДАНИЛА')  # установка текста
        self.main_text.move(10, 25)  # перемещение текста внутри окна
        self.main_text.adjustSize()  # выравнивание текста по длине самого текста

        self.new_text = QtWidgets.QLabel(self)  # добавление изменяющегося текста
        self.new_text.setText('')
        self.new_text.move(150, 55)
        self.new_text.adjustSize()

        self.sub_text = QtWidgets.QLabel(self)  # добавление текста для суммы
        self.sub_text.setText(' ')
        self.sub_text.move(50, 25)
        self.sub_text.adjustSize()

        self.run_button = QtWidgets.QPushButton(self)  # добавление кнопки для вызова преобразователя голоса
        self.run_button.setText('Сказать команду:')
        self.run_button.move(10, 50)
        self.run_button.adjustSize()
        self.run_button.clicked.connect(self.voice_asistant)  # связь между кнопкой и запуском асистента
        tts.say("Привет я голосовой асистент ДАНИЛА")
        tts.runAndWait()

    def voice_asistant(self):  # запуск самого асистента
        sr = speech_recognition.Recognizer()  # инициализация текстового преобразователя
        sr.pause_threshold = 0.5  # пауза между словами = 0.5 секунды
        oper = ""  # переменная для поиска слов(словосочетаний)
        translator = Translator(to_lang="Russian")
        try:

            with speech_recognition.Microphone() as mic:  # запуск преобразователя(микрофона)
                sr.adjust_for_ambient_noise(source=mic, duration=0.5)  # подавление шумов
                audio = sr.listen(source=mic)  # ввод голоса напрмую из микрофона
                oper = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
                # присваивание значения переменной для поиска слов
                self.new_text.setText(sr.recognize_google(audio_data=audio, language='ru-RU').lower())
                print(sr.recognize_google(audio_data=audio, language='ru-RU').lower())
                # напечатать то что сказали
                self.new_text.adjustSize()
                self.sub_text.setText(' ')  # отчиска текста для избежания наложения

            if (oper.find("Привет") >= 0) or (oper.find("Здравствуй") >= 0):  # добавление приветсвия
                tts.say("Привет")  # что будет говорить ассистент(Привет)
                tts.runAndWait()
                self.main_text.setText('Привет)')
                self.main_text.adjustSize()

            elif (oper.find("Пока") >= 0) or (oper.find("До свидания") >= 0):  # добавление функции - Пока(
                tts.say("Пока")
                tts.runAndWait()
                self.main_text.setText('Пока(')
                self.main_text.adjustSize()
                self.close()  # закрытие приложения

            elif (oper.find("открой мне диспетчер задач") >= 0) or \
                    (oper.find("открыть диспетчер задач") >= 0):  # открытие диспетчера задач(если слово найдено)
                tts.say("Открывается диспетчер задач")
                tts.runAndWait()
                self.main_text.setText('Открывается диспетчер задач')
                self.main_text.adjustSize()
                os.system('Taskmgr')  # командная строка = taskmgr

            elif (oper.find("открой настройки") >= 0) or (oper.find("открыть настройки") >= 0):  # открытие настроек
                tts.say("Открываются настройки системы")
                tts.runAndWait()
                self.main_text.setText('Открываются настройки системы')
                self.main_text.adjustSize()
                os.system('Control')  # командная строка = control

            elif (oper.find("выключи мой компьютер") >= 0) or (oper.find("выключи компьютер") >= 0):  # выключение компьютера
                tts.say("Выключается компьютер")
                tts.runAndWait()
                self.main_text.setText('Выключается компьютер')
                self.main_text.adjustSize()
                os.system('shutdown /s /t 60') # командная строка = shutdown -s


            elif (oper.find("поиск в интернете") >= 0) or (oper.find("найди в интернете") >= 0) or \
                    (oper.find("найти в интернете") >= 0):  # поисковый запрос в гугле
                all_word = ""  # введение новой переменной для теста
                split = oper.split(" ")  # разделение текста на слова по пробелам
                poisk = split[3:]  # (не учитывать первые три слова)
                for word in poisk:
                    all_word += word + " "  # сборка всего поискового запроса

                url = 'https://www.google.com/search?q=' + all_word  # url поискового запроса
                tts.say("Ищу в интернете ваш запрос" + all_word)
                tts.runAndWait()
                self.main_text.setText('Ищу в интернете ваш запрос:' + all_word)
                self.main_text.adjustSize()
                webbrowser.open_new(url)  # открыть браузер с писковым запросом(url)

            elif oper.find("что такое") >= 0:  # поисковый запрос в гугле
                all_word = ""  # введение новой переменной для теста
                split = oper.split(" ")  # разделение текста на слова по пробелам
                poisk = split[2:]  # (не учитывать первые три слова)
                for word in poisk:
                    all_word += word + " "  # сборка всего поискового запроса

                url = 'https://ru.wikipedia.org/wiki/' + all_word  # url поискового запроса
                tts.say("Ищу в интернете ваш запрос" + all_word)
                tts.runAndWait()
                self.main_text.setText('Ищу в интернете ваш запрос:' + all_word)
                self.main_text.adjustSize()
                webbrowser.open_new(url)  # открыть браузер с писковым запросом(url)

            elif (oper.find("открыть новую вкладку в браузере") >= 0) or (
                    oper.find("открой новую вкладку в браузере") >= 0):
                # октрытие новой вкладки в браузере
                tts.say("Открытие новой вкладки в браузере")
                tts.runAndWait()
                self.main_text.setText('Открытие новой вкладки в браузере')
                self.main_text.adjustSize()
                webbrowser.open_new('https:')  # открыть браузер с новой вкладкой

            elif (oper.find("сколько будет") >= 0) or (oper.find("посчитай сколько будет") >= 0):  # поиск слов
                if (oper.find("+") >= 0) or (oper.find("плюс") >= 0):
                    nums = re.findall('[0-9]+', oper)  # поиск и отлов цифр(regex)
                    rez = int(nums[0]) + int(nums[1])  # сложение цифр(в формате int)
                    tts.say("Ответ:" + str(rez))
                    tts.runAndWait()
                    self.main_text.setText('Ответ:')
                    self.main_text.adjustSize()
                    self.sub_text.setText(str(rez))
                    self.sub_text.adjustSize()
                    # вывод результата

                elif (oper.find("-") >= 0) or (oper.find("минус") >= 0):
                    nums = re.findall('[0-9]+', oper)  # поиск и отлов цифр(regex)
                    rez = int(nums[0]) - int(nums[1])  # вычитание цифр(в формате int)
                    tts.say("Ответ:" + str(rez))
                    tts.runAndWait()
                    self.main_text.setText('Ответ:')
                    self.main_text.adjustSize()
                    self.sub_text.setText(str(rez))
                    self.sub_text.adjustSize()
                    # вывод результата

                elif (oper.find("х") >= 0) or (oper.find("*") >= 0) or (oper.find("умножить") >= 0):
                    nums = re.findall('[0-9]+', oper)  # поиск и отлов цифр(regex)
                    rez = int(nums[0]) * int(nums[1])  # умножение цифр(в формате int)
                    tts.say("Ответ:" + str(rez))
                    tts.runAndWait()
                    self.main_text.setText('Ответ:')
                    self.main_text.adjustSize()
                    self.sub_text.setText(str(rez))
                    self.sub_text.adjustSize()
                    # вывод результата

                elif (oper.find("/") >= 0) or (oper.find("разделить") >= 0) or (oper.find("дробью") >= 0):
                    nums = re.findall('[0-9]+', oper)  # поиск и отлов цифр(regex)
                    if float(nums[1]) == 0.0:  # добавление исключений = / 0
                        tts.say("На ноль делить нельзя")
                        tts.runAndWait()
                        self.main_text.setText('На ноль делить нельзя')
                        self.main_text.adjustSize()
                    else:
                        rez = float(nums[0]) / float(nums[1])  # деление цифр(в формате float)
                        tts.say("Ответ:" + str(int(rez)))
                        tts.runAndWait()
                        self.main_text.setText('Ответ:')
                        self.main_text.adjustSize()
                        self.sub_text.setText(str(rez))
                        self.sub_text.adjustSize()
                        # вывод результата


            else:
                tts.say("Я вас не понял")
                tts.runAndWait()
                self.main_text.setText('Я вас не понял')  # если не понял написать - (Я вас не понял)
                self.main_text.adjustSize()

        except speech_recognition.UnknownValueError:
            tts.say("Я вас не понял")
            tts.runAndWait()
            self.main_text.setText('Я вас не понял')  # если не понял написать - (Я вас не понял)
            self.main_text.adjustSize()


def application():  # создание приложения и получение системных настроек
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())  # закрытие приложения


if __name__ == "__main__":  # запуск приложения
    application()