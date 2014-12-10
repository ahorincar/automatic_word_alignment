from PyQt4.QtGui import *
from PyQt4.QtCore import *
from views.alignments_view import AlignmentsView
from models.corpus import Corpus

class NormalisationView(QWidget):
  def __init__(self, init_view):
    super(NormalisationView, self).__init__()

    self.init_view = init_view
    self.showOptions()

  def showOptions(self):
    if self.init_view.first_corpus_btn:
      self.init_view.first_corpus_btn = self.init_view.deleteWidget(self.init_view.first_corpus_btn,
                                                                       self.init_view.button_layout)
      self.init_view.second_corpus_btn = self.init_view.deleteWidget(self.init_view.second_corpus_btn,
                                                                         self.init_view.button_layout)
      self.init_view.next_btn = self.init_view.deleteWidget(self.init_view.next_btn,
                                                       self.init_view.button_layout)
      self.init_view.instructions_label = self.init_view.deleteWidget(self.init_view.instructions_label,
                                                                             self.init_view.text_layout)
      self.init_view.title_label = self.init_view.deleteWidget(self.init_view.title_label, self.init_view.title_layout)

    if self.init_view.back_btn:
      self.init_view.back_btn = self.init_view.deleteWidget(self.init_view.back_btn,
                                                       self.init_view.button_layout)

    if self.init_view.results_swidget:
      self.init_view.results_swidget = self.init_view.deleteWidget(self.init_view.results_swidget,
                                                                    self.init_view.results_layout)
      self.init_view.results_cbox = self.init_view.deleteWidget(self.init_view.results_cbox,
                                                              self.init_view.results_layout)

    self.init_view.model_label = QLabel("<h2>IBM Models</h2>")
    self.init_view.model_label.setWordWrap(True)
    self.init_view.model_label.setAlignment(Qt.AlignCenter)
    self.init_view.model_label.setMaximumHeight(20)

        # Radio buttons
    self.init_view.ibm1_btn = QRadioButton("IBM Model 1")
    self.init_view.ibm2_btn = QRadioButton("IBM Model 2")
    self.init_view.ibms_btn = QRadioButton("Both")

    self.init_view.model_layout.addWidget(self.init_view.ibm1_btn)
    self.init_view.model_layout.addWidget(self.init_view.ibm2_btn)
    self.init_view.model_layout.addWidget(self.init_view.ibms_btn)

    self.init_view.model_text_layout.addWidget(self.init_view.model_label)

    self.init_view.normalisation_label = QLabel("<h2>Preprocessing options</h2>")
    # self.init_view.normalisation_label.setStyleSheet("font-size: 15px;")
    self.init_view.normalisation_label.setWordWrap(True)
    self.init_view.normalisation_label.setAlignment(Qt.AlignCenter)
    self.init_view.normalisation_label.setMaximumHeight(20)

    self.init_view.text_layout.addWidget(self.init_view.normalisation_label)


    # Radio buttons
    self.init_view.stemming_btn = QRadioButton("Stemming")
    self.init_view.lemmatisation_btn = QRadioButton("Lemmatisation")
    self.init_view.none_btn = QRadioButton("None")

    self.init_view.radio_layout.addWidget(self.init_view.stemming_btn)
    self.init_view.radio_layout.addWidget(self.init_view.lemmatisation_btn)
    self.init_view.radio_layout.addWidget(self.init_view.none_btn)

    # Checkbox
    self.init_view.capitalisation_cbox = QCheckBox('Capitalisation')
    self.init_view.capitalisation_cbox.move(300, 220)
    self.init_view.capitalisation_cbox.toggle()
    self.init_view.capitalisation_cbox.setCheckState(False)

    self.init_view.checkbox_layout.addWidget(self.init_view.capitalisation_cbox)

    # QPushButtons
    self.init_view.next_btn = self.init_view.insertButton("Next", self.chooseAlignments)
    self.init_view.back_btn = self.init_view.insertButton("Back",
                                         self.init_view.viewInit)

  def chooseAlignments(self):
    if self.init_view.ibm1_btn.isChecked():
      self.init_view.ibm = "ibm1"
    elif self.init_view.ibm2_btn.isChecked():
      self.init_view.ibm = "ibm2"
    elif self.init_view.ibms_btn.isChecked():
      self.init_view.ibm = "both"
    else:
      warning_mbox = QMessageBox.information(self, 'Warning',
      'You must choose a translation model!', QMessageBox.Ok)
      return

    self.normalise()

  def normalise(self):

    if self.init_view.stemming_btn.isChecked():
      self.init_view.corpuses[0] = Corpus.doStemming(self.init_view.corpuses[0])
      self.init_view.corpuses[1] = Corpus.doStemming(self.init_view.corpuses[1])
    elif self.init_view.lemmatisation_btn.isChecked():
      self.init_view.corpuses[0] = Corpus.doLemmatisation(self.init_view.corpuses[0])
      self.init_view.corpuses[1] = Corpus.doLemmatisation(self.init_view.corpuses[1])

    if self.init_view.capitalisation_cbox.checkState():
      self.init_view.corpuses[0] = Corpus.doCapitalisation(self.init_view.corpuses[0])
      self.init_view.corpuses[1] = Corpus.doCapitalisation(self.init_view.corpuses[1])

    self.init_view.main_widget = AlignmentsView(self.init_view, self)
