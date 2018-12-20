from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from aqt.utils import showText
from codecs import open
from anki.utils import json
import os


class AddonManTest:
    hotkey = 'Shift+a'

    def __init__(self):
        addHook('profileLoaded', self.onProfileLoaded)

        #for test previews
        addHook('showQuestion', self.onShowQuestion) 


    def onProfileLoaded(self):
        #Add timer, must be loaded after addonmanger21 loads.
        mw.progress.timer(200,self.setHotkeys,False)
        mw.progress.timer(300,self.setHotkeysCallback,False)


    def setHotkeysCallback(self):
        if getattr(mw.addonManager, "setConfigUpdatedAction", None):
            mw.addonManager.setConfigUpdatedAction(__name__, self.setHotkeys)
        else:
            print('addonManager21 Not Loaded')


    def setHotkeys(self, config=None):
        if not config:
            if getattr(mw.addonManager, "getConfig", None):
                config=mw.addonManager.getConfig(__name__)
            else:
                moduleDir, _ = os.path.split(__file__)
                path = os.path.join(moduleDir, 'config.json')
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        data=f.read()
                    config=json.loads(data)

        if config:
            self.hotkey=config.get('hotkey','Shift+a')


    def onShowQuestion(self):  #for test previews
        showText("Hotkey is "+self.hotkey)
        #Now try changing the key using addonManager21's config manager

test=AddonManTest()
