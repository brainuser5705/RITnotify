from pprint import pprint
import os
import re

from discord import Colour
from bs4 import BeautifulSoup
import requests
import discord
from datetime import datetime

def get_menu(location_name):

    URL = 'https://www.rit.edu/fa/diningservices/daily-specials'
    page = requests.get(URL)
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

def get_hours(includeClose):
    URL = "https://www.rit.edu/fa/diningservices/places-to-eat/hours"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find('div', class_='view-content')

    places = content.find_all('div', class_='hours-title')
    current_time = datetime.now()
    current_hour = current_time.hour

    embed = discord.Embed(color=Colour.orange(), title="RIT Dining Hours", description="Open or closed?")

    for place in places:
        box = place.find_next_sibling('div', class_="container-fluid location-box panel panel-default hours-all-panel")
        time = box.find('div', class_='row panel-body')

        timeRegex = re.compile(r'(1[012]:|[1-9]:|am|pm|Closed)')
        timesGroup = timeRegex.findall(time.text)

        s = ""
        if timesGroup[0] == 'Closed':
            if includeClose:
                embed.add_field(name=place.text + ":red_circle: (CLOSED)", value="CLOSED", inline=False)
        else:
            s += time.find('div', class_='col-sm-5').text

            starthour = int(timesGroup[0][:-1])
            endhour = int(timesGroup[2][:-1])

            if timesGroup[1] == 'pm':
                starthour = (starthour % 12) + 12
            if timesGroup[-1] == 'pm':
                endhour = (endhour % 12) + 12

            if starthour <= current_hour <= endhour:
                embed.add_field(name=place.text + ":green_circle: (OPEN)", value=s, inline=False)
            elif includeClose:
                embed.add_field(name=place.text + ":red_circle: (CLOSED)", value=s, inline=False)

    return embed

