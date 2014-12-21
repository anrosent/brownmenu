#!/usr/bin/env python
import sys
import urllib2
import json

from collections import defaultdict
from BeautifulSoup import BeautifulSoup as soup

RATTY_URL_BASE = "https://docs.google.com/spreadsheet/pub?hl=en_US&hl=en_US&key=0AlK5raaYNAu5dC14alJ1dk5BaW50RDhmUWpSUkR4Nnc&gid=0&output=html&widget=false&range=%s:%s"
VDUB_URL_BASE  = "https://docs.google.com/spreadsheet/pub?hl=en_US&hl=en_US&key=0AlK5raaYNAu5dGpnY2lqdFJrRGY4VWN0Yi1oUlpMbXc&gid=0&output=html&widget=false&range=%s:%s"

eateries = {'ratty', 'vdub'}
daySeq = ['sunday', 'monday','tuesday','wednesday','thursday','friday','saturday']
mealSeq = ['breakfast','lunch','dinner']
day_ranges = {'monday': {
                            'breakfast':['R2C1','R14C4'],
                            'lunch':['R2C5','R14C8'],
                            'dinner':['R2C9', 'R14C12']
                       },
             'tuesday':{
                            'breakfast':['R2C13','R14C16'],
                            'lunch':['R2C17','R14C20'],
                            'dinner':['R2C21', 'R14C24']
                       },

             'wednesday':{
                            'breakfast':['R2C25','R14C28'],
                            'lunch':['R2C29','R14C32'],
                            'dinner':['R2C33', 'R14C36']
                       },
             'thursday':{
                            'breakfast':['R2C37','R14C40'],
                            'lunch':['R2C41','R14C44'],
                            'dinner':['R2C45', 'R14C48']
                       },
             'friday':{
                            'breakfast':['R2C49','R14C52'],
                            'lunch':['R2C53','R14C56'],
                            'dinner':['R2C57', 'R14C60']
                       },
             'saturday':{
                            'breakfast':['R2C61','R14C64'],
                            'lunch':['R2C65','R14C68'],
                            'dinner':['R2C69', 'R14C72']
                       },
             'sunday':{
                            'breakfast':['R2C73','R14C76'],
                            'lunch':['R2C77','R14C80'],
                            'dinner':['R2C81', 'R14C84']
                       }
             }

def _parse_meal(eatery, html):
    if eatery == 'ratty':
        return __parse_meal_ratty(html)
    else:
        return {}

def __parse_meal_ratty(html):
    parsed = soup(html)
    table  = parsed.find('table', {'id':'tblMain'})
    rows   = table.findAll('tr')[1:]
    cols = [urllib2.unquote(col.text) for col in rows[0].findAll('td')[1:]]
    print 'Cols: ' + str(cols)
    data = {col:[] for col in cols}
    for row in rows[1:-1]:
        row_cols = row.findAll('td')[1:]
        for ix, c in enumerate(row_cols):
            if c.text:
                data[cols[ix]].append(c.text)
    data['Other'] = [col.text for col in rows[-1].findAll('td') if col.text and col.text != '.']
    return data

def _get_meal(eatery, day, meal):
    if eatery != 'ratty':
        return {}
    meal_range = day_ranges[day][meal]
    meal_url  = _get_url(eatery, meal_range)
    meal_html = _get_html(meal_url)
    meal_data = _parse_meal(eatery, meal_html)
    return meal_data

def get_gen(eateries, days, meals):
    data = defaultdict(lambda : defaultdict(dict))
    for eatery in eateries:
        for day in days:
            for meal in meals:
                data[eatery][day][meal] = _get_meal(eatery, day, meal)
    return data

def _get_url(eatery, meal_range):
    if eatery == 'ratty':
        return RATTY_URL_BASE % tuple(meal_range)
    else:
        raise NotImplementedError

def _get_html(meal_url):
    req = urllib2.Request(meal_url)
    read = urllib2.urlopen(req).read()
    return read

