from datetime import datetime

import discord
import discord.ext
import pytz
from discord.enums import ButtonStyle
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from discord_components import Button, ButtonStyle

intents = discord.Intents.default()

bot = discord.Client()
channel = discord.utils.get(bot.get_all_channels())
bot = commands.Bot(command_prefix='!', help_command=None, intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                        name="https://github.com/LoyalWolf1404/DiscordPython",
                                                        status=discord.Status.online))


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
async def rechne(ctx, operation: str):
    await ctx.send(eval(operation))


@bot.command(name='userinfo')
async def userinfo(ctx, member: discord.Member):
    de = pytz.timezone('Europe/Berlin')
    embed = discord.Embed(title=f'> Userinfo für {member.display_name}',
                          description='', color=discord.Colour.purple(), timestamp=datetime.now().astimezone(tz=de))

    embed.add_field(name='Name', value=f'```{member.name}#{member.discriminator}```', inline=True)
    embed.add_field(name='Bot', value=f'```{("Ja" if member.bot else "Nein")}```', inline=True)
    embed.add_field(name='Nickname', value=f'```{(member.nick if member.nick else "Nicht gesetzt")}```', inline=True)
    embed.add_field(name='Server beigetreten', value=f'```{member.joined_at}```', inline=True)
    embed.add_field(name='Discord beigetreten', value=f'```{member.created_at}```', inline=True)
    embed.add_field(name='Rollen', value=f'```{len(member.roles)}```', inline=True)
    embed.add_field(name='Höchste Rolle', value=f'```{member.top_role.name}```', inline=True)
    embed.add_field(name='Farbe', value=f'```{member.color}```', inline=True)
    embed.add_field(name='Booster', value=f'```{("Ja" if member.premium_since else "Nein")}```', inline=True)
    embed.set_footer(text=f'Angefordert von {ctx.author.name} • {ctx.author.id}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
async def gh(ctx):
    await ctx.send("_ _", components=[
        Button(label="Github", style=ButtonStyle.URL, url="https://github.com/LoyalWolf1404/DiscordPython")])


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Du hast keinen User angegeben.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Du hast keine Berechtigung dafür.")


@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Entbannt: {user.mention}')
            return


@bot.command(description="Muted einen User.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                          read_messages=False)
    embed = discord.Embed(title="Mute", description=f"{member.mention} wurde gemutet ",
                          colour=discord.Colour.light_gray())
    embed.add_field(name="Grund:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" Du wurdest in {guild.name} gemutet mit dem Grund: {reason}")


@bot.command()
async def tutel(ctx):
    await ctx.send('Tutel :>')


@bot.command()
async def ticketcreate(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title='Ticket system',
        description='Reagiere mit 📩 um ein Ticket zu machen.',
        color=0
    )

    embed.set_footer(text="LoyalWolfLP#6733")

    msg = await ctx.send(embed=embed)
    await msg.add_reaction('📩')

    def check(reaction, user):
        return str(reaction) == '📩' and ctx.author == user

    await bot.wait_for("reaction_add", check=check)
    name = 'Tickettest'
    category = discord.utils.get(ctx.guild.categories, name=name)

    await ctx.guild.create_text_channel(name=f'Ticket von {ctx.author}', category=category)


@bot.command()
@has_permissions(administrator=True, manage_channels=True)
async def ticketdelete(ctx, channel_name):
    # check if the channel exists
    existing_channel = discord.utils.get(bot.get_all_channels(), name=channel_name)

    # if the channel exists
    if existing_channel is not None:
        await existing_channel.delete()
    # if the channel does not exist, inform the user
    else:
        await ctx.send(f'No channel named, "{channel_name}", was found')


@bot.command()
async def help(context):
    embed = discord.Embed(title="Commands",
                          description="!help - Zeigt das hier an\n\
                !test - Einfach nur zum testen\n\
                !kill - Bringt jemanden um jajaja.\n\
                !say - Sagt ein word für dich,\n\
                weil du zu dumm bist das wort\n\
                auszusprechen\n\
                !argumenttest - Mach einfach\n\
                !caps - macht alles in caps\n\
                !rechne - rechnet dir alles\n\
                !userinfo - zeigt dir die Userinfo an\n\
                !gh - Github Button zu meinem Profil\n\
                !ban - bannt einen User\n\
                !unban - entbannt einen User\n\
                !mute - Mutet einen User.",
                          color=discord.Colour.purple())
    await context.send(embed=embed)


bot.run('Token')

