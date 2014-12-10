import random
import functools
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from models.corpus import Corpus

class AlignmentsView(QWidget):

  def __init__(self, init_view, normal_view):
    super(AlignmentsView, self).__init__()

    self.init_view = init_view
    self.normal_view = normal_view
    self.initAlignments()

  def initAlignments(self):
    self.init_view.results_cbox = QComboBox()
    self.init_view.results_cbox.setObjectName('__qt__passive_comboBox')
    self.init_view.results_swidget = QStackedWidget()

    self.showAlignments()

  def showAlignments(self):
    if self.init_view.stemming_btn:
      self.init_view.stemming_btn = self.init_view.deleteWidget(self.init_view.stemming_btn,
                                                               self.init_view.radio_layout)
      self.init_view.lemmatisation_btn = self.init_view.deleteWidget(self.init_view.lemmatisation_btn,
                                                                         self.init_view.radio_layout)
      self.init_view.capitalisation_cbox = self.init_view.deleteWidget(self.init_view.capitalisation_cbox,
                                                                           self.init_view.checkbox_layout)
      self.init_view.none_btn = self.init_view.deleteWidget(self.init_view.none_btn,
                                                       self.init_view.radio_layout)
      self.init_view.next_btn = self.init_view.deleteWidget(self.init_view.next_btn,
                                                       self.init_view.button_layout)
      self.init_view.normalisation_label = self.init_view.deleteWidget(self.init_view.normalisation_label, self.init_view.text_layout)
      self.init_view.model_label = self.init_view.deleteWidget(self.init_view.model_label, self.init_view.model_text_layout)
      self.init_view.ibm1_btn = self.init_view.deleteWidget(self.init_view.ibm1_btn, self.init_view.model_layout)
      self.init_view.ibm2_btn = self.init_view.deleteWidget(self.init_view.ibm2_btn, self.init_view.model_layout)
      self.init_view.ibms_btn = self.init_view.deleteWidget(self.init_view.ibms_btn, self.init_view.model_layout)

    if self.init_view.back_btn:
      self.init_view.back_btn = self.init_view.deleteWidget(self.init_view.back_btn,
                                                       self.init_view.button_layout)


    self.init_view.back_btn = self.init_view.insertButton("Back",
                                    self.normal_view.showOptions)

    self.aligned_sents = None
    self.ibm2_aligned_sents = None

    if not self.init_view.ibm == "both":
      self.aligned_sents = Corpus.computeAlignments(self.init_view.corpuses[0],
                                             self.init_view.corpuses[1], self.init_view.ibm)
    else:
      self.aligned_sents, self.ibm2_aligned_sents = Corpus.computeAlignments(self.init_view.corpuses[0],
                                                              self.init_view.corpuses[1], self.init_view.ibm)

    for i in xrange(len(self.aligned_sents)):
      porc = QWidget()
      alignment_layout = QHBoxLayout(porc)
      al_sent = self.aligned_sents[i]
      al_draw = AlignmentsDraw(al_sent)
      alignment_layout.addWidget(al_draw)

      if self.ibm2_aligned_sents:
        ibm2_al_sent = self.ibm2_aligned_sents[i]
        ibm2_al_draw = AlignmentsDraw(ibm2_al_sent)
        alignment_layout.addWidget(ibm2_al_draw)

      self.init_view.results_swidget.addWidget(porc)


    for i in xrange(len(self.aligned_sents)):
      self.init_view.results_cbox.addItem("Alignment " + str(i+1))


    self.init_view.results_layout.addWidget(self.init_view.results_swidget)
    self.init_view.results_layout.addWidget(self.init_view.results_cbox)

    self.init_view.results_cbox.activated.connect(self.init_view.results_swidget.setCurrentIndex)

class AlignmentsDraw(QWidget):
  def __init__(self, al_sent):
    super(AlignmentsDraw, self).__init__()
    self.al_sent = al_sent
    self.qp = QPainter()
    self.show()

  def paintEvent(self, event):
    self.qp.begin(self)
    self.drawText(event)
    self.qp.end()

  def drawText(self, event):
    x = 10
    y = 20

    self.qp.setFont(QFont('Decorative', 15))
    self.qp.setPen(QColor(168, 34, 3))

    words_pos = {}
    words = self.al_sent.words
    mots = self.al_sent.mots
    for i in xrange(len(words)):
      words_pos[words[i]] = i
      self.qp.drawText(x, y, words[i].decode('unicode_escape').rstrip('\n'))
      y+=30

    x = 10
    y = 20

    mots_colours = {}
    mots_pos = {}
    for i in xrange(len(mots)):
      mots_pos[mots[i]] = i
      if mots[i] not in mots_colours:
        mots_colours[mots[i]] = QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
      self.qp.drawText(x+400, y, mots[i].decode('unicode_escape').rstrip('\n') + '\n')
      y+=30

    x = 10
    y = 20

    for (pos_word, pos_mot) in self.al_sent.alignment:
      self.qp.setPen(mots_colours[self.al_sent.mots[pos_mot]])
      self.qp.drawLine(x+100, 30*pos_word+y, x+390, 30*pos_mot+y)
