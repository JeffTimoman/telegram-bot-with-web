from typing import Final, List, Optional
from telebot import TeleBot

from sqlalchemy import create_engine, String, Column, Integer, ForeignKey, Date
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from pytz import timezone
class Config():
    def __init__(self):
        self.DB_PLATFORM = 'mysql+pymysql'
        # self.DB_PLATFORM = 'postgresql
        self.DB_SERVER = 'localhost'
        self.DB_NAME = 'telebot'
        self.DB_USERNAME = 'root'
        self.DB_PASSWORD = ''
        self.DB_PORT = '3306'
        
        self.TIMEZONE = 'Asia/Jakarta'
        
        self.SECRET_KEY = "secret-key"
        self.BROADCAST_KEY = "broadcast-key"

        self.SQLALCHEMY_DATABASE_URI = f'{self.DB_PLATFORM}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = True
        

class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

class Command(Base):
    __tablename__ = 'command'
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    keyword: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    message: Mapped[str] = mapped_column(String(1000), nullable=False)
    expired_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    
    def __repr__(self):
        return f"Command('{self.message}', '{self.expired_date}')"

class ConnectedUser(Base):
    __tablename__ = 'connected_user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(String(100), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(100))
    date_connected: Mapped[str] = mapped_column(String(100), nullable=False, default = timezone(Config().TIMEZONE).localize(datetime.now()).strftime('%Y-%m-%d %H:%M:%S'))
    
    def __repr__(self):
        return f"ConnectedUser('{self.user_id}', '{self.chat_id}')"

class WebVariables(Base):
    __tablename__ = 'web_variables'
    name: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str] = mapped_column(String(1000))
    
    def __repr__(self):
        return f"WebVariables('{self.name}', '{self.value}')"

from sqlalchemy import create_engine, select
engine = create_engine(Config().SQLALCHEMY_DATABASE_URI, echo=True)
stmt = select(Command).where(Command.keyword == 'start')

Session = sessionmaker(bind=engine)
# session = Session()
# command = session.query(Command).first()
# print(command.message)

key = '6822085521:AAF_vz5Ag8EzU2zuyREHjdSWt8OQUrrJr9o'

bot = TeleBot(key)


@bot.message_handler(commands=['start'])
def start(message):
    session = Session()
    command = session.query(Command).filter(Command.keyword == 'start').first()
    bot.send_message(message.chat.id, command.message)
    
    

@bot.message_handler(regexp=r'broadcast (.*)')
def broadcast(message):
    
    session = Session()
    if not session.query(ConnectedUser).filter(ConnectedUser.chat_id == message.chat.id).first():
        session.add(ConnectedUser(chat_id=message.chat.id, username=message.chat.username))
        session.commit()
    
    word = list(map(str, message.text.lower().split(' ')[1:]))
    print(word)
    
    if len(word) != 2:
        bot.send_message(message.chat.id, 'Invalid command structure to use broadcast. \nTry typing /broadcast <command> broadcast_key')
        return
    
    if word[0][0] == '/':
        word[0] = word[0][1:]
    print(word)
    
    broadcast_key = session.query(WebVariables).filter(WebVariables.name == 'BROADCAST_KEY').first()
    if not broadcast_key:
        bot.send_message(message.chat.id, 'Broadcast key not found.')
        return
    
    if word[1] != broadcast_key.value:
        bot.send_message(message.chat.id, 'Invalid broadcast key. \nTry typing /broadcast <command> broadcast_key')
        return
    
    command = session.query(Command).filter(Command.keyword == word[0]).first()
    
    if not command:
        bot.send_message(message.chat.id, 'Invalid command structure to use broadcast. \nTry typing broadcast <command>.')
        return
    
    if command.expired_date and command.expired_date.strftime('%Y-%m-%d') < timezone(Config().TIMEZONE).localize(datetime.now()).strftime('%Y-%m-%d'):
        bot.send_message(message.chat.id, 'The command has expired.')
        return
    
    users = session.query(ConnectedUser).all()
    for user in users:
        bot.send_message(user.chat_id, command.message)    
        
    session.close()

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    session = Session()
    user_id = message.chat.id
    check = session.query(ConnectedUser).filter(ConnectedUser.chat_id == user_id).first()
    command_name = message.text.lower()
    print(command_name)
    if command_name[0] == '/':
        command_name = command_name[1:]
    
    if not check:
        session.add(ConnectedUser(chat_id=user_id, username=message.chat.username))
        session.commit()
        
    now = timezone(Config().TIMEZONE).localize(datetime.now()).strftime('%Y-%m-%d')
    
    
    
    # fetch the suitable command that hasn't expired yet
    query = session.query(Command).filter(Command.keyword == command_name).first()
    print(command_name)
    
    if query and query.expired_date and query.expired_date.strftime('%Y-%m-%d') < now:
        print('thi')
        query = None
    
    if query:
        bot.send_message(message.chat.id, query.message)
    else:
        error_msg = session.query(Command).filter(Command.keyword == 'error').first()
        bot.send_message(message.chat.id, f"{error_msg.message}")
        
    session.close()

bot.polling(none_stop=True)
