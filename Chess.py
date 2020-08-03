#started 7/21/2020 by Muhannad Alsenan
class Square:
    #white and black square unicode (white could be black and vice versa depending on your screen's background)
    bSquare = '\u2B1B '
    wSquare = '\u2B1C '

    #square constructor
    def __init__(self, position, piece):
        self.piece = piece
        self.position = position
        self.isSquare = True


    #'toString' for python
    def __str__(self):
        return self.piece
        #return self.position




#a piece IS-A square
class Piece(Square):
    #pieces unicode
    wPawn = '\u2659 '
    bPawn = '\u265F '
    wRook = '\u2656 '
    bRook = '\u265C '
    wKnight = '\u2658 '
    bKnight = '\u265E '
    wBishop = '\u2657 '
    bBishop = '\u265D '
    wQueen = '\u2655 '
    bQueen = '\u265B '
    wKing = '\u2654 '
    bKing = '\u265A '

    #piece constructor uses super (square) constructor
    def __init__(self, position, piece, color, moved, name):
        super().__init__(position, piece)
        self.name = name
        self.moved = moved
        self.color = color
        self.isSquare = False
        self.enPass = False

    #change position function to make move function easier
    def changePos(self, newPos):
        self.position = newPos
        self.moved = True

class Space:
    def __init__(self, rank, file, open):
        self.rank = rank
        self.file = file
        self.open = open
        self.position = chr(file + 97) + str(8 - rank)




#Square(POSITION,PIECE,SIDE)
#Piece(POSITION,PIECE,COLOR,MOVED,NAME)
class Board:
    #8x8 board initialization
    board = [[Square(None, None) for i in range(8)] for j in range(8)]

    #board constructor
    def __init__(self):
        self.turn = 'white'
        for i in range(8):
            for j in range(8):
                #rook placement
                if i == 0 and (j == 0 or j == 7):
                    self.board[i][j] = Piece(chr(97 + j) + str(8 - i), Piece.bRook, 'black', False, 'rook')
                elif i == 7 and (j == 0 or j == 7):
                    self.board[i][j] = Piece(chr(97 + j) + str(8 - i), Piece.wRook, 'white', False, 'rook')
                #knights
                elif i == 0 and (j == 1 or j == 6):
                    self.board[i][j] = Piece(chr(97 + j) + str(8 - i), Piece.bKnight, 'black', False, 'knight')
                elif i == 7 and (j == 1 or j == 6):
                    self.board[i][j] = Piece(chr(97 + j) + str(8 - i), Piece.wKnight, 'white', False, 'knight')
                #bishops
                elif i == 0 and (j == 2 or j == 5):
                    self.board[i][j] = Piece(chr(97 + j) + str(8 - i), Piece.bBishop, 'black', False, 'bishop')
                elif i == 7 and (j == 2 or j == 5):
                    self.board[i][j] = Piece(chr(97 + j) + str(8 - i), Piece.wBishop, 'white', False, 'bishop')
                #queens
                elif i == 0 and j == 3:
                    self.board[i][j] = Piece(chr(97 + j) + str(8 - i), Piece.bQueen, 'black', False, 'queen')
                elif i == 7 and j == 3:
                    self.board[i][j] = Piece(chr(97 + j) + str(8 - i), Piece.wQueen, 'white', False, 'queen')
                #kings
                elif i == 0 and j == 4:
                    self.board[i][j] = Piece(chr(97 + j) + str(8 - i), Piece.bKing, 'black', False, 'king')
                elif i == 7 and j == 4:
                    self.board[i][j] = Piece(chr(97 + j) + str(8 - i), Piece.wKing, 'white', False, 'king')
                #pawns
                elif i == 1:
                    self.board[i][j] = Piece(chr(97 + j) + str(8 - i), Piece.bPawn, 'black', False, 'pawn')
                elif i == 6:
                    self.board[i][j] = Piece(chr(97 + j) + str(8 - i), Piece.wPawn, 'white', False, 'pawn')
                #the rest of the black and white squares
                elif (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    self.board[i][j] = Square(chr(97 + j) + str(8 - i), Square.wSquare)
                else:
                    self.board[i][j] = Square(chr(97 + j) + str(8 - i), Square.bSquare)

    #makes new white or black square (depending on position)
    def newSquare(self, pos):
        file = ord(pos[0]) - 97
        rank = 8 - int(pos[1])
        if (rank % 2 == 0 and file % 2 == 0) or (rank % 2 == 1 and file % 2 == 1):
            return Square(pos, Square.wSquare)
        else:
            return Square(pos, Square.bSquare)

    #prints whole board
    def printBoard(self):
        if self.turn == 'white':
            for i in range(8):
                for j in range(8):
                    print(self.board[i][j], end = '')
                print(8 - i)

            for k in range(8):
                print(chr(97 + k) + '  ', end = '')

        elif self.turn == 'black':
            for i in range(8):
                for j in range(8):
                    print(self.board[7 - i][7 - j], end = '')
                print(i + 1)
            for k in range(8):
                print(chr(104 - k) + '  ', end = '')
        print('')

    #check for checks
    def checkCheck(self, pos, piece):
        check = False

        checkCount = 0  #variable to check how many pieces are checking the king at once (if it is more than one, then the king must move cuz they cant both be blocked at once)
        checkRank = 0   #more variables to see if the piece checking the king can be taken or not in checkmateCheck()
        checkFile = 0

        file = ord(pos[0]) - 97
        rank = 8 - int(pos[1])
        # check for pawns
        # white king
        if piece.color == 'white':
            if rank > 0:
                if file > 0 and (not self.board[rank - 1][file - 1].isSquare) and self.board[rank - 1][file - 1].name == 'pawn' and (not piece.color == self.board[rank - 1][file - 1].color):
                    check = True
                    checkCount += 1
                    checkRank = rank - 1
                    checkFile = file - 1
                elif file < 7 and (not self.board[rank - 1][file + 1].isSquare) and self.board[rank - 1][file + 1].name == 'pawn' and (not piece.color == self.board[rank - 1][file + 1].color):
                    check = True
                    checkCount += 1
                    checkRank = rank - 1
                    checkFile = file + 1
        # black king
        elif piece.color == 'black':
            if rank < 7:
                if file > 0 and (not self.board[rank + 1][file - 1].isSquare) and self.board[rank + 1][file - 1].name == 'pawn' and (not piece.color == self.board[rank + 1][file - 1].color):
                    check = True
                    checkCount += 1
                    checkRank = rank + 1
                    checkFile = file - 1
                elif file < 7 and (not self.board[rank + 1][file + 1].isSquare) and self.board[rank + 1][file + 1].name == 'pawn' and (not piece.color == self.board[rank + 1][file + 1].color):
                    check = True
                    checkCount += 1
                    checkRank = rank + 1
                    checkFile = file + 1

        # rook and queen
        # up
        for i in range(1, rank + 1):
            if (not self.board[rank - i][file].isSquare) and (piece.color == self.board[rank - i][file].color or self.board[rank - i][file].name == 'pawn' or self.board[rank - i][file].name == 'knight' or self.board[rank - i][file].name == 'bishop'):
                break
            elif (not self.board[rank - i][file].isSquare) and (not piece.color == self.board[rank - i][file].color) and (self.board[rank - i][file].name == 'queen' or self.board[rank - i][file].name == 'rook'):
                check = True
                checkCount += 1
                checkRank = rank - i
                checkFile = file
        # down
        for i in range(1, 8 - rank):
            if (not self.board[rank + i][file].isSquare) and (piece.color == self.board[rank + i][file].color or self.board[rank + i][file].name == 'pawn' or self.board[rank + i][file].name == 'knight' or self.board[rank + i][file].name == 'bishop'):
                break
            elif (not self.board[rank + i][file].isSquare) and (not piece.color == self.board[rank + i][file].color) and (self.board[rank + i][file].name == 'queen' or self.board[rank + i][file].name == 'rook'):
                check = True
                checkCount += 1
                checkRank = rank + i
                checkFile = file
        # left
        for i in range(1, file + 1):
            if (not self.board[rank][file - i].isSquare) and (piece.color == self.board[rank][file - i].color or self.board[rank][file - i].name == 'pawn' or self.board[rank][file - i].name == 'knight' or self.board[rank][file - i].name == 'bishop'):
                break
            elif (not self.board[rank][file - i].isSquare) and (not piece.color == self.board[rank][file - i].color) and (self.board[rank][file - i].name == 'queen' or self.board[rank][file - i].name == 'rook'):
                check = True
                checkCount += 1
                checkRank = rank
                checkFile = file - i
        # right
        for i in range(1, 8 - file):
            if (not self.board[rank][file + i].isSquare) and (piece.color == self.board[rank][file + i].color or self.board[rank][file + i].name == 'pawn' or self.board[rank][file + i].name == 'knight' or self.board[rank][file + i].name == 'bishop'):
                break
            elif (not self.board[rank][file + i].isSquare) and (not piece.color == self.board[rank][file + i].color) and (self.board[rank][file + i].name == 'queen' or self.board[rank][file + i].name == 'rook'):
                check = True
                checkCount += 1
                checkRank = rank
                checkFile = file + i

        # bishop and queen
        uRank = rank + 1  # some variables to iterate thru and stay on the board
        dRank = 8 - rank
        lFile = file + 1
        rFile = 8 - file
        # upleft
        if uRank > lFile or uRank == lFile:
            for i in range(1, lFile):
                if (not self.board[rank - i][file - i].isSquare) and (piece.color == self.board[rank - i][file - i].color or self.board[rank - i][file - i].name == 'pawn' or self.board[rank - i][file - i].name == 'knight' or self.board[rank - i][file - i].name == 'rook'):
                    break
                elif (not self.board[rank - i][file - i].isSquare) and (not piece.color == self.board[rank - i][file - i].color) and (self.board[rank - i][file - i].name == 'queen' or self.board[rank - i][file - i].name == 'bishop'):
                    check = True
                    checkCount += 1
                    checkRank = rank - i
                    checkFile = file - i
        elif uRank < lFile:
            for i in range(1, uRank):
                if (not self.board[rank - i][file - i].isSquare) and (piece.color == self.board[rank - i][file - i].color or self.board[rank - i][file - i].name == 'pawn' or self.board[rank - i][file - i].name == 'knight' or self.board[rank - i][file - i].name == 'rook'):
                    break
                elif (not self.board[rank - i][file - i].isSquare) and (not piece.color == self.board[rank - i][file - i].color) and (self.board[rank - i][file - i].name == 'queen' or self.board[rank - i][file - i].name == 'bishop'):
                    check = True
                    checkCount += 1
                    checkRank = rank - i
                    checkFile = file - i
        # upright
        if uRank > rFile or uRank == rFile:
            for i in range(1, rFile):
                if (not self.board[rank - i][file + i].isSquare) and (piece.color == self.board[rank - i][file + i].color or self.board[rank - i][file + i].name == 'pawn' or self.board[rank - i][file + i].name == 'knight' or self.board[rank - i][file + i].name == 'rook'):
                    break
                elif (not self.board[rank - i][file + i].isSquare) and (not piece.color == self.board[rank - i][file + i].color) and (self.board[rank - i][file + i].name == 'queen' or self.board[rank - i][file + i].name == 'bishop'):
                    check = True
                    checkCount += 1
                    checkRank = rank - i
                    checkFile = file + i
        elif uRank < rFile:
            for i in range(1, uRank):
                if (not self.board[rank - i][file + i].isSquare) and (piece.color == self.board[rank - i][file + i].color or self.board[rank - i][file + i].name == 'pawn' or self.board[rank - i][file + i].name == 'knight' or self.board[rank - i][file + i].name == 'rook'):
                    break
                elif (not self.board[rank - i][file + i].isSquare) and (not piece.color == self.board[rank - i][file + i].color) and (self.board[rank - i][file + i].name == 'queen' or self.board[rank - i][file + i].name == 'bishop'):
                    check = True
                    checkCount += 1
                    checkRank = rank - i
                    checkFile = file + i
        # downleft
        if dRank > lFile or dRank == lFile:
            for i in range(1, lFile):
                if (not self.board[rank + i][file - i].isSquare) and (piece.color == self.board[rank + i][file - i].color or self.board[rank + i][file - i].name == 'pawn' or self.board[rank + i][file - i].name == 'knight' or self.board[rank + i][file - i].name == 'rook'):
                    break
                elif (not self.board[rank + i][file - i].isSquare) and (not piece.color == self.board[rank + i][file - i].color) and (self.board[rank + i][file - i].name == 'queen' or self.board[rank + i][file - i].name == 'bishop'):
                    check = True
                    checkCount += 1
                    checkRank = rank + i
                    checkFile = file - i
        elif dRank < lFile:
            for i in range(1, dRank):
                if (not self.board[rank + i][file - i].isSquare) and (piece.color == self.board[rank + i][file - i].color or self.board[rank + i][file - i].name == 'pawn' or self.board[rank + i][file - i].name == 'knight' or self.board[rank + i][file - i].name == 'rook'):
                    break
                elif (not self.board[rank + i][file - i].isSquare) and (not piece.color == self.board[rank + i][file - i].color) and (self.board[rank + i][file - i].name == 'queen' or self.board[rank + i][file - i].name == 'bishop'):
                    check = True
                    checkCount += 1
                    checkRank = rank + i
                    checkFile = file - i
        # downright
        if dRank > rFile or dRank == rFile:
            for i in range(1, rFile):
                if (not self.board[rank + i][file + i].isSquare) and (piece.color == self.board[rank + i][file + i].color or self.board[rank + i][file + i].name == 'pawn' or self.board[rank + i][file + i].name == 'knight' or self.board[rank + i][file + i].name == 'rook'):
                    break
                elif (not self.board[rank + i][file + i].isSquare) and (not piece.color == self.board[rank + i][file + i].color) and (self.board[rank + i][file + i].name == 'queen' or self.board[rank + i][file + i].name == 'bishop'):
                    check = True
                    checkCount += 1
                    checkRank = rank + i
                    checkFile = file + i
        elif dRank < rFile:
            for i in range(1, dRank):
                if (not self.board[rank + i][file + i].isSquare) and (piece.color == self.board[rank + i][file + i].color or self.board[rank + i][file + i].name == 'pawn' or self.board[rank + i][file + i].name == 'knight' or self.board[rank + i][file + i].name == 'rook'):
                    break
                elif (not self.board[rank + i][file + i].isSquare) and (not piece.color == self.board[rank + i][file + i].color) and (self.board[rank + i][file + i].name == 'queen' or self.board[rank + i][file + i].name == 'bishop'):
                    check = True
                    checkCount += 1
                    checkRank = rank + i
                    checkFile = file + i

        # knights
        # up2
        if rank >= 2:
            # left1
            if file >= 1:
                if (not self.board[rank - 2][file - 1].isSquare) and (not piece.color == self.board[rank - 2][file - 1].color) and (self.board[rank - 2][file - 1].name == 'knight'):
                    check = True
                    checkCount += 1
                    checkRank = rank - 2
                    checkFile = file - 1
            # right1
            if file <= 6:
                if (not self.board[rank - 2][file + 1].isSquare) and (not piece.color == self.board[rank - 2][file + 1].color) and (self.board[rank - 2][file + 1].name == 'knight'):
                    check = True
                    checkCount += 1
                    checkRank = rank - 2
                    checkFile = file + 1
        # down2
        if rank <= 5:
            # left1
            if file >= 1:
                if (not self.board[rank + 2][file - 1].isSquare) and (not piece.color == self.board[rank + 2][file - 1].color) and (self.board[rank + 2][file - 1].name == 'knight'):
                    check = True
                    checkCount += 1
                    checkRank = rank + 2
                    checkFile = file - 1
            # right1
            if file <= 6:
                if (not self.board[rank + 2][file + 1].isSquare) and (not piece.color == self.board[rank + 2][file + 1].color) and (self.board[rank + 2][file + 1].name == 'knight'):
                    check = True
                    checkCount += 1
                    checkRank = rank + 2
                    checkFile = file + 1
        # left2
        if file >= 2:
            # up1
            if rank >= 1:
                if (not self.board[rank - 1][file - 2].isSquare) and (not piece.color == self.board[rank - 1][file - 2].color) and (self.board[rank - 1][file - 2].name == 'knight'):
                    check = True
                    checkCount += 1
                    checkRank = rank - 1
                    checkFile = file - 2
            # down1
            if rank <= 6:
                if (not self.board[rank + 1][file - 2].isSquare) and (not piece.color == self.board[rank + 1][file - 2].color) and (self.board[rank + 1][file - 2].name == 'knight'):
                    check = True
                    checkCount += 1
                    checkRank = rank + 1
                    checkFile = file - 2
        # right2
        if file <= 5:
            # up1
            if rank >= 1:
                if (not self.board[rank - 1][file + 2].isSquare) and (not piece.color == self.board[rank - 1][file + 2].color) and (self.board[rank - 1][file + 2].name == 'knight'):
                    check = True
                    checkCount += 1
                    checkRank = rank - 1
                    checkFile = file + 2
            # down1
            if rank <= 6:
                if (not self.board[rank + 1][file + 2].isSquare) and (not piece.color == self.board[rank + 1][file + 2].color) and (self.board[rank + 1][file + 2].name == 'knight'):
                    check = True
                    checkCount += 1
                    checkRank = rank + 1
                    checkFile = file + 2

        # kings (prevents illegal moves, i.e. king moves right next to the other king)
        if piece.name == 'king':
            # up
            if rank >= 1:
                # up1
                if (not self.board[rank - 1][file].isSquare) and (not piece.color == self.board[rank - 1][file].color) and self.board[rank - 1][file].name == 'king':
                    check = True
                # upleft
                if file >= 1:
                    if (not self.board[rank - 1][file - 1].isSquare) and (not piece.color == self.board[rank - 1][file - 1].color) and self.board[rank - 1][file - 1].name == 'king':
                        check = True
                # upright
                if file <= 6:
                    if (not self.board[rank - 1][file + 1].isSquare) and (not piece.color == self.board[rank - 1][file + 1].color) and self.board[rank - 1][file + 1].name == 'king':
                        check = True
            # down
            if rank <= 6:
                # down1
                if (not self.board[rank + 1][file].isSquare) and (not piece.color == self.board[rank + 1][file].color) and self.board[rank + 1][file].name == 'king':
                    check = True
                # downleft
                if file >= 1:
                    if (not self.board[rank + 1][file - 1].isSquare) and (not piece.color == self.board[rank + 1][file - 1].color) and self.board[rank + 1][file - 1].name == 'king':
                        check = True
                # downright
                if file <= 6:
                    if (not self.board[rank + 1][file + 1].isSquare) and (not piece.color == self.board[rank + 1][file + 1].color) and self.board[rank + 1][file + 1].name == 'king':
                        check = True
            # left1
            if file >= 1:
                if (not self.board[rank][file - 1].isSquare) and (not piece.color == self.board[rank][file - 1].color) and self.board[rank][file - 1].name == 'king':
                    check = True
            # right1
            if file <= 6:
                if (not self.board[rank][file + 1].isSquare) and (not piece.color == self.board[rank][file + 1].color) and self.board[rank][file + 1].name == 'king':
                    check = True

        checkPos = chr(checkFile + 97) + str(8 - checkRank)
        return check, checkCount, checkPos


    #check if square is blockable (basically check method but on square)
    def squareBlockable(self, rank, file, piece):
        blockable = False
        if self.board[rank][file].isSquare:
            #pawns
            if rank < 6:
                if (not self.board[rank + 1][file].isSquare) and self.board[rank + 1][file].name == 'pawn' and piece.color == self.board[rank + 1][file].color == 'white':
                    blockable = True
            elif rank > 1:
                if (not self.board[rank + 1][file].isSquare) and self.board[rank - 1][file].name == 'pawn' and piece.color == self.board[rank + 1][file].color == 'black':
                    blockable = True

            #rooks and queens
            #up
            for i in range(1, rank + 1):
                if (not self.board[rank - i][file].isSquare) and piece.color != self.board[rank - i][file].color:
                    break
                elif (not self.board[rank - i][file].isSquare) and (self.board[rank - i][file].name == 'rook' or self.board[rank - i][file].name == 'queen') and piece.color == self.board[rank - i][file].color:
                    blockable = True
            #down
            for i in range(1, 8 - rank):
                if (not self.board[rank + i][file].isSquare) and piece.color != self.board[rank + i][file].color:
                    break
                elif (not self.board[rank + i][file].isSquare) and (self.board[rank + i][file].name == 'rook' or self.board[rank + i][file].name == 'queen') and piece.color == self.board[rank + i][file].color:
                    blockable = True
            #left
            for i in range(1, file + 1):
                if (not self.board[rank][file - i].isSquare) and piece.color != self.board[rank][file - i].color:
                    break
                elif (not self.board[rank][file - i].isSquare) and (self.board[rank][file - i].name == 'rook' or self.board[rank][file - i].name == 'queen') and piece.color == self.board[rank][file - i].color:
                    blockable = True
            #right
            for i in range(1, 8 - file):
                if (not self.board[rank][file + i].isSquare) and piece.color != self.board[rank][file + i].color:
                    break
                elif (not self.board[rank][file + i].isSquare) and (self.board[rank][file + i].name == 'rook' or self.board[rank][file + i].name == 'queen') and piece.color == self.board[rank][file + i].color:
                    blockable = True

            #bishops and queens
            uRank = rank + 1
            dRank = 8 - rank
            lFile = file + 1
            rFile = 8 - file
            #upleft
            if uRank > lFile or uRank == lFile:
                for i in range(1, lFile):
                    if (not self.board[rank - i][file - i].isSquare) and piece.color != self.board[rank - i][file - i].color:
                        break
                    elif (not self.board[rank - i][file - i].isSquare) and (self.board[rank - i][file - i].name == 'bishop' or self.board[rank - i][file - i].name == 'queen') and piece.color == self.board[rank - i][file - i].color:
                        blockable = True
            elif uRank < lFile:
                for i in range(1, uRank):
                    if (not self.board[rank - i][file - i].isSquare) and piece.color != self.board[rank - i][file - i].color:
                        break
                    elif (not self.board[rank - i][file - i].isSquare) and (self.board[rank - i][file - i].name == 'bishop' or self.board[rank - i][file - i].name == 'queen') and piece.color == self.board[rank - i][file - i].color:
                        blockable = True
            #upright
            if uRank > rFile or uRank == rFile:
                for i in range(1, rFile):
                    if (not self.board[rank - i][file + i].isSquare) and piece.color != self.board[rank - i][file + i].color:
                        break
                    elif (not self.board[rank - i][file + i].isSquare) and (self.board[rank - i][file + i].name == 'bishop' or self.board[rank - i][file + i].name == 'queen') and piece.color == self.board[rank - i][file + i].color:
                        blockable = True
            elif uRank < rFile:
                for i in range(1, uRank):
                    if (not self.board[rank - i][file + i].isSquare) and piece.color != self.board[rank - i][file + i].color:
                        break
                    elif (not self.board[rank - i][file + i].isSquare) and (self.board[rank - i][file + i].name == 'bishop' or self.board[rank - i][file + i].name == 'queen') and piece.color == self.board[rank - i][file + i].color:
                        blockable = True
            #downleft
            if dRank > lFile or dRank == lFile:
                for i in range(1, lFile):
                    if (not self.board[rank + i][file - i].isSquare) and piece.color != self.board[rank + i][file - i].color:
                        break
                    elif (not self.board[rank + i][file - i].isSquare) and (self.board[rank + i][file - i].name == 'bishop' or self.board[rank + i][file - i].name == 'queen') and piece.color == self.board[rank + i][file - i].color:
                        blockable = True
            elif dRank < lFile:
                for i in range(1, dRank):
                    if (not self.board[rank + i][file - i].isSquare) and piece.color != self.board[rank + i][file - i].color:
                        break
                    elif (not self.board[rank + i][file - i].isSquare) and (self.board[rank + i][file - i].name == 'bishop' or self.board[rank + i][file - i].name == 'queen') and piece.color == self.board[rank + i][file - i].color:
                        blockable = True
            #downright
            if dRank > rFile or dRank == rFile:
                for i in range(1, rFile):
                    if (not self.board[rank + i][file + i].isSquare) and piece.color != self.board[rank + i][file + i].color:
                        break
                    elif (not self.board[rank + i][file + i].isSquare) and (self.board[rank + i][file + i].name == 'bishop' or self.board[rank + i][file + i].name == 'queen') and piece.color == self.board[rank + i][file + i].color:
                        blockable = True
            elif dRank < rFile:
                for i in range(1, dRank):
                    if (not self.board[rank + i][file + i].isSquare) and piece.color != self.board[rank + i][file + i].color:
                        break
                    elif (not self.board[rank + i][file + i].isSquare) and (self.board[rank + i][file + i].name == 'bishop' or self.board[rank + i][file + i].name == 'queen') and piece.color == self.board[rank + i][file + i].color:
                        blockable = True

            #knights
            #up2
            if rank >= 2:
                #left1
                if file >= 1:
                    if (not self.board[rank - 2][file - 1].isSquare) and self.board[rank - 2][file - 1].name == 'knight' and piece.color == self.board[rank - 2][file - 1].color:
                        blockable = True
                #right1
                if file <= 6:
                    if (not self.board[rank - 2][file + 1].isSquare) and self.board[rank - 2][file + 1].name == 'knight' and piece.color == self.board[rank - 2][file + 1].color:
                        blockable = True
            #down 2
            if rank <= 5:
                #left1
                if file >= 1:
                    if (not self.board[rank + 2][file - 1].isSquare) and self.board[rank + 2][file - 1].name == 'knight' and piece.color == self.board[rank + 2][file - 1].color:
                        blockable = True
                #right1
                if file <= 6:
                    if (not self.board[rank + 2][file + 1].isSquare) and self.board[rank + 2][file + 1].name == 'knight' and piece.color == self.board[rank + 2][file + 1].color:
                        blockable = True
            #left2
            if file >= 2:
                #up1
                if file >= 1:
                    if (not self.board[rank - 1][file - 2].isSquare) and self.board[rank - 1][file - 2].name == 'knight' and piece.color == self.board[rank - 1][file - 2].color:
                        blockable = True
                #right1
                if file <= 6:
                    if (not self.board[rank + 1][file - 2].isSquare) and self.board[rank + 1][file - 2].name == 'knight' and piece.color == self.board[rank + 1][file - 2].color:
                        blockable = True
            #right2
            if file <= 5:
                #up1
                if file >= 1:
                    if (not self.board[rank - 1][file + 2].isSquare) and self.board[rank - 1][file + 2].name == 'knight' and piece.color == self.board[rank - 1][file + 2].color:
                        blockable = True
                #right1
                if file <= 6:
                    if (not self.board[rank + 1][file + 2].isSquare) and self.board[rank + 1][file + 2].name == 'knight' and piece.color == self.board[rank + 1][file + 2].color:
                        blockable = True

        return blockable

    #squareBlockable(rank, file, piece)
    #method to see if the checking piece can be blocked
    def checkBlockable(self, piece, checkpiece):
        blockable = False
        file = ord(piece.position[0]) - 97
        rank = 8 - int(piece.position[1])
        checkRank = 8 - int((self.checkCheck(piece.position, piece)[2])[1])
        checkFile = ord((self.checkCheck(piece.position, piece)[2])[0]) - 97



        #rook and queen checking the king
        if checkFile == file:
            #up
            if checkRank < rank:
                for i in range(1, rank - checkRank):
                    blockable = self.squareBlockable(rank - i, file, piece)
                    if blockable == True:
                        break
            #down
            elif checkRank > rank:
                for i in range(1, checkRank - rank):
                    blockable = self.squareBlockable(rank + i, file, piece)
                    if blockable == True:
                        break
        elif checkRank == rank:
            #left
            if checkFile < file:
                for i in range(1, file - checkFile):
                    blockable = self.squareBlockable(rank, file - i, piece)
                    if blockable == True:
                        break
            #right
            if checkFile > file:
                for i in range(1, checkFile - file):
                    blockable = self.squareBlockable(ranke, file + i, piece)
                    if blockable == True:
                        break
        #bishop and queen checking the king
        elif abs(checkRank - rank) == abs(checkFile - file):
            #up
            if checkRank < rank:
                #upleft
                if checkFile < file:
                    for i in range (1, file - checkFile):
                        blockable == self.squareBlockable(rank - i, file - i, piece)
                        if blockable == True:
                            break
                #upright
                elif checkFile > file:
                    for i in range(1, checkFile - file):
                        blockable = self.squareBlockable(rank - i, file + i, piece)
                        if blockable == True:
                            break
            #down
            elif checkRank > rank:
                #downleft
                if checkFile < file:
                    for i in range (1, file - checkFile):
                        blockable = self.squareBlockable(rank + i, file - i, piece)
                        if blockable == True:
                            break
                #downright
                elif checkFile > file:
                    for i in range(1, checkFile - file):
                        blockable = self.squareBlockable(rank + i, file + i, piece)
                        if blockable == True:
                            break

        return blockable


    #checks if king can move to any adjacent square to get out of check
    def checkmateHelper(self, rank, file, piece):
        noMoves = False
        # list to iterate thru open spaces (or spaces that dont have a piece of the same color)
        openSpaces = []
        # counter for usage later
        spaceCount = 0
        if rank > 0 and rank < 7:
            if file > 0 and file < 7:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if self.board[rank + i][file + j].isSquare or ((not self.board[rank + i][file + j].isSquare) and piece.color != self.board[rank + i][file + j].color):
                            openSpaces.append(Space(rank + i, file + j, True))
                            spaceCount += 1

                self.board[rank][file] = self.newSquare(piece.position)
                for space in openSpaces:
                    if space.open and self.checkCheck(space.position, piece)[0]:
                        spaceCount -= 1
                self.board[rank][file] = piece
            elif file == 0:
                for i in range(-1, 2):
                    for j in range(2):
                        if self.board[rank + i][file + j].isSquare or ((not self.board[rank + i][file + j].isSquare) and piece.color != self.board[rank + i][file + j].color):
                            openSpaces.append(Space(rank + i, file + j, True))
                            spaceCount += 1
                self.board[rank][file] = self.newSquare(piece.position)
                for space in openSpaces:
                    if space.open and self.checkCheck(space.position, piece)[0]:
                        spaceCount -= 1
                self.board[rank][file] = piece
            elif file == 7:
                for i in range(-1, 2):
                    for j in range(-1, 1):
                        if self.board[rank + i][file + j].isSquare or ((not self.board[rank + i][file + j].isSquare) and piece.color != self.board[rank + i][file + j].color):
                            openSpaces.append(Space(rank + i, file + j, True))
                            spaceCount += 1
                self.board[rank][file] = self.newSquare(piece.position)
                for space in openSpaces:
                    if space.open and self.checkCheck(space.position, piece)[0]:
                        spaceCount -= 1
                self.board[rank][file] = piece
        elif rank == 0:
            if file > 0 and file < 7:
                for i in range(2):
                    for j in range(-1, 2):
                        if self.board[rank + i][file + j].isSquare or ((not self.board[rank + i][file + j].isSquare) and piece.color != self.board[rank + i][file + j].color):
                            openSpaces.append(Space(rank + i, file + j, True))
                            spaceCount += 1
                self.board[rank][file] = self.newSquare(piece.position)
                for space in openSpaces:
                    if space.open and self.checkCheck(space.position, piece)[0]:
                        spaceCount -= 1
                self.board[rank][file] = piece
            elif file == 0:
                for i in range(2):
                    for j in range(2):
                        if self.board[rank + i][file + j].isSquare or ((not self.board[rank + i][file + j].isSquare) and piece.color != self.board[rank + i][file + j].color):
                            openSpaces.append(Space(rank + i, file + j, True))
                            spaceCount += 1
                self.board[rank][file] = self.newSquare(piece.position)
                for space in openSpaces:
                    if space.open and self.checkCheck(space.position, piece)[0]:
                        spaceCount -= 1
                self.board[rank][file] = piece
            elif file == 7:
                for i in range(2):
                    for j in range(-1, 1):
                        if self.board[rank + i][file + j].isSquare or ((not self.board[rank + i][file + j].isSquare) and piece.color != self.board[rank + i][file + j].color):
                            openSpaces.append(Space(rank + i, file + j, True))
                            spaceCount += 1
                self.board[rank][file] = self.newSquare(piece.position)
                for space in openSpaces:
                    if space.open and self.checkCheck(space.position, piece)[0]:
                        spaceCount -= 1
                self.board[rank][file] = piece
        elif rank == 7:
            if file > 0 and file < 7:
                for i in range(-1, 1):
                    for j in range(-1, 2):
                        if self.board[rank + i][file + j].isSquare or ((not self.board[rank + i][file + j].isSquare) and piece.color != self.board[rank + i][file + j].color):
                            openSpaces.append(Space(rank + i, file + j, True))
                            spaceCount += 1
                self.board[rank][file] = self.newSquare(piece.position)
                for space in openSpaces:
                    if space.open and self.checkCheck(space.position, piece)[0]:
                        spaceCount -= 1
                self.board[rank][file] = piece
            elif file == 0:
                for i in range(-1, 1):
                    for j in range(2):
                        if self.board[rank + i][file + j].isSquare or ((not self.board[rank + i][file + j].isSquare) and piece.color != self.board[rank + i][file + j].color):
                            openSpaces.append(Space(rank + i, file + j, True))
                            spaceCount += 1
                self.board[rank][file] = self.newSquare(piece.position)
                for space in openSpaces:
                    if space.open and self.checkCheck(space.position, piece)[0]:
                        spaceCount -= 1
                self.board[rank][file] = piece
            elif file == 7:
                for i in range(-1, 1):
                    for j in range(-1, 1):
                        if self.board[rank + i][file + j].isSquare or ((not self.board[rank + i][file + j].isSquare) and piece.color != self.board[rank + i][file + j].color):
                            openSpaces.append(Space(rank + i, file + j, True))
                            spaceCount += 1
                self.board[rank][file] = self.newSquare(piece.position)
                for space in openSpaces:
                    if space.open and self.checkCheck(space.position, piece)[0]:
                        spaceCount -= 1
                self.board[rank][file] = piece
                # HAVE TO CHECK IF MY OWN PIECES ARE BLOCKING THE BOARD BUT I THINK I ALREADY DO THAT IN checkCheck()
        # HAVE TO CHECK IF ONE OF MY PIECES CAN BLOCK THE CHECK
        if spaceCount == 0:
            noMoves = True
        return noMoves

    #checkmateHelper(rank, file, piece)
    #Space(self, rank, file, open)
    #checkCheck(pos, piece)
        #returns check(boolean), checkCount(int), checkPos(str)
    def checkCheckmate(self, piece):
        checkmate = False
        file = ord(piece.position[0]) - 97
        rank = 8 - int(piece.position[1])
        checkRank = 8 - int((self.checkCheck(piece.position, piece)[2])[1])
        checkFile = ord((self.checkCheck(piece.position, piece)[2])[0]) - 97


        #checkmate if more than one piece checking the king and the king has no free spaces
        if self.checkmateHelper(rank, file, piece) and self.checkCheck(piece.position, piece)[1] > 1:
            checkmate = True

        #checkmate if king has no moves and the piece checking cannot be taken or blocked
        if self.checkCheck(piece.position, piece)[0] and self.checkmateHelper(rank, file, piece) and (not self.checkCheck(self.checkCheck(piece.position, piece)[2], self.board[checkRank][checkFile])[0]) and (not self.checkBlockable(piece, self.board[checkRank][checkFile])):
            checkmate = True

        return checkmate

    #stalemate checker
    def checkStalemate(self, piece):
        stalemate = True
        kingRank = 8 - int(piece.position[1])
        kingFile = ord(piece.position[0]) - 97
        if self.checkmateHelper(kingRank, kingFile, piece) and (not self.checkCheck(piece.position, piece)[0]):
            print('what')
            for i in range(8):
                for j in range(8):
                    if (not self.board[i][j].isSquare) and piece.color == self.board[i][j].color:
                        oPiece = self.board[i][j]
                        #pawns
                        if oPiece.name == 'pawn':
                            if oPiece.color == 'white':
                                if j > 0 and (not self.board[i - 1][j - 1].isSquare) and piece.color != self.board[i - 1][j - 1].color:
                                    taken = self.board[i - 1][j - 1]
                                    self.board[i - 1][j - 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i - 1][j - 1] = taken
                                    self.board[i][j] = oPiece
                                if j < 7 and (not self.board[i - 1][j + 1].isSquare) and piece.color != self.board[i - 1][j + 1].color:
                                    taken = self.board[i - 1][j + 1]
                                    self.board[i - 1][j + 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i - 1][j + 1] = taken
                                    self.board[i][j] = oPiece
                                if self.board[i - 1][j].isSquare:
                                    taken = self.board[i - 1][j]
                                    self.board[i - 1][j] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i - 1][j] = taken
                                    self.board[i][j] = oPiece
                            elif oPiece.color == 'black':
                                if j > 0 and (not self.board[i + 1][j - 1].isSquare) and piece.color != self.board[i + 1][j - 1].color:
                                    taken = self.board[i + 1][j - 1]
                                    self.board[i + 1][j - 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i + 1][j - 1] = taken
                                    self.board[i][j] = oPiece
                                if j < 7 and (not self.board[i + 1][j + 1].isSquare) and piece.color != self.board[i + 1][j + 1].color:
                                    taken = self.board[i + 1][j + 1]
                                    self.board[i + 1][j + 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i + 1][j + 1] = taken
                                    self.board[i][j] = oPiece
                                if self.board[i + 1][j].isSquare:
                                    taken = self.board[i + 1][j]
                                    self.board[i + 1][j] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i + 1][j] = taken
                                    self.board[i][j] = oPiece
                        elif oPiece.name == 'rook':
                            if i > 0:
                                if not ((not self.board[i - 1][j].isSquare) and piece.color == self.board[i - 1][j].color):
                                    taken = self.board[i - 1][j]
                                    self.board[i - 1][j] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i - 1][j] = taken
                                    self.board[i][j] = oPiece
                            if i < 7:
                                if not ((not self.board[i + 1][j].isSquare) and piece.color == self.board[i + 1][j].color):
                                    taken = self.board[i + 1][j]
                                    self.board[i + 1][j] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i + 1][j] = taken
                                    self.board[i][j] = oPiece
                            if j > 0:
                                if not ((not self.board[i][j - 1].isSquare) and piece.color == self.board[i][j - 1].color):
                                    taken = self.board[i][j - 1]
                                    self.board[i][j - 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i][j - 1] = taken
                                    self.board[i][j] = oPiece
                            if j < 7:
                                if not ((not self.board[i][j + 1].isSquare) and piece.color == self.board[i][j + 1].color):
                                    taken = self.board[i][j + 1]
                                    self.board[i][j + 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i][j + 1] = taken
                                    self.board[i][j] = oPiece
                        elif oPiece.name == 'knight':
                            if i >= 2:
                                if j > 0:
                                    if not ((not self.board[i - 2][j - 1].isSquare) and piece.color == self.board[i - 2][j - 1].color):
                                        taken = self.board[i - 2][j - 1]
                                        self.board[i - 2][j - 1] = oPiece
                                        self.board[i][j] = self.newSquare(oPiece.position)
                                        if not self.checkCheck(piece.position, piece)[0]:
                                            stalemate = False
                                        self.board[i - 2][j - 1] = taken
                                        self.board[i][j] = oPiece
                                if j < 7:
                                    if not ((not self.board[i - 2][j + 1].isSquare) and piece.color == self.board[i - 2][j + 1].color):
                                        taken = self.board[i - 2][j + 1]
                                        self.board[i - 2][j + 1] = oPiece
                                        self.board[i][j] = self.newSquare(oPiece.position)
                                        if not self.checkCheck(piece.position, piece)[0]:
                                            stalemate = False
                                        self.board[i - 2][j + 1] = taken
                                        self.board[i][j] = oPiece
                            if i <= 5:
                                if j > 0:
                                    if not ((not self.board[i + 2][j - 1].isSquare) and piece.color == self.board[i + 2][j - 1].color):
                                        taken = self.board[i + 2][j - 1]
                                        self.board[i + 2][j - 1] = oPiece
                                        self.board[i][j] = self.newSquare(oPiece.position)
                                        if not self.checkCheck(piece.position, piece)[0]:
                                            stalemate = False
                                        self.board[i + 2][j - 1] = taken
                                        self.board[i][j] = oPiece
                                if j < 7:
                                    if not ((not self.board[i + 2][j + 1].isSquare) and piece.color == self.board[i + 2][j + 1].color):
                                        taken = self.board[i + 2][j + 1]
                                        self.board[i + 2][j + 1] = oPiece
                                        self.board[i][j] = self.newSquare(oPiece.position)
                                        if not self.checkCheck(piece.position, piece)[0]:
                                            stalemate = False
                                        self.board[i + 2][j + 1] = taken
                                        self.board[i][j] = oPiece
                            if j >= 2:
                                if i > 0:
                                    if not ((not self.board[i - 1][j - 2].isSquare) and piece.color == self.board[i - 1][j - 2].color):
                                        taken = self.board[i - 1][j - 2]
                                        self.board[i - 1][j - 2] = oPiece
                                        self.board[i][j] = self.newSquare(oPiece.position)
                                        if not self.checkCheck(piece.position, piece)[0]:
                                            stalemate = False
                                        self.board[i - 1][j - 2] = taken
                                        self.board[i][j] = oPiece
                                if i < 7:
                                    if not ((not self.board[i + 1][j - 2].isSquare) and piece.color == self.board[i + 1][j - 2].color):
                                        taken = self.board[i + 1][j - 2]
                                        self.board[i + 1][j - 2] = oPiece
                                        self.board[i][j] = self.newSquare(oPiece.position)
                                        if not self.checkCheck(piece.position, piece)[0]:
                                            stalemate = False
                                        self.board[i + 1][j - 2] = taken
                                        self.board[i][j] = oPiece
                            if j <= 5:
                                if i > 0:
                                    if not ((not self.board[i - 1][j + 2].isSquare) and piece.color == self.board[i - 1][j + 2].color):
                                        taken = self.board[i - 1][j + 2]
                                        self.board[i - 1][j + 2] = oPiece
                                        self.board[i][j] = self.newSquare(oPiece.position)
                                        if not self.checkCheck(piece.position, piece)[0]:
                                            stalemate = False
                                        self.board[i - 1][j + 2] = taken
                                        self.board[i][j] = oPiece
                                if i < 7:
                                    if not ((not self.board[i + 1][j + 2].isSquare) and piece.color == self.board[i + 1][j + 2].color):
                                        taken = self.board[i + 1][j + 2]
                                        self.board[i + 1][j + 2] = oPiece
                                        self.board[i][j] = self.newSquare(oPiece.position)
                                        if not self.checkCheck(piece.position, piece)[0]:
                                            stalemate = False
                                        self.board[i + 1][j + 2] = taken
                                        self.board[i][j] = oPiece
                        elif oPiece.name == 'bishop':
                            if i > 0:
                                if j > 0 and (not ((not self.board[i - 1][j - 1].isSquare) and piece.color == self.board[i - 1][j - 1].color)):
                                    taken = self.board[i - 1][j - 1]
                                    self.board[i - 1][j - 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i - 1][j - 1] = taken
                                    self.board[i][j] = oPiece
                                if j < 7 and (not ((not self.board[i - 1][j + 1].isSquare) and piece.color == self.board[i - 1][j + 1].color)):
                                    taken = self.board[i - 1][j + 1]
                                    self.board[i - 1][j + 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i - 1][j + 1] = taken
                                    self.board[i][j] = oPiece
                            if i < 7:
                                if j > 0 and (not ((not self.board[i + 1][j - 1].isSquare) and piece.color == self.board[i + 1][j - 1].color)):
                                    taken = self.board[i + 1][j - 1]
                                    self.board[i + 1][j - 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i + 1][j - 1] = taken
                                    self.board[i][j] = oPiece
                                if j < 7 and (not ((not self.board[i + 1][j + 1].isSquare) and piece.color == self.board[i + 1][j + 1].color)):
                                    taken = self.board[i + 1][j + 1]
                                    self.board[i + 1][j + 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i + 1][j + 1] = taken
                                    self.board[i][j] = oPiece
                        elif oPiece.name == 'queen':
                            if i > 0:
                                if not ((not self.board[i - 1][j].isSquare) and piece.color == self.board[i - 1][j].color):
                                    taken = self.board[i - 1][j]
                                    self.board[i - 1][j] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i - 1][j] = taken
                                    self.board[i][j] = oPiece
                                if j > 0 and (not ((not self.board[i - 1][j - 1].isSquare) and piece.color == self.board[i - 1][j - 1].color)):
                                    taken = self.board[i - 1][j - 1]
                                    self.board[i - 1][j - 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i - 1][j - 1] = taken
                                    self.board[i][j] = oPiece
                                if j < 7 and (not ((not self.board[i - 1][j + 1].isSquare) and piece.color == self.board[i - 1][j + 1].color)):
                                    taken = self.board[i - 1][j + 1]
                                    self.board[i - 1][j + 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i - 1][j + 1] = taken
                                    self.board[i][j] = oPiece
                            if i < 7:
                                if not ((not self.board[i + 1][j].isSquare) and piece.color == self.board[i + 1][j].color):
                                    taken = self.board[i + 1][j]
                                    self.board[i + 1][j] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i + 1][j] = taken
                                    self.board[i][j] = oPiece
                                if j > 0 and (not ((not self.board[i + 1][j - 1].isSquare) and piece.color == self.board[i + 1][j - 1].color)):
                                    taken = self.board[i + 1][j - 1]
                                    self.board[i + 1][j - 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i + 1][j - 1] = taken
                                    self.board[i][j] = oPiece
                                if j < 7 and (not ((not self.board[i + 1][j + 1].isSquare) and piece.color == self.board[i + 1][j + 1].color)):
                                    taken = self.board[i + 1][j + 1]
                                    self.board[i + 1][j + 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i + 1][j + 1] = taken
                                    self.board[i][j] = oPiece
                            if j > 0:
                                if not ((not self.board[i][j - 1].isSquare) and piece.color == self.board[i][j - 1].color):
                                    taken = self.board[i][j - 1]
                                    self.board[i][j - 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i][j - 1] = taken
                                    self.board[i][j] = oPiece
                            if j < 7:
                                if not ((not self.board[i][j + 1].isSquare) and piece.color == self.board[i][j + 1].color):
                                    taken = self.board[i][j + 1]
                                    self.board[i][j + 1] = oPiece
                                    self.board[i][j] = self.newSquare(oPiece.position)
                                    if not self.checkCheck(piece.position, piece)[0]:
                                        stalemate = False
                                    self.board[i][j + 1] = taken
                                    self.board[i][j] = oPiece

                if not stalemate:
                    break
        elif (not self.checkmateHelper(kingRank, kingFile, piece) or self.checkCheck(piece.position, piece)[0]):
            stalemate = False
        return stalemate


    #pawn promotion method
    def promotion(self, piece):
        promote = input('Promote pawn to a queen, rook, bishop, or knight? ')
        if promote.lower() == 'queen':
            piece.name = 'queen'
            if piece.color == 'white':
                piece.piece = Piece.wQueen
            else:
                piece.piece = Piece.bQueen
        elif promote.lower() == 'rook':
            piece.name = 'rook'
            if piece.color == 'white':
                piece.piece = Piece.wRook
            else:
                piece.piece = Piece.bRook
        elif promote.lower() == 'bishop':
            piece.name = 'bishop'
            if piece.color == 'white':
                piece.piece = Piece.wBishop
            else:
                piece.piece = Piece.bBishop
        elif promote.lower() == 'knight':
            piece.name = 'knight'
            if piece.color == 'white':
                piece.piece = Piece.wKnight
            else:
                piece.piece = Piece.bKnight
        else:
            print('Not a valid piece. Please type "queen" or "rook", etc.')
            self.promotion(piece)

    #en passant checker
    #purpose: the capture can only be made on the move immediately after the enemy pawn makes the double-step move
    #so once another move other than en passant is made, i have to make piece.enPass = False for all pawns
    def enPassCheck(self):
        for i in range(8):
            for j in range(8):
                if (not self.board[i][j].isSquare) and self.board[i][j].name == 'pawn' and self.board[i][j].enPass == True:
                    self.board[i][j].enPass = False

    #move function for each piece
    def move(self, fromPos, toPos):
        fromRank = 0
        fromFile = 0
        toRank = 0
        toFile = 0
        pieceMoved = False

        try:
            # set files and ranks to something usable when calling board[][]
            fromFile = ord(fromPos[0]) - 97
            fromRank = 8 - int(fromPos[1])
            toFile = ord(toPos[0]) - 97
            toRank = 8 - int(toPos[1])
        except:
            print('Invalid input. Please enter a valid square on the board.')





        '''
        I HAVE TO IMPLEMENT SOME SPECIAL CASES:
        1. CASTLING (done)
        2. EN PASSANT
        3. WHEN A PAWN MAKES IT TO THE LAST RANK, IT CAN CHANGE TO A ROOK, BISHOP, KNIGHT, OR QUEEN (done) 
        '''
        #check if the move is on the board (can't move to side squares and can't go off board like 'x10' instead of 'e3')
        if fromRank >= 0 and fromRank <= 7 and fromFile >= 0 and fromFile <= 7 and toRank >= 0 and toRank <= 7 and toFile >= 0 and toFile <= 7:

            if (not self.board[fromRank][fromFile].isSquare) and self.turn == self.board[fromRank][fromFile].color:
                piece = self.board[fromRank][fromFile]
                #look for king to use checkCheck on every move (if a piece was moved that lead to their own king to be checked, that move is invalid)
                king = Piece(None, None, None, None, None)
                for i in range(8):
                    for j in range(8):
                        if (not self.board[i][j].isSquare) and self.board[i][j].color == piece.color and self.board[i][j].name == 'king':
                            king = self.board[i][j]

                #pawns
                if piece.name == 'pawn':
                    #pawn moves 2 spaces forward so i have to check if the spaces are empty
                    if piece.moved == False and ((piece.color == 'white' and int(toPos[1]) - int(fromPos[1]) == 2) or (piece.color == 'black' and int(fromPos[1]) - int(toPos[1]) == 2)) and fromFile == toFile and self.board[toRank][toFile].isSquare and ((piece.color == 'white' and self.board[fromRank - 1][fromFile].isSquare) or (piece.color == 'black' and self.board[fromRank + 1][fromFile].isSquare)):
                        piece.changePos(toPos)
                        self.board[toRank][toFile] = piece
                        self.board[fromRank][fromFile] = self.newSquare(fromPos)
                        piece.moved = True
                        if self.checkCheck(king.position, king)[0]:
                            piece.move(toPos, fromPos)
                            piece.moved = False
                            print('Invalid move. King is in check or will be in check from this move.')
                        else:
                            self.enPassCheck()
                            piece.enPass = True
                            pieceMoved = True

                    #pawn moves 1 space forward
                    elif ((piece.color == 'white' and int(toPos[1]) - int(fromPos[1]) == 1) or (piece.color == 'black' and int(fromPos[1]) - int(toPos[1]) == 1)) and fromFile == toFile and self.board[toRank][toFile].isSquare:
                        piece.changePos(toPos)
                        self.board[toRank][toFile] = piece
                        self.board[fromRank][fromFile] = self.newSquare(fromPos)
                        checkMoved = piece.moved
                        piece.moved = True
                        if self.checkCheck(king.position, king)[0]:
                            piece.move(toPos, fromPos)
                            print('Invalid move. King is in check or will be in check from this move.')
                            if not checkMoved:
                                piece.moved = False
                        elif piece.color == 'white' and toPos[1] == '8':
                            self.promotion(piece)
                            self.enPassCheck()
                            pieceMoved = True
                        elif piece.color == 'black' and toPos[1] == '1':
                            self.promotion(piece)
                            self.enPassCheck()
                            pieceMoved = True
                        else:
                            self.enPassCheck()
                            pieceMoved = True

                    #pawn capture (have to check if the piece being captured is of the opposite color)
                    elif ((piece.color == 'white' and int(toPos[1]) - int(fromPos[1]) == 1) or (piece.color == 'black' and int(fromPos[1]) - int(toPos[1]) == 1)) and (abs(fromFile - toFile) == 1) and (not self.board[toRank][toFile].isSquare) and (not piece.color == self.board[toRank][toFile].color):
                        piece.changePos(toPos)
                        captured = self.board[toRank][toFile]
                        self.board[toRank][toFile] = piece
                        self.board[fromRank][fromFile] = self.newSquare(fromPos)
                        piece.moved = True
                        if self.checkCheck(king.position, king)[0]:
                            piece.changePos(fromPos)
                            self.board[fromRank][fromFile] = piece
                            self.board[toRank][toFile] = captured
                            print('Invalid move. King is in check or will be in check from this move.')
                            if not checkMoved:
                                piece.moved = False
                        elif piece.color == 'white' and toPos[1] == 8:
                            self.promotion(piece)
                            self.enPassCheck()
                            pieceMoved = True
                        elif piece.color == 'black' and toPos[1] == 1:
                            self.promotion(piece)
                            self.enPassCheck()
                            pieceMoved = True
                        else:
                            self.enPassCheck()
                            pieceMoved = True

                    #en passant
                    elif ((piece.color == 'white' and int(toPos[1]) - int(fromPos[1]) == 1) or (piece.color == 'black' and int(fromPos[1]) - int(toPos[1]) == 1)) and (abs(fromFile - toFile) == 1) and self.board[toRank][toFile].isSquare:
                        #miraculously, this en passant method works on every board color and every pawn color and everything :D
                        if (not self.board[fromRank][toFile].isSquare) and piece.color != self.board[fromRank][toFile].color and self.board[fromRank][toFile].name == 'pawn' and self.board[fromRank][toFile].enPass == True:
                            piece.changePos(toPos)
                            passed = self.board[fromRank][toFile]
                            self.board[toRank][toFile] = piece
                            self.board[fromRank][fromFile] = self.newSquare(fromPos)
                            self.board[fromRank][toFile] = self.newSquare(self.board[fromRank][toFile].position)
                            if self.checkCheck(king.position, king)[0]:
                                piece.changePos(fromPos)
                                self.board[toRank][toFile] = self.newSquare(toPos)
                                self.board[fromRank][fromFile] = piece
                                self.board[fromRank][toFile] = passed
                                print('Invalid move. King is in check or will be in check from this move.')
                            else:
                                self.enPassCheck()
                                pieceMoved = True



                    else:
                        print('Not a valid pawn move.')

                #knights move is easier (i think) because i dont have to check for empty squares
                #only check if landing square is empty or has a piece of the opposite color
                elif piece.name == 'knight':
                    #forward/back 2, left/right 1
                    if (abs(fromRank - toRank) == 2) and (abs(fromFile - toFile) == 1) and (self.board[toRank][toFile].isSquare or (not piece.color == self.board[toRank][toFile].color)):
                        captured = self.board[toRank][toFile]
                        piece.changePos(toPos)
                        self.board[toRank][toFile] = piece
                        self.board[fromRank][fromFile] = self.newSquare(fromPos)
                        if self.checkCheck(king.position, king)[0]:
                            self.board[toRank][toFile] = captured
                            piece.changePos(fromPos)
                            self.board[fromRank][fromFile] = piece
                            print('Invalid move. King is in check or will be in check from this move.')
                        else:
                            self.enPassCheck()
                            pieceMoved = True

                    #left/right 2, forward/back 1
                    elif (abs(fromRank - toRank) == 1) and (abs(fromFile - toFile) == 2) and (self.board[toRank][toFile].isSquare or (not piece.color == self.board[toRank][toFile].color)):
                        captured = self.board[toRank][toFile]
                        piece.changePos(toPos)
                        self.board[toRank][toFile] = piece
                        self.board[fromRank][fromFile] = self.newSquare(fromPos)
                        if self.checkCheck(king.position, king)[0]:
                            self.board[toRank][toFile] = captured
                            piece.changePos(fromPos)
                            self.board[fromRank][fromFile] = piece
                            print('Invalid move. King is in check or will be in check from this move.')
                        else:
                            self.enPassCheck()
                            pieceMoved = True

                    else:
                        print('Not a valid knight move.')

                #rooks
                #gonna be a tough one cuz i gotta check for all squares ahead, behind, to the left, and to the right of the piece
                elif piece.name == 'rook':
                    clear = True  #boolean to check if the path of movement is clear
                    #forward and back
                    if fromFile == toFile:
                        if fromRank > toRank:
                            for i in range(toRank, fromRank):
                                if not self.board[i][fromFile].isSquare:
                                    if piece.color == self.board[i][fromFile].color:
                                        clear = False
                                    elif i > toRank and (not piece.color == self.board[i][fromFile].color):
                                        clear = False
                        elif fromRank < toRank:
                            for i in range(fromRank + 1, toRank + 1):
                                if (not self.board[i][fromFile].isSquare):
                                    if piece.color == self.board[i][fromFile].color:
                                        clear = False
                                    elif i < toRank and (not piece.color == self.board[i][fromFile].color):
                                        clear = False
                        else:
                            clear = False
                    #left and right
                    elif fromRank == toRank:
                        if fromFile > toFile:
                            for i in range(toFile, fromFile):
                                if not self.board[fromRank][i].isSquare:
                                    if piece.color == self.board[fromRank][i].color:
                                        clear = False
                                    elif i > toFile and (not piece.color == self.board[fromRank][i].color):
                                        clear = False
                        elif fromFile < toFile:
                            for i in range(fromFile + 1, toFile + 1):
                                if not self.board[fromRank][i].isSquare:
                                    if piece.color == self.board[fromRank][i].color:
                                        clear = False
                                    elif i < toFile and (not piece.color == self.board[fromRank][i]):
                                        clear = False
                        else:
                            clear = False
                    else:
                        clear = False
                    if clear:
                        captured = self.board[toRank][toFile]
                        piece.changePos(toPos)
                        self.board[toRank][toFile] = piece
                        self.board[fromRank][fromFile] = self.newSquare(fromPos)
                        if self.checkCheck(king.position, king)[0]:
                            self.board[toRank][toFile] = captured
                            piece.changePos(fromPos)
                            self.board[fromRank][fromFile] = piece
                            print('Invalid move. King is in check or will be in check from this move.')
                            if not checkMoved:
                                piece.moved = False
                        else:
                            piece.moved = True
                            self.enPassCheck()
                            pieceMoved = True

                    else:
                        print('Not a valid rook move.')

                #bishops
                #even tougher than the rook (i think) cuz i gotta check all DIAGONAL squares
                elif piece.name == 'bishop':
                    clear = True  #boolean to check if path is clear
                    #up
                    if abs(fromRank - toRank) == abs(fromFile - toFile):
                        if toRank < fromRank:
                            #upleft
                            if toFile < fromFile:
                                for i in range(fromRank - toRank):
                                    if (not self.board[toRank + i][toFile + i].isSquare) and (piece.color == self.board[toRank + i][toFile + i].color):
                                        clear = False
                                    elif (toFile + i > toFile) and (not self.board[toRank + i][toFile + i].isSquare) and (not piece.color == self.board[toRank + i][toFile + i].color):
                                        clear = False
                            #upright
                            elif toFile > fromFile:
                                for i in range(fromRank - toRank):
                                    if (not self.board[toRank + i][toFile - i].isSquare) and (piece.color == self.board[toRank + i][toFile - i].color):
                                        clear = False
                                    elif (toFile - i < toFile) and (not self.board[toRank + i][toFile - i].isSquare) and (not piece.color == self.board[toRank + i][toFile - i].color):
                                        clear = False
                        #down
                        elif toRank > fromRank:
                            #downleft
                            if toFile < fromFile:
                                for i in range(toRank - fromRank):
                                    if (not self.board[toRank - i][toFile + i].isSquare) and (piece.color == self.board[toRank - i][toFile + i].color):
                                        clear = False
                                    elif (toFile + i > toFile) and (not self.board[toRank - i][toFile + i].isSquare) and (not piece.color == self.board[toRank - i][toFile + i].color):
                                        clear = False
                            #downright
                            elif toFile > fromFile:
                                for i in range(toRank - fromRank):
                                    if (not self.board[toRank - i][toFile - i].isSquare) and (piece.color == self.board[toRank - i][toFile - i].color):
                                        clear = False
                                    elif (toFile - i < toFile) and (not self.board[toRank - i][toFile - i].isSquare) and (not piece.color == self.board[toRank - i][toFile - i].color):
                                        clear = False
                        else:
                            clear = False
                    else:
                        clear = False
                    if clear:
                        captured = self.board[toRank][toFile]
                        piece.changePos(toPos)
                        self.board[toRank][toFile] = piece
                        self.board[fromRank][fromFile] = self.newSquare(fromPos)
                        if self.checkCheck(king.position, king)[0]:
                            self.board[toRank][toFile] = captured
                            piece.changePos(fromPos)
                            self.board[fromRank][fromFile] = piece
                            print('Invalid move. King is in check or will be in check from this move.')
                        else:
                            self.enPassCheck()
                            pieceMoved = True
                    else:
                        print('Not a valid bishop move.')

                #queens
                #should be pretty easy now since its a combo of rook+bishop
                elif piece.name == 'queen':
                    clear = True  #boolean to check if path is clear
                    #up/down
                    if fromFile == toFile:
                        #up
                        if fromRank > toRank:
                            for i in range(toRank, fromRank):
                                if not self.board[i][fromFile].isSquare:
                                    if piece.color == self.board[i][fromFile].color:
                                        clear = False
                                    elif i > toRank and (not piece.color == self.board[i][fromFile].color):
                                        clear = False
                        #down
                        elif fromRank < toRank:
                            for i in range(fromRank + 1, toRank + 1):
                                if (not self.board[i][fromFile].isSquare):
                                    if piece.color == self.board[i][fromFile].color:
                                        clear = False
                                    elif i < toRank and (not piece.color == self.board[i][fromFile].color):
                                        clear = False
                        else:
                            clear = False
                    #left/right
                    elif fromRank == toRank:
                        #left
                        if fromFile > toFile:
                            for i in range(toFile, fromFile):
                                if not self.board[fromRank][i].isSquare:
                                    if piece.color == self.board[fromRank][i].color:
                                        clear = False
                                    elif i > toFile and (not piece.color == self.board[fromRank][i].color):
                                        clear = False
                        #right
                        elif fromFile < toFile:
                            for i in range(fromFile + 1, toFile + 1):
                                if not self.board[fromRank][i].isSquare:
                                    if piece.color == self.board[fromRank][i].color:
                                        clear = False
                                    elif i < toFile and (not piece.color == self.board[fromRank][i]):
                                        clear = False
                        else:
                            clear = False
                    #diagonal
                    elif abs(fromRank - toRank) == abs(fromFile - toFile):
                        #up
                        if toRank < fromRank:
                            #upleft
                            if toFile < fromFile:
                                for i in range(fromRank - toRank):
                                    if (not self.board[toRank + i][toFile + i].isSquare) and (piece.color == self.board[toRank + i][toFile + i].color):
                                        clear = False
                                    elif (toFile + i > toFile) and (not self.board[toRank + i][toFile + i].isSquare) and (not piece.color == self.board[toRank + i][toFile + i].color):
                                        clear = False
                            #upright
                            elif toFile > fromFile:
                                for i in range(fromRank - toRank):
                                    if (not self.board[toRank + i][toFile - i].isSquare) and (piece.color == self.board[toRank + i][toFile - i].color):
                                        clear = False
                                    elif (toFile - i < toFile) and (not self.board[toRank + i][toFile - i].isSquare) and (not piece.color == self.board[toRank + i][toFile - i].color):
                                        clear = False
                        #down
                        elif toRank > fromRank:
                            #downleft
                            if toFile < fromFile:
                                for i in range(toRank - fromRank):
                                    if (not self.board[toRank - i][toFile + i].isSquare) and (piece.color == self.board[toRank - i][toFile + i].color):
                                        clear = False
                                    elif (toFile + i > toFile) and (not self.board[toRank - i][toFile + i].isSquare) and (not piece.color == self.board[toRank - i][toFile + i].color):
                                        clear = False
                            #downright
                            elif toFile > fromFile:
                                for i in range(toRank - fromRank):
                                    if (not self.board[toRank - i][toFile - i].isSquare) and (piece.color == self.board[toRank - i][toFile - i].color):
                                        clear = False
                                    elif (toFile - i < toFile) and (not self.board[toRank - i][toFile - i].isSquare) and (not piece.color == self.board[toRank - i][toFile - i].color):
                                        clear = False
                        else:  #if fromRank - toRank == 0 (not moving)
                            clear = False
                    else:
                        clear = False
                    if clear:
                        captured = self.board[toRank][toFile]
                        piece.changePos(toPos)
                        self.board[toRank][toFile] = piece
                        self.board[fromRank][fromFile] = self.newSquare(fromPos)
                        if self.checkCheck(king.position, king)[0]:
                            self.board[toRank][toFile] = captured
                            piece.changePos(fromPos)
                            self.board[fromRank][fromFile] = piece
                            print('Invalid move. King is in check or will be in check from this move.')
                        else:
                            self.enPassCheck()
                            pieceMoved = True
                    else:
                        print('Not a valid queen move.')

                #king will be a bit difficult cuz i have to check for legality of the move (if it will be in check on the place i move it)
                #should i make a method that checks for a check? yes... i did
                #checkCheck(pos, piece)
                elif piece.name == 'king':
                    #up
                    if fromRank - toRank == 1:
                        #upleft
                        if fromFile - toFile == 1:
                            self.board[fromRank][fromFile] = self.newSquare(fromPos)
                            if not self.checkCheck(toPos, piece)[0]:
                                piece.changePos(toPos)
                                self.board[toRank][toFile] = piece
                                piece.moved = True
                                self.enPassCheck()
                                pieceMoved = True
                            else:
                                self.board[fromRank][fromFile] = piece
                                print('Invalid move. King will be in check from this move.')
                        #up1
                        elif fromFile == toFile:
                            self.board[fromRank][fromFile] = self.newSquare(fromPos)
                            if not self.checkCheck(toPos, piece)[0]:
                                piece.changePos(toPos)
                                self.board[toRank][toFile] = piece
                                piece.moved = True
                                self.enPassCheck()
                                pieceMoved = True
                            else:
                                self.board[fromRank][fromFile] = piece
                                print('Invalid move. King will be in check from this move.')
                        #upright
                        elif fromFile - toFile == -1:
                            self.board[fromRank][fromFile] = self.newSquare(fromPos)
                            if not self.checkCheck(toPos, piece)[0]:
                                piece.changePos(toPos)
                                self.board[toRank][toFile] = piece
                                piece.moved = True
                                self.enPassCheck()
                                pieceMoved = True
                            else:
                                self.board[fromRank][fromFile] = piece
                                print('Invalid move. King will be in check from this move.')
                        else:
                            print('Not a valid king move.')
                    #down
                    elif fromRank - toRank == -1:
                        #downleft
                        if fromFile - toFile == 1:
                            self.board[fromRank][fromFile] = self.newSquare(fromPos)
                            if not self.checkCheck(toPos, piece)[0]:
                                piece.changePos(toPos)
                                self.board[toRank][toFile] = piece
                                piece.moved = True
                                self.enPassCheck()
                                pieceMoved = True
                            else:
                                self.board[fromRank][fromFile] = piece
                                print('Invalid move. King will be in check from this move.')
                        #down1
                        elif fromFile == toFile:
                            self.board[fromRank][fromFile] = self.newSquare(fromPos)
                            if not self.checkCheck(toPos, piece)[0]:
                                piece.changePos(toPos)
                                self.board[toRank][toFile] = piece
                                piece.moved = True
                                self.enPassCheck()
                                pieceMoved = True
                            else:
                                self.board[fromRank][fromFile] = piece
                                print('Invalid move. King will be in check from this move.')
                        #downright
                        elif fromFile - toFile == -1:
                            self.board[fromRank][fromFile] = self.newSquare(fromPos)
                            if not self.checkCheck(toPos, piece)[0]:
                                piece.changePos(toPos)
                                self.board[toRank][toFile] = piece
                                piece.moved = True
                                self.enPassCheck()
                                pieceMoved = True
                            else:
                                self.board[fromRank][fromFile] = piece
                                print('Invalid move. King will be in check from this move.')
                        else:
                            print('Not a valid king move.')
                    #left/right
                    elif fromRank == toRank and abs(fromFile - toFile) == 1:
                        #left
                        if fromFile - toFile == 1:
                            self.board[fromRank][fromFile] = self.newSquare(fromPos)
                            if not self.checkCheck(toPos, piece)[0]:
                                piece.changePos(toPos)
                                self.board[toRank][toFile] = piece
                                piece.moved = True
                                self.enPassCheck()
                                pieceMoved = True
                            else:
                                self.board[fromRank][fromFile] = piece
                                print('Invalid move. King will be in check from this move.')
                        #right
                        elif fromFile - toFile == -1:
                            self.board[fromRank][fromFile] = self.newSquare(fromPos)
                            if not self.checkCheck(toPos, piece)[0]:
                                piece.changePos(toPos)
                                self.board[toRank][toFile] = piece
                                piece.moved = True
                                self.enPassCheck()
                                pieceMoved = True
                            else:
                                self.board[fromRank][fromFile] = piece
                                print('Invalid move. King will be in check from this move.')
                        else:
                            print('Not a valid king move.')
                    #castling
                    elif (not piece.moved) and (not self.checkCheck(piece.position, piece)[0]):
                        #O-O
                        if toFile - fromFile == 2 and (not self.board[fromRank][fromFile + 3].isSquare) and self.board[fromRank][fromFile + 3].color == piece.color and self.board[fromRank][fromFile + 3].name == 'rook' and self.board[fromRank][fromFile + 3].moved == False and self.board[fromRank][fromFile + 1].isSquare and self.board[fromRank][fromFile + 2].isSquare:
                            rook = self.board[fromRank][fromFile + 3]
                            self.board[fromRank][fromFile] = self.newSquare(piece.position)
                            piece.position = self.board[fromRank][fromFile + 1].position
                            if not self.checkCheck(piece.position, piece)[0]:
                                piece.position = self.board[fromRank][fromFile + 2].position
                                if not self.checkCheck(piece.position, piece)[0]:
                                    self.board[fromRank][fromFile + 3] = self.newSquare(rook.position)
                                    rook.position = self.board[fromRank][fromFile + 1].position
                                    self.board[fromRank][fromFile + 1] = rook
                                    self.board[fromRank][fromFile + 2] = piece
                                    rook.moved = True
                                    piece.moved = True
                                    self.enPassCheck()
                                    pieceMoved = True
                                else:
                                    piece.position = self.board[fromRank][fromFile].position
                                    self.board[fromRank][fromFile] = piece
                                    print('Castling not valid since king is checked in the process')
                            else:
                                piece.position = self.board[fromRank][fromFile].position
                                self.board[fromRank][fromFile] = piece
                                print('Castling not valid since king is checked in the process')

                        #O-O-O
                        elif fromFile - toFile == 2 and (not self.board[fromRank][fromFile - 4].isSquare) and self.board[fromRank][fromFile - 4].color == piece.color and self.board[fromRank][fromFile - 4].name == 'rook' and self.board[fromRank][fromFile - 4].moved == False and self.board[fromRank][fromFile - 1].isSquare and self.board[fromRank][fromFile - 2].isSquare and self.board[fromRank][fromFile - 3].isSquare:
                            rook = self.board[fromRank][fromFile - 4]
                            self.board[fromRank][fromFile] = self.newSquare(piece.position)
                            piece.position = self.board[fromRank][fromFile - 1].position
                            if not self.checkCheck(piece.position, piece)[0]:
                                piece.position = self.board[fromRank][fromFile - 2].position
                                if not self.checkCheck(piece.position, piece)[0]:
                                    self.board[fromRank][fromFile - 4] = self.newSquare(rook.position)
                                    rook.position = self.board[fromRank][fromFile - 1].position
                                    self.board[fromRank][fromFile - 1] = rook
                                    self.board[fromRank][fromFile - 2] = piece
                                    rook.moved = True
                                    piece.moved = True
                                    self.enPassCheck()
                                    pieceMoved = True
                                else:
                                    piece.position = self.board[fromRank][fromFile].position
                                    self.board[fromRank][fromFile] = piece
                                    print('Castling not valid since king is checked in the process')
                            else:
                                piece.position = self.board[fromRank][fromFile].position
                                self.board[fromRank][fromFile] = piece
                                print('Castling not valid since king is checked in the process')
                        else:
                            print('Not a valid king move.')
                    else:
                        print('Not a valid king move.')

            else:
                print('Invalid piece. Please chose your own color piece.')

        else:
            print('Invalid move.')
        return pieceMoved

    #method to play actual game with turns
    def game(self):
        print('All moves should be in board notation. Like From: "e2" To: "e4".')
        gameOver = False
        stalemate = False
        while not (gameOver or stalemate):
            #find kings to check for checkmate after move
            opponentKing = None
            for i in range(8):
                for j in range(8):
                    if (not self.board[i][j].isSquare) and self.board[i][j].name == 'king' and self.board[i][j].color != self.turn:
                        opponentKing = self.board[i][j]
                        kRank = i
                        kFile = j
            self.printBoard()
            print(self.turn + ' to move.')
            fromPos = input('From square: ')
            toPos = input('To square: ')
            pieceMoved = self.move(fromPos, toPos)
            if not pieceMoved:
                pass

            else:
                if self.checkCheckmate(opponentKing):
                    gameOver = True
                elif self.checkStalemate(opponentKing):
                    stalemate = True
                elif self.turn == 'white':
                    self.turn = 'black'
                elif self.turn == 'black':
                    self.turn = 'white'
        if gameOver:
            print('Game over. ' + self.turn+ ' won!')
        else:
            print('Game over. It\'s a draw!')




if __name__ == '__main__':
    board = Board()
    board.game()