from PySide6 import QtWidgets
from PySide6.QtCore import Slot
import sys
import datetime
from .client_logic import ClientConnector

class Reminders(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Reminders, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        self.create_labeled_widget(QtWidgets.QComboBox(self), 'reciever', 'Recipiente: ')
        self.reciever.addItem('alvespedro0225@gmail.com')
        self.reciever.addItem('dak7alves74@gmail.com')
        rec_layout = self.create_hor_layout(self.reciever, self.reciever_label)
        self.create_labeled_widget(QtWidgets.QLineEdit(), 'send_date', 'Data de envio: (dd/mm)')
        date_layout = self.create_hor_layout(self.send_date, self.send_date_label)
        self.create_labeled_widget(QtWidgets.QLineEdit(), 'send_time', 'Horario de envio: (hh:mm)')
        time_layout = self.create_hor_layout(self.send_time, self.send_time_label)
        self.create_labeled_widget(QtWidgets.QLineEdit(), 'subject', 'Assunto: ')
        subject_layout = self.create_hor_layout(self.subject, self.subject_label)
        self.create_labeled_widget(QtWidgets.QPlainTextEdit(), 'message', 'Mensagem')
        self.send = QtWidgets.QPushButton('Enviar')
        self.send.clicked.connect(self.send_data)
        self.configure_layout_layouts(layout, rec_layout, date_layout, time_layout, subject_layout)
        self.configure_layout_widgets(layout, self.message_label, self.message, self.send)
        self.setLayout(layout)
        self.setWindowTitle('Lembretes')      
        self.resize(500, 300)
        self.today = datetime.date.today()

    def create_hor_layout(self, widget:QtWidgets.QWidget, label:QtWidgets.QLabel):
        hor_layout = QtWidgets.QHBoxLayout()
        hor_layout.addWidget(label)
        hor_layout.addWidget(widget)
        return hor_layout
    
    def create_labeled_widget(self, widget:QtWidgets.QWidget, field_name:str, label_message:str):
        label_name = f"{field_name}_label"
        label = QtWidgets.QLabel(label_message)
        setattr(self, field_name, widget)
        setattr(self, label_name, label)

    def configure_layout_widgets(self, layout:QtWidgets.QVBoxLayout, *args):
        for widget in args:
            layout.addWidget(widget)
    
    def configure_layout_layouts(self, layout:QtWidgets.QVBoxLayout, *args:QtWidgets.QHBoxLayout|QtWidgets.QVBoxLayout):
        for widget in args:
            layout.addLayout(widget)

    @Slot()
    def send_data(self):

        data = self.get_data()
        if self.validate_data(data):
            self.format_datetime(data)
            ClientConnector.send_message(data)
            self.confirmation()


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
            if (send_date_dateclass < self.today):
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