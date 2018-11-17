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
        addHook('showQuestion', self.onShowQuestion) #for test previews
        addHook('profileLoaded', self.onProfileLoaded)

    def onProfileLoaded(self):
        self.setHotkeys()
        mw.progress.timer(1000,self.setHotkeysCallback,False)

    def setHotkeysCallback(self):
        try: #Must be loaded after profile loads, after addonmanger21 loads.
            mw.addonManager.setConfigUpdatedAction(__name__, self.setHotkeys) 
        except AttributeError: pass

    def setHotkeys(self, config=None):
        if not config:
            try:
                config=mw.addonManager.getConfig(__name__)
            except AttributeError:
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
