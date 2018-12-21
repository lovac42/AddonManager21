# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/AddonManager21
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook, runHook
from codecs import open
from anki.utils import json
import os


class Config():
    config = None

    def __init__(self, addonName):
        self.addonName=addonName
        addHook('profileLoaded', self.onProfileLoaded)

    def onProfileLoaded(self):
        mw.progress.timer(300,self.setConfig,False)

    def get(self, key, default=None):
        return self.config.get(key, default);

    def setConfig(self):
        if getattr(mw.addonManager, "getConfig", None):
            config=mw.addonManager.getConfig(__name__)
            mw.addonManager.setConfigUpdatedAction(__name__, self.updateConfig)
        else:
            config=self.readConfig('config.json')
        self.updateConfig(config)
        runHook(self.addonName+'.configLoaded')

    def updateConfig(self, config):
        self.config=config

    def readConfig(self, fname):
        moduleDir, _ = os.path.split(__file__)
        path = os.path.join(moduleDir,fname)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data=f.read()
            return json.loads(data)

