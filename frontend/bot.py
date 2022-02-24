from distutils.cmd import Command
from telegram.ext import Updater
from handler.handler import Handler

'''
Reference for converstaionhandler: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py
Design: https://lucid.app/lucidchart/6330a386-4d09-4764-83df-8f9ae152d38d/edit?invitationId=inv_fe30ac88-b3b8-4bda-b97c-3e2416cac9f5
'''

class Bot:

    def __init__(self, TOKEN) -> None:
        self.TOKEN = TOKEN

    def start(self) -> None:
        '''
        Starts the bot
        -   Create updater with bot's token [Updater receives updates from bot]
        -   Create dispatcher [Dispatcher sends commands to bot]
        -   Create handlers to attach to dispatcher
        '''
        updater = Updater(token=self.TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        handler = Handler()
        handler.eventManager.createEvent(-678200997, "Event 1")
        handler.eventManager.createEvent(-678200997, "Event 2")
        handler.eventManager.createEvent(-678200997, "Event 3")
        handler.eventManager.createEvent(-678200997, "Event 4")
        handler.eventManager.createEvent(-678200997, "Event 6")
        handler.eventManager.createEvent(-678200997, "Event 7")
        handler.eventManager.createEvent(-678200997, "Event 8")
        handler.eventManager.createEvent(-678200997, "Event 9")
        handler.eventManager.createEvent(-678200997, "Event 10")
        dispatcher.add_handler(handler.getHandler())

        #starts the bot
        updater.start_polling()
        #run bot until Ctrl + C
        updater.idle()