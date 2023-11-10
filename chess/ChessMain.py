import pygame as p
import ChessEngine, SmartMoveFinder
import performance
from SmartMoveFinder import moveCounter, moveTime

# kích thước bàn cờ
WIDTH = HEIGHT = 512
# số ô mỗi chiều
DIMENSION = 8
# kích thước 1 ô
SQ_SIZE = HEIGHT // DIMENSION
# số khung hình tối đa mỗi giây
MAX_FPS = 15
# ảnh các quân cờ
IMAGES = {}

def loadImages():
    """
    Tải ảnh các quân cờ từ thư mục images và lưu vào biến IMAGES.
    """
    ...

def main():
    """
    Hàm chính của chương trình, thực hiện khởi tạo trạng thái ban đầu của bàn cờ, lấy thông tin click chuột của người chơi, 
    xử lý các sự kiện, thực hiện các nước đi hợp lệ, vẽ bàn cờ và kiểm tra kết thúc trò chơi.
    """
    ...

def highlightSquares(screen, gs, validMoves, sqSelected):
    """
    Tô màu các ô cờ trên bàn cờ để thể hiện các nước đi hợp lệ và ô cờ đang được chọn.
    
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param gs: GameState object, trạng thái hiện tại của trò chơi
    :param validMoves: list, danh sách các nước đi hợp lệ
    :param sqSelected: tuple, tọa độ ô cờ đang được chọn
    """
    ...

def drawBoard(screen):
    """
    Vẽ bàn cờ với 2 màu trắng và xám.
    
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    """
    ...

def drawPieces(screen, board):
    """
    Vẽ các quân cờ trên bàn cờ.
    
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param board: list, danh sách các quân cờ trên bàn cờ
    """
    ...

def drawGameState(screen, gs, validMoves, sqSelected):
    """
    Vẽ trạng thái hiện tại của bàn cờ.
    
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param gs: GameState object, trạng thái hiện tại của trò chơi
    :param validMoves: list, danh sách các nước đi hợp lệ
    :param sqSelected: tuple, tọa độ ô cờ đang được chọn
    """
    ...

def animateMove(move, screen, board, clock):
    """
    Thực hiện animation cho một nước đi trên bàn cờ.
    
    :param move: Move object, nước đi cần thực hiện animation
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param board: list, danh sách các quân cờ trên bàn cờ
    :param clock: pygame.time.Clock object, đồng hồ đếm thời gian
    """
    ...

def drawText(screen, text):
    """
    Vẽ text trên màn hình.
    
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param text: str, text cần vẽ
    """
    ...

if __name__ == "__main__":
    main()
import ChessEngine, SmartMoveFinder

WIDTH = HEIGHT = 512  # kich thuoc ban co
DIMENSION = 8  # số ô mỗi chiều
SQ_SIZE = HEIGHT // DIMENSION  # kich thuoc 1 ô
MAX_FPS = 15  # FOR ANIMATIONS LATER ON
IMAGES = {}


def loadImages():
    """
    Tải ảnh các quân cờ từ thư mục images và lưu vào biến IMAGES.
    """
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


# ham thực thi
def main():
    """
    Hàm chính của chương trình, thực hiện khởi tạo trạng thái ban đầu của bàn cờ, lấy thông tin click chuột của người chơi, 
    xử lý các sự kiện, thực hiện các nước đi hợp lệ, vẽ bàn cờ và kiểm tra kết thúc trò chơi.
    """
    move_times = []
    move_counts = []
    
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()  # khoi tao trang thai ban dau
    animate = False
    moveMade = False  # flag varible for when a move is made
    loadImages()  # tao mang chua anh cac quan cờ
    running = True
    sqSelected = ()  # cac ô cờ được click
    playerClicks = []
    # lưu trư thong tin click cua nguoi choi
    validMoves = gs.getValidMoves()
    gameOver = False
    playerOne = True
    playerTwo = False
    while running:  # neu dang thuc thi chuong trinh
        humanTurn = (gs.whiteToMove and playerOne) or (gs.whiteToMove and playerTwo)

        for e in p.event.get():  # sử lý  kiện clicked chuột
            if e.type == p.QUIT:
                running = False
            # mouse handle
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())  # in ra vi tri bat dau va ket thuc cua quan co
                        validMoves = gs.getValidMoves()
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])  # chuyen quan co den vi tri moi
                                if moveMade:
                                    move_times.append(moveTime)
                                    move_counts.append(moveCounter)
                                moveMade = True
                                animate = True
                                sqSelected = ()  # khởi tạo lại trạng thái click
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # nhan z
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    validMoves = gs.getValidMoves()
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMoveMinMax(gs, validMoves)
            
            if (AIMove is None):
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
        

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            
            # Cập nhật dữ liệu hiệu suất sau mỗi nước đi
            move_times.append(SmartMoveFinder.moveTime)
            move_counts.append(SmartMoveFinder.moveCounter)

        drawGameState(screen, gs, validMoves, sqSelected)  # ve ban co

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins")
            else:
                drawText(screen, "White wins")
        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate")

        clock.tick(MAX_FPS)  # gioi han so khung hinh moi giay
        p.display.flip()  # không co che do full man hinh
        
        if gameOver:
            # Hiển thị biểu đồ hiệu suất
            performance.plot_performance(move_times, move_counts)



def highlightSquares(screen, gs, validMoves, sqSelected):
    """
    Tô màu các ô cờ trên bàn cờ để thể hiện các nước đi hợp lệ và ô cờ đang được chọn.
    
    :param screen: pygame.Surface object, màn hình hiển thị bàn cờ
    :param gs: GameState object, trạng thái hiện tại của trò chơi
    :param validMoves: list, danh sách các nước đi hợp lệ
    :param sqSelected: tuple, tọa độ ô cờ đang được chọn
    """

    if sqSelected is not None:
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


# goc phía trên bên trái luôn là màu trắng
# vẽ 2 màu trắng v xám cho bàn cờ


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# dua cac quan co vao ban co
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# vẽ ban co va quan co
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # if move.pieceCaptured != '--':
        #     screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                    HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == "__main__":
    main()
