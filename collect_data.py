import requests
from bs4 import BeautifulSoup


def slot_data(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})
    table_rows = table.find_all('tr')
    table_data = []
    for i in table_rows:
        data = i.find_all('td')
        table_data.append(data)
    table_data.remove(table_data[0])
    for i in table_data:
        name = i[0]
        name = name.find('a')
        i[0] = name.get('title')
        for j in range(2, len(i)):
            data = i[j]
            data = str(data)
            data = data[18:-5]
            try:
                data = int(data)
            except ValueError:
                data = 0
            i[j] = data
        i.remove(i[1])
    return table_data


total_data = [slot_data("https://oldschool.runescape.wiki/w/Head_slot_table"),
              slot_data("https://oldschool.runescape.wiki/w/Cape_slot_table"),
              slot_data("https://oldschool.runescape.wiki/w/Neck_slot_table"),
              slot_data("https://oldschool.runescape.wiki/w/Ammunition_slot_table"),
              slot_data("https://oldschool.runescape.wiki/w/Weapon_slot_table"),
              slot_data("https://oldschool.runescape.wiki/w/Two-handed_slot_table"),
              slot_data("https://oldschool.runescape.wiki/w/Body_slot_table"),
              slot_data("https://oldschool.runescape.wiki/w/Shield_slot_table"),
              slot_data("https://oldschool.runescape.wiki/w/Legs_slot_table"),
              slot_data("https://oldschool.runescape.wiki/w/Hand_slot_table"),
              slot_data("https://oldschool.runescape.wiki/w/Feet_slot_table"),
              slot_data("https://oldschool.runescape.wiki/w/Ring_slot_table")]

data_names = ["head", "cape", "neck", "ammo", "weapon", "2hand", "body", "shield", "legs", "hand", "boot", "ring"]

index = 0
for i in total_data:
    filename = "data/" + data_names[index] + ".txt"
    index += 1
    with open(filename, 'w') as file:
        for j in i:
            line = ','.join([str(elem) for elem in j])
            line = line + '\n'
            file.write(line)
