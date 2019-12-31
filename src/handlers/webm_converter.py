#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from util import bakchod_util
from util import chaddi_util
import ffmpeg
import datetime
import os

# Enable logging
logger = logging.getLogger(__name__)


# Convert Webm to mp4
def handle(bot, update):
    
    logger.info("webm: Handling webm request from user '%s' in group '%s'", update.message.from_user['username'], update.message.chat.title)

    document = update.message.document

    if document.file_name.endswith(".webm"):

        logger.info("webm: Got a webm - " + str(document.file_id))

        conversion_inform_message = update.message.reply_text(text="ヾ(＾-＾)ノ starting webm conversion!")
        conversion_inform_message = conversion_inform_message.result()

        time_before = datetime.datetime.now()

        try:
            # Download the webm file
            webm_file = bot.get_file(document.file_id)
            webm_file.download('resources/' + str(document.file_id) + '.webm')
            logger.info("webm: Downloaded webm - " + str(document.file_id) + '.webm')

            stream = ffmpeg.input('resources/' + str(document.file_id) + '.webm')
            video = stream.video.filter('crop', 'iw-mod(iw,2)', 'ih-mod(ih,2)')

            # Check if webm file has audio
            probe = ffmpeg.probe('resources/' + str(document.file_id) + '.webm')
            has_audio = check_for_audio(probe)
            logger.info("webm: has_audio=%s", has_audio)

            if has_audio:
                audio = stream.audio
                joined = ffmpeg.concat(video, audio, v=1, a=1).node
                output = ffmpeg.output(joined[0], joined[1], 'resources/' + str(document.file_id) + '.mp4', vcodec='libx265', crf=28, acodec='libvorbis')
                output = ffmpeg.overwrite_output(output)
                ffmpeg.run(output)
            else:
                output = ffmpeg.output(video, 'resources/' + str(document.file_id) + '.mp4', vcodec='libx265', crf=28, acodec='libvorbis')
                output = ffmpeg.overwrite_output(output)
                ffmpeg.run(output)

            # Calculate time taken
            time_after = datetime.datetime.now()
            difference = time_after - time_before
            pretty_time_delta = chaddi_util.pretty_time_delta(difference.seconds)
            logger.info("webm: Finished converting webm=%s , timeTaken=%s", str(document.file_id), pretty_time_delta)

            og_from = update.message.from_user
            if(og_from['username']):
                og_sender = "@" + og_from['username']
            elif(og_from['firstname']):
                og_sender = og_from['firstname']

            caption = og_sender + " converted your WebM to MP4 in " + str(pretty_time_delta) + " \n (＾－＾)"

            bot.send_video(
                chat_id=update.message.chat_id,
                video=open('resources/' + str(document.file_id) + '.mp4', 'rb'),
                timeout=5000,
                caption=caption
            )

            try:
                bot.delete_message(
                    chat_id=update.message.chat_id,
                    message_id=conversion_inform_message.message_id
                )
                bot.delete_message(
                    chat_id=update.message.chat_id,
                    message_id=update.message.message_id
                )
            except:
                logger.warn("webm: caught error when trying to delete")

        except Exception as e:
            
            logger.error("webm: Caught error in webm_converter - %s", e)

            try:
                bot.delete_message(
                    chat_id=update.message.chat_id,
                    message_id=conversion_inform_message.message_id
                )
            except Exception as e:
                logger.warn("webm: caught error when trying to delete")

            response = "Error occured during WebM conversion - `" + str(e) + "`"
            update.message.reply_text(
                text=response, 
                parse_mode=ParseMode.MARKDOWN
            )

        clean_up('resources/' + str(document.file_id) + '.webm')
        clean_up('resources/' + str(document.file_id) + '.mp4')


def clean_up(file):
    if os.path.exists(file):
        os.remove(file)
        logger.info("webm: cleaned up - %s", file)
    else:
        logger.warn("webm: file does not exist - %s", file)


def check_for_audio(probe):

    has_audio = False

    for stream in probe['streams']:
        if stream['codec_type'] == 'audio':
            has_audio = True

    return has_audio