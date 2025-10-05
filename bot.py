import requests
import telebot
import re

#@diwazz
BOT_TOKEN = '8374941881:AAGI8cU4W85SEN0WbEvg_eTZiGZdvXAmVCk' #here bot token nigga
# Apne dono API ke URLs yahan daalein
STRIPE_API_URL = "https://stripe-by-diwazz.onrender.com/check" 
BRAINTREE_API_URL = "https://b3-auth-xebec.onrender.com" # Isko apne naye API URL se badalna

bot = telebot.TeleBot(BOT_TOKEN)

#
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """<b>Welcome! I am a Nigaa Gateway Bot.</b>

Use <code>/st CC|MM|YY|CVV</code> for Stripe Auth.
Use <code>/bt CC|MM|YY|CVV</code> for Braintree Auth.""", parse_mode='HTML')

#@diwazz
def process_card_check(message, api_url, gateway_name):
    try:
        command_text = message.text.split(' ', 1)[1]
    except IndexError:
        bot.reply_to(message, f"<b>Please provide card details for {gateway_name}.</b>", parse_mode='HTML')
        return

    match = re.match(r'(\d{16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})', command_text)
    if not match:
        bot.reply_to(message, "<b>Invalid format. Use:</b> <code>CC|MM|YY|CVV</code>", parse_mode='HTML')
        return

    full_cc_string = match.group(0)
    sent_message = bot.reply_to(message, f"<i>Calling {gateway_name} API, please wait...</i>", parse_mode='HTML')

    try:
        api_params = {'card': full_cc_string}
        api_response = requests.get(api_url, params=api_params, timeout=60)
        api_response.raise_for_status()
        result = api_response.json()

        status = result.get('status', 'Declined')
        response_message = result.get('response', 'No response from API.')
        bin_info = result.get('bin_info', {})
        
        brand = bin_info.get('brand', 'Unknown')
        card_type = bin_info.get('type', 'Unknown')
        country = bin_info.get('country', 'Unknown')
        country_flag = bin_info.get('country_flag', '')
        bank = bin_info.get('bank', 'Unknown')

        #@diwazz
        if status == "Approved":
            final_message = f"""<b>𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅ ({gateway_name})</b>

<b>𝗖𝗮𝗿𝗱:</b> <code>{full_cc_string}</code>
<b>𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞:</b> {response_message}

<b>𝗜𝗻𝗳𝗼:</b> {brand} - {card_type}
<b>𝐈𝐬𝐬𝐮𝐞𝐫:</b> {bank}
<b>𝐂𝐨𝐮𝐧𝐭𝐫𝐲:</b> {country} {country_flag}"""
        else:
            final_message = f"""<b>𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌ ({gateway_name})</b>

<b>𝗖𝗮𝗿𝗱:</b> <code>{full_cc_string}</code>
<b>𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞:</b> {response_message}

<b>𝗜𝗻𝗳𝗼:</b> {brand} - {card_type}
<b>𝐈𝐬𝐬𝐮𝐞𝐫:</b> {bank}
<b>𝐂𝐨𝐮𝐧𝐭𝐫𝐲:</b> {country} {country_flag}"""

    except requests.exceptions.RequestException as e:
        final_message = f"<b>Error:</b> Could not connect to the {gateway_name} API. <code>{e}</code>"
    except Exception as e:
        final_message = f"<b>An unexpected error occurred:</b> <code>{e}</code>"

    bot.edit_message_text(final_message, chat_id=message.chat.id, message_id=sent_message.message_id, parse_mode='HTML')

#@diwazz
@bot.message_handler(commands=['st'])
def handle_st_command(message):
    process_card_check(message, STRIPE_API_URL, "Stripe")

@bot.message_handler(commands=['bt'])
def handle_bt_command(message):
    process_card_check(message, BRAINTREE_API_URL, "Braintree")

#starting our nigga bot @diwazz
print("Nigaa Bot is running My Owner @diwazz 🤗")
bot.polling()
