#!/usr/bin/env python
import datetime
import json

from collections import defaultdict
from flask import Flask
from scrape import get_gen, eateries, daySeq, mealSeq

app = Flask(__name__)
ERROR =  {'status': 'error'}

OK = lambda d: {'status': 'ok', 'result': d}

def format_response(data):
    return json.dumps(OK(data), sort_keys=True, indent=2)

# We'll store everything here forever
g_cache = defaultdict(dict)

##########################################################################

@app.route('/q/<day>/<eatery>/<meal>')
def get_day_meal(day=None, eatery=None, meal=None):
    v_days, v_eateries, v_meals = validate_day(day), validate_eatery(eatery), validate_meal(meal)
    if v_days and v_eateries and v_meals:

        # If we don't have the week cached
        if cur_week() not in g_cache:
            # Get all data for week
            data = get_gen(eateries, daySeq, mealSeq)

            # Cache all data for week
            g_cache[cur_week()] = data

        # Pick out parts requested
        resp = get_cached(v_eateries, v_days, v_meals)

        # Send
        return format_response(resp)
    else:
        return json.dumps(ERROR)

@app.route('/now')
def get_now():
    cur_day, cur_meal = get_cur_day_meal()
    return get_day_meal(str(cur_day), 'all', str(cur_meal))


##########################################################################

def is_cur_week_cached():
    return cur_week() in g_cache

#FIXME: actually cur_day
def cur_week():
    return datetime.datetime.now().strftime("%m/%d/%Y")

def get_cached(v_eateries, v_days, v_meals):
    return get_from_all(g_cache[cur_week()], v_eateries, v_days, v_meals)

def get_from_all(alldata, v_eateries, v_days, v_meals):
    data = defaultdict(lambda: defaultdict(dict))
    for eatery in v_eateries:
        for day in v_days:
            for meal in v_meals:
                data[eatery][day][meal] = alldata[eatery][day][meal]
    return data

##########################################################################

def validate_day(day):
    return validate_gen(day, daySeq)

def validate_meal(meal):
    return validate_gen(meal, mealSeq)

def validate_eatery(eatery):
    return validate_gen(eatery, eateries)

def validate_gen(var, allvars):
    parts = var.split(',')
    if not parts:
        return []
    if all(part in allvars for part in parts):
        return parts
    if len(parts) == 1 and parts[0] == 'all':
        return allvars
    return False

def get_cur_day_meal():
    from datetime import datetime
    now = datetime.now()
    cur_day = daySeq[now.weekday()]
    if now.hour < 11:
        cur_meal = 'breakfast'
    elif now.hour < 16:
        cur_meal = 'lunch'
    else:
        cur_meal = 'dinner'
    return cur_day, cur_meal

##########################################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0')

