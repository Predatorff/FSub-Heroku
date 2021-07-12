import time
import logging
from config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              cb.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(cb.id, text="**❗ നിങ്ങൾ ഇപ്പോഴും ചാനലിൽ ജോയിൻ ചെയ്തിട്ടില്ല.ജോയിൻ ചെയ്‌ത ശേഷം '🔉 UnMute Me 🔊' ബട്ടൺ വീണ്ടും അമർത്തുക.**", show_alert=True)
      else:
        client.answer_callback_query(cb.id, text="⚠ നിങ്ങളെ വേറെ എന്തിനോ Admins👥 Mute🔇 ചെയ്തതാണ്.", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{cb.from_user.mention} എന്ന ഇയാൾ സ്വയം UnMute ചെയ്യാൻ ശ്രമിക്കുന്നു പക്ഷെ എനിക്കെ ഇയാളെ UnMute ചെയ്യാൻ കഴിയില്ല കാരണം ഞാൻ ഈ ഗ്രൂപ്പിൽ Admin അല്ല എന്നെ ഒരു പ്രാവശ്യവും കൂടെ Admin ആയി ഗ്രൂപ്പിൽ ആഡ് ചെയ്യുക ❗.**\nതൽകാലം ഞാൻ ഈ ഗ്രൂപ്പ് വിട്ട് പോകുന്നു,\nബൈ 👋")
        client.leave_chat(chat_id)
      else:
        client.answer_callback_query(cb.id, text="⚠️ Warning : വെറുതെ ഈ ബട്ടൺ ഞെക്കരുത്❗", show_alert=True)



@Client.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_photo(
             photo="https://telegra.ph/file/3737329f8b82b6e72e0fe.jpg",
             caption = "**ഹായ് {},നിങ്ങൾ ഇപ്പോഴും ചാനലിൽ ജോയിൻ ചെയ്തിട്ടില്ല ജോയിൻ ചെയ്യാൻ [ഇവിടെ ക്ലിക്ക് ചെയുക](https://t.me/{})\nശേഷം താഴെയുള്ള    '🔉 UnMute Me 🔊'  ബട്ടൺ അമർത്തുക\n\n⭕️NB:ഈ മെസ്സേജ് വേഗം ഡിലീറ്റ് ആകും അതുകൊണ്ട് ഇപ്പോൾ തന്നെ ജോയിൻ ചെയ്യുക.**".format(message.from_user.mention, channel, channel),
             reply_markup=InlineKeyboardMarkup(
                 [[InlineKeyboardButton("🔉 UnMute Me 🔊", callback_data="onUnMuteRequest")]], 
                 [[InlineKeyboardButton("💬 Subscribe", url=url)]]
             )
          )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **⚠ ഞാൻ ഈ ഗ്രൂപ്പിൽ അഡ്മിൻ അല്ല എന്നെ ഒരു പ്രാവശ്യവും കൂടെ Admin ആയി ഗ്രൂപ്പിൽ ആഡ് ചെയ്യുക.\nതൽകാലം ഞാൻ ഈ ഗ്രൂപ്പ് വിട്ട് പോകുന്നു,\nബൈ 👋")
          client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"⚠ ഞാൻ ഈ @{channel}**\nചാനലിൽ അഡ്മിൻ അല്ല എന്നെ Admin ആയി ചാനലിൽ ആഡ് ചെയ്യുക.\nതൽകാലം ഞാൻ ഈ ഗ്രൂപ്പ് വിട്ട് പോകുന്നു,\nബൈ 👋")
        client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def fsub(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status is "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        message.reply_text("❌ **Force Subscribe ഒഴിവാക്കിയിരിക്കുന്നു.**")
      elif input_str.lower() in ('clear'):
        sent_message = message.reply_text('❌ **ഞാൻ Mute ചെയ്‌ത എല്ലാവരെയും UnMute ചെയ്യുന്നു........**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **ഞാൻ Mute ചെയ്‌ത എല്ലാവരെയും UnMute ചെയ്‌തിരിക്കുന്നു.**')
        except ChatAdminRequired:
          sent_message.edit('❗ **ഞാൻ‌ ഈ ചാറ്റിൽ‌ ഒരു അഡ്‌മിൻ‌ അല്ല.**\nഎനിക്ക് അംഗങ്ങളെ UnMute ചെയ്യാൻ കഴിയില്ല കാരണം ഞാൻ ഈ ചാറ്റിലെ Admin അല്ല എന്നെ Ban Permission തന്ന് അഡ്മിൻ ആക്കുക')
      else:
        try:
          client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          message.reply_text(f"✅ **Force Subscribe പ്രവർത്തനക്ഷമമാക്കി**\n__Force Subscribe is പ്രവർത്തനക്ഷമമാക്കിയിരിക്കുന്നു,ഈ ഗ്രൂപ്പിൽ മെസ്സേജ് അയക്കണമെങ്കിൽ എല്ലാ ഗ്രൂപ്പ് അംഗങ്ങളും ഈ [ചാനൽ](https://t.me/{input_str}) സബ്സ്ക്രൈബ് ചെയ്യണം ❗", disable_web_page_preview=True)
        except UserNotParticipant:
          message.reply_text(f"❗ **Not an Admin in the Channel**\n__I am not an admin in the [channel](https://t.me/{input_str}). Add me as a admin in order to enable ForceSubscribe.__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          message.reply_text(f"❗ **Invalid Channel Username.**")
        except Exception as err:
          message.reply_text(f"❗ **ERROR:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        message.reply_text(f"✅ **Force Subscribe is enabled in this chat.**\n__For this [Channel](https://t.me/{sql.fs_settings(chat_id).channel})__", disable_web_page_preview=True)
      else:
        message.reply_text("❌ **Force Subscribe is disabled in this chat.**")
  else:
      message.reply_text("❗ **Group Creator Required**\n__You have to be the group creator to do that.__")
