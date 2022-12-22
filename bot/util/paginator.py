from __future__ import annotations

from typing import (
    Generic, 
    List,
    TYPE_CHECKING,
    Type, 
    TypeVar
)

import discord
from discord.ext import commands

T = TypeVar('T')


class BaseButtonPaginator(Generic[T], discord.ui.View):
    """
    The Base Button Paginator class. Will handle all page switching without
    you having to do anything.
    
    Attributes
    ----------
    entries: List[Any]
        A list of entries to get spread across pages.
    per_page: :class:`int`
        The number of entries that get passed onto one page.
    pages: List[List[Any]]
        A list of pages which contain all entries for that page.
    clamp_pages: :class:`bool`
        Whether or not to clamp the pages to the min and max. 
    """
    if TYPE_CHECKING:
        ctx: commands.Context[commands.Bot]
    
    def __init__(self, *, embeds: List[T], clamp_pages: bool = True) -> None:
        super().__init__(timeout=180)
        self.embeds: List[T] = embeds

        self.clamp_pages: bool = clamp_pages
            
        self._current_page = 0
        self.pages = len(embeds)
        
    @property
    def max_page(self) -> int:
        """:class:`int`: The max page count for this paginator."""
        return self.pages
    
    @property
    def min_page(self) -> int:
        """:class:`int`: The min page count for this paginator."""
        return 1

    @property
    def current_page(self) -> int:
        """:class:`int`: The current page the user is on."""
        return self._current_page + 1
    
    @property
    def total_pages(self) -> int:
        """:class:`int`: Returns the total amount of pages."""
        return self.pages
    
    
    @discord.ui.button(emoji='\U000025c0', style=discord.ButtonStyle.blurple)
    async def on_arrow_backward(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self._current_page -= 1
        if self._current_page < 0:
            self._current_page = self.pages - 1

        return await interaction.response.edit_message(embed=self.embeds[self._current_page])

    @discord.ui.button(emoji='\U000023f9', style=discord.ButtonStyle.blurple)
    async def on_stop(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        for child in self.children:
            child.disabled = True # type: ignore
            
        self.stop()
        
        return await interaction.response.edit_message(view=self)
        
    @discord.ui.button(emoji='\U000025b6', style=discord.ButtonStyle.blurple)
    async def on_arrow_forward(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self._current_page += 1
        if self._current_page > self.pages - 1:
            self._current_page = 0
        return await interaction.response.edit_message(embed=self.embeds[self._current_page])
    
    @classmethod
    async def start(
        cls: Type[BaseButtonPaginator],
        context: commands.Context,
        *, 
        entries: List[T],
        clamp_pages: bool = True
    ) -> BaseButtonPaginator[T]:
        """|coro|
        
        Used to start the paginator.
        
        Parameters
        ----------
        context: :class:`commands.Context`
            The context to send to. This could also be discord.abc.Messageable as `ctx.send` is the only method
            used.
        entries: List[T]
            A list of entries to pass onto the paginator.
        per_page: :class:`int`
            A number of how many entries you want per page.
            
        Returns
        -------
        :class:`BaseButtonPaginator`[T]
            The paginator that was started.
        """
        new = cls(embeds=entries, clamp_pages=clamp_pages)
        new.ctx = context
        
        embed = new.embeds[0]
        await context.response.send_message(embed=embed, view=new)
        return new