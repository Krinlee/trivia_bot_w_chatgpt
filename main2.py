import discord, os, random, asyncio, datetime, openai
from discord.ext import commands, tasks
from Trivia_List import *
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='%', intents = intents)

# usedQ = []
# q = []
# if_not = []


# .env parts

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
tchan = os.getenv('TEST_CHANNEL')
tchan = int(tchan)
bchan = os.getenv('BOT_CHANNEL')
bchan = int(bchan)
myID = os.getenv('MY_USR_ID')



# This chooses which channel to target (for trivia)

target_channel_id = tchan



# Time settings

utc = datetime.timezone.utc
time = datetime.time(hour=13, minute = 35)



# Test command

@bot.command()
async def test(ctx):
    await ctx.send("This is a test!")





    




# Getting the Bot ready

@bot.event
async def on_ready():
    print('\n{0.user} is ready for action'.format(bot))
    trivia.start()


# Command to have the bot DM the answer

# async def ans_dm(member):
	# f = open('answer.txt', 'r')
	# trivia_ans = f.read()
	# f.close()
	# await member.send(trivia_ans)

@bot.command()
async def ans(ctx):
	if ctx.author.id == int(myID):
		f = open('answer.txt', 'r')
		trivia_ans = f.read()
		f.close()
		await ctx.send(trivia_ans)
	else:
		await ctx.send("You can't have the answer yet!")
		
	
	



# Trivia loop

@tasks.loop(time=time)
async def trivia():
    usedQ = []
    q = []
    openai.api_key = os.getenv("OPENAI_API_KEY")
    message_channel = bot.get_channel(target_channel_id)
    f = open('question.txt', 'r')
    o_question = f.read()
    f.close()
    f = open('answer.txt', 'r')
    o_answer = f.read()
    f.close()
    await message_channel.send(f"""@here Yesterday's question was:
    
     ¯\_(ツ)_/¯  {o_question}  ¯\_(ツ)_/¯""")
    await message_channel.send(f"""The answer is		(っ ͡ ͡º - ͡ ͡º ς)		 -> {o_answer} <-

(人❛ᴗ❛)♪тнайк　чоц♪(❛ᴗ❛*人)""")
    await message_channel.send("""@everyone 
    
    As always, post your answers to the trivia in the trivia-answers channel.

    (っ'ヮ'c)	The answer will be posted here on the next day before the next trivia question.""")
    await asyncio.sleep(3)


    # chatgpt ask trivia

    async def qTrivia():
        while True:
            # with open("used.txt", "r") as f:
            #     usedQuestions = f.read().splitlines()
            f = open("used.txt", "r")
            usedQuestions = f.read()
            f.close()
            usedQ.append(usedQuestions)
            prompt = "Give me a really good trivia question."
            completion = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = [{"role": "system", "content": f"Your name is Porkchop. You are a dog. You will not state that you are a computer program or an AI language model. You are a trivia master."},
                        {"role": "user", "content": prompt}],
                    temperature = 0.1,
                    max_tokens = 1000
                    )
            
            response = completion.choices[0].message.content
            f = open("question.txt", "w")
            f.write(f"{response}")
            f.close()
            with open("question.txt", "r") as f:
                notin = f.read().splitlines()
            f.close()
            q.append(notin[2])
            if q not in usedQ:
                print(q)

                f = open("used.txt", "a")
                f.write(f"{q}")
                f.close()
                break
            
            
        # print(test)
        await message_channel.send(f"""🧠    🧠   -> {response} <-    🧠   🧠
        
        # (∩｀-´)⊃━☆ﾟ.*･｡ﾟ""")
        

    # chatgpt gives answer

    async def aTrivia():
        # f = open("question.txt", "r")
        # question = f.read()
        # f.close()
        prompt = f"What is the answer to '{q}'?"
        completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [{"role": "user", "content": prompt}],
                temperature = 0.1,
                max_tokens = 100
                )
        
        response = completion.choices[0].message.content
        f = open("answer.txt", "w")
        f.write(f"{response}")
        f.close()


    await qTrivia()
    await aTrivia()



@trivia.before_loop
async def before_trivia():
    print("\n\nTrivia is good to go!")
    await bot.wait_until_ready()



# Runs the Bot

try:
    bot.run(TOKEN)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
