# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2019 Lovac42
# Support: https://github.com/lovac42/AddonManager21
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import aqt
from aqt import mw
from anki.hooks import wrap
from .main import *

def setupProfile(self):
    if not self.addon_loaded:
        self.addonManager = AddonManager21(self)
        self.addon_loaded=True

aqt.main.AnkiQt.addon_loaded=False
aqt.main.AnkiQt.setupProfile=wrap(aqt.main.AnkiQt.setupProfile, setupProfile, 'before')
