from frontend.bot import Bot
from backend.eventlist import EventList

def main():
    TOKEN = '5100503329:AAEd2hcnal5qbvYL0BvnzCEEL-yTJebJfY0'
    eventlist = EventList()
    bot = Bot(TOKEN, eventlist)
    bot.start()

if __name__ == '__main__':
    main()