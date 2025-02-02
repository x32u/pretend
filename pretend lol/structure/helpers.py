import sys
import json
import asyncio
import datetime
import humanize

from discord.ext.commands.cog import Cog
from discord.interactions import Interaction

from typing import Mapping, Coroutine, List, Any, Callable, Optional, Union, Dict


from discord.ext.commands import (
    Context,
    BadArgument,
    Command,
    MissingPermissions,
    check,
    Group,
    AutoShardedBot as AB,
    FlagConverter,
)

from discord import (
    Role,
    ButtonStyle,
    Message,
    Embed,
    StickerItem,
    Interaction,
    User,
    Member,
    Attachment,
    WebhookMessage,
    TextChannel,
    Guild,
    utils,
    Thread,
)

import discord
from discord.ext import commands
from typing import List

class Cache:
    def __init__(self):
        self.cache_inventory = {}

    def __repr__(self) -> str:
        return str(self.cache_inventory)

    async def do_expiration(self, key: str, expiration: int) -> None:
        await asyncio.sleep(expiration)
        self.cache_inventory.pop(key)

    def get(self, key: str) -> Any:
        """Get the object that is associated with the given key"""
        return self.cache_inventory.get(key)

    async def set(self, key: str, object: Any, expiration: Optional[int] = None) -> Any:
        """Set any object associatng with the given key"""
        self.cache_inventory[key] = object
        if expiration:
            asyncio.ensure_future(self.do_expiration(key, expiration))
        return object

    def remove(self, key: str) -> None:
        """An alias for delete method"""
        return self.delete(key)

    def delete(self, key: str) -> None:
        """Delete a key from the cache"""
        if self.get(key):
            del self.cache_inventory[key]
            return None

    def sadd(self, key: str, value: Any) -> None:
        """Add a value to a set in the cache."""
        if key not in self.cache_inventory:
            self.cache_inventory[key] = set()
        self.cache_inventory[key].add(value)