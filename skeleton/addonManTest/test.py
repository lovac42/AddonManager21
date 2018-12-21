import os
from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from aqt.utils import showText
from codecs import open
from anki.utils import json
from .config import *


ADDON_NAME='test'

class AddonManTest:
    def __init__(self):
        self.config=Config(ADDON_NAME)
        # addHook(ADDON_NAME+".configLoaded", self.onConfigLoaded)

        #for test previews
        addHook('showQuestion', self.onShowQuestion) 

    def onShowQuestion(self):  #for test previews
        hotkey=self.config.get('hotkey','Shift+a')
        showText("Hotkey is "+hotkey)
        #Now try changing the key using addonManager21's config manager

test=AddonManTest()
