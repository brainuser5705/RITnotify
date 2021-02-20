from pprint import pprint
import os

from discord import Colour
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

import discord

load_dotenv()

URL = os.getenv('DINING_URL')
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

location_ids = {'bcc': "103", 'cmc': "104", 'tc': "105", 'gracies': "107"}
location_names = {'bcc': "Brick City Cafe", 'cmc': "Cafe & Market at Crossroads", 'tc': "The Commons", 'gracies': "Gracie's"}
meals = {'DINNER', 'LUNCH', 'BREAKFAST'}
content = soup.find('div', class_='ds-output')

def get_menu(location_name, content=content):

    id = location_ids.get(location_name)
    menu_section = content.find(id=id)

    s = 'Showing  menus for: ' + menu_section.find('h3').text
    error = ""
    embeds = []

    for meal in meals:

        embed = discord.Embed(title=meal, colour=Colour.orange())

        meal_menu = menu_section.find(id=meal + '-' + id)
        if meal_menu is None:
            error = "**" + location_names.get(location_name) + ' is closed today.**'
            break

        items_section = meal_menu.find('div', class_='col-xs-12 col-md-12 menu-category-items')
        if items_section is None:
            embed.add_field(name='No ' + meal + ' menu today.', value='------')
            embeds.append(embed)
            continue

        options_list = items_section.find_all('div', class_='col-xs-12 col-md-6 menu-category-list')
        for option in options_list:
            station = option.find('div', class_='menu-category')
            dish = option.find('div', class_='menu-items')

            dish_string = ""
            for content in dish.contents:
                if str(content) not in ['<br/>', '\n']:
                    dish_string += '- ' + str(content) + '\n'
                
            embed.add_field(name='**' + station.text + '**', value=dish_string)

        embeds.append(embed)

    return s, error, embeds