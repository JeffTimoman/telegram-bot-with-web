import os
from random import choice
class Config():
    def __init__(self):
        self.DB_PLATFORM = 'mysql+pymysql'
        # self.DB_PLATFORM = 'postgresql
        self.DB_SERVER = 'localhost'
        self.DB_NAME = 'telebot'
        self.DB_USERNAME = 'root'
        self.DB_PASSWORD = ''
        self.DB_PORT = '3306'
        self.RESERVED_KEYWORDS = ['error', 'start']
        self.SECRET_KEY = "secret-key"
        self.TIMEZONE = 'Asia/Jakarta'

        self.SQLALCHEMY_DATABASE_URI = f'{self.DB_PLATFORM}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = True
        self.RANDOM_GREETINGS = [
            'Have a nice day!',
            "Don't forget to smile!",
            "Don't forget to pray!",
            "Always be grateful!",
            "Don't forget to drink water!",
            "Embrace the day with a positive spirit!",
            "Sending you good vibes for a wonderful day!",
            "May your day be filled with joy and laughter!",
            "Wishing you a day as bright as your smile!",
            "Start your day with a grateful heart!",
            "Radiate positivity and watch the world respond!",
            "Make today amazing – you've got this!",
            "Shine bright like the sunshine today!",
            "May your day be sprinkled with moments of happiness!",
            "Your journey today deserves a soundtrack of laughter!",
            "Let your kindness be a light for others today!",
            "Seize the day with a heart full of gratitude!",
            "Embrace each moment, for they are all precious!",
            "Don't forget to sprinkle kindness wherever you go!",
            "Today is a canvas – paint it with your favorite colors!",
            "Smile often, it suits you well!",
            "Wishing you a day filled with positive surprises!",
            "Be a rainbow in someone else's cloud today!",
            "Pause, breathe, and appreciate the beauty around you!",
            "Your positive energy is contagious – share it generously!"
        ]
