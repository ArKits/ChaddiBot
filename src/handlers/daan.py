from loguru import logger
from util import util
from db import dao
from telegram import ParseMode
from models.bakchod import Bakchod
import shortuuid
import datetime
import traceback


def handle(update, context):

    try:

        util.log_chat("daan", update)

        # Extract query...
        query = update.message.text
        query = query.split(" ")

        if len(query) < 2:
            update.message.reply_text(
                text="Haat chutiya! Syntax is `/daan @username 786`",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        # Extract Sender by ID
        sender = dao.get_bakchod_by_id(update.message.from_user["id"])
        if sender is None:
            sender = Bakchod.fromUpdate(update)
            dao.insert_bakchod(sender)

        # Extract Receiver
        receiver = None

        if update.message.reply_to_message:
            # Request is a reply to message... Extract receiver from ID
            receiver = dao.get_bakchod_by_id(
                update.message.reply_to_message.from_user["id"]
            )

            # Donation can be the rest of the message
            donation = query[1:]

        else:
            # Request includes the username as a mention
            if update.message.entities:
                for entity in update.message.entities:
                    if entity.type == "text_mention" and entity.user is not None:
                        receiver = dao.get_bakchod_by_id(entity.user.id)

            # Last attempt... try to lookup username in DB
            if receiver is None:

                receiver_username = query[1]

                # Remove the "@" prefix
                if receiver_username.startswith("@"):
                    receiver_username = receiver_username[1:]

                receiver = dao.get_bakchod_by_username(receiver_username)

            # Donation can be the rest of the message
            donation = query[2:]

        # Handle if receiver could be extracted
        if receiver is None:
            if receiver_username:
                update.message.reply_text(receiver_username + "??? Who dat???")
                return
            else:
                update.message.reply_text("Kisko daan do be????")
                return

        # Parse Daan amount
        try:
            daan = float("".join(donation))
            daan = round(daan, 2)
            daan = abs(daan)
        except Exception as e:
            update.message.reply_text("Kitna ₹okda be???")
            return

        logger.info(
            "[daan] sender={} receiver={} daan={}",
            util.extract_pretty_name_from_bakchod(sender),
            util.extract_pretty_name_from_bakchod(receiver),
            daan,
        )

        if (sender.rokda - daan) < 0:
            update.message.reply_text("Gareeb saale! You don't have enough ₹okda!")
            return

        if sender.id == receiver.id:
            file_id = "CAADAwADrQADnozgCI_qxocBgD_OFgQ"
            sticker_to_send = file_id
            update.message.reply_sticker(sticker=sticker_to_send)
            return

        # Commit Daan transaction to DB
        sender.rokda = sender.rokda - daan
        dao.insert_bakchod(sender)

        receiver.rokda = receiver.rokda + daan
        dao.insert_bakchod(receiver)

        daan_id = shortuuid.uuid()

        dao.insert_daan(
            daan_id, sender.id, receiver.id, daan, str(datetime.datetime.now())
        )

        update.message.reply_text(
            text="{} gave {} 🤲 a daan of {} ₹okda! 🎉 \n Daan ID - <code>{}</code>".format(
                util.extract_pretty_name_from_bakchod(sender),
                util.extract_pretty_name_from_bakchod(receiver),
                daan,
                daan_id,
            ),
            parse_mode=ParseMode.HTML,
        )
        return

    except Exception as e:
        logger.error(
            "Caught Error in daan.handle - {} \n {}", e, traceback.format_exc(),
        )
