import disnake
import uuid
import typing

# change int to always be shown as millify when printed
def millify(n : typing.Union[int, float, str]) -> str:
    if isinstance(n, str): return n

    data = "QT,18|Q,15|T,12|B,9|M,6|k,3"
    for item in data.split("|"):
        s = item.split(",")
        if n >= 10 ** int(s[1]):
            return f"{round(n / (10 ** int(s[1])), 2)}{s[0]}"
    n = round(n, 2)
    if n == int(n):
        return str(int(n))
    else:
        return str(n)

class Embed(disnake.Embed):
    def __init__(self, **kwargs):
        if 'color' not in kwargs: kwargs['color'] = 0x2b2d31
        super().__init__(**kwargs)

class Tab:
    def __init__(self, callback : typing.Callable, _id, name : typing.Optional[str] = None, emoji : typing.Optional[str] = None):
        self.callback = callback
        self.id = _id
        self.name = name
        self.emoji = emoji
    
    async def render(self, inter : disnake.Interaction):
        return await self.callback(inter, self)

class TabResponse: 
    def __init__(self, content : typing.Optional[str] = None, embeds : typing.Optional[typing.List[disnake.Embed]] = None):
        self.content = content
        self.embeds = embeds

class TabView(disnake.ui.View):
    class TabButton(disnake.ui.Button):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
        
        async def callback(self, inter : disnake.MessageInteraction):
            await inter.response.defer()
            
            if self.view.tab_group.current_tab == self.custom_id: return
            self.view.tab_group.current_tab = self.custom_id


            await inter.edit_original_message(**await self.view.tab_group.render(inter), attachments=[])
    
    class TabSelect(disnake.ui.Select):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        async def callback(self, inter : disnake.MessageInteraction):
            await inter.response.defer()
            
            if self.view.tab_group.current_tab == self.values[0]: return
            self.view.tab_group.current_tab = self.values[0]

            await inter.edit_original_message(**await self.view.tab_group.render(inter), attachments=[])


    def __init__(self, tab_group):
        super().__init__()
        self.tab_group = tab_group

        self.items = []

    def add_item(self, tab : Tab):
        self.items.append(tab)
    
    def render(self):
        if len(self.items) <= 1: return self
        if len(self.items) <= 5: 
            for item in self.items:
                current = item.id == self.tab_group.current_tab
                button = self.TabButton(
                    disabled = current,
                    style = disnake.ButtonStyle.secondary if not current else disnake.ButtonStyle.primary,
                    label = item.name,
                    emoji = item.emoji,
                    custom_id = item.id
                )
                super().add_item(button)
        if len(self.items) > 5:
            options = []
            for item in self.items:
                current = item.id == self.tab_group.current_tab
                options.append(disnake.SelectOption(label=item.name, emoji=item.emoji, value=item.id))
            select = self.TabSelect(
                placeholder = "Select a tab",
                options = options,
                custom_id = "tab_select"
            )
            super().add_item(select)
        return self

class TabGroup:
    def __init__(self): 
        self.tabs = {}
        self.current_tab = None

    def add_tab(self, tab : Tab):
        self.tabs[tab.id] = tab

        if self.current_tab is None:
            self.current_tab = tab.id
    
    def tab(self, name : typing.Optional[str] = None, emoji : typing.Optional[str] = None, _id : typing.Optional[str] = None):
        def decorator(callback):
            tab = Tab(callback, _id or str(uuid.uuid4()), name, emoji)
            self.add_tab(tab)
            return callback
        return decorator
    
    async def start(self, inter : disnake.ApplicationCommandInteraction, ephemeral : bool = False):
        await inter.response.defer(with_message=True, ephemeral=ephemeral)
        response = await self.render(inter)
        await inter.followup.send(**response)

    async def render(self, inter : disnake.Interaction) -> typing.Dict[str, typing.Any]:
        view = TabView(self)
    
        for tab in self.tabs.values():
            view.add_item(tab)
        response = await self.tabs[self.current_tab].render(inter)

        return {
            'content': response.content or '',
            'embeds': response.embeds or [],
            'view': view.render()
        }