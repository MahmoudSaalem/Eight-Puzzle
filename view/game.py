import tkinter
from PIL import Image, ImageTk


class Window(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Eight Puzzle")
        window_width = 300
        window_height = 400
        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.winfo_screenheight() / 2 - window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")


class Board(tkinter.Canvas):
    def __init__(self, master=None, state=None, width=242, height=242, bg="red"):
        if master is None or state is None:
            raise Exception("Invalid Arguments")
        super().__init__(master, width=width, height=height, bg=bg)
        self.master = master
        self.state = state
        self.pack()
        self.drawing = False
        self._img_compatible = [None] * 10
        self._tiles = [None] * 10
        self.draw()
        self.bind("<Button-1>", self.move_tile)
        self.bind("<Motion>", self.hover)
        self.bind("<Leave>", self.refresh)

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
        # self.refresh()
        if self.test_goal():
            self.config(bg="green")
        else:
            self.config(bg="red")

    def try_move_down(self, tile):
        if tile // 3 == 0 or self.state[tile - 3] != 0:
            return False
        total = 64 + 10
        dy = - total / 5
        self.slide(self._tiles[tile], 0, dy)
        self.swap_images(tile, tile - 3)
        return True

    def try_move_left(self, tile):
        if tile % 3 == 2 or self.state[tile + 1] != 0:
            return False
        total = 64 + 10
        dx = total / 5
        self.slide(self._tiles[tile], dx, 0)
        self.swap_images(tile, tile + 1)
        return True

    def try_move_up(self, tile):
        if tile // 3 == 2 or self.state[tile + 3] != 0:
            return False
        total = 64 + 10
        dy = total / 5
        self.slide(self._tiles[tile], 0, dy)
        self.swap_images(tile, tile + 3)
        return True

    def try_move_right(self, tile):
        if tile % 3 == 0 or self.state[tile - 1] != 0:
            return False
        total = 64 + 10
        dx = - total / 5
        self.slide(self._tiles[tile], dx, 0)
        self.swap_images(tile, tile - 1)
        return True

    def try_double_move_down(self, tile):
        if tile // 3 != 2 or self.state[tile - 6] != 0:
            return False
        total = 64 + 10
        dy = - total / 5
        self.double_slide(self._tiles[tile], self._tiles[tile - 3], 0, dy)
        self.swap_images(tile - 3, tile - 6)
        self.swap_images(tile, tile - 3)
        return True

    def try_double_move_left(self, tile):
        if tile % 3 != 0 or self.state[tile + 2] != 0:
            return False
        total = 64 + 10
        dx = total / 5
        self.double_slide(self._tiles[tile], self._tiles[tile + 1], dx, 0)
        self.swap_images(tile + 1, tile + 2)
        self.swap_images(tile, tile + 1)
        return True

    def try_double_move_up(self, tile):
        if tile // 3 != 0 or self.state[tile + 6] != 0:
            return False
        total = 64 + 10
        dy = total / 5
        self.double_slide(self._tiles[tile], self._tiles[tile + 3], 0, dy)
        self.swap_images(tile + 3, tile + 6)
        self.swap_images(tile, tile + 3)
        return True

    def try_double_move_right(self, tile):
        if tile % 3 != 2 or self.state[tile - 2] != 0:
            return False
        total = 64 + 10
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

    def draw(self):
        img_path = "../src/images/"
        img_ext = ".png"
        if self.drawing:
            return
        self.drawing = True
        for i, num in enumerate(self.state):
            if num == 0:
                continue
            path = img_path + str(num) + img_ext
            img = Image.open(path)
            self._img_compatible[i] = ImageTk.PhotoImage(image=img)
            x = (64 + 10) * (i % 3)
            y = (64 + 10) * (i // 3)
            self._tiles[i] = self.create_image(x, y, anchor="nw", image=self._img_compatible[i])
        self.drawing = False

    def hover(self, event):
        if self.drawing:
            return
        tile = self.get_tile(event.x, event.y)
        self.refresh()
        if tile is None or self.state[tile] == 0:
            return
        self.delete(self._img_compatible[tile])
        path = "../src/hover/" + str(self.state[tile]) + ".png"
        img = Image.open(path)
        self._img_compatible[tile] = ImageTk.PhotoImage(image=img)
        x = (64 + 10) * (tile % 3)
        y = (64 + 10) * (tile // 3)
        self._tiles[tile] = self.create_image(x, y, anchor="nw", image=self._img_compatible[tile])

    def get_tile(self, x, y):
        if 18 < x < 84 and 18 < y < 84:
            return 0
        elif 92 < x < 158 and 18 < y < 84:
            return 1
        elif 166 < x < 232 and 18 < y < 84:
            return 2
        elif 18 < x < 84 and 92 < y < 158:
            return 3
        elif 92 < x < 158 and 92 < y < 158:
            return 4
        elif 166 < x < 232 and 92 < y < 158:
            return 5
        elif 18 < x < 84 and 166 < y < 232:
            return 6
        elif 92 < x < 158 and 166 < y < 232:
            return 7
        elif 166 < x < 232 and 166 < y < 232:
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


def main():
    config = [1, 0, 2, 3, 4, 5, 6, 7, 8]
    root = Window()
    game = Board(root, config)
    game.mainloop()


if __name__ == "__main__":
    main()
