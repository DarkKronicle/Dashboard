# Dashboard Display

This is a dashboard to load onto a Raspberry Pi to display information. This is almost entirely curated just for me, so you may not get much use out of this repository.

## Current Features

- Display bus estimates
- Display laundry estimates

## Credits

I used discord.py's [task class](https://github.com/Rapptz/discord.py/blob/master/discord/ext/tasks/__init__.py) to make it easier for me to schedule events.

For asyncio pygame help I used AlexElvers [pygame-with-asyncio](https://github.com/AlexElvers/pygame-with-asyncio) (with the fix in issues). This was used just to get the event loop functioning since I still found that stuff confusing.

I used Tekore's [serialise class](https://github.com/felix-hilden/tekore/blob/master/tekore/_model/serialise.py) to help with API backends. This is a super elegant and cool way to transfer JSON data into objects automatically.

For the main rendering I used [pygame-gui](https://github.com/MyreMylar/pygame_gui) to help with that. Because of that, some themes are modified pygame-gui themes.