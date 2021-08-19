import discord
import pymysql
import brucebot

client = discord.Client()

@client.event
async def on_message(message):
    global conn
    
    if message.author == client.user: return

    if message.author.bot: return
    
    if message.content.startswith('$get_engagement'):
        # grab the the sql file and display engagement stats
        table = brucebot.fetch_users(conn)
        max_length = max([len(table[0][i]+":"+str(table[1][i])) for i in range(len(table[0]))])
        s = '```\n'
        for i in range(len(table[0])):
            user = table[0][i]
            score = table[1][i]
            s += user + ":" + " "*(max_length - len(user) - len(str(score)) + 2) + str(score) + "\n"
        s += '```'
        await message.channel.send(s)
        
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.mention_everyone: 
        # add 5 to the user engagement
        brucebot.add_engagement(message.author.name, 5, conn)
        return

    if message.author != client.user:
        # add 2 to the user engagement
        brucebot.add_engagement(message.author.name, 2, conn)
        return

@client.event
async def on_reaction_add(reaction, user):
    global conn
    brucebot.add_engagement(user.name, 1, conn)
    return

if __name__ == '__main__':
    conf = brucebot.get_config('config2.ini', 'db')
    conn = pymysql.connect(charset = 'utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        **conf)
    brucebot.create_table(conn)
    token = brucebot.get_config('config2.ini', 'bot')['token']
    print('running')
    client.run(token)
