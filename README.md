# AddonManager21
AnkiAddon: Backported Addon Manager For Anki 2.0

## About:
With this addon, users can edit the config.json files in Anki 2.0 and update dictionary keys just like 2.1's addon manager. Edited text are saved to a file called meta.json and is not overwritten on updates. Without this addon, if it's ever removed or if a user didn't have it installed, developers should ensure their code reads the config.json file directly. See the skeleton folder for an example template provided.

All files are backported from anki-2.1.5-src. This addon must be loaded first, so the first file is named __init__.py in the main directory. And each addon must have it's own folder with a config.json file.

## Screenshots:
<img src="https://github.com/lovac42/AddonManager21/blob/master/screenshot/addonmenu.png?raw=true" />  
<img src="https://github.com/lovac42/AddonManager21/blob/master/screenshot/confeditor.png?raw=true" />  
