import discord
from discord.ext import commands
import discord.ext

client = discord.Client()
bot = commands.Bot(command_prefix='!', help_command=None)


def caps_pls(text):
    return text.upper()


@bot.command()
async def test(ctx):
    await ctx.send('test')


@bot.command()
async def kill(ctx, member: discord.Member):
    await ctx.send(f'{member.display_name} ist eine neue runde')


@kill.error
async def kill_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Benutz den Command doch richtig')


@bot.command()
async def jajaja(ctx):
    await ctx.send('Dein Aquarium brennt')


@bot.command()
async def say(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def argumenttest(ctx, *args):
    await ctx.send('{} Deutsche Wörter: {}'.format(len(args), ', '.join(args)))


@bot.command()
async def caps(ctx, *, arg: caps_pls):
    await ctx.send(arg)


@bot.command()
async def rechne(ctx, operation:str):
    await ctx.send(eval(operation))


@bot.command()
async def help(context):
    embed = discord.Embed(title="Commands",
                          url="https://github.com/LoyalWolf1404/DiscordPython",
                          description="!help - Zeigt das hier an\n\
                !test - Einfach nur zum testen\n\
                !kill - Bringt jemanden um jajaja.\n\
                !say - Sagt ein word für dich, weil du zu dumm bist das wort auszusprechen\n\
                !argumenttest - Mach einfach\n\
                !caps - macht alles in caps",
                          color=discord.Colour.purple())
    await context.send(embed=embed)



bot.run('Token')
