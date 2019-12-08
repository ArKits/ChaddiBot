#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import pytz
from datetime import datetime, date, timezone
from util import bakchod_util
from util import chaddi_util

# Enable logging
logger = logging.getLogger(__name__)


# Handle /timesince
def handle(bot, update):
    
    # Update Bakchod pickle
    # bakchod_util.bakchod_updater(update.message.from_user)

    logger.info("/superpower: Handling /superpower request from user '%s' in group '%s'", update.message.from_user['username'], update.message.chat.title)
    response = superpower_countdown_calc()
    logger.info("/superpower: Returing response=%s", response)
    update.message.reply_text(response)


# Calculates timedelta between current time and Dec 31st 2019 IST.
def superpower_countdown_calc():

    ist = pytz.timezone("Asia/Kolkata")

    # Current time in IST
    now = datetime.now(ist)
    
    # Dec 31 in IST
    superpower_day = datetime(year = 2020, month = 1, day = 1, hour = 0, minute = 0, second = 0)
    superpower_day = ist.localize(superpower_day)
    
    # Get timedelta
    td = superpower_day - now

    if td.total_seconds() > 0:
        response = "🇮🇳🙏 Time Until Super Power™️: " + chaddi_util.pretty_time_delta(td.total_seconds()) + " 🙏🇮🇳"
    else:
        td = now - superpower_day
        response = "🇮🇳🙏 WE INVANT SUPER POWER 🙏🇮🇳 \n Time Since: " + chaddi_util.pretty_time_delta(td.total_seconds())

    return(response)
