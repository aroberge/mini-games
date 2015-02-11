
from PyQt4 import QtGui
from PyQt4 import QtCore

import model

images = {}

for nb_mines in range(1, 9):
    images[nb_mines] = QtGui.QImage("images/{}.png".format(nb_mines))

for name in ["covered", "empty", "flag_mine", "flag_mine_wrong",
             "flag_suspect", "mine", "mine_wrong"]:
    images[name] = QtGui.QImage("images/{}.png".format(name))


class GameBoard(QtGui.QWidget):

    def __init__(self, parent, nb_cols=10, nb_rows=10, tile_size=32):
        super().__init__()
        self.board = model.Board(nb_cols=nb_cols, nb_rows=nb_rows)
        self.parent = parent
        self.tile_size = tile_size
        self.width = self.tile_size * self.board.nb_cols
        self.height = self.tile_size * self.board.nb_rows

    def reset(self):
        self.board.new_game()
        self.repaint()

    def paintEvent(self, event):  # noqa
        '''Overriden QWidget method'''
        painter = QtGui.QPainter()
        painter.begin(self)
        self.draw(painter)
        painter.end()

    def draw(self, painter):
        '''Basic drawing method; usually overriden'''
        for tile in self.board.grid:
            col, row = tile
            painter.drawImage(col*self.tile_size, row*self.tile_size,
                images[self.board.grid[tile]["appear"]])

    def mousePressEvent(self, event):  # noqa
        '''Overriden QWidget method'''
        if self.board.game_over:
            return
        tile = self.which_tile_clicked(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.board.reveal_tile(tile)
        elif event.button() == QtCore.Qt.RightButton:
            self.board.mark_tile(tile)
        self.repaint()
        if self.board.game_over:
            message = self.board.game_over
        else:
            message = "{} mines left out of {}.".format(
                self.board.nb_mines - self.board.marked_mines,
                self.board.nb_mines)
        self.parent.receive_message(message)

    def which_tile_clicked(self, event):
        '''Determine which row and col mouse click occurred'''
        x = event.x()
        y = event.y()
        col = x // self.tile_size
        row = y // self.tile_size
        return col, row


class TestGame(QtGui.QMainWindow):
    '''Non real game set up to try various functions/methods
       that can be used in games'''

    def __init__(self):
        super().__init__()
        self.game_board = GameBoard(self, tile_size=24)
        self.init_ui()

    def init_ui(self):

        self.setWindowTitle("Test Game")
        self.statusbar = self.statusBar()
        menu = self.menuBar()
        new_game_menu = menu.addMenu("New Game")
        new_game_action = QtGui.QAction("Easy", self)
        new_game_action.triggered.connect(self.game_board.reset)
        new_game_menu.addAction(new_game_action)
        self.setCentralWidget(self.game_board)
        self.resize(self.game_board.width, self.game_board.height)
        self.setFixedSize(self.game_board.width,
            self.game_board.height+self.statusbar.height()+menu.height())
        self.show()

    def receive_message(self, message):
        self.statusbar.showMessage(message)


def main():

    app = QtGui.QApplication([])
    TestGame()
    app.exec_()

if __name__ == '__main__':
    main()
