import discord, os, random, asyncio, datetime, openai
from discord.ext import commands, tasks
from Trivia_List import *
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='%', intents = intents)

usedQ = []
q = []
randomN = random.randint(1, 100)


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
time = datetime.time(hour=2, minute = 37)



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

    try:
        with open('question.txt', 'r') as f:
            o_question = f.read()
    except IOError as e:
        print(f"Error reading question.txt: {e}")

    try:
        with open('answer.txt', 'r') as f:
            o_answer = f.read()
    except IOError as e:
        print(f"Error reading answer.txt: {e}")

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
            usedQ.clear()
            q.clear()
            try:
                with open("used.txt", "r") as f:
                    usedQuestions = f.read()
            except IOError as e:
                print(f"Error reading used.txt: {e}")

            usedQ.extend(usedQuestions.splitlines())

            prompt = "Give me a really good trivia question."
            completion = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = [{"role": "system", "content": f"Your name is Porkchop. You are a dog. You will not state that you are a computer program or an AI language model. You are a trivia master."},
                        {"role": "user", "content": prompt}],
                    temperature = 0.1,
                    max_tokens = 1000
                    )
            
            response = completion.choices[0].message.content

            try:
                with open("question.txt", "r") as f:
                    notin = f.read().splitlines()
            except IOError as e:
                print(f"Error reading question.txt: {e}")

            if len(notin) == 3:
                q.append(notin[2])
            elif len(notin) == 1:
                q.append(notin[0])

            if q not in usedQ:
                try:
                    with open("question.txt", "w") as f:
                        f.write(f"{q}")
                except IOError as e:
                    print(f"Error writing to question.txt: {e}")

                try:
                    with open("used.txt", "a") as f:
                        f.write(f"{q}\n")
                except IOError as e:
                    print(f"Error writing to used.txt: {e}")

                break
            
            
        await message_channel.send(f"""🧠    🧠   -> {response} <-    🧠   🧠
        
        # (∩｀-´)⊃━☆ﾟ.*･｡ﾟ""")
        

    # chatgpt gives answer

    async def aTrivia():
        prompt = f"What is the answer to '{q}'?"
        completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [{"role": "user", "content": prompt}],
                temperature = 0.1,
                max_tokens = 100
                )
        
        response = completion.choices[0].message.content
        with open("answer.txt", "w") as f:
            f.write(f"{response}")
        


    await qTrivia()
    await aTrivia()
    with open("test.txt", "w") as f:
        f.write(f"{randomN}")



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
