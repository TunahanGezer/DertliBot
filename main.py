import os
import discord
import requests
import json
import random
import asyncio

sad_words=["sad","depressed","unhappy","angry"]
start_enco=[
  "Cheer up!",
  "Hang in.",
  "You are great person / bot!",
]

intents = discord.Intents.default()
intents.message_content=True
intents.members = True
client = discord.Client(intents=intents)

desc_sozluk = {
    "clear sky": "Açık",
    "few clouds": "Az bulutlu",
    "scattered clouds": "Parçalı bulutlu",
    "broken clouds": "Bulutlu",
    "overcast clouds": "Kapalı",
    "mist": "Sisli",
    "light rain": "Hafif yağmurlu",
    "moderate rain": "Orta şiddetli yağmurlu",
    "heavy intensity rain": "Şiddetli yağmurlu",
    "very heavy rain": "Çok şiddetli yağmurlu",
    "extreme rain": "Şiddetli yağmurlu",
    "freezing rain": "Dondurucu yağmurlu",
    "light snow": "Hafif kar yağışlı",
    "heavy snow": "Yoğun kar yağışlı",
    "sleet": "Sulu kar",
    "shower rain": "Sağanak yağmurlu",
    "thunderstorm": "Gök gürültülü fırtınalı",
    "haze": "Puslu"
}

def get_Hava_Key():
    my_secret3 = os.environ['Hava_Key']
    return my_secret3

def get_weather(city_name):
    hava_key = get_Hava_Key()
    hava_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={hava_key}&units=metric"
    response = requests.get(hava_url)
    data = response.json()
    temperature = data["main"]["temp"]
    description_eng = data["weather"][0]["description"]
    description_tr = desc_sozluk.get(description_eng, "Atama")
    return description_tr,temperature

def get_news_headlines():
  my_secret2 = os.environ['News_Key']
  News_URL=f"https://newsapi.org/v2/top-headlines?country=tr&apiKey={my_secret2}"
  response=requests.get(News_URL)
  data = response.json()
  headlines = [news['title'] for news in data['articles']]
  return headlines

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
@client.event
async def on_connect():
  print("Connected!")
@client.event
async def on_member_join(member):
  print(f"Hoşgeldin{member}")
@client.event
async def on_member_remove(member):
  print(f"Gule Gule{member}!")
@client.event
async def on_member_uptade(before,after):
  if before.roles!=after.roles:
    print(f"{after.name} adlı kullanicinin rolü değişti")
  if before.displayname!=after.displayname:
    print(f"{after.name} adlı kullanicinin ismi değişti")
  if before.flags!=after.flags:
    print(f"{after.name} kullanicin bayragi degisti")
  if before.avatar!=after.avatar:
    print(f"{after.name} kullanicinin avatari degisti")
    
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg=message.content
  
  if message.content=="$Admin":
    await message.channel.send("Bu serverin admini Paşa Tunahandır!")
    
  if message.content=="$Hello":
    await message.channel.send("Hoşgeldin gral!")
    
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(start_enco))
    
  if message.content=="$Roll":
    number=random.randint(1,6)
    await message.channel.send(f"Gelen sayi: {number} kardeşim hadi isine")
    
  if message.content =="$News":
    headlines = get_news_headlines()
    news_string = '\n'.join(headlines)
    await message.channel.send('İşte güncel haber başlıkları:\n' + news_string)

  if message.content == "$Weather":
    await message.channel.send("Şehir adını girin:")
        
    def check(m):
      return m.author == message.author and m.channel == message.channel
        
    try:
      city_message = await client.wait_for('message', check=check, timeout=3)
      city_name = city_message.content
            
      weather_description,temperature = get_weather(city_name)
      await message.channel.send(f"{city_name} şehrinin hava durumu:  {weather_description}\nSıcaklık değeri: {temperature}°C'dir")
            
    except asyncio.TimeoutError:
      await message.channel.send("Lütfen tekrar yazın zaman aşımına uğradı! İşlem iptal edildi.")
            

my_secret = os.environ['TOKEN']
client.run(my_secret)