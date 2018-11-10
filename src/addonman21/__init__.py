# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/AddonManager21
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.2

import aqt
from aqt import mw
from anki.hooks import addHook
from .main import *

def setupAddons(self):
    if not self.addon_loaded:
        self.addonManager = AddonManager21(self)
        self.addon_loaded=True

aqt.main.AnkiQt.addon_loaded=False
aqt.main.AnkiQt.setupAddons=setupAddons
addHook('profileLoaded', mw.setupAddons)
