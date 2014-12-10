from nltk.align import IBMModel1, AlignedSent, Alignment
from collections import defaultdict
from copy import deepcopy

class IBMModel2(object):

    def __init__(self, aligned_sents, convergent_threshold=1e-2):
        # Dictionary of translation probabilities t(e,f).
        # Lexical step
        self.aligned_sents = aligned_sents
        self.convergent_threshold = convergent_threshold
        self.probabilities = IBMModel1(aligned_sents).probabilities
        self._train()

    def _train(self):
        english_words = set()
        foreign_words = set()

        for aligned_sent in self.aligned_sents:
            english_words.update(aligned_sent.words)
            foreign_words.update(aligned_sent.mots)

        foreign_words.add(None)
        num_probs = len(english_words)*len(foreign_words)

        globally_converged = False
        iteration_count = 0
        a = {}
        for aligned_sent in self.aligned_sents:
            le = len(aligned_sent.words)
            lf = len(aligned_sent.mots)

            for j in xrange(le):
                for i in xrange(lf + 1):
                    a[i, j, le, lf] = 1.0 / (lf + 1)

        old_t = defaultdict(float)
        old_a = defaultdict(float)

        while not globally_converged:
            count = defaultdict(float)
            total = defaultdict(float)
            count_a = defaultdict(float)
            total_a = defaultdict(float)

            for aligned_sent in self.aligned_sents:
                le = len(aligned_sent.words)
                e_s = aligned_sent.words
                lf = len(aligned_sent.mots)
                f_s = aligned_sent.mots +[None]
                s_total = {}

                for j in xrange(le):
                    s_total[e_s[j]] = 0.0
                    for i in xrange(lf+1):
                        s_total[e_s[j]] += self.probabilities[e_s[j], f_s[i]] * a[i, j, le, lf]

                for j in xrange(le):
                    for i in xrange(lf+1):
                        c = self.probabilities[e_s[j], f_s[i]] * a[i, j, le, lf] / s_total[e_s[j]]
                        count[e_s[j], f_s[i]] += c
                        total[f_s[i]] += c
                        count_a[i, j, le, lf] += c
                        total_a[j, le, lf] += c

            t = defaultdict(float)
            a = defaultdict(float)

            num_converged_t = 0
            for e in english_words:
                for f in foreign_words:
                    t[e, f] = count[e, f] / total[f]
                    delta = abs(t[e, f] - old_t[e, f])
                    if delta < self.convergent_threshold:
                        num_converged_t += 1


            num_converged_a = 0
            for aligned_sent in self.aligned_sents:
                le = len(aligned_sent.words)
                lf = len(aligned_sent.mots)

                for j in xrange(le):
                    for i in xrange(lf+1):
                        a[i, j, le, lf] = count_a[i, j, le, lf] / total_a[j, le, lf]
                        delta = abs(a[i, j, le, lf] - old_a[i, j, le, lf])
                        if delta < self.convergent_threshold:
                            num_converged_a += 1

            old_t = deepcopy(t)
            old_a = deepcopy(a)

            if num_converged_t == num_probs:
                globally_converged = True

        self.probabilities = dict(t)
        self.alignments = dict(a)

        # print(self.probabilities)

    def aligned(self):
        if self.probabilities is None:
            raise ValueError("No probabilities calculated")

        aligned = []
        # Alignment Learning from t(e|f)
        for aligned_sent in self.aligned_sents:
            alignment = []
            le = len(aligned_sent.words)
            lf = len(aligned_sent.mots)

            for j, e_w in enumerate(aligned_sent.words):
                f_max = (self.alignments[lf, j, le, lf], None)
                for i, f_w in enumerate(aligned_sent.mots):
                    f_max = max(f_max, (self.alignments[i, j, le, lf], i))
                    print(f_max)
                    # print self.alignments[i, j, le, lf]


            # for every English word
            # for j, e_w in enumerate(aligned_sent.words):
                # find the French word that gives maximized t(e|f)
                # NULL token is the initial candidate
                # f_max = (self.probabilities[e_w, None], None)
                # for i, f_w in enumerate(aligned_sent.mots):
                    # f_max = max(f_max, (self.probabilities[e_w, f_w], i))

                # only output alignment with non-NULL mapping
                if f_max[1] is not None:
                    alignment.append((j, f_max[1]))

            # substitute the alignment of AlignedSent with the yielded one
            aligned.append(AlignedSent(aligned_sent.words,
                    aligned_sent.mots,  alignment))

        return aligned
