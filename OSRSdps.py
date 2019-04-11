from tkinter import *
from PIL import Image, ImageTk
from math import floor


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("OSRS DPS Calculator by MrKren")  # Sets title

        """Menu Bar"""
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        """look up"""
        self.lookup = Frame(self.master)
        self.lookup.grid(column=1, row=1, columnspan=3)

        self.player_name = StringVar()

        Label(self.lookup, text="Player name").grid(column=1, row=1)
        Entry(self.lookup, textvariable=self.player_name, width=12).grid(column=2, row=1, columnspan=2)

        """Skill Inputs"""
        self.player_stats = Frame(self.master)
        self.player_stats.grid(column=1, row=2, columnspan=3)

        self.attack_num = IntVar(value=1)
        self.strength_num = IntVar(value=1)
        self.defence_num = IntVar(value=1)
        self.range_num = IntVar(value=1)
        self.prayer_num = IntVar(value=1)
        self.magic_num = IntVar(value=1)
        self.hitpoints_num = IntVar(value=10)
        self.combat_lvl = IntVar(value=3)

        Label(self.player_stats, text="Player Stats").grid(column=1, row=1, columnspan=3)

        self.make_image(self.player_stats, "graphics/Attack_icon.png", (1, 2))
        Label(self.player_stats, text="Attack").grid(column=2, row=2)
        Entry(self.player_stats, width=2, textvariable=self.attack_num).grid(column=3, row=2)

        self.make_image(self.player_stats, "graphics/Strength_icon.png", (1, 3))
        Label(self.player_stats, text="Strength").grid(column=2, row=3)
        Entry(self.player_stats, width=2, textvariable=self.strength_num).grid(column=3, row=3)

        self.make_image(self.player_stats, "graphics/Defence_icon.png", (1, 4))
        Label(self.player_stats, text="Defence").grid(column=2, row=4)
        Entry(self.player_stats, width=2, textvariable=self.defence_num).grid(column=3, row=4)

        self.make_image(self.player_stats, "graphics/Ranged_icon.png", (1, 5))
        Label(self.player_stats, text="Ranged").grid(column=2, row=5)
        Entry(self.player_stats, width=2, textvariable=self.range_num).grid(column=3, row=5)

        self.make_image(self.player_stats, "graphics/Prayer_icon.png", (1, 6))
        Label(self.player_stats, text="Prayer").grid(column=2, row=6)
        Entry(self.player_stats, width=2, textvariable=self.prayer_num).grid(column=3, row=6)

        self.make_image(self.player_stats, "graphics/Magic_icon.png", (1, 7))
        Label(self.player_stats, text="Magic").grid(column=2, row=7)
        Entry(self.player_stats, width=2, textvariable=self.magic_num).grid(column=3, row=7)

        self.make_image(self.player_stats, "graphics/Hitpoints_icon.png", (1, 8))
        Label(self.player_stats, text="Hitpoints").grid(column=2, row=8)
        Entry(self.player_stats, width=2, textvariable=self.hitpoints_num).grid(column=3, row=8)

        # Combat level
        Button(self.player_stats, text="Calculate", command=self.calc_combat).grid(column=1, columnspan=3, row=9,
                                                                                   padx=20, pady=10)

        Entry(self.player_stats, width=3, textvariable=self.combat_lvl).grid(column=3, row=10)
        Label(self.player_stats, text="Combat Level").grid(column=2, row=10)

        """"""

    def calc_combat(self):
        base = 0.25*floor(self.defence_num.get() + self.hitpoints_num.get() + floor(self.prayer_num.get()/2))
        melee = 0.325*(self.attack_num.get() + self.strength_num.get())
        ranged = 0.325*floor(3*self.range_num.get()/2)
        mage = 0.325*floor(3*self.magic_num.get()/2)
        final = floor(base + max((melee, ranged, mage)))
        self.combat_lvl.set(final)

    def make_image(self, frame, image_name, image_pos):
        load = Image.open(image_name)
        render = ImageTk.PhotoImage(load)

        img = Label(frame, image=render)
        img.image = render
        img.grid(column=image_pos[0], row=image_pos[1])

    def client_exit(self):
        exit()


root = Tk()

root.geometry("500x300")


app = Window(root)
root.mainloop()
