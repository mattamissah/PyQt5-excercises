import sys
import time
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtWidgets import QApplication, QLabel


app = QApplication(sys.argv)

try:
    due = QTime.currentTime()
    message = "Alert"
    if len(sys.argv) < 2:
        raise ValueError
    hours, mins = sys.argv[1].split(":")
    due = QTime(int(hours), int(mins))
    if not due.isValid():
        raise ValueError
    if len(sys.argv) > 2:
        message = "".join(sys.argv[2:])
except ValueError:
    message = "Usage: alert.pyw HH:MM [optional message]"

while QTime.currentTime() < due:
    time.sleep(20)


label = QLabel()
label.setWindowFlags(Qt.SplashScreen)
label.show()
QTimer.singleShot(60000, app.quit) # 1 minute
label.setWindowFlags(Qt.SplashScreen)
label.show()
QTimer.singleShot(60000, app.quit)  # 1 minute

app.exec_()