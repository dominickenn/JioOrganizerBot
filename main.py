from frontend.bot import Bot

def main():
    TOKEN = 'FILL IN WITH TOKEN ID FROM BOTFATHER'
    bot = Bot(TOKEN)
    bot.start()

if __name__ == '__main__':
    main()