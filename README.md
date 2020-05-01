WiiUVC icon and banner generator
--------------------------------

### Description
The `icon-banner-generator.py` script will generate WiiUVC icon and banner images for batch processing in [TeconMoon-s-WiiVC-Injector-Mod](https://github.com/timefox/TeconMoon-s-WiiVC-Injector-Mod). The generated images are downloaded from [GameTDB](https://www.gametdb.com) and are sorted within each game directory.

### Preparation
Images should be placed in separate directories under the following naming convention:
`<Title> [<GameID>]`.
The preparation step could be done by using [wiibackupmanager](http://www.wiibackupmanager.co.uk) and/or using [Gamecube ISO/GCM Organizer Script](https://gbatemp.net/threads/gamecube-iso-gcm-organizer-script.480619/).

### Generate images:
`python3 icon-banner-generator.py <game_directory>`

Note: `<game_directory>` should contain all games, sorted in directories.
