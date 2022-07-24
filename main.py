import os

from crossword.lib import Crossword, BLACK, read_vocab


xw = Crossword(3)
vocab = read_vocab(os.path.join("vocab", "tiny.dict"))
xw.set_vocab(vocab)

xw[0, 2] = BLACK
xw[2, 0] = BLACK

fill_generator = xw.fill_generator()
for solution in fill_generator:
    print(solution)
