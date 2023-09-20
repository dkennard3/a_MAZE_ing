from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title = "My first window!"
        self.root.geometry(f"{self.width}x{self.height}")
        self.canvas = Canvas(master=self.root, width=self.width, height=self.height, background="gray")
        self.canvas.pack()
        self.isRunning = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.isRunning = True
        while self.isRunning:
            self.redraw()

    def close(self):
        self.isRunning = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.x1 = self.start_point.x
        self.y1 = self.start_point.y

        self.end_point = end_point
        self.x2 = self.end_point.x
        self.y2 = self.end_point.y

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2
        )
        canvas.pack()

class Cell():
    def __init__(self, window):
        self._win = window
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self, point1, point2):
        self._x1 = point1.x
        self._x2 = point2.x
        self._y1 = point1.y
        self._y2 = point2.y

        self.top_left = point1 if self._x1 < self._x2 and self._y1 < self._y2 else point2
        self.bottom_right = point2 if self.top_left == point1 else point1

        self.bottom_left = Point(self.top_left.x, self.bottom_right.y)
        self.top_right = Point(self.bottom_right.x, self.top_left.y)

        self._win.draw_line(Line(self.top_left, self.bottom_left), self._line_color(self.has_left_wall))
        self._win.draw_line(Line(self.top_left, self.top_right), self._line_color(self.has_top_wall))
        self._win.draw_line(Line(self.top_right, self.bottom_right), self._line_color(self.has_right_wall))
        self._win.draw_line(Line(self.bottom_left, self.bottom_right), self._line_color(self.has_bottom_wall))

    def _line_color(self, has_wall):
        return "black" if has_wall else "gray"

    def draw_move(self, to_cell, undo=False):
        fill_color = "red" if not undo else "white"
        mid_x = (self.top_right.x + self.top_left.x) / 2
        mid_y = (self.bottom_left.y + self.top_left.y) / 2
        from_center = Point(mid_x, mid_y)
        to_mid_x = (to_cell.top_right.x + to_cell.top_left.x) / 2
        to_mid_y = (to_cell.bottom_left.y + to_cell.top_left.y) / 2
        to_center = Point(to_mid_x, to_mid_y)

        self._win.draw_line(Line(from_center, to_center), fill_color)

def main():
    win = Window(800, 600)
    first = Cell(win)
    first.draw(Point(50, 50), Point(150, 150))
    second = Cell(win)
    second.draw(Point(150, 50), Point(250, 150))

    first.draw_move(second)

    win.wait_for_close()    


if __name__ == "__main__":
    main()
