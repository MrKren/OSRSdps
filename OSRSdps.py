from tkinter import *
from tkinter.ttk import *
from tkinter_extras import *
from PIL import Image, ImageTk
from math import floor
import requests
from bs4 import BeautifulSoup
from ToolTip import Tooltip


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
        Entry(self.lookup, textvariable=self.player_name, width=12).grid(column=2, row=1, padx=10)
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

        self.melee_potions = ["None", "Regular", "Super", "Zamorak Brew", "Overload (Raids)"]
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

        self.equip1 = Equipment(self.master, "Equipment Set 1")
        self.equip1.frame.grid(column=6, row=1, padx=50, rowspan=10)
        self.equip2 = Equipment(self.master, "Equipment Set 2")
        self.equip2.frame.grid(column=7, row=1, rowspan=10)

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

        self.head_slot = StringVar()
        head_slot = self.make_image_button(self.frame, "graphics/slots/Head_slot.png", "data/head.txt", self.head_slot)
        head_slot_tip = Tooltip(head_slot, text=self.head_slot)
        self.head_slot.trace_add("write",
                                 lambda name, index, mode, sv=self.head_slot, tooltip=head_slot_tip: self.change_label(
                                     sv, tooltip))  
        # Not really sure how this works but it does (sometimes nature really do be like that)
        head_slot.grid(column=2, row=2, pady=5, padx=5)

        self.cape_slot = StringVar()
        cape_slot = self.make_image_button(self.frame, "graphics/slots/Cape_slot.png", "data/cape.txt", self.cape_slot)
        cape_slot_tip = Tooltip(cape_slot, text=self.cape_slot)
        self.cape_slot.trace_add("write",
                                 lambda name, index, mode, sv=self.cape_slot, tooltip=cape_slot_tip: self.change_label(
                                     sv, tooltip))
        cape_slot.grid(column=1, row=3, pady=5, padx=5)
        self.neck_slot = StringVar()
        neck_slot = self.make_image_button(self.frame, "graphics/slots/Neck_slot.png", "data/neck.txt", self.neck_slot)
        neck_slot_tip = Tooltip(neck_slot, text=self.neck_slot)
        self.neck_slot.trace_add("write",
                                 lambda name, index, mode, sv=self.neck_slot, tooltip=neck_slot_tip: self.change_label(
                                     sv, tooltip))
        neck_slot.grid(column=2, row=3, pady=5, padx=5)
        self.ammo_slot = StringVar()
        ammo_slot = self.make_image_button(self.frame, "graphics/slots/Ammo_slot.png", "data/ammo.txt", self.ammo_slot)
        ammo_slot_tip = Tooltip(ammo_slot, text=self.ammo_slot)
        self.ammo_slot.trace_add("write",
                                 lambda name, index, mode, sv=self.ammo_slot, tooltip=ammo_slot_tip: self.change_label(
                                     sv, tooltip))
        ammo_slot.grid(column=3, row=3, pady=5, padx=5)

        self.weapon_slot = StringVar()
        weapon_slot = self.make_image_button(self.frame, "graphics/slots/Weapon_slot.png", "data/weapon.txt", self.weapon_slot)
        weapon_slot_tip = Tooltip(weapon_slot, text=self.weapon_slot)
        self.weapon_slot.trace_add("write",
                                 lambda name, index, mode, sv=self.weapon_slot, tooltip=weapon_slot_tip: self.change_label(
                                     sv, tooltip))
        weapon_slot.grid(column=1, row=4, pady=5, padx=5)
        self.body_slot = StringVar()
        body_slot = self.make_image_button(self.frame, "graphics/slots/Body_slot.png", "data/body.txt", self.body_slot)
        body_slot_tip = Tooltip(body_slot, text=self.body_slot)
        self.body_slot.trace_add("write",
                                 lambda name, index, mode, sv=self.body_slot, tooltip=body_slot_tip: self.change_label(
                                     sv, tooltip))
        body_slot.grid(column=2, row=4, pady=5, padx=5)
        self.shield_slot = StringVar()
        shield_slot = self.make_image_button(self.frame, "graphics/slots/Shield_slot.png", "data/shield.txt", self.shield_slot)
        shield_slot_tip = Tooltip(shield_slot, text=self.shield_slot)
        self.shield_slot.trace_add("write",
                                 lambda name, index, mode, sv=self.shield_slot, tooltip=shield_slot_tip: self.change_label(
                                     sv, tooltip))
        shield_slot.grid(column=3, row=4, pady=5, padx=5)

        self.legs_slot = StringVar()
        legs_slot = self.make_image_button(self.frame, "graphics/slots/Legs_slot.png", "data/legs.txt", self.legs_slot)
        legs_slot_tip = Tooltip(legs_slot, text=self.legs_slot)
        self.legs_slot.trace_add("write",
                                 lambda name, index, mode, sv=self.legs_slot, tooltip=legs_slot_tip: self.change_label(
                                     sv, tooltip))
        legs_slot.grid(column=2, row=5, pady=5, padx=5)

        self.hand_slot = StringVar()
        gloves_slot = self.make_image_button(self.frame, "graphics/slots/Gloves_slot.png", "data/hand.txt", self.hand_slot)
        head_slot_tip = Tooltip(head_slot, text=self.head_slot)
        self.head_slot.trace_add("write",
                                 lambda name, index, mode, sv=self.head_slot, tooltip=head_slot_tip: self.change_label(
                                     sv, tooltip))
        gloves_slot.grid(column=1, row=6, pady=5, padx=5)
        self.boot_slot = StringVar()
        boots_slot = self.make_image_button(self.frame, "graphics/slots/Boots_slot.png", "data/boot.txt", self.boot_slot)
        boot_slot_tip = Tooltip(boots_slot, text=self.boot_slot)
        self.boot_slot.trace_add("write",
                                 lambda name, index, mode, sv=self.boot_slot, tooltip=boot_slot_tip: self.change_label(
                                     sv, tooltip))
        boots_slot.grid(column=2, row=6, pady=5, padx=5)
        self.ring_slot = StringVar()
        ring_slot = self.make_image_button(self.frame, "graphics/slots/Ring_slot.png", "data/ring.txt", self.ring_slot)
        ring_slot_tip = Tooltip(ring_slot, text=self.ring_slot)
        self.ring_slot.trace_add("write",
                                 lambda name, index, mode, sv=self.ring_slot, tooltip=ring_slot_tip: self.change_label(
                                     sv, tooltip))
        ring_slot.grid(column=3, row=6, pady=5, padx=5)

    def make_image_button(self, frame, image_name, filename, textvar):
        """makes images in tkinter"""
        load = Image.open(image_name)
        render = ImageTk.PhotoImage(load)
        img = Button(frame, image=render, command=lambda: self.make_popup(filename, textvar))
        img.image = render
        return img

    def read_data(self, filename):
        slot_data = []
        with open(filename, 'r') as file:
            for line in file:
                data = list(line.split(','))
                slot_data.append(data)
        names = []
        for i in slot_data:
            names.append(i[0])
        return names

    def make_popup(self, filename, textvar):
        popup = EquipSelect(self.read_data(filename), textvar)

    def change_label(self, sv, tooltip):
        tooltip.text = sv.get()


class EquipSelect(object):

    def __init__(self, slot, textvar):
        self.window = Tk()
        self.window.title("Equipment select")
        self.window.geometry("165x80")
        self.choice = AutocompleteCombobox(self.window)
        self.choice.set_completion_list(slot)
        self.choice.set(textvar.get())
        self.choice.grid(column=1, row=1, pady=10, padx=10)
        Button(self.window, text="Confirm", command=lambda: self.print_value(textvar)).grid(column=1, row=2)
        self.window.mainloop()

    def print_value(self, textvar):
        print(self.choice.get())
        textvar.set(self.choice.get())
        self.window.destroy()


root = Tk()

root.geometry("1000x400")


app = Window(root)
root.mainloop()
