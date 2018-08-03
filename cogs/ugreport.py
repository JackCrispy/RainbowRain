import discord
import os
from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks

class UGReport:
    """Report Users"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/ugreport/settings.json')

    async def init(self, server):
        self.settings[server.id] = {
            'report-channel': '0'
}
    async def error(self, ctx):  #In case files dont exist.
        for folder in folders:
            if not os.path.exists(folder):
                message_file += "`{}` folder\n".format(folder)
                print("Creating " + folder + " folder...")
                os.makedirs(folder)
                error_file = 1
        for filename in files:
            if not os.path.isfile('data/ugreport/{}'.format(filename)):
                print("Creating empty {}".format(filename))
                dataIO.save_json('data/ugreport/{}'.format(filename), {})
                message_file += "`{}` is missing\n".format(filename)
                error_file = 1
        if error_file == 1:
            message_file += "The files were successfully re-created. Try again your command (you may need to set your local settings again)"
            await self.bot.say(message_file)
        if ctx.message.server.id not in self.settings:
            await self.init(ctx.message.server)


    @commands.group(pass_context=True)
    @checks.admin()
    async def reportchannel(self, ctx, *, channel: discord.Channel=None):
        """Sets a channel as log"""
    
        if not channel:
            channel = ctx.message.channel
        else:
            pass
        server = ctx.message.server
        if server.id not in self.settings:
            await self.init(server)
        self.settings[server.id]['report-channel'] = channel.id
        await self.bot.say("Reports will be sent to **" + channel.name + "**.")
        dataIO.save_json('data/ugreport/settings.json', self.settings)


    @commands.command(pass_context=True, no_pm=True)
    async def report(self, ctx, person, *, reason): #changed terminology. Discord has people not players.
        """Report a user. Please provide evidence.""" #Where is the evidence field? Might want to add one
        author = ctx.message.author.name #String for the Author's name
        server = ctx.message.server
        try:
            reportchannel = self.bot.get_channel(self.settings[server.id]['report-channel'])
        except:
            KeyError
            await self.bot.send_message(ctx.message.author, "Uh Oh! Your report was not sent D: Please let an admin know that they need to set the default report channel")
            return
        embed=discord.Embed(title="Report:", description="A Report has been filed against somebody!")
        embed.set_author(name="Report System") 
        embed.add_field(name="User:", value=person, inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Reported By:", value=author, inline=True)
        embed.set_footer(text="Thanks for the report!") #Lovely thing for a footer
        await self.bot.send_message(ctx.message.author, "Your report against {} has been created.".format(person)) #Privately whispers to a user that said report was created and sent
        await self.bot.send_message(reportchannel, embed=embed) #Sends report to the channel we specified earlier


def check_folders():
    folders = ('data', 'data/ugreport/')
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)

def check_files():
    ignore_list = {'SERVERS': [], 'CHANNELS': []}
    
    files = {
        'settings.json'         : {}
    }

    for filename, value in files.items():
        if not os.path.isfile('data/ugreport/{}'.format(filename)):
            print("Creating empty {}".format(filename))
            dataIO.save_json('data/ugreport/{}'.format(filename), value)

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(UGReport(bot))
