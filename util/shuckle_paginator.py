from __future__ import annotations

import discord
from discord.ext import commands
from io import BytesIO

class ShucklePaginator(discord.ui.View):
    """
    Embed Paginator, modified from the simple paginator library.
    Modified to allow local files sent along with the pages

    Parameters:
    ----------
    timeout: int
        How long the Paginator should timeout in, after the last interaction. (In seconds) (Overrides default of 60)
    PreviousButton: discord.ui.Button
        Overrides default previous button.
    NextButton: discord.ui.Button
        Overrides default next button.
    PageCounterStyle: discord.ButtonStyle
        Overrides default page counter style.
    InitialPage: int
        Page to start the pagination on.
    """

    def __init__(self, *,
                 timeout: int = 60,
                 PreviousButton: discord.ui.Button = discord.ui.Button(emoji=discord.PartialEmoji(name="\U000025c0")),
                 NextButton: discord.ui.Button = discord.ui.Button(emoji=discord.PartialEmoji(name="\U000025b6")),
                 PageCounterStyle: discord.ButtonStyle = discord.ButtonStyle.grey,
                 InitialPage: int = 0,
                 ephemeral: bool = False) -> None:
        self.PreviousButton = PreviousButton
        self.NextButton = NextButton
        self.PageCounterStyle = PageCounterStyle
        self.InitialPage = InitialPage
        self.ephemeral = ephemeral

        self.pages = None
        self.ctx = None
        self.message = None
        self.current_page = None
        self.page_counter = None
        self.total_page_count = None

        super().__init__(timeout=timeout)

    async def start(self, ctx: discord.Interaction|commands.Context, pages: list[discord.Embed] | list[tuple[discord.Embed, bytes, str, str]]):
        '''
        Accepts a list of embeds
        Or, a list of tuples that contains the embed, file as bytes, filename, then file extension

        If the file is passed in as a discord.File as soon as its tabbed away from the file gets destroyed
        '''
        if isinstance(ctx, discord.Interaction):
            ctx = await commands.Context.from_interaction(ctx)

        self.pages = pages
        self.total_page_count = len(pages)
        self.ctx = ctx
        self.current_page = self.InitialPage

        self.PreviousButton.callback = self.previous_button_callback
        self.NextButton.callback = self.next_button_callback

        self.page_counter = ShucklePaginatorPageCounter(style=self.PageCounterStyle,
                                                       TotalPages=self.total_page_count,
                                                       InitialPage=self.InitialPage)

        self.add_item(self.PreviousButton)
        self.add_item(self.page_counter)
        self.add_item(self.NextButton)

        page = self.pages[self.InitialPage]
        if isinstance(page, tuple):
            embed, bytes, filename, extension = page
            file = discord.File(BytesIO(bytes), filename=f'{filename}.{extension}')
            self.message = await ctx.send(embed=embed, file=file, view=self)
        else:
            self.message = await ctx.send(embed=page, view=self)

    async def previous(self):
        if self.current_page == 0:
            self.current_page = self.total_page_count - 1
        else:
            self.current_page -= 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        page = self.pages[self.current_page]
        if isinstance(page, tuple):
            embed, bytes, filename, extension = page
            file = discord.File(BytesIO(bytes), filename=f'{filename}.{extension}')
            await self.message.edit(embed=embed, attachments=[file], view=self)
        else:
            await self.message.edit(embed=page, view=self)

    async def next(self):
        if self.current_page == self.total_page_count - 1:
            self.current_page = 0
        else:
            self.current_page += 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        page = self.pages[self.current_page]
        if isinstance(page, tuple):
            embed, bytes, filename, extension = page
            file = discord.File(BytesIO(bytes), filename=f'{filename}.{extension}')
            await self.message.edit(embed=embed, attachments=[file], view=self)
        else:
            await self.message.edit(embed=page, view=self)

    async def next_button_callback(self, interaction: discord.Interaction):
        '''
        if interaction.user != self.ctx.author:
            embed = discord.Embed(description="You cannot control this pagination because you did not execute it.",
                                  color=discord.Colour.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        '''
        await self.next()
        await interaction.response.defer()

    async def previous_button_callback(self, interaction: discord.Interaction):
        '''
        if interaction.user != self.ctx.author:
            embed = discord.Embed(description="You cannot control this pagination because you did not execute it.",
                                  color=discord.Colour.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        '''
        await self.previous()
        await interaction.response.defer()



class ShucklePaginatorPageCounter(discord.ui.Button):
    def __init__(self, style: discord.ButtonStyle, TotalPages, InitialPage):
        super().__init__(label=f"{InitialPage + 1}/{TotalPages}", style=style, disabled=True)
