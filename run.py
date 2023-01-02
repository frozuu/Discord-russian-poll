import discord
import asyncio

intents = discord.Intents().all()
client = discord.Client(intents=intents)

poll_in_progress = False

Token = "YOUR_BOT_TOKEN"
@client.event
async def on_message(message, poll_in_progress=False):
    if message.content.startswith("!rus_poll"):
        await client.change_presence(activity=discord.Game(name="!rus_poll"))
        # Check if there is already a poll in progress
        if poll_in_progress:
            await message.channel.send("obecnie trwa głosowanie (dev442)")
            return

            # Check if a user was mentioned in the command
        if len(message.mentions) == 0:
            await message.channel.send("You must mention a user to start a poll")
            return


        await message.delete()



            # Get the user who sent the command
        command_user = message.author
        print("Command user:", command_user)

        # Get the user mentioned in the command
        mentioned_user = message.mentions[0]
        print("Mentioned user:", mentioned_user)

        # Send the poll message and get the message object
        embed = discord.Embed(title="Russian poll", description="Should we kick {}?".format(mentioned_user.mention),
                              color=0x00ff00)
        embed.add_field(name="Time left to vote", value="60s")
        embed.set_footer(text="✨")

        # Send the poll message and get the message object

        poll_message = await message.channel.send(embed=embed)

        # Add the "yes" and "no" reactions
        await poll_message.add_reaction("👍")
        await poll_message.add_reaction("👎")

        # Wait 1 minute before ending the poll
        for i in range(50, 0, -10):
            await asyncio.sleep(10)
            embed.set_field_at(index=0, name="Time left to vote", value="{}s".format(i))
            await poll_message.edit(embed=embed)
        await asyncio.sleep(10)
        embed.set_field_at(index=0, name="Time left to vote", value="Voting ended")
        await poll_message.edit(embed=embed)

        # Get the channel where the message was sent
        channel = client.get_channel(poll_message.channel.id)

        # Fetch the message with all of the reactions
        poll_message = await channel.fetch_message(poll_message.id)

        # Count the number of "yes" and "no" reactions
        yes_count = 0
        no_count = 0
        for reaction in poll_message.reactions:
            if str(reaction.emoji) == "👍":
                yes_count = reaction.count
            if str(reaction.emoji) == "👎":
                no_count = reaction.count

        print("Yes count:", yes_count)
        print("No count:", no_count)

        # Determine the result of the poll
        if yes_count > no_count:
            try:
                await message.guild.kick(mentioned_user)
                print("Kicked mentioned user")
                await message.channel.send("{} was kicked!".format(mentioned_user.mention))
            except discord.Forbidden:
                await message.channel.send("I can't kick this person! :(")

        elif no_count > yes_count:
            try:
                await message.guild.kick(command_user)
                print("Kicked command user")
                await message.channel.send("{} was kicked!".format(command_user.mention))
            except:
                await message.channel.send("I can't kick this person! :(")

        elif no_count == yes_count:
            await message.channel.send("DRAW! :0 holy fuck")


client.run(Token)
