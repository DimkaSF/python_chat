from PyQt5 import QtWidgets
import design
import requests
import datetime
import threading
import time

class MessengerApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
	def __init__(self):
		super().__init__() # call init of parent class (parent class - superclass)
		self.setupUi(self)
		self.pushButton.clicked.connect(self.send)
		threading.Thread(target=self.recieve).start()

	def send(self):
		username = self.lineEdit.text()
		password = self.lineEdit_2.text()
		text = self.plainTextEdit.toPlainText()
		
		if not username or not password or not text:
			return
		
		try:
			requests.post(
				"http://localhost:5000/send",
				json={"username":username, "password": password, "text":text}
			)
		except: #ловим все ошибки
			pass #или print('connection error')
			
		self.plainTextEdit.setPlainText("")
		#self.plainTextEdit.repaint() - перерисовка элемента
			
	def recieve(self):
		last_recieved = 0
		while True:
			response = requests.get(
				"http://localhost:5000/messages",
				params={"after": last_recieved}
			)
			if response.status_code == 200:
				messages = response.json()["messages"]
				for mes in messages:
					username = mes["username"]
					time_1 = datetime.datetime.fromtimestamp(mes["time"])
					time_str = time_1.strftime("%Y:%m:%d %H:%M:%S")
					text = mes["text"]
				
					self.textBrowser.append(f'{username} {time_str}')
					self.textBrowser.append(text)
					self.textBrowser.append("")
					
					
					last_recieved = mes["time"]
			time.sleep(1)
		

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	window = MessengerApp() #вызываем приложение
	window.show() #показываем пользователю
	app.exec_() #включаем интерактив