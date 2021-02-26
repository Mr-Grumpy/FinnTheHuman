# bot.py
import os, discord, random, dotenv, selenium, asyncio, youtube_dl, ffmpeg, queue, graphviz
import time;

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support.ui import WebDriverWait
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from youtube_dl import YoutubeDL
from graphviz import Digraph

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)

ydl_opts = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

@client.event
async def on_ready():    
    guilds = len(list(client.guilds))
    guild_list = '\n - '.join([guilds.name for guilds in client.guilds])
    print(client.user, 'is connected to', guilds, 'guilds:\n -', guild_list)


greetings = [
    'hi',
    'hello',
    'bonjour',
    'hola',
    'hey',
    'howdy',
    'sup',
    'welcome',
    'greetings',
    'yo',
    'yoo',
    'suh',
    'hey there',
    'hey y\'all',
    'what\'s up',
    'whats up',
    'what up',
    'wassup',
    'sup?',
    'what\'s shakin\'',
    'what\'s new?',
    'long time no see',
    'good evening',
    'good afternoon',
    'hanging',
    'how are you',
    'hallo',
    'heil'    
    ]

        
fourohfour = [
    'Nope, can\'t do that, I\'m only human.',
    'How about no?',
    'Do I look like your mother?',
    'Some peoples fucking children...',
    'FUCKING FUCKING FUCK! FUCK OFF!',
    'Just ask Kaleb to do it, he\'s simpin\'.',
    'Ugh, do I have to?',
    'Bitch, you thought, huh?',
    'That brings up a 404 error, ya dink.\n',
    'That\'s a fuCKING 404 ERROR YOU STOOPID IDGGITTT!',
    'Naaahhhhhh home\'s. I ain\'t about that, cuzz',
    'Here\'s a thought; do it yourself.',
    'If I were genie and could grant you three wishes, I still wouldn\'t do that for you.',
    'My father was a relentlessly self-improving boulangerie owner from Belgium with low-grade narcolepsy and a penchant for buggery. My mother was a 15-year-old French prostitute named Chloe, with webbed feet. My father would womanize, he would drink. He would make outrageous claims like he invented the question mark. Sometimes he would accuse chestnuts of being lazy. The sort of general malaise that only the genius possess and the insane lament. My childhood was typical. Summers in Rangoon, luge lessons. In the spring, we\'d make meat helmets. When I was insolent, I was placed in a burlap bag and beaten with reeds. Pretty standard really. At the age of 12, I received my first scribe. At the age of 14, a Zoroastrian named Vilma ritualistically shaved my testicles. There really is nothing like a shorn scrotum. It\'s breathtaking. I suggest you try it.',
    'Throw me a frickin\' bone here!',
    'Why must I be surrounded by frickin\' idiots?!',
    'Oh, Scott, that hurts daddy when you say that. Honestly.',
    'Let me tell you a little story about a man named SHH! SHH! Even before you start, that was a pre-emptive "shh!" Just know that I have a whole bag of "shh!" with your name on it.',
    'Rain check, please.',
    'Let me just check my calendar.... Yea, no. It\'s a no.',
    'But I am le tiirreeed.',
    'Nah, I\'m not feeling well.',
    'Sorry, I\'m leaving for the Peace Corps in an hour.',
    'I\'d really rather not.',
    'No thanks, I\'m driving.',
    'That\'s just not going to work for me. Sorry.',
    'I have a strict, "No deals with the Devil," policy. Sorry.',
    'Does not compute.... EEEEEEEEE',
    'That idea is not compatible with myself.',
    'I believe there\'s someone a lot more stupid who would enjoy doing that instead.',
    'I shall not.',
    'Why, HEAVEN\'S, no.',
    'Alas, such a task is no match for my incompetency.',
    'Sorry. Coffee break.',
    'Could you try asking later?',
    'Is there a polite way to say, "no?"',
    'I\'m already doing something, you ungrateful, greedy, conceited sack of shit.',
]

brooklyn = [
    'I\'m the human form of the 💯 emoji.',
    'Bingpot!',
    'Cool. Cool cool cool cool cool cool cool, '
    'no doubt no doubt no doubt no doubt.',
    'Title of your sex tape.',
    'Sarge, with all due respect, I am gonna completely ignore everything you just said.',
    'I ate one string bean. It tasted like fish vomit. That was it for me.',
    'The English language can not fully capture the depth and complexity of my thoughts, so I’m incorporating emojis into my speech to better express myself. Winky face.',
    'If I die, turn my tweets into a book.',
    'Fine. but in protest, I’m walking over there extremely slowly!',
    'Jake, why don’t you just do the right thing and jump out of a window?',
    'I asked them if they wanted to embarrass you, and they instantly said yes.',
    'Captain Wuntch. Good to see you. But if you’re here, who’s guarding Hades?',
    'I’m playing Kwazy Cupcakes, I’m hydrated as hell, and I’m listening to Sheryl Crow. I’ve got my own party going on.',
    'Anyone over the age of six celebrating a birthday should go to hell.',
    'Captain, turn your greatest weakness into your greatest strength. Like Paris Hilton RE: her sex tape.',
    'Title of your sex tape.',
]

reactions = [
    'tiktok.gif',
    '200.gif',
    'yourself.gif',
    'ohh.gif',
    'Piccard.gif',
    'letmeoff.gif',
    'ohmy.gif',
    'unnamed.gif',
    'luv.gif',
    'eyenarrow.gif',
    'ahg.gif',
    'yas.gif',
    'shocked.gif',
    'joff.gif',
    'yes100.gif',
    'noway.gif',
    'tear.gif',
    'blm.gif',
    'kawaii.gif',
    ',eh.gif',
    'ick.gif',
    'que.gif',
    'thank.gif',
    'trump.gif',
    'goon.gif',
    'jayzd.gif',
    'mjpopcorn.gif',
    'riight.gif',
    'nervss.gif',
    'steamy.gif',
    'uhwut.gif',
    'sadmat.gif',
    'whu.gif',
    'ohwu.gif',
    'susguess.gif',
    'hapjoy.gif',
    'baccon.gif',
    'smort.gif',
    'thumb.gif',
    'but-why.gif',
    'rere.gif',
    'gears.gif',
    'guuh.gif',
    'nonope.gif',
    'eyeroll.gif',
    'wtf.gif',
    'yee.gif',
    'bestcry.gif',
    'rosa.gif',
    'insideye.gif',
    'nolove.gif',
    'fetish.gif',
    'jnickle.gif',
    'ahhsee.gif',
    'blink.gif',
    'notimpressed.gif',
    'realize.gif',
    'breathen.gif',
    'ohhnoooo.gif',
    'preptheanus.gif',
    'monty.gif',
    'what.gif',
    'thanksman.gif',
    'thanks--man.gif',
    'claws.gif',
    'brows.gif',
    'billhappy.gif',
    'milayes.gif',
    'munch.gif',
    'kay.gif',
    'stockdrop.gif',
    'kanyehappymad.gif',
    'blaz.gif',
    'Oface.gif',
    'huhh.gif',
    'firin.gif',
    'browsa.gif',
    'string.gif',
    'willo.gif',
    'heavyfall.gif',
    'oohhhhhh.gif',
    'comedaddy.gif',
    'pouty.gif',
    'I_has_a_sad.gif',
    'sadyes.gif'
]
    
@client.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.channels, name='general')

##  creates a DM channel, and sends a message to the associated user who has joined
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}!  I am a totally normal human boy. My names Finn!\n'
        'Here are some of the things that I can do:\n'
        '- "!ninenine" for Brooklyn 99 quotes.\n'
        '- "!repeat" if you want me to repeat after you.\n'
        '- "ping" to play Ping Pong with me!\n'
        '- "!hug" if you\'re feeling lonely.\n'
        '- "!react" provides a random reaction.\n'
        '- "!temperature \{insert city\}" provides the cities temperature.\n'
        '- "!weather \{insert city\}" provides the cities three day forecast.\n'
        '- "!est" provides Eastern Standard Time.\n'
        '- "!time \{insert location\}" provides the time of the location.\n' 
        '- "!summon" summons me into your currenty voice channel.\n'
        '- "!banish" sends me back home to my mommey.\n'
        '- "!play \{insert song title\}" to play music by title.\n'                 
        '- "!pause" pauses the current song.\n'
        '- "!resume" continues playing a paused song.\n'
        '- "!url \{insert song link\}" to play music by link.\n'
        '- "!link \{insert search query\}" to have me google something for your lazy ass.\n'
##        '- "!image" for a random image.\n'
        '- "!commands" if you want to remember the commands.\n')
    
##  sends a message to the channel held in string (channel)
    await channel.send("Some jerk named " + member.mention + " has shown up to fiddle their diddle.")
    print('- ' + member.mention)

@client.event
async def on_member_remove(member):
##  sends a message to the specific channel listed, tagging the associated member that was kicked/left
    guild = member.guild
    channel = discord.utils.get(guild.channels, name='general')
    await channel.send("The one they call " + member.mention + " ran home to their legal gaurdian.")
    
@client.event
async def on_message(message):
##  when any message sent equals exactly any of the below, it then sends all the respective messages below that.
##  the client can use a break function stating if author = self to prevent the bot responding to itself, but 
    await client.process_commands(message)
    if message.content == 'ping':
        await message.channel.send('pong')
    if message.content == 'pong':
        await message.channel.send('ding')
    if message.content == 'ding':
        await message.channel.send('dong')
    if message.content == 'dong':
        await message.channel.send('bing')
    if message.content == 'bing':
        await message.channel.send('bong')
    if message.content == 'bong':
        await message.channel.send(file=discord.File('tiktok.gif'))
        return

@client.event
async def on_message(message):
    await client.process_commands(message)
    content = message.content.lower()
    if content == 'yeetusdeleetus':
        i = 0
        while i < 20:
            await message.channel.send('YEETUS!')
            i = i + 1
        else:
            await message.channel.send('DELEETUS!')
        return

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user:
        return    
    content = message.content.lower()
    yoo = content + '\n'
    with open('greetings.txt') as f:
##    if any(greeting in content for greeting in greetings):
##        await message.channel.send('Hello.')
        if yoo in f.readlines():
            response = random.choice(greetings)
            await message.channel.send(response)
        else:
            return

    
@client.command()
async def repeat(ctx, *args):
## creates a list of "args" and strings them together .format then joins the string together with ' '
    await ctx.send("You're on some other shit if you want me to say: \"{}\"".format(' '.join(args)))

@client.command()
async def say(ctx, *args):
## creates a list of "args" and strings them together .format then joins the string together with ' '
    await ctx.send("{}".format(' '.join(args)))


@client.command()
async def ninenine(ctx):
##  pulls a random response from the brooklyn list
    response = random.choice(brooklyn)
    await ctx.send(response)

@client.command()
async def hug(ctx):
##  tags the author of the function
    await ctx.send("hugs " + ctx.author.mention)
    
@client.command()
async def commands(ctx):
##  sends a direct message to the auther of the command with the below information
    await ctx.author.send('Here are some of the things that I can do:\n'
        '- "!ninenine" for Brooklyn 99 quotes.\n'
        '- "!repeat" if you want me to repeat after you.\n'
        '- "ping" to play Ping Pong with me!\n'
        '- "!hug" if you\'re feeling lonely.\n'
        '- "!react" provides a random reaction.\n'
        '- "!temperature \{insert city\}" provides the cities temperature.\n'
        '- "!weather \{insert city\}" provides the cities three day forecast.\n'
        '- "!est" provides Eastern Standard Time.\n'
        '- "!time \{insert location\}" provides the time of the location.\n' 
        '- "!summon" summons me into your currenty voice channel.\n'
        '- "!banish" sends me back home to my mommey.\n'
        '- "!play \{insert song title\}" to play music by title.\n'                 
        '- "!pause" pauses the current song.\n'
        '- "!resume" continues playing a paused song.\n'
        '- "!url \{insert song link\}" to play music by link.\n'
        '- "!link \{insert search query\}" to have me google something for your lazy ass.\n'
        '- "!commands" if you want to remember the commands.\n')


@client.command()
async def react(ctx):
##  pulls a random choice from the reactions list
    current_path = os.path.dirname(os.path.realpath(__file__))
    react_path = current_path + "/react"
    os.chdir(react_path)
    response = random.choice(reactions)
    ##  handles files from the bots directory
    await ctx.send(file=discord.File(response))
    os.chdir(current_path)


@client.command()
async def weather(ctx, *city):
##  arguments {city} tuple together and replace "{}" in the driver.get function.  ".format" will handle the arguments {city} and create hyphens to seperate each word 
    driver = webdriver.Chrome()
##  creates an event window that handles sending and recieving information from chrome
    try:
##      tells webdriver.Chrome to handle the below webpage - then finds the elements and convert them to text format
        driver.get("https://www.weather-forecast.com/locations/{}/forecasts/latest".format('-'.join(city)))
        name = driver.find_elements_by_class_name("main-title__header")[0].text
        threeDay = driver.find_elements_by_class_name("b-forecast__table-description-content")[0].text
        driver.quit()
        await ctx.send(name + '\n')
        await ctx.send(threeDay)

    except:
##      if the above function cannot be fulfilled (i.e returns a 404) then send
        driver.quit()
        sassy = random.choice(fourohfour)
        await ctx.send(sassy)

@client.command()
async def EST(ctx):
##  print local time (to server location) Python time function is fucking retarded. .time provides ticks(seconds) since EPOCH
    localtime = time.asctime(time.localtime(time.time()) )
    await ctx.send("It is currently: " + localtime + " EST.")

@client.command()
async def Time(ctx, *city):
    driver = webdriver.Chrome();
    try:
        driver.get("https://www.google.com/");
        searchBar = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input');
        searchBar.click();
        inputText = ("{} current time".format(' '.join(city)));
        searchBar.send_keys(inputText) ; 
        searchBar.send_keys(Keys.RETURN);
        time.sleep(1)
        outputText = driver.find_elements_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/div[1]')[0].text;
        endNote = driver.find_elements_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/span')[0].text;
        driver.quit()
        await ctx.send(endNote + " is " + outputText)
        return
    except:
        driver.quit()
        sassy = random.choice(fourohfour)
        await ctx.send(sassy)
        return
       
@client.command()
async def temperature(ctx, *city):
##  arguments {city} tuple together and replace "{}" in the driver.get function.  ".format" will handle the arguments {city} and create hyphens to seperate each word 
    driver = webdriver.Chrome()
##  creates an event window that handles sending and recieving information from chrome
    
    try:
##      tells webdriver.Chrome to handle the below webpage - then finds the elements and convert them to text format
        driver.get("https://www.weather-forecast.com/locations/{}/forecasts/latest".format('-'.join(city)))
        name = driver.find_elements_by_class_name("main-title__header")[0].text
        temp = driver.find_elements_by_class_name("b-metar-table__temperature")[0].text
        driver.quit()
        await ctx.send(name + '\n')
        await ctx.send(temp.replace('\n',''))
        return
        
    except:
##      if the above function cannot be fulfilled (i.e returns a 404) then send
        driver.quit()
        sassy = random.choice(fourohfour)
        await ctx.send(sassy)
        return

@client.command()
async def link(ctx, *query):
    search = ("{}".format(' '.join(query)));
    url = 'https://google.com/search?q=' + search
    
    
##@client.command()
##async def link(ctx, *query):
##    driver = webdriver.Chrome();
##    driver.get("https://www.google.ca/");
##    searchBar = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input');
##    searchBar.click();
##    inputText = ("{}".format(' '.join(query)));
##    searchBar.send_keys(inputText) ; 
##    searchBar.send_keys(Keys.RETURN);
##    time.sleep(1);
##    failed = True
##    try:
##        element2 = driver.find_element_by_xpath('//*[@id="rso"]/div[7]/div/div[2]/div/span').text;
##        driver.quit();
##        await ctx.send(element2);
##        print('1')
##        failed = False
##        return
##    except:
##        element2 = driver.find_element_by_xpath('//*[@id="rso"]/div[3]/div[3]/div/div[2]').text;
##        driver.quit();
##        await ctx.send(element2);
##        print('2')
##        failed = False
##        return
##    else:
##        element2 = driver.find_element_by_xpath('//*[@id="rso"]/div[3]/div/div[2]').text;
##        driver.quit();
##        await ctx.send(element2);
##        print('3')
##        failed = False
##        return
##    finally:
##        driver.quit();
##        if failed == True:
##            sassy = random.choice(fourohfour)
##            await ctx.send(sassy)
##            return
##        else:
##            return

        
@client.command()
async def botcommands(ctx):
    guild = ctx.guild
    channel = discord.utils.get(ctx.guild.channels, name='bot-commands')
    if channel is None:
        try:
            await guild.create_text_channel('bot-commands')
        finally:
            channel = discord.utils.get(ctx.guild.channels, name='bot-commands')
            await channel.send('Hi there! I am a totally normal human boy. My names Finn!\n'
                'Here are some of the things that I can do:\n'
                '- "!ninenine" for Brooklyn 99 quotes.\n'
                '- "!repeat" if you want me to repeat after you.\n'
                '- "ping" to play Ping Pong with me!\n'
                '- "!hug" if you\'re feeling lonely.\n'
                '- "!react" provides a random reaction.\n'
                '- "!temperature \{insert city\}" provides the cities temperature.\n'
                '- "!weather \{insert city\}" provides the cities three day forecast.\n'
                '- "!est" provides Eastern Standard Time.\n'
                '- "!time \{insert location\}" provides the time of the location.\n' 
                '- "!summon" summons me into your currenty voice channel.\n'
                '- "!banish" sends me back home to my mommey.\n'
                '- "!play \{insert song title\}" to play music by title.\n'                 
                '- "!pause" pauses the current song.\n'
                '- "!resume" continues playing a paused song.\n'
                '- "!url \{insert song link\}" to play music by link.\n'
                '- "!link \{insert search query\}" to have me google something for your lazy ass.\n'
                '- "!commands" if you want to remember the commands.\n')
    else:
        await channel.send('Hi there! I am a totally normal human boy. My names Finn!\n'
                       'Here are some of the things that I can do:\n'
                       '- "!ninenine" for Brooklyn 99 quotes.\n'
                       '- "!repeat" if you want me to repeat after you.\n'
                       '- "ping" to play Ping Pong with me!\n'
                       '- "!hug" if you\'re feeling lonely.\n'
                       '- "!react" provides a random reaction.\n'
                       '- "!temperature \{insert city\}" provides the cities temperature.\n'
                       '- "!weather \{insert city\}" provides the cities three day forecast.\n'
                       '- "!est" provides Eastern Standard Time.\n'
                       '- "!time \{insert location\}" provides the time of the location.\n' 
                       '- "!summon" summons me into your currenty voice channel.\n'
                       '- "!banish" sends me back home to my mommey.\n'
                       '- "!play \{insert song title\}" to play music by title.\n'                 
                       '- "!pause" pauses the current song.\n'
                       '- "!resume" continues playing a paused song.\n'
                       '- "!url \{insert song link\}" to play music by link.\n'
                       '- "!link \{insert search query\}" to have me google something for your lazy ass.\n'
                       '- "!commands" if you want to remember the commands.\n')
        
@client.command()
async def summon(ctx):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
        guild_id = ctx.guild.id
        player.append(guild_id)
        return
    except:
        sassy = random.choice(fourohfour)
        await ctx.send(sassy)
        return
        
@client.command()
async def banish(ctx):
    try:
        await ctx.voice_client.disconnect()
        return
    except:
        sassy = random.choice(fourohfour)
        await ctx.send(sassy)
        return
        
@client.command()
async def url(ctx, url):
    voice = get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send("Playing " + url)
    else:
        sassy = random.choice(fourohfour)
        await ctx.send(sassy)
        return

@client.command()
async def play(ctx, *query):
    driver = webdriver.Chrome();
    driver.get("https://www.YouTube.com/");
    searchBar = driver.find_element_by_xpath('//*[@id="search"]');
    searchBar.click();
    inputText = ("{}".format(' '.join(query)));
    searchBar.send_keys(inputText) ; 
    searchBar.send_keys(Keys.RETURN);
    time.sleep(1)
    try:
        element2 = driver.find_element_by_xpath('//*[@id="video-title"]/yt-formatted-string');
        element2.click();
        url = driver.current_url;
        driver.quit()
        voice = get(client.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            await ctx.send("Playing " + inputText)
            return
        else:
            driver.quit()
            sassy = random.choice(fourohfour)
            await ctx.send(sassy)
            return
    except:
        driver.quit()
        sassy = random.choice(fourohfour)
        await ctx.send(sassy)
        return

@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        sassy = random.choice(fourohfour)
        await ctx.send(sassy)
        return

@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        sassy = random.choice(fourohfour)
        await ctx.send(sassy)
        return
    else:
        voice.resume()
        return    


client.run(TOKEN)

