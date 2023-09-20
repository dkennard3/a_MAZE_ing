from components import Cell, Window, Line, Point 
import time
import random
class Maze():
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win,
            seed=None
        ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.create_cells()
        self.seed = seed
        if self.seed != None:
            random.seed(self.seed)

    def create_cells(self):
        self._cells = []
        for i in range(self.num_cols):
            cols = []
            for j in range(self.num_rows):
                cols.append(Cell(self.win))
            self._cells.append(cols)
    
        self._break_entrance_and_exit()

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        top_left_x = self.x1 + (i * self.cell_size_x)
        top_left_y = self.y1 + (j * self.cell_size_y)
        bottom_right_x = top_left_x + self.cell_size_x
        bottom_right_y = top_left_y + self.cell_size_y

        p1 = Point(top_left_x, top_left_y)
        p2 = Point(bottom_right_x, bottom_right_y)

        # print(f"drawing _cells[{i}][{j}]")
        cell.draw(p1, p2)
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.8)
        
    def _break_entrance_and_exit(self):
        print(f"rows: {self.num_rows}, cols: {self.num_cols}")
        self.start_cell = self._cells[0][0]
        self.end_cell = self._cells[self.num_cols-1][self.num_rows-1]

        self.start_cell.has_top_wall = False
        self.end_cell.has_bottom_wall = False

        self._draw_cell(0, 0)
        self._draw_cell(self.num_cols-1, self.num_rows-1)

    def _break_walls_r(self, i, j):
        curr_cell = self._cells[i][j]
        curr_cell.visited = True

        up, down, left, right = [None for direction in range(4)]

        while True:
            unvisited = []
            # up
            if j != 0 and not self._cells[i][j-1].visited:
                unvisited.append((i, j-1))
                up = self._cells[i][j-1]
            # down
            if j != self.num_rows - 1 and not self._cells[i][j+1].visited:
                unvisited.append((i, j+1))
                down = self._cells[i][j+1]
            # left
            if i != 0 and not self._cells[i-1][j].visited:
                unvisited.append((i-1, j))
                left = self._cells[i-1][j]
            # right
            if i != self.num_cols - 1 and not self._cells[i+1][j].visited:
                unvisited.append((i+1, j))
                right = self._cells[i+1][j]
            
            if not unvisited:
                self._draw_cell(i, j)
                return

            rand_index = random.randrange(0, len(unvisited))
            next_i, next_j = unvisited[rand_index]
            if next_i == i-1:
                curr_cell.has_left_wall = False
                # left.has_right_wall = False
            elif next_i == i+1:
                curr_cell.has_right_wall = False
                # right.has_left_wall = False
            elif next_j == j-1:
                curr_cell.has_top_wall = False
                # up.has_bottom_wall = False
            elif next_j == j+1:
                curr_cell.has_bottom_wall = False
                # down.has_top_wall = False
            self._animate()
            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def _solve_r(self, i, j):
        self._animate()
        curr_cell = self._cells[i][j]
        curr_cell.visited = True

        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        if j != 0 and not self._cells[i][j-1].visited:
            if not curr_cell.has_top_wall:
                up = self._cells[i][j-1]
                curr_cell.draw_move(up)
                if self._solve_r(i, j-1):
                    return True
                curr_cell.draw_move(up, undo=True)
        
        if j != self.num_rows - 1 and not self._cells[i][j+1].visited:
            if not curr_cell.has_bottom_wall:
                down = self._cells[i][j+1]
                curr_cell.draw_move(down)
                if self._solve_r(i, j+1):
                    return True
                curr_cell.draw_move(down, undo=True) 

        if i != 0 and not self._cells[i-1][j].visited:
            if not curr_cell.has_left_wall:
                left = self._cells[i-1][j]
                curr_cell.draw_move(left)
                if self._solve_r(i-1, j):
                    return True
                curr_cell.draw_move(left, undo=True)
        
        if i != self.num_cols - 1 and not self._cells[i+1][j].visited:
            if not curr_cell.has_right_wall:
                right = self._cells[i+1][j]
                curr_cell.draw_move(right)
                if self._solve_r(i+1, j):
                    return True
                curr_cell.draw_move(right, undo=True) 

        return False

    def solve(self):
        return self._solve_r(0,0)


def main():
    win = Window(900, 900)
    m = Maze(200, 200, 10, 10, 60, 60, win) #, seed=25) 
    print("Generating Random Maze...")
    m._break_walls_r(0, 0)
    m._reset_cells_visited()
    print("Begin to solve...")
    m.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()
