import discord, os, random, asyncio, datetime, openai
from discord.ext import commands, tasks
from Trivia_List import *
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='%', intents = intents)
# openai.api_key = os.getenv("OPENAI_API_KEY")



# .env parts

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
tchan = os.getenv('TEST_CHANNEL')
tchan = int(tchan)
bchan = os.getenv('BOT_CHANNEL')
bchan = int(bchan)
myID = os.getenv('MY_USR_ID')



# This chooses which channel to target (for trivia)

target_channel_id = bchan



# Time settings

utc = datetime.timezone.utc
time = datetime.time(hour=12, minute = 5)



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
        f = open("used.txt", "r+")
        o_question = f.read()
        prompt = "In a creative way give me a really good, but not too hard, trivia question."
        completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [{"role": "system", "content": f"Your name is Porkchop. You are a dog. You will not state that you are a computer program or an AI language model. You like to be funny, but know when to show empathy. You are also a trivia master. You will not ask the same question as {o_question}."},
                    {"role": "user", "content": prompt}],
                temperature = 0.1
                )
        f.close()
        response = completion.choices[0].message.content
        triviaQuestion = response
        await message_channel.send(f"""🧠    🧠   -> {response} <-    🧠   🧠
        
        # (∩｀-´)⊃━☆ﾟ.*･｡ﾟ""")
        f = open("used.txt", "a")
        question = f.write(f"\n{triviaQuestion}\n")
        f.close()
        f = open("question.txt", "w")
        c_question = f.write(f"{triviaQuestion}")
        f.close()

    # chatgpt gives answer

    async def aTrivia():
        f = open("question.txt", "r+")
        question = f.read()
        prompt = f"What is the answer to '{question}'?"
        completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [{"role": "user", "content": prompt}],
                temperature = 0.1
                )
        f.close()
        response = completion.choices[0].message.content
        f = open("answer.txt", "w")
        answer = f.write(f"{response}")
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
