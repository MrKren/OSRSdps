import requests
from bs4 import BeautifulSoup
import time


def slot_data(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})
    table_rows = table.find_all('tr')
    table_data = []
    table_links = []
    for i in table_rows:
        data = i.find_all('td')
        table_data.append(data)
    table_data.remove(table_data[0])
    for i in table_data:
        name = i[0]
        name = name.find('a')
        i[0] = name.get('title')
        table_links.append(name.get('href'))
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
    return table_data, table_links


total_data = [slot_data("https://oldschool.runescape.wiki/w/Head_slot_table")[0],
              slot_data("https://oldschool.runescape.wiki/w/Cape_slot_table")[0],
              slot_data("https://oldschool.runescape.wiki/w/Neck_slot_table")[0],
              slot_data("https://oldschool.runescape.wiki/w/Ammunition_slot_table")[0],
              slot_data("https://oldschool.runescape.wiki/w/Weapon_slot_table")[0],
              slot_data("https://oldschool.runescape.wiki/w/Two-handed_slot_table")[0],
              slot_data("https://oldschool.runescape.wiki/w/Body_slot_table")[0],
              slot_data("https://oldschool.runescape.wiki/w/Shield_slot_table")[0],
              slot_data("https://oldschool.runescape.wiki/w/Legs_slot_table")[0],
              slot_data("https://oldschool.runescape.wiki/w/Hand_slot_table")[0],
              slot_data("https://oldschool.runescape.wiki/w/Feet_slot_table")[0],
              slot_data("https://oldschool.runescape.wiki/w/Ring_slot_table")[0]]

total_links = [slot_data("https://oldschool.runescape.wiki/w/Head_slot_table")[1],
               slot_data("https://oldschool.runescape.wiki/w/Cape_slot_table")[1],
               slot_data("https://oldschool.runescape.wiki/w/Neck_slot_table")[1],
               slot_data("https://oldschool.runescape.wiki/w/Ammunition_slot_table")[1],
               slot_data("https://oldschool.runescape.wiki/w/Weapon_slot_table")[1],
               slot_data("https://oldschool.runescape.wiki/w/Two-handed_slot_table")[1],
               slot_data("https://oldschool.runescape.wiki/w/Body_slot_table")[1],
               slot_data("https://oldschool.runescape.wiki/w/Shield_slot_table")[1],
               slot_data("https://oldschool.runescape.wiki/w/Legs_slot_table")[1],
               slot_data("https://oldschool.runescape.wiki/w/Hand_slot_table")[1],
               slot_data("https://oldschool.runescape.wiki/w/Feet_slot_table")[1],
               slot_data("https://oldschool.runescape.wiki/w/Ring_slot_table")[1]]

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

start_time = time.time()
index = 0
base_url = "https://oldschool.runescape.wiki"
for i in total_links:
    filepath = "graphics/items/" + data_names[index] + "/"
    index_file = filepath + data_names[index] + ".txt"
    file_index = 0
    with open(index_file, 'w') as file:
        for j in i:
            page_url = base_url + j
            page = requests.get(page_url).text
            soup = BeautifulSoup(page, 'html.parser')
            item_table = soup.find('table', {'class': 'rsw-infobox'})
            item_info = item_table.find_all('td')
            image = item_info[1]
            image = image.find('img')
            try:
                image_url = base_url + image.get('src')
                r = requests.get(image_url, stream=True)
                if r.status_code == 200:
                    with open(filepath + image.get('alt'), 'wb') as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
                    f.close()
                text = str(image.get('alt')) + "," + str(total_data[index][file_index][0]) + "\n"
                file.write(text)
                print(file_index, text)
                file_index += 1
            except AttributeError:
                text = "No file" + "," + str(total_data[index][file_index][0]) + "\n"
                print(file_index, text)
                file_index += 1
            except TypeError:
                text = "No file" + "," + str(total_data[index][file_index][0]) + "\n"
                print(file_index, text)
                file_index += 1
    file.close()
    index += 1

end_time = time.time()
total_time = (end_time-start_time)/60
text = "\033[1;32;40m " + "Total time taken to gather data: " + str(total_time)
print(text)
