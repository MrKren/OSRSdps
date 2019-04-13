from tkinter import *
from tkinter.ttk import *
from tkinter_extras import *
from PIL import Image, ImageTk
from math import floor
import requests
from bs4 import BeautifulSoup


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        """Main widget window"""
        self.master.title("OSRS DPS Calculator by MrKren")  # Sets title

        """Menu Bar"""
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        """look up"""
        self.lookup = Frame(self.master)
        self.lookup.grid(column=1, row=1, columnspan=5)

        self.player_name = StringVar()

        Label(self.lookup, text="Player name").grid(column=1, row=1)
        Entry(self.lookup, textvariable=self.player_name, width=12).grid(column=2, row=1)
        Button(self.lookup, text="Lookup", command=self.look_up).grid(column=1, row=2, columnspan=2, pady=5)

        """Skill Inputs"""
        self.player_stats = Frame(self.master)
        self.player_stats.grid(column=1, row=2, columnspan=5)

        self.attack_num = IntVar(value=1)
        self.strength_num = IntVar(value=1)
        self.defence_num = IntVar(value=1)
        self.ranged_num = IntVar(value=1)
        self.prayer_num = IntVar(value=1)
        self.magic_num = IntVar(value=1)
        self.hitpoints_num = IntVar(value=10)
        self.combat_lvl = IntVar(value=3)

        self.melee_potions = ["None", "Regular", "Super", "Zamorack Brew", "Overload (Raids)"]
        self.melee_prayers = ["None", "5%", "10%", "15%", "Chivalry", "Piety"]
        self.ranged_potions = ["None", "Regular", "Super", "Overload (Raids)"]
        self.ranged_prayers = ["None", "5%", "10%", "15%", "Rigour", "Augury"]
        self.magic_potions = ["None", "Regular", "Super", "Imbued Heart", "Overload (Raids)"]
        self.attack_pot = StringVar(value=self.melee_potions[0])
        self.strength_pot = StringVar(value=self.melee_potions[0])
        self.defence_pot = StringVar(value=self.melee_potions[0])
        self.ranged_pot = StringVar(value=self.ranged_potions[0])
        self.magic_pot = StringVar(value=self.magic_potions[0])
        self.attack_pray = StringVar(value=self.melee_prayers[0])
        self.strength_pray = StringVar(value=self.melee_prayers[0])
        self.defence_pray = StringVar(value=self.melee_prayers[0])
        self.ranged_pray = StringVar(value=self.ranged_prayers[0])
        self.magic_pray = StringVar(value=self.ranged_prayers[0])

        Label(self.player_stats, text="Player Stats").grid(column=2, row=1)
        Label(self.player_stats, text="Potion").grid(column=4, row=1)
        Label(self.player_stats, text="Prayer").grid(column=5, row=1)

        self.make_image(self.player_stats, "graphics/skills/Attack_icon.png", (1, 2))
        Label(self.player_stats, text="Attack").grid(column=2, row=2)
        Entry(self.player_stats, width=2, textvariable=self.attack_num).grid(column=3, row=2)
        a_pot = OptionMenu(self.player_stats, self.attack_pot, self.melee_potions[0], *self.melee_potions)
        a_pot.grid(column=4, row=2)  # Note this the option menu from ttk not tkinter
        a_pot.config(width=17)
        a_pray = OptionMenu(self.player_stats, self.attack_pray, self.melee_prayers[0], *self.melee_prayers)
        a_pray.grid(column=5, row=2)
        a_pray.config(width=8)

        self.make_image(self.player_stats, "graphics/skills/Strength_icon.png", (1, 3))
        Label(self.player_stats, text="Strength").grid(column=2, row=3)
        Entry(self.player_stats, width=2, textvariable=self.strength_num).grid(column=3, row=3)
        s_pot = OptionMenu(self.player_stats, self.strength_pot, self.melee_potions[0], *self.melee_potions)
        s_pot.grid(column=4, row=3)
        s_pot.config(width=17)
        s_pray = OptionMenu(self.player_stats, self.strength_pray, self.melee_prayers[0], *self.melee_prayers)
        s_pray.grid(column=5, row=3)
        s_pray.config(width=8)

        self.make_image(self.player_stats, "graphics/skills/Defence_icon.png", (1, 4))
        Label(self.player_stats, text="Defence").grid(column=2, row=4)
        Entry(self.player_stats, width=2, textvariable=self.defence_num).grid(column=3, row=4)
        dpot = OptionMenu(self.player_stats, self.defence_pot, self.melee_potions[0], *self.melee_potions)
        dpot.grid(column=4, row=4)
        dpot.config(width=17)
        dpray = OptionMenu(self.player_stats, self.defence_pray, self.melee_prayers[0], *self.melee_prayers)
        dpray.grid(column=5, row=4)
        dpray.config(width=8)

        self.make_image(self.player_stats, "graphics/skills/Ranged_icon.png", (1, 5))
        Label(self.player_stats, text="Ranged").grid(column=2, row=5)
        Entry(self.player_stats, width=2, textvariable=self.ranged_num).grid(column=3, row=5)
        a_pot = OptionMenu(self.player_stats, self.ranged_pot, self.ranged_potions[0], *self.ranged_potions)
        a_pot.grid(column=4, row=5)
        a_pot.config(width=17)
        a_pray = OptionMenu(self.player_stats, self.ranged_pray, self.ranged_prayers[0], *self.ranged_prayers)
        a_pray.grid(column=5, row=5)
        a_pray.config(width=8)

        self.make_image(self.player_stats, "graphics/skills/Magic_icon.png", (1, 6))
        Label(self.player_stats, text="Magic").grid(column=2, row=6)
        Entry(self.player_stats, width=2, textvariable=self.magic_num).grid(column=3, row=6)
        a_pot = OptionMenu(self.player_stats, self.magic_pot, self.magic_potions[0], *self.magic_potions)
        a_pot.grid(column=4, row=6)
        a_pot.config(width=17)
        a_pray = OptionMenu(self.player_stats, self.magic_pray, self.ranged_prayers[0], *self.ranged_prayers)
        a_pray.grid(column=5, row=6)
        a_pray.config(width=8)

        self.make_image(self.player_stats, "graphics/skills/Prayer_icon.png", (1, 7))
        Label(self.player_stats, text="Prayer").grid(column=2, row=7)
        Entry(self.player_stats, width=2, textvariable=self.prayer_num).grid(column=3, row=7)

        self.make_image(self.player_stats, "graphics/skills/Hitpoints_icon.png", (1, 8))
        Label(self.player_stats, text="Hitpoints").grid(column=2, row=8)
        Entry(self.player_stats, width=2, textvariable=self.hitpoints_num).grid(column=3, row=8)

        # Combat level
        Button(self.player_stats, text="Calculate", command=self.calc_combat).grid(column=1, columnspan=3, row=9,
                                                                                   padx=20, pady=10)

        Entry(self.player_stats, width=3, textvariable=self.combat_lvl).grid(column=3, row=10)
        Label(self.player_stats, text="Combat Level").grid(column=2, row=10)

        """Equipment Section 1"""

        equip1 = Equipment(self.master, "Equipment Set 1")
        equip1.frame.grid(column=6, row=1, padx=50, rowspan=10)
        equip1 = Equipment(self.master, "Equipment Set 2")
        equip1.frame.grid(column=7, row=1, rowspan=10)

    def look_up(self):
        """Collects players data from RuneScape HiScores webpage"""
        url = "http://services.runescape.com/m=hiscore_oldschool/hiscorepersonal.ws?user1="
        self.player_name.set(self.player_name.get().replace(" ", "_"))
        url = url + self.player_name.get()
        print("Sending request to:")
        print(url)
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find('div', {'id': 'contentHiscores'})
        table_rows = table.find_all('tr')
        table_data = []
        for i in table_rows:
            data = i.find_all('td')
            table_data.append(data)
        for j in range(4, 11):
            data = table_data[j][3]
            data = str(data)
            data = data[18:-5]
            table_data[j][3] = data
        self.attack_num.set(table_data[4][3])
        self.strength_num.set(table_data[6][3])
        self.defence_num.set(table_data[5][3])
        self.hitpoints_num.set(table_data[7][3])
        self.ranged_num.set(table_data[8][3])
        self.prayer_num.set(table_data[9][3])
        self.magic_num.set(table_data[10][3])
        self.calc_combat()

    def calc_combat(self):
        """Calculates combat level based off stats inputted"""
        base = 0.25*floor(self.defence_num.get() + self.hitpoints_num.get() + floor(self.prayer_num.get()/2))
        melee = 0.325*(self.attack_num.get() + self.strength_num.get())
        ranged = 0.325*floor(3 * self.ranged_num.get() / 2)
        mage = 0.325*floor(3*self.magic_num.get()/2)
        final = floor(base + max((melee, ranged, mage)))
        self.combat_lvl.set(final)

    def make_image(self, frame, image_name, image_pos):
        """makes images in tkinter"""
        load = Image.open(image_name)
        render = ImageTk.PhotoImage(load)

        img = Label(frame, image=render)
        img.image = render
        img.grid(column=image_pos[0], row=image_pos[1])

    def client_exit(self):
        exit()


class Equipment(object):

    def __init__(self, master, equip_num):
        self.frame = Frame(master)
        self.set_num = Label(self.frame, text=equip_num).grid(column=1, row=1, columnspan=3)

        head_slot = self.make_image_button(self.frame, "graphics/slots/Head_slot.png")
        head_slot.grid(column=2, row=2, pady=5, padx=5)

        cape_slot = self.make_image_button(self.frame, "graphics/slots/Cape_slot.png")
        cape_slot.grid(column=1, row=3, pady=5, padx=5)
        neck_slot = self.make_image_button(self.frame, "graphics/slots/Neck_slot.png")
        neck_slot.grid(column=2, row=3, pady=5, padx=5)
        ammo_slot = self.make_image_button(self.frame, "graphics/slots/Ammo_slot.png")
        ammo_slot.grid(column=3, row=3, pady=5, padx=5)

        weapon_slot = self.make_image_button(self.frame, "graphics/slots/Weapon_slot.png")
        weapon_slot.grid(column=1, row=4, pady=5, padx=5)
        body_slot = self.make_image_button(self.frame, "graphics/slots/Body_slot.png")
        body_slot.grid(column=2, row=4, pady=5, padx=5)
        shield_slot = self.make_image_button(self.frame, "graphics/slots/Shield_slot.png")
        shield_slot.grid(column=3, row=4, pady=5, padx=5)

        legs_slot = self.make_image_button(self.frame, "graphics/slots/Legs_slot.png")
        legs_slot.grid(column=2, row=5, pady=5, padx=5)

        gloves_slot = self.make_image_button(self.frame, "graphics/slots/Gloves_slot.png")
        gloves_slot.grid(column=1, row=6, pady=5, padx=5)
        boots_slot = self.make_image_button(self.frame, "graphics/slots/Boots_slot.png")
        boots_slot.grid(column=2, row=6, pady=5, padx=5)
        ring_slot = self.make_image_button(self.frame, "graphics/slots/Ring_slot.png")
        ring_slot.grid(column=3, row=6, pady=5, padx=5)

    def make_image_button(self, frame, image_name):
        """makes images in tkinter"""
        load = Image.open(image_name)
        render = ImageTk.PhotoImage(load)

        img = Button(frame, image=render, command=lambda: EquipSelect(["Sword", "Bow", "Axe"]))
        img.image = render
        return img


class EquipSelect(object):

    def __init__(self, slot):
        self.window = Tk()
        self.window.title("Equipment select")
        self.window.geometry("165x80")

        self.choice = AutocompleteCombobox(self.window)
        self.choice.set_completion_list(slot)
        self.choice.grid(column=1, row=1, pady=10, padx=10)

        Button(self.window, text="Confirm").grid(column=1, row=2)


root = Tk()

root.geometry("1000x400")


app = Window(root)
root.mainloop()
