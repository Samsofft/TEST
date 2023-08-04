from pyrogram import Client ,filters
from pyrogram.types import Message
import Navigation 

alternative_garage_session = 'BAF_FiQAF3DUSR0_ZmAJwfEdiC8M0pdRmdkZEztwa8DKIacnKsZ2cYz0Nf5DVlkkM6NNymu5f1CJB5QSBXaYmM2Aim7E_GAXRRU9RimhITYSDgwAISwLRx4GynCIbhK_nKZsebBCoRlxLKBFe7V1oZ0B_jpVv16M4jufu7H3yAQN2_LTfOsaRjPZoPeqGJGMvcmZg2iALeazVIKNBPBxYkBgCTc_PRGp8pMRmxcmjKcBhpqQEsB_hm88mf5abkAogVH18TIa2quAHrzJ5sIkJoC8dIh5OPf_AZzCTze2Jgi_t2fAboKLhxvZObPFAR1y_S7U0872lDwxv3MFQxWV-z_9ogomyAAAAAFdcPJ3AQ'
Appointmen_test_session='BAF_FiQAM3QZB4xD8LWLEHwRAWxDCDww_ce6Ab1TiIvxBM3Y50WHWk47aMr8Nyb3acSaocn-nog7wDyj6qSvaRtwbrsMyQ9mFm_hVG4srlIRuzqdxFYNqDdK3I9NAC5caPIlAPyJbGlE8Wbd_13mcmJVtMsS18blYj6U0ql-jx3-nllVi5yz-dQqlzsEI4nYGZPNwl3cLK2q51nbG_hH_QP8WoKnDWVxvl4AEBROqTSX7ErrVyxXwBHnsdIlPS3pPu9TuliEchJUjPsDq-sKDQWxKtzIgFlwH5K7mzgntNd3HPPe-yEBUQnkVfSSnngtLJoM5ejNCdkj2usHqSNdr0bCW8ZAOwAAAAF5PUItAQ'
bot = Client("alternative_garage",session_string=Appointmen_test_session)    # connecting to the Telegram

@bot.on_message(filters.media) # wait receiving media file from telegram
async def media_handler(client:Client,message:Message):
    await Navigation.media_handler(client,message) # Handle the media

@bot.on_message() # wait receiving a message from telegram
async def message_handler(client:Client,message:Message): 
    await Navigation.message_handler(client,message) # Handle the message

@bot.on_callback_query()  # wait receiving query from telegram InlineButtons
async def callback_query_handler(client:Client,callback_query):
    await Navigation.callback_query_handler(client,callback_query) # Handle the query

print ('bot Started ...')
bot.run() # run the bot
