import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from models.corpus import Corpus
from views.init_view import InitView

class MainView(QMainWindow):

  def __init__(self):
    super(MainView, self).__init__()
    self.initMain()


  def initMain(self):
    self.main_widget = InitView()
    self.setCentralWidget(self.main_widget)
    self.setGeometry(600, 600, 1300, 700)
    self.setWindowTitle('Word Alignment Tool')
    self.show()



