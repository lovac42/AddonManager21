# Files are backported from anki-2.1.5 src

import aqt, os, re
from aqt import mw
from aqt.qt import *
from aqt.utils import getText, tooltip, showText, showInfo
from codecs import open
from anki.utils import json
from aqt.addons import AddonManager
from .dialog import AddonsDialog


class AddonManager21(AddonManager):
    _configButtonActions = {}
    _configUpdatedActions = {}

    def __init__(self, mw):
        self.mw = mw
        action = QAction('>> AM21 Configurations <<', mw)
        action.triggered.connect(self.onAddonsDialog)
        mw.form.menuPlugins.addAction(action)

    def setConfigUpdatedAction(self, module, fn):
        addon = self.addonFromModule(module)
        self._configUpdatedActions[addon] = fn

    def configUpdatedAction(self, addon):
        return self._configUpdatedActions.get(addon)

    def getConfig(self, module):
        addon = self.addonFromModule(module)
        # get default config
        config = self.addonConfigDefaults(addon)
        if config is None:
            return None
        # merge in user's keys
        meta = self.addonMeta(addon)
        userConf = meta.get("config", {})
        config.update(userConf)
        return config

    def allAddons(self):
        l = []
        for d in os.listdir(self.addonsFolder()):
            path = self.addonsFolder(d)
            if not os.path.exists(os.path.join(path, "__init__.py")):
                continue
            l.append(d)
        l.sort()
        if os.getenv("ANKIREVADDONS", ""):
            l = reversed(l)
        return l

    def addonsFolder(self, dir=None):
        root = self.mw.pm.addonFolder()
        if not dir:
            return root
        return os.path.join(root, dir)

    def _addonMetaPath(self, dir):
        return os.path.join(self.addonsFolder(dir), "meta.json")

    def addonMeta(self, dir):
        path = self._addonMetaPath(dir)
        try:
            with open(path, encoding="utf8") as f:
                return json.load(f)
        except:
            return dict()

    def addonName(self, dir):
        return self.addonMeta(dir).get("name", dir)

    def configAction(self, addon):
        return self._configButtonActions.get(addon)

    def configUpdatedAction(self, addon):
        return self._configUpdatedActions.get(addon)

    def addonConfigHelp(self, dir):
        path = os.path.join(self.addonsFolder(dir), "config.md")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return f.read().replace('\n','<br>')
        else:
            return ""

    def onAddonsDialog(self, path=None):
        AddonsDialog(self)
 
    def writeConfig(self, module, conf):
        addon = self.addonFromModule(module)
        meta = self.addonMeta(addon)
        meta['config'] = conf
        self.writeAddonMeta(addon, meta)

    def writeAddonMeta(self, dir, meta):
        path = self._addonMetaPath(dir)
        with open(path, "w", encoding="utf8") as f:
            json.dump(meta, f)

    def addonFromModule(self, module):
        return module.split(".")[0]

    def addonsFolder(self, dir=None):
        root = self.mw.pm.addonFolder()
        if not dir:
            return root
        return os.path.join(root, dir)

    def addonConfigDefaults(self, dir):
        path = os.path.join(self.addonsFolder(dir), "config.json")
        try:
            with open(path, encoding="utf8") as f:
                return json.load(f)
        except:
            return None
