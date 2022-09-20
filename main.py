import sys
import pygame
from pygame.locals import *

WIDTH = 540
HEIGH = 540
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SCREEN = pygame.display.set_mode((WIDTH, HEIGH))
CLOCK = pygame.time.Clock()
pygame.init()


class Cell:
    def __init__(self, rect, text):
        self.rect = rect
        self.text = text
        self.color = BLACK
        self.color_border = BLACK

    def draw_cell(self):
        pygame.draw.rect(SCREEN, self.color_border, self.rect, 1)
        f = pygame.font.Font("freesansbold.ttf", 40)
        textSurface = f.render(self.text, True, self.color)
        textRect = textSurface.get_rect(center=self.rect.center)
        SCREEN.blit(textSurface, textRect)


class Board:
    def __init__(self):
        self.board = []
        self.active = (None, None)
        for i in range(9):
            temp_list = []
            for j in range(9):
                temp_list.append(Cell(pygame.rect.Rect(j * 60, i * 60, 60, 60), ""))
            self.board.append(temp_list)

    def draw_board(self):
        for i in range(9):
            for j in range(9):
                self.board[i][j].draw_cell()

    def check_valid_sudoku(self):
        def check_each_cell(row, col):
            numbers = []
            for i in range(9):
                if self.board[row][i].text != "":
                    numbers.append(self.board[row][i].text)
            if len(numbers)!=len(set(numbers)):
                return False
            numbers=[]
            for i in range(9):
                if self.board[i][col].text != "":
                    numbers.append(self.board[i][col].text)
            if len(numbers)!=len(set(numbers)):
                return False
            numbers=[]
            box_row = (row // 3) * 3
            box_col = (col // 3) * 3
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if self.board[i][j].text != "":
                        numbers.append(self.board[i][j].text)
            if len(numbers)!=len(set(numbers)):
                return False
            return True


        for row in range(9):
            for col in range(9):
                if not check_each_cell(row,col):
                    return False
        return True

    def solve_board(self):
        global check
        check = False
        board = []
        for i in range(9):
            lst = []
            for j in range(9):
                lst.append(self.board[i][j].text)
            board.append(lst)
        color = []

        def get_number_left_in_row_col_subbox(row, col):
            myset = set()
            for i in range(9):
                if board[row][i] != "":
                    myset.add(board[row][i])
            for i in range(9):
                if board[i][col] != "":
                    myset.add(board[i][col])

            box_row = (row // 3) * 3
            box_col = (col // 3) * 3
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if board[i][j] != "":
                        myset.add(board[i][j])

            ans = set()
            for i in range(1, 10):
                if str(i) not in myset:
                    ans.add(str(i))
            return ans

        self.lst = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == "":
                    self.lst.append((i, j))

        def recur(idx):
            global check
            if idx == len(self.lst):
                check = True
                return
            if check:
                return
            row, col = self.lst[idx]
            numbers_left = get_number_left_in_row_col_subbox(row, col)
            if len(numbers_left) == 0:
                return

            for number in numbers_left:
                if not check:
                    board[row][col] = str(number)
                    color.append((idx, str(number)))
                    recur(idx + 1)
                    if not check:
                        board[row][col] = ""
                else:
                    return

        recur(0)
        print(len(color))
        for i in range(1, len(color)):
            idx1, number1 = color[i]
            idx2, number2 = color[i - 1]

            if idx1 > idx2:
                self.display_higher(idx2, idx1, number2, number1)
            elif idx1 == idx2:
                self.display_equal(idx2, number2, number1)
            else:
                self.display_lower(idx2, idx1, number2, number1)

    def update_screen(self):
        check_quit()
        SCREEN.fill(WHITE)
        self.draw_board()
        pygame.display.update()

    def display_higher(self, i, j, n1, n2):
        row1, col1 = self.lst[i]
        row2, col2 = self.lst[j]
        self.board[row1][col1].text = n1
        self.board[row1][col1].color = GREEN
        self.board[row1][col1].color_border = GREEN
        self.update_screen()
        self.board[row2][col2].text = n2
        self.board[row2][col2].color = GREEN
        self.board[row2][col2].color_border = GREEN
        self.update_screen()

    def display_equal(self, idx, n1, n2):
        row, col = self.lst[idx]
        self.board[row][col].text = n1
        self.board[row][col].color = RED
        self.board[row][col].color_border = RED
        self.update_screen()
        self.board[row][col].text = n2
        self.board[row][col].color = GREEN
        self.board[row][col].color_border = GREEN
        self.update_screen()

    def display_lower(self, i, j, n1, n2):
        row1, col1 = self.lst[i]
        row2, col2 = self.lst[j]
        self.board[row1][col1].text = n1
        self.board[row1][col1].color_border = GREEN
        self.update_screen()

        for k in range(i, j, -1):
            row, col = self.lst[k]
            self.board[row][col].text = ""
            self.board[row][col].color_border = RED
            self.update_screen()
        self.board[row2][col2].text = n2
        self.board[row][col].color = GREEN
        self.board[row][col].color_border = GREEN
        self.update_screen()

    def get_cell(self, x, y):
        return y // 60, x // 60

    def check_mouse(self):
        pos_x, pos_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            row, col = self.get_cell(pos_x, pos_y)
            self.active = (row, col)

    def check_keyboard(self):
        keyboard = pygame.key.get_pressed()
        row, col = self.active
        if row is None:
            return
        for i in range(49, 58):
            if keyboard[i]:
                self.board[row][col].text = str(i - 48)
                if not self.check_valid_sudoku():
                    self.board[row][col].text = ""
                break
        if keyboard[pygame.K_BACKSPACE]:
            self.board[row][col].text = ""
        if keyboard[pygame.K_SPACE]:
            self.solve_board()


    def effect(self):
        row, col = self.active
        if self.active != (None, None) and self.board[row][col].text == "":
            row, col = self.active
            rect = self.board[row][col].rect
            x, y = rect.topleft
            pygame.draw.line(SCREEN, BLACK, (x + 10, y + 10), (x + 10, y + 50))


myboard = Board()


def check_quit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def main():
    game = True
    while game:
        SCREEN.fill(WHITE)
        myboard.draw_board()
        myboard.check_mouse()
        myboard.effect()
        myboard.check_keyboard()
        check_quit()
        pygame.display.update()
        CLOCK.tick(144)


main()
