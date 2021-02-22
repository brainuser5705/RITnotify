import os
import re

from discord import Colour
from bs4 import BeautifulSoup
import requests
import discord
from datetime import datetime

MENU_URL = 'https://www.rit.edu/fa/diningservices/daily-specials'
HOURS_URL = 'https://www.rit.edu/fa/diningservices/places-to-eat/hours'

def get_menu(location_name):

    page = requests.get(MENU_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    location_ids = {'bcc': "103", 'cmc': "104", 'tc': "105", 'gracies': "107"}
    location_names = {'bcc': "Brick City Cafe", 'cmc': "Cafe & Market at Crossroads", 'tc': "The Commons",
                      'gracies': "Gracie's"}
    meals = {'DINNER', 'LUNCH', 'BREAKFAST'}
    content = soup.find('div', class_='ds-output')

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

def get_hours(is_include_closed):
    current_time = datetime.now()
    time_regex = re.compile(r'(1[012]|[1-9]):([0-5][0-9])(am|pm)')

    page = requests.get(HOURS_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    places = soup.find_all('div', class_='hours-title')

    embed = discord.Embed(color=Colour.orange(), title="RIT Dining Hours", description="See which stores are open or closed")

    for place in places:
        box = place.find_next_sibling('div', class_="container-fluid location-box panel panel-default hours-all-panel")
        time = box.find('div', class_='row panel-body')

        time_groups = time_regex.findall(time.text)

        if time.text == 'Closed' and is_include_closed:

            embed.add_field(name=place.text + ':red_circle: (CLOSED)', value='-----------', inline=False)

        else:

            start_hour = int(time_groups[0][0])
            start_minute=int(time_groups[0][1])
            start_meridiem = time_groups[0][2]
            end_hour = int(time_groups[1][0])
            end_minute = int(time_groups[1][1])
            end_meridiem = time_groups[1][2]

            start_hour = (start_hour % 12) + 12 if start_meridiem == 'pm' else start_hour
            end_hour = (end_hour % 12) + 12 if end_meridiem == 'pm' else end_hour

            place_hours = time.find('div', class_='col-sm-5').text.strip()

            start_datetime = current_time.replace(hour=start_hour, minute=start_minute)
            end_datetime = current_time.replace(hour=end_hour, minute=end_minute)

            if start_datetime <= current_time <= end_datetime:
                embed.add_field(name=place.text + ':green_circle: (OPEN)', value=place_hours, inline=False)
            elif is_include_closed:
                embed.add_field(name=place.text + ':red_circle: (CLOSED)', value=place_hours, inline=False)

    if not embed.fields:
        embed.add_field(name='No places are open now.', value='-----------')

    return embed

