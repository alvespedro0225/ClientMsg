from client_logic.widget import Reminders
from PySide6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Reminders()
    form.show()
    app.exec()