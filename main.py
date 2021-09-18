from twitchio.ext import commands
import nest_asyncio
import seaborn as sns
import matplotlib.pyplot as plt
import time
import regex
from nltk.stem import PorterStemmer,SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from collections import deque
from processing import Token_List,Chat_processor,Token,Tester

nest_asyncio.apply()
class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        self.nlp_processor = Chat_processor()
        self.last_time_graph = time.time()
        super().__init__(token='chd088egdk7ocqx4rbqs9ux367gckw', prefix='?', initial_channels=['bananashooter07'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return
                
        # we need to process the message first before dictionary
        # remember to add rstrip and lstrip
        self.nlp_processor.process_string(message.content,message.author.name)
        
        
        # need to run build graph once the program starts and then it will call itself after every n seconds
        print('time difference')
        print(time.time() - self.last_time_graph)
        
        if time.time() - self.last_time_graph > 5:
            self.build_graph(self.nlp_processor.getCommon())
            self.last_time_graph = time.time()
        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)
    
    def build_graph(self,inputs):
        # we first sort the array and clean it to get it into plotting format
        if inputs:
            print('graph input')
            print(inputs)
            x_axis = []
            y_axis = []
            for i in inputs:
                x_axis.append(i[0])
                y_axis.append(i[1])
            
            plt.figure(figsize=(10,8))
            plt.title("Word Frequency")
            ax = sns.barplot(x = x_axis, y = y_axis,palette=("OrRd_r"))
            plt.savefig(r'C:\Users\TheDarkAce\Jupyter scripts\Twitchbot/barchart.png')
            print('graph was printed')
            
    @commands.command()
    async def hello(self, ctx: commands.Context):
        
        await ctx.send(f'Hello kya bol raha hai Bhowsadike')

def __init__():
    bot = Bot()
    bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.