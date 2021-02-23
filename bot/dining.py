import os
import re

from discord import Colour
from bs4 import BeautifulSoup
import requests
import discord
from datetime import datetime

MENU_URL = 'https://www.rit.edu/fa/diningservices/daily-specials'
HOURS_URL = 'https://www.rit.edu/fa/diningservices/places-to-eat/hours'


def get_menu(loc_arg):
    """
    Web scrapes the RIT dining specials website.
    :param loc_arg: location to get menu of
    :return: list of Embeds of menus
    """

    page = requests.get(MENU_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    # each location has a div with an id of the following numbers
    loc_ids = {'bcc': "103", 'cmc': "104", 'tc': "105", 'gracies': "107"}

    menu_tag = soup.find(id=loc_ids.get(loc_arg))

    # contains the dining location name
    loc_name = menu_tag.find('h3').text

    # div where the menus are contained
    menus = menu_tag.find('div', class_='ds-loc-title')

    embeds = []

    if not menus.contents:
        string = '**' + loc_name + '** is closed today.'
    else:
        string = 'Showing  menus for: **' + loc_name + '**'

        for menu in menus.findChildren(recursive=False):  # only find direct children, e.g. <BREAKFAST-107>, <LUNCH-107>

            menu_name = menu.find('div', class_='menu-type').text

            embed = discord.Embed(title=menu_name, color=Colour.orange())

            # container for the actual list of options in menu
            items_section = menu.find('div', class_='col-xs-12 col-md-12 menu-category-items')

            if items_section is None:
                embed.add_field(name='No ' + menu_name + ' today.', value='-')

            # gets each individual option
            stations = items_section.find_all('div',
                                              class_='col-xs-12 col-md-6 menu-category-list')  # b/c there is another div class='clear'
            for item in stations:
                station_name = item.find('div', class_='menu-category').text
                dish = item.find('div', class_='menu-items')

                dish_string = ""
                for content in dish.contents[:-1]:  # there is a new line at the end
                    if str(content) != '<br/>':
                        dish_string += '- ' + str(content) + '\n'

                embed.add_field(name=station_name, value=dish_string)

            embeds.append(embed)  # outside of the for loop after everything is added

    return string, embeds


def get_hours(is_include_closed):
    """
    Web scrapes the RIT dining hours webpage
    :param is_include_closed: whether to show closed places or not
    :return: Embed of all the places
    """

    current_time = datetime.now()
    time_regex = re.compile(r'(1[012]|[1-9]):([0-5][0-9])(am|pm)')

    page = requests.get(HOURS_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    embed = discord.Embed(color=Colour.orange(), title="RIT Dining Hours",
                          description="See which stores are open or closed")

    # hours-title div is the starting tag for all places, specifically the name of the place
    places = soup.find_all('div', class_='hours-title')

    for place in places:

        # container for the day and time of place
        box = place.find_next_sibling('div', class_="container-fluid location-box panel panel-default hours-all-panel")
        # the time container
        time = box.find('div', class_='row panel-body')

        if time.text == 'Closed' and is_include_closed:

            embed.add_field(name=place.text + ':red_circle: (CLOSED)', value='-----------', inline=False)

        else:

            # groups into (HH):(mm)(am|pm)
            time_groups = time_regex.findall(time.text)

            start_hour = int(time_groups[0][0])
            start_minute = int(time_groups[0][1])
            start_meridiem = time_groups[0][2]
            end_hour = int(time_groups[1][0])
            end_minute = int(time_groups[1][1])
            end_meridiem = time_groups[1][2]

            # convert into 24-hr format
            start_hour = (start_hour % 12) + 12 if start_meridiem == 'pm' else start_hour
            end_hour = (end_hour % 12) + 12 if end_meridiem == 'pm' else end_hour

            # Creates new datetime object for comparison with current time
            start_datetime = current_time.replace(hour=start_hour, minute=start_minute)
            end_datetime = current_time.replace(hour=end_hour, minute=end_minute)

            place_hours = time.find('div', class_='col-sm-5').text.strip()

            if start_datetime <= current_time <= end_datetime:
                embed.add_field(name=place.text + ':green_circle: (OPEN)', value=place_hours, inline=False)
            elif is_include_closed:
                embed.add_field(name=place.text + ':red_circle: (CLOSED)', value=place_hours, inline=False)

    if not embed.fields:
        embed.add_field(name='No places are open now.', value='-')

    return embed
