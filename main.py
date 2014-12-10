import sys
from views.main_view import MainView
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def demo():

  app = QApplication(sys.argv)
  app_window = MainView()
  sys.exit(app.exec_())


if __name__ == '__main__':
  demo()
