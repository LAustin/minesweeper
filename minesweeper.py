import sys
import random

class Game():
  grid = None
  isRunning = 0

  def __init__(self):
    self.isRunning = 1
    self.grid = Grid(2,2,1)

  def printGame(self):
    self.grid.printGrid()

  def guess(self, xPos, yPos):
    self.grid.guess(xPos, yPos)



class Grid():
  width = 0
  height = 0
  numMines = 0
  cells = None
  numRevealed = 0
  numCells = 0

  def __init__(self,width,height,numMines):
    self.width = width
    self.height = height
    self.numMines = numMines
    self.cells = list()
    minesAssigned = 0
    self.numCells = width * height

    for rowNum in range(height):
      row = list()
      for colNum in range(width):
        cell = Cell(rowNum, colNum)
        row.append(cell)
      self.cells.append(row)

    # until all mines are distributed
    while minesAssigned < self.numMines:
      # randomly choose an X position
      xPos = random.randint(0,self.width-1)
      # randomly choose a Y position
      yPos = random.randint(0,self.height-1)
      # check if that cell is already a mine
      row = self.cells[yPos]
      cell = row[xPos]
      if not cell.isMine:
        # if not, make it one
        cell.isMine = 1
        # then increment minesAssigned
        minesAssigned +=1

    # now check mine adjacency
    for rowNum in range(height):
      for colNum in range(width):
        self.countMines(rowNum,colNum)


  def printGrid(self):
    for row in self.cells:
      for cell in row:
        cell.printCell()
      print "\n",

  def revealAll(self):
    for row in self.cells:
      for cell in row:
        cell.reveal()
    self.printGrid()

  def countMines(self, pY, pX):
    # look at cells at cardinal points
    # N
    # S
    if pY != 0:
      # not top row?
      if self.cells[pY-1][pX].isMine:
        self.cells[pY][pX].adjMines += 1

      # what about the diagonals?
      if pX != 0:
        # "you can look up to the left"
        if self.cells[pY-1][pX-1].isMine:
          self.cells[pY][pX].adjMines += 1
      if pX != self.width-1:
        # "you can look up to the right"
        if self.cells[pY-1][pX+1].isMine:
          self.cells[pY][pX].adjMines += 1


    if pY != self.height-1:
      # not bottom row?
      if self.cells[pY+1][pX].isMine:
        self.cells[pY][pX].adjMines += 1

      if pX != 0:
        # "you can look up to the left"
        if self.cells[pY+1][pX-1].isMine:
          self.cells[pY][pX].adjMines += 1
      if pX != self.width-1:
        # "you can look up to the right"
        if self.cells[pY+1][pX+1].isMine:
          self.cells[pY][pX].adjMines += 1

    # E
    # W
    if pX != 0:
      #left edge
      if self.cells[pY][pX-1].isMine:
        self.cells[pY][pX].adjMines += 1

    if pX != self.width-1:
      #right edge
      if self.cells[pY][pX+1].isMine:
        self.cells[pY][pX].adjMines += 1

  def guess(self,pX,pY):
    # if this is a mine, kaboom!
    # else reveal count
    
    if self.cells[pY][pX].isMine:
      print "KABOOM!"
      self.revealAll()
      exit()
    else:
      self.cells[pY][pX].reveal()
      self.numRevealed +=1

    if self.numCells - self.numRevealed == self.numMines:
      print "We win!"
      exit()


class Cell():
  xPos = 0
  yPos = 0
  show = 0
  isMine = 0
  adjMines = 0

  def __init__(self, pX, pY):
    self.xPos = pX
    self.yPos = pY

  def printCell(self):
    if self.show:
      if self.isMine:
        print "*",
      else:
        print self.adjMines,
    else:
      print "U",
      #print self.adjMines,

  def reveal(self):
    self.show = 1


def main():
  args = sys.argv[1:]
  game = Game()

  while game.isRunning:
    game.printGame()
    command = raw_input('Move: ').strip()
    if command == "X":
      exit()
    else:
      # "3,1"
      parts = command.split(',')
      game.guess(int(parts[0]), int(parts[1]))


if __name__ == "__main__":
  main()