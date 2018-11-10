# AddonManager21
AnkiAddon: Backported Addon Manager From Anki 2.1

## About:
With this addon, users can edit the config.json files in Anki 2.0 and update dictionary keys just like 2.1's addon manager. Edited text are saved to a file called meta.json and is not overwritten on updates. Developers can get the config data using mw.addonManager.getConfig and mw.addonManager.setConfigUpdatedAction and it'll work for both Anki 2.0 and 2.1. Without this addon, if it's ever removed or if a user didn't have it installed, developers should ensure their code reads the config.json file directly. See the skeleton folder for an example template provided.

All files are backported from anki-2.1.5-src. This addon must be loaded first, so the first file is named 111111111.py in the main directory. And each addon must have it's own folder with a config.json and a config.md files.


## Conflict:
Should there be any conflict and this addon is not loaded before another, rename it to something else like 1111111.py or 2222222.py


## Symbolic Links or Junction Points:
Addon writen using this method may use sym links (or junction points on windows) and make the plugin available to both versions of Anki.


## Screenshots:
<img src="https://github.com/lovac42/AddonManager21/blob/master/screenshot/menutools.png?raw=true" />  
<img src="https://github.com/lovac42/AddonManager21/blob/master/screenshot/addonmenu.png?raw=true" />  
<img src="https://github.com/lovac42/AddonManager21/blob/master/screenshot/confeditor.png?raw=true" />  
<img src="https://github.com/lovac42/AddonManager21/blob/master/screenshot/errorcheck.png?raw=true" />  
