from loguru import logger
from util import util
import traceback
import datetime
import subprocess
import os

WEBM_RESOURCES_DIR = "resources/webm_conversions/"


def handle(update, context):

    try:

        util.log_chat("webm", update)

        document = update.message.document

        # return if the document isn't a webm
        if not document.file_name.endswith(".webm"):
            return

        try:

            # Count time taken for webm conversion
            time_start = datetime.datetime.now()

            # Download the webm file
            logger.info(
                "[webm] Starting webm download - " + str(document.file_id) + ".webm"
            )
            webm_file = context.bot.get_file(document.file_id)
            webm_file.download(WEBM_RESOURCES_DIR + str(document.file_id) + ".webm")
            logger.info(
                "[webm] Finished downloading webm - " + str(document.file_id) + ".webm"
            )

            # Webm to mp4 conversion via ffmpeg
            logger.info(
                "[webm] Starting webm conversion with ffmpeg - "
                + str(document.file_id)
                + ".webm"
            )
            ffmpeg_conversion = subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    WEBM_RESOURCES_DIR + str(document.file_id) + ".webm",
                    WEBM_RESOURCES_DIR + str(document.file_id) + ".mp4",
                ]
            )

            if ffmpeg_conversion.returncode != 0:
                logger.error(
                    "[webm] ffmpeg conversion had a non-zero return code! webm={} ffmpeg_conversion={}",
                    str(document.file_id),
                    ffmpeg_conversion,
                )
                update.message.reply_text(
                    text="(｡•́︿•̀｡) webm conversion failed (｡•́︿•̀｡)"
                )
                return

            # Calculate time taken to convert
            time_end = datetime.datetime.now()
            diff = time_end - time_start
            pretty_diff = util.pretty_time_delta(diff.seconds)

            logger.info(
                "[webm] ffmpeg conversion complete! webm={} time_taken={}",
                str(document.file_id),
                pretty_diff,
            )

            original_sender = util.extract_pretty_name_from_tg_user(
                update.message.from_user
            )

            caption = random_webm_caption(original_sender, pretty_diff)

            logger.info(
                "[webm] sending converted video webm={} caption={}",
                str(document.file_id),
                caption,
            )
            context.bot.send_video(
                chat_id=update.message.chat_id,
                video=open(WEBM_RESOURCES_DIR + str(document.file_id) + ".mp4", "rb"),
                timeout=5000,
                caption=caption,
            )

            delete_file(WEBM_RESOURCES_DIR + str(document.file_id) + ".webm")
            delete_file(WEBM_RESOURCES_DIR + str(document.file_id) + ".mp4")

        except Exception as e:
            logger.error(
                "Caught Error in webm.conversion - {} \n {}", e, traceback.format_exc(),
            )

    except Exception as e:
        logger.error(
            "Caught Error in webm.handle - {} \n {}", e, traceback.format_exc(),
        )


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)
        logger.info("[webm] deleted file! - {}", file)
    else:
        logger.warn("[webm] file does not exist - {}", file)


def random_webm_caption(original_sender, pretty_diff):

    captions = [
        "{} converted your webm to mp4 in {}".format(original_sender, pretty_diff),
        "{} bhaak bsdk webm post karte hai bc... {} lage convert karne mein".format(
            original_sender, pretty_diff
        ),
        "haaaaat {}... kal se webm cancel! {} lage convert karne mein".format(
            original_sender, pretty_diff
        ),
    ]

    random_caption = util.choose_random_element_from_list(captions)

    return random_caption
