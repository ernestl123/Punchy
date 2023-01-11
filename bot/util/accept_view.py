import discord

class AcceptView(discord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.value = None
        self.user = user
        self.timeout = 60
    
    async def interaction_check(self, interaction) -> bool:
        return interaction.user == self.user

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Accept', emoji="✅", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Reject', emoji = "❌", style=discord.ButtonStyle.gray)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()