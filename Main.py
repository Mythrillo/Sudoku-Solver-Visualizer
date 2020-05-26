import sys
import pygame
import pygame.freetype
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

sudoku = [[0, 0, 4, 5, 0, 6, 0, 7, 0],
         [3, 0, 6, 7, 1, 2, 5, 8, 0],
         [0, 0, 8, 0, 4, 0, 1, 2, 6],
         [0, 8, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 4, 6, 0, 3, 0, 8],
         [0, 0, 0, 1, 7, 0, 6, 0, 2],
         [5, 0, 0, 0, 0, 0, 0, 6, 7],
         [0, 1, 7, 6, 0, 4, 0, 3, 9],
         [0, 0, 9, 0, 2, 7, 0, 1, 0]]

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 900
WINDOW_WIDTH = 900


class Sudoku:

    def __init__(self, board):

        self.board = board
        self.past_filled = []
        self.current_backtrack = 0
        self.numbers = []

    def check_row(self, number, row):

        if number in self.board[row]:
            return False
        return True

    def check_column(self, number, column):

        for i in range(9):
            if number == self.board[i][column]:
                return False
        return True

    def check_square(self, number, row, column):

        row = row - row % 3
        column = column - column % 3

        for i in range(row, row + 3):
            for j in range(column, column + 3):
                if number == self.board[i][j]:
                    return False
        return True

    def no_solution(self):

        screen.fill(WHITE)
        font.render_to(screen, (WINDOW_HEIGHT / 2 - 50, WINDOW_WIDTH / 2 - 50), "NO SOLUTION", BLACK)
        pygame.display.update()
        pygame.time.wait(5000)
        pygame.quit()
        sys.exit()

    def fill_empty(self, number, row, column):

        if number == 9 and self.board[row][column] == 9:
            self.board[row][column] = 0
            self.current_backtrack -= 1
            if self.current_backtrack < -len(self.past_filled):
                self.no_solution()
            self.backtrack()
            self.fill_empty(0, row, column)
        for new_number in range(number + 1, 10):

            self.change_cell_color(new_number, row, column)

            if self.check_row(new_number, row) and self.check_column(new_number, column) and self.check_square(
                    new_number, row,
                    column):
                if self.current_backtrack < 0:
                    self.current_backtrack += 1
                self.board[row][column] = new_number
                if [row, column] in self.past_filled:
                    break
                else:
                    self.past_filled.append([row, column])
                    break

            elif new_number == 9:
                self.board[row][column] = 0
                self.current_backtrack -= 1
                if self.current_backtrack < -len(self.past_filled):
                    self.no_solution()
                self.backtrack()
                self.fill_empty(0, row, column)
            else:
                continue

    def change_cell_color(self, number, row, column):
        pygame.draw.rect(screen, (204, 255, 51), (column * 100 + 1, row * 100 + 1, 99, 99))
        font.render_to(screen, (50 + column * 100, 50 + row * 100), str(number), BLACK)
        pygame.display.update()
        pygame.time.wait(50)

    def backtrack(self):

        row = self.past_filled[self.current_backtrack][0]
        column = self.past_filled[self.current_backtrack][1]
        number = self.board[row][column]

        self.fill_empty(number, row, column)

    def solve(self):

        for row in range(9):
            for column in range(9):
                if self.board[row][column] == 0:
                    self.draw_sudoku()
                    pygame.time.wait(50)
                    self.fill_empty(0, row, column)
                    while self.current_backtrack < 0:
                        self.fill_empty(0, row, column)
                else:
                    continue
        self.draw_sudoku()

    def draw_sudoku(self):
        exit_handler()
        screen.fill(WHITE)
        draw_grid()
        for row in range(9):
            for column in range(9):
                if self.board[row][column] == 0:
                    continue
                else:
                    font.render_to(screen, (50 + column * 100, 50 + row * 100), str(self.board[row][column]), BLACK)
        pygame.display.update()


def draw_grid():
    for x in range(0, WINDOW_WIDTH, int(WINDOW_WIDTH / 9)):
        pygame.draw.line(screen, BLACK, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, int(WINDOW_HEIGHT / 9)):
        pygame.draw.line(screen, BLACK, (0, y), (WINDOW_WIDTH, y))


def exit_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def main():
    global screen, clock, font

    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Sudoku solver")
    screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    screen.fill(WHITE)
    font = pygame.freetype.SysFont("monospace", 30)

    sudo = Sudoku(sudoku)

    sudo.solve()


if __name__ == "__main__":
    main()
