import sys

from PyQt5.QtWidgets import QApplication

from signal_slot.progress import ProgressBar_Dialog
from signal_slot.slider import Slider_Dialog

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sd = Slider_Dialog()
    pb = ProgressBar_Dialog()
    pb.make_connection(sd)
    sys.exit(app.exec_())