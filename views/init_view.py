from PyQt4.QtGui import *
from PyQt4.QtCore import *
from models.corpus import Corpus
from views.normalisation_view import NormalisationView

from models.ibmmodel2 import IBMModel2, IBMModel1
from nltk.align import AlignedSent, Alignment

class InitView(QWidget):
  def __init__(self):
    super(InitView, self).__init__()

    self.main_layout = QVBoxLayout(self)
    self.results_layout = QVBoxLayout()
    self.title_layout = QVBoxLayout()
    # self.title_layout.setAlignment(Qt.AlignCenter)
    self.text_layout = QVBoxLayout()
    self.text_layout.setAlignment(Qt.AlignCenter)
    self.button_layout = QVBoxLayout()
    self.button_layout.setAlignment(Qt.AlignCenter)
    self.checkbox_layout = QHBoxLayout()
    self.radio_layout = QHBoxLayout()
    self.model_layout = QHBoxLayout()
    self.alignments_layout = QVBoxLayout()
    self.alignments_layout.setContentsMargins(0,0,0,0)
    self.alignments_layout.setSpacing(0)
    self.model_text_layout = QVBoxLayout()

    # Add sublayouts to main layout
    self.main_layout.addLayout(self.alignments_layout)
    self.main_layout.addLayout(self.results_layout)
    self.main_layout.addLayout(self.model_text_layout)
    self.main_layout.addLayout(self.model_layout)
    self.main_layout.addLayout(self.title_layout)
    self.main_layout.addLayout(self.text_layout)
    self.main_layout.addLayout(self.radio_layout)
    self.main_layout.addLayout(self.checkbox_layout)
    self.main_layout.addLayout(self.button_layout)


    # Corpuses
    self.first_corpus = None
    self.second_corpus = None
    self.corpuses = [None, None]

    self.stemming_btn = None
    self.lemmatisation_btn = None
    self.none_btn = None
    self.capitalisation_cbox = None
    self.back_btn = None
    self.model_label = None
    self.title_label = None
    self.normalisation_label = None
    self.instructions_label = None
    self.first_corpus_btn = None
    self.second_corpus_btn = None
    self.next_btn = None
    self.ibm1_btn = None
    self.ibm2_btn = None
    self.ibms_btn = None
    # self.alignments = None
    self.results_swidget = None
    self.results_cbox = None
    self.ibm = None

    self.viewInit()

  def viewInit(self):
    if self.stemming_btn:
      self.stemming_btn = self.deleteWidget(self.stemming_btn,
                                           self.radio_layout)
      self.lemmatisation_btn = self.deleteWidget(self.lemmatisation_btn,
                                                     self.radio_layout)
      self.none_btn = self.deleteWidget(self.none_btn, self.radio_layout)
      self.capitalisation_cbox = self.deleteWidget(self.capitalisation_cbox,
                                                         self.checkbox_layout)
      self.next_btn = self.deleteWidget(self.next_btn, self.button_layout)
      self.back_btn = self.deleteWidget(self.back_btn, self.button_layout)
      self.normalisation_label = self.deleteWidget(self.normalisation_label, self.text_layout)
      self.model_label = self.deleteWidget(self.model_label, self.model_text_layout)
      self.ibm1_btn = self.deleteWidget(self.ibm1_btn, self.model_layout)
      self.ibm2_btn = self.deleteWidget(self.ibm2_btn, self.model_layout)
      self.ibms_btn = self.deleteWidget(self.ibms_btn, self.model_layout)

    # Text Area
    self.title_label = QLabel("<h1>Automatic Word Alignment Tool</h1>")
    self.title_label.setWordWrap(True)
    self.title_label.setAlignment(Qt.AlignCenter)
    self.title_layout.addWidget(self.title_label)

    self.instructions_label = QLabel("<h3>Instructions</h3>"
                                    "<ol><li>Please provide two corpuses. "
                                    "(<b>Note:</b> Each sentence in the corpuses must be "
                                    "stored on a new line)</li>"
                                    "<li>Please choose your preprocessing preferences from the existing options.<li>"
                                    "<li>Navigate through the alignments.</li></ol>")
    self.instructions_label.setStyleSheet("font-size: 15px;")
    self.instructions_label.setWordWrap(True)
    self.instructions_label.setAlignment(Qt.AlignLeft)

    self.title_label.setMaximumHeight(100)
    self.instructions_label.setMaximumHeight(400)

    self.text_layout.addWidget(self.instructions_label)

    # Labels for corpuses buttons
    if self.first_corpus:
        first_corpus_lbl = "Corpus 1: Choose another corpus"
    else:
        first_corpus_lbl = "Corpus 1: Add first corpus"

    if self.second_corpus:
        second_corpus_lbl = "Corpus 2: Choose another corpus"
    else:
        second_corpus_lbl = "Corpus 2: Add second corpus"

    # Buttons to choose corpuses
    self.first_corpus_btn = self.insertButton(first_corpus_lbl,
                                       self.processFirstCorpus)
    self.second_corpus_btn = self.insertButton(second_corpus_lbl,
                                        self.processSecondCorpus)

    self.next_btn = self.insertButton("Next", self.nextCallback)


  def processFirstCorpus(self):
    self._processCorpus('frst')

  def processSecondCorpus(self):
    self._processCorpus('scnd')

  def _processCorpus(self, corpus):
    fname = QFileDialog.getOpenFileName(self, 'Add corpus',
            '/home/documents/Code/dissertation/data')

    c = Corpus(fname)

    if corpus == "frst":
        self.first_corpus = True
        self.first_corpus_btn.setText("Corpus 1: Choose another corpus")
        self.corpuses[0] = c
    else:
        self.second_corpus = True
        self.second_corpus_btn.setText("Corpus 2: Choose another corpus")
        self.corpuses[1] = c

  def insertButton(self, label, method_to_call):
    button = QPushButton(label, self)
    button.clicked.connect(method_to_call)
    button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    self.button_layout.addWidget(button)
    return button

  def deleteWidget(self, widget, layout):
    layout.removeWidget(widget)
    widget.deleteLater()
    return None

  def nextCallback(self):
    if not self.first_corpus and not self.second_corpus:
      warning_mbox = QMessageBox.information(self, 'Warning',
           'You must add two corpuses!', QMessageBox.Ok)
      return
    elif not self.first_corpus:
      warning_mbox = QMessageBox.information(self, 'Warning',
       'Corpus 1: Please add a corpus!', QMessageBox.Ok)
      return
    elif not self.second_corpus:
      warning_mbox = QMessageBox.information(self, 'Warning',
       'Corpus 2: Please add a corpus!', QMessageBox.Ok)
      return

    self.main_widget = NormalisationView(self)
