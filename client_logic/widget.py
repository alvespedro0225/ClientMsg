from PySide6 import QtWidgets
from PySide6.QtCore import Slot
import sys
import datetime
from .client_logic import ClientConnector

class Reminders(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Reminders, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.reciever = QtWidgets.QComboBox(self)
        self.reciever.addItem('alvespedro0225@gmail.com')
        self.reciever.addItem('dak7alves74@gmail.com')
        self.reciever_label = QtWidgets.QLabel('Recipiente:')
        rec_layout = QtWidgets.QHBoxLayout()
        rec_layout.addWidget(self.reciever_label)
        rec_layout.addWidget(self.reciever)
        self.send_date = QtWidgets.QLineEdit()
        self.send_date_label = QtWidgets.QLabel('Data de envio (dd/mm)')
        date_layout = QtWidgets.QHBoxLayout()
        date_layout.addWidget(self.send_date_label)
        date_layout.addWidget(self.send_date)
        self.send_time = QtWidgets.QLineEdit()
        self.send_time_label = QtWidgets.QLabel('Horario de envio: (hh:mm)')
        time_layout = QtWidgets.QHBoxLayout()
        time_layout.addWidget(self.send_time_label)   
        time_layout.addWidget(self.send_time)   
        self.subject = QtWidgets.QLineEdit()
        self.subject_label = QtWidgets.QLabel('Assunto: ')
        subject_layout = QtWidgets.QHBoxLayout()
        subject_layout.addWidget(self.subject_label)
        subject_layout.addWidget(self.subject)
        self.message = QtWidgets.QPlainTextEdit()
        self.message_label = QtWidgets.QLabel('Mensagem:')
        self.send = QtWidgets.QPushButton('Enviar')
        self.send.clicked.connect(self.send_data)
        layout.addLayout(rec_layout)
        layout.addLayout(date_layout)
        layout.addLayout(time_layout)
        layout.addLayout(subject_layout)
        layout.addWidget(self.message_label)
        layout.addWidget(self.message)
        layout.addWidget(self.send)
        self.setLayout(layout)
        self.setWindowTitle('Lembretes')      
        self.resize(500, 300)
        self.today = datetime.date.today()

    @Slot()
    def send_data(self):

        data = self.get_data()
        if self.validate_data(data):
            self.format_datetime(data)
            ClientConnector.send_message(data)
            #self.confirmation()


    def confirmation(self):
            pop_up = QtWidgets.QDialog(self)
            layout = QtWidgets.QVBoxLayout()
            h_layout = QtWidgets.QHBoxLayout()
            confirmation = QtWidgets.QPushButton('Agendar outra mensagem')
            confirmation.clicked.connect(pop_up.accept)
            text = QtWidgets.QPlainTextEdit('Mensagem agendada.')
            closing = QtWidgets.QPushButton('Fechar')
            closing.clicked.connect(quit)
            text.setReadOnly(True)
            layout.addWidget(text)
            h_layout.addWidget(confirmation)
            h_layout.addWidget(closing)
            layout.addLayout(h_layout)
            pop_up.setWindowTitle('Confirmaçao de Envio')
            pop_up.setLayout(layout)
            pop_up.resize(200, 100)
            pop_up.exec()
            if pop_up.result():
                self.send_date.clear()
                self.send_time.clear()
                self.subject.clear()
                self.message.clear()


    

    def get_data(self) -> list[str]:

        data = []
        data.append(self.reciever.currentText())
        data.append(self.send_date.text())
        data.append(self.send_time.text())
        data.append(self.subject.text())
        message = self.message.document()
        data.append(str(message.toRawText()))
        return data
    
    def validate_data(self, data:list[str]):
        send_date = data[1]
        try:
            send_date_dateclass = datetime.date(month=int(send_date[3:]), day=int(send_date[:2]), year=self.today.year)
            if (send_date_dateclass <= self.today):
                raise ValueError
            if not ((send_date[2] == '/') or (send_date[2] == '-')):
                raise IndentationError
        except IndentationError:
            pop_up = QtWidgets.QDialog(self)
            layout = QtWidgets.QVBoxLayout(pop_up)
            confirmation = QtWidgets.QPushButton('OK')
            confirmation.clicked.connect(pop_up.accept)
            text = QtWidgets.QPlainTextEdit('Erro de formatação.\nExpectativa: dd/mm')
            text.setReadOnly(True)
            layout.addWidget(text)
            layout.addWidget(confirmation)
            pop_up.setWindowTitle('Erro de Formatação')
            pop_up.setLayout(layout)
            pop_up.resize(200, 100)
            pop_up.exec()
            return False
        
        except ValueError:
            pop_up = QtWidgets.QDialog(self)
            layout = QtWidgets.QVBoxLayout(pop_up)
            confirmation = QtWidgets.QPushButton('OK')
            confirmation.clicked.connect(pop_up.accept)
            text = QtWidgets.QPlainTextEdit('Data invalida.')
            text.setReadOnly(True)
            layout.addWidget(text)
            layout.addWidget(confirmation)
            pop_up.setWindowTitle('Data Invalida')
            pop_up.setLayout(layout)
            pop_up.resize(200, 100)
            pop_up.exec()
            return False
        


        send_time = data[2]
        try:
            send_time_timeclass = datetime.time(hour=int(send_time[:2]), minute=int(send_time[3:]))
            if (send_time[2] != ':'):
                raise IndentationError
        except IndentationError:
            pop_up = QtWidgets.QDialog(self)
            layout = QtWidgets.QVBoxLayout(pop_up)
            confirmation = QtWidgets.QPushButton('OK')
            confirmation.clicked.connect(pop_up.accept)
            text = QtWidgets.QPlainTextEdit('Formatação invalida.')
            text.setReadOnly(True)
            layout.addWidget(text)
            layout.addWidget(confirmation)
            pop_up.setWindowTitle('Erro de Formatação')
            pop_up.setLayout(layout)
            pop_up.resize(200, 100)
            pop_up.exec()
            return False

        except ValueError:
            pop_up = QtWidgets.QDialog(self)
            layout = QtWidgets.QVBoxLayout(pop_up)
            confirmation = QtWidgets.QPushButton('OK')
            confirmation.clicked.connect(pop_up.accept)
            text = QtWidgets.QPlainTextEdit('Hora invalida')
            text.setReadOnly(True)
            layout.addWidget(text)
            layout.addWidget(confirmation)
            pop_up.setWindowTitle('Hora Invalida')
            pop_up.setLayout(layout)
            pop_up.resize(200, 100)
            pop_up.exec()        
            return False        

        return True
    
    def format_datetime(self, data:list[str]):

        send_date = data[1]
        send_time = data[2]
        data[1] = str(datetime.date(month=int(send_date[3:]), day=int(send_date[:2]), year=self.today.year))
        data[2] = str(datetime.time(hour=int(send_time[:2]), minute=int(send_time[3:])))

        return data


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = Reminders()
    form.show()
    app.exec()