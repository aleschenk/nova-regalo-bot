from bot import bot
from recommendation import RecommendationService

def main():
    RecommendationService().start()
    bot.start()

if __name__ == '__main__':
    main()