import tkinter
from PIL import Image, ImageTk
from driver import solve, PuzzleState


class Window(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Eight Puzzle")
        window_width = 480
        window_height = 800
        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.winfo_screenheight() / 2 - window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")


class Backgroud(tkinter.Canvas):
    def __init__(self, master=None):
        super().__init__(master, highlightthickness=0)
        self.img_path = "../src/background/background.png"
        self.img = Image.open(self.img_path)
        self.img_compatible = ImageTk.PhotoImage(image=self.img)
        self.create_image(0, 0, anchor="nw", image=self.img_compatible)
        self.pack(fill=tkinter.BOTH, expand=1)


class Logo(tkinter.Canvas):
    def __init__(self, master=None):
        super().__init__(master, width=450, height=200, bg="#EDEAE1", highlightthickness=0)
        self.img_path = "../src/background/logo.png"
        self.img = Image.open(self.img_path)
        self.img = self.img.resize((450, 300), Image.ANTIALIAS)
        self.img_compatible = ImageTk.PhotoImage(image=self.img)
        self.create_image(5, -15, anchor="nw", image=self.img_compatible)
        self.place(x=0, y=0, anchor="nw", )


class Board(tkinter.Canvas):
    def __init__(self, master=None, state=None, width=453, height=453):
        if master is None or state is None:
            raise Exception("Invalid Arguments")
        super().__init__(master, width=width, height=height, bg="#EDEAE1", highlightthickness=0)
        self.master = master
        self.state = state
        self.pack(fill=tkinter.BOTH, expand=1)
        self.place(x=15, y=200, anchor="nw")
        self.drawing = False
        self._img_compatible = [None] * 10
        self._board_compatible = None
        self._tiles = [None] * 10
        self.tile_width = 130
        self.tile_height = 130
        self.board_margin = 31.5
        self.images = [None] * 10
        self.images_hover = [None] * 10
        self.load_images()
        self.draw_board()
        self.draw()
        self.bind("<Button-1>", self.move_tile)
        self.bind("<Motion>", self.hover)
        self.bind("<Leave>", self.refresh)
        self.bind("<Double-Button-1>", self.solve)

    def move_tile(self, event):
        tile = self.get_tile(event.x, event.y)
        if tile is None or self.state[tile] == 0:
            return
        if self.drawing:
            return
        self.drawing = True
        moved = False
        moved = moved or self.try_move_down(tile)
        moved = moved or self.try_move_left(tile)
        moved = moved or self.try_move_up(tile)
        moved = moved or self.try_move_right(tile)
        moved = moved or self.try_double_move_down(tile)
        moved = moved or self.try_double_move_left(tile)
        moved = moved or self.try_double_move_up(tile)
        moved = moved or self.try_double_move_right(tile)
        if not moved:
            self.shake(tile)
        self.drawing = False
        if self.test_goal():
            pass
        else:
            pass

    def try_move_down(self, tile):
        if tile // 3 == 0 or self.state[tile - 3] != 0:
            return False
        total = self.tile_height
        dy = - total / 5
        self.slide(self._tiles[tile], 0, dy)
        self.swap_images(tile, tile - 3)
        return True

    def try_move_left(self, tile):
        if tile % 3 == 2 or self.state[tile + 1] != 0:
            return False
        total = self.tile_width
        dx = total / 5
        self.slide(self._tiles[tile], dx, 0)
        self.swap_images(tile, tile + 1)
        return True

    def try_move_up(self, tile):
        if tile // 3 == 2 or self.state[tile + 3] != 0:
            return False
        total = self.tile_height
        dy = total / 5
        self.slide(self._tiles[tile], 0, dy)
        self.swap_images(tile, tile + 3)
        return True

    def try_move_right(self, tile):
        if tile % 3 == 0 or self.state[tile - 1] != 0:
            return False
        total = self.tile_width
        dx = - total / 5
        self.slide(self._tiles[tile], dx, 0)
        self.swap_images(tile, tile - 1)
        return True

    def try_double_move_down(self, tile):
        if tile // 3 != 2 or self.state[tile - 6] != 0:
            return False
        total = self.tile_height
        dy = - total / 5
        self.double_slide(self._tiles[tile], self._tiles[tile - 3], 0, dy)
        self.swap_images(tile - 3, tile - 6)
        self.swap_images(tile, tile - 3)
        return True

    def try_double_move_left(self, tile):
        if tile % 3 != 0 or self.state[tile + 2] != 0:
            return False
        total = self.tile_width
        dx = total / 5
        self.double_slide(self._tiles[tile], self._tiles[tile + 1], dx, 0)
        self.swap_images(tile + 1, tile + 2)
        self.swap_images(tile, tile + 1)
        return True

    def try_double_move_up(self, tile):
        if tile // 3 != 0 or self.state[tile + 6] != 0:
            return False
        total = self.tile_height
        dy = total / 5
        self.double_slide(self._tiles[tile], self._tiles[tile + 3], 0, dy)
        self.swap_images(tile + 3, tile + 6)
        self.swap_images(tile, tile + 3)
        return True

    def try_double_move_right(self, tile):
        if tile % 3 != 2 or self.state[tile - 2] != 0:
            return False
        total = self.tile_width
        dx = - total / 5
        self.double_slide(self._tiles[tile], self._tiles[tile - 1], dx, 0)
        self.swap_images(tile - 1, tile - 2)
        self.swap_images(tile, tile - 1)
        return True

    def slide(self, tile, dx, dy):
        for i in range(6):
            self.move(tile, dx, dy)
            self.update()
        for i in range(4):
            self.move(tile, -dx / 4, -dy / 4)
            self.update()

    def double_slide(self, tile1, tile2, dx, dy):
        for i in range(6):
            self.move(tile1, dx, dy)
            self.move(tile2, dx, dy)
            self.update()
        for i in range(4):
            self.move(tile1, -dx / 4, -dy / 4)
            self.move(tile2, -dx / 4, -dy / 4)
            self.update()

    def swap_images(self, i, j):
        self.state[i], self.state[j] = self.state[j], self.state[i]
        self._img_compatible[i], self._img_compatible[j] = self._img_compatible[j], self._img_compatible[i]
        self._tiles[i], self._tiles[j] = self._tiles[j], self._tiles[i]

    def shake(self, tile):
        dx = 3
        for i in range(2):
            self.move(self._tiles[tile], dx, 0)
            self.update()
        for i in range(2):
            self.move(self._tiles[tile], -dx, 0)
            self.update()
        for i in range(2):
            self.move(self._tiles[tile], -dx, 0)
            self.update()
        for i in range(2):
            self.move(self._tiles[tile], dx, 0)
            self.update()
        for i in range(2):
            self.move(self._tiles[tile], dx, 0)
            self.update()
        for i in range(2):
            self.move(self._tiles[tile], -dx, 0)
            self.update()

    def shake_all(self):
        if self.drawing:
            return
        self.drawing = True
        dx = 3
        for i in range(2):
            for tile in self._tiles:
                if tile is None:
                    continue
                self.move(tile, dx, 0)
            self.update()
        for i in range(2):
            for tile in self._tiles:
                if tile is None:
                    continue
                self.move(tile, -dx, 0)
            self.update()
        for i in range(2):
            for tile in self._tiles:
                if tile is None:
                    continue
                self.move(tile, -dx, 0)
            self.update()
        for i in range(2):
            for tile in self._tiles:
                if tile is None:
                    continue
                self.move(tile, dx, 0)
            self.update()
        for i in range(2):
            for tile in self._tiles:
                if tile is None:
                    continue
                self.move(tile, dx, 0)
            self.update()
        for i in range(2):
            for tile in self._tiles:
                if tile is None:
                    continue
                self.move(tile, -dx, 0)
            self.update()
        self.drawing = False

    def load_images(self):
        img_path = "../src/images/"
        img_ext = ".png"
        self.images[0] = None
        for i in range(1, 9):
            path = img_path + str(i) + img_ext
            img = Image.open(path)
            self.images[i] = img.resize((self.tile_width, self.tile_height), Image.ANTIALIAS)
        img_path = "../src/hover/"
        img_ext = ".png"
        self.images[0] = None
        for i in range(1, 9):
            path = img_path + str(i) + img_ext
            img = Image.open(path)
            self.images_hover[i] = img.resize((self.tile_width, self.tile_height), Image.ANTIALIAS)

    def draw(self):
        if self.drawing:
            return
        self.drawing = True
        for i, num in enumerate(self.state):
            if num == 0:
                continue
            self._img_compatible[i] = ImageTk.PhotoImage(image=self.images[num])
            x = self.board_margin + self.tile_width * (i % 3)
            y = self.board_margin + self.tile_height * (i // 3)
            self._tiles[i] = self.create_image(x, y, anchor="nw", image=self._img_compatible[i])
        self.drawing = False

    def draw_board(self):
        path = "../src/background/board.png"
        img = Image.open(path)
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        img = img.resize((width, height), Image.ANTIALIAS)
        self._board_compatible = ImageTk.PhotoImage(image=img)
        self.create_image(0, 0, anchor="nw", image=self._board_compatible)

    def hover(self, event):
        if self.drawing:
            return
        tile = self.get_tile(event.x, event.y)
        self.refresh()
        if tile is None or self.state[tile] == 0:
            return
        self.delete(self._img_compatible[tile])
        self._img_compatible[tile] = ImageTk.PhotoImage(image=self.images_hover[self.state[tile]])
        x = self.board_margin + self.tile_width * (tile % 3)
        y = self.board_margin + self.tile_height * (tile // 3)
        self._tiles[tile] = self.create_image(x, y, anchor="nw", image=self._img_compatible[tile])

    def get_tile(self, x, y):
        if 31.5 < x < 160.5 and 31.5 < y < 160.5:
            return 0
        elif 160.5 < x < 289.5 and 31.5 < y < 160.5:
            return 1
        elif 289.5 < x < 418.5 and 31.5 < y < 160.5:
            return 2
        elif 31.5 < x < 160.5 and 160.5 < y < 289.5:
            return 3
        elif 160.5 < x < 289.5 and 160.5 < y < 289.5:
            return 4
        elif 289.5 < x < 418.5 and 160.5 < y < 289.5:
            return 5
        elif 31.5 < x < 160.5 and 289.5 < y < 418.5:
            return 6
        elif 160.5 < x < 289.5 and 289.5 < y < 418.5:
            return 7
        elif 289.5 < x < 418.5 and 289.5 < y < 418.5:
            return 8
        return None

    def refresh(self, _=None):
        for img in self._img_compatible:
            if img is None:
                continue
            self.delete(img)
        self.draw()

    def test_goal(self):
        goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        return self.state == goal_state

    def solve(self, event):
        if self.drawing:
            return
        if self.test_goal():
            self.shake_all()
            return
        if self.state[self.get_tile(event.x, event.y)] == 0:
            hard_state = PuzzleState(tuple(self.state), 3)
            path = solve(hard_state, "bfs")
            if not path:
                # The board is not solvable
                self.shake_all()
                return
            blank_tile = 0
            for i, item in enumerate(self.state):
                if item == 0:
                    blank_tile = i
                    break
            self.drawing = True
            for command in path:
                if command == "Up":
                    blank_tile -= 3
                    self.try_move_up(blank_tile)
                elif command == "Down":
                    blank_tile += 3
                    self.try_move_down(blank_tile)
                elif command == "Left":
                    blank_tile -= 1
                    self.try_move_left(blank_tile)
                elif command == "Right":
                    blank_tile += 1
                    self.try_move_right(blank_tile)
            self.drawing = False
        if self.test_goal():
            pass
        else:
            pass


def main():
    config = [8, 1, 2, 0, 4, 3, 7, 6, 5]
    # config = [8, 6, 4, 2, 1, 3, 5, 7, 0]
    root = Window()
    Backgroud(root)
    Logo(root)
    Board(root, config)
    root.mainloop()


if __name__ == "__main__":
    main()
