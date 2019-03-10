# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2019 Lovac42
# Support: https://github.com/lovac42/AddonManager21
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# Original Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# Files are backported from anki-2.1.5 src with a few mods here and there.


import aqt, os, re
from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from aqt.utils import getText, tooltip, showText, showInfo
from codecs import open
from anki.utils import json
from .forms.addonconf import ConfigEditor_Ui_Dialog


class ConfigEditor(QDialog):

    def __init__(self, dlg, addon, conf):
        QDialog.__init__(self,dlg)
        self.addon = addon
        self.conf = conf
        self.mgr = dlg.mgr
        self.form = ConfigEditor_Ui_Dialog()
        self.form.setupUi(self)
        restore = self.form.buttonBox.button(QDialogButtonBox.RestoreDefaults)
        restore.clicked.connect(self.onRestoreDefaults)
        self.updateHelp()
        self.updateText(self.conf)
        self.show()

    def onRestoreDefaults(self):
        default_conf = self.mgr.addonConfigDefaults(self.addon)
        self.updateText(default_conf)

    def updateHelp(self):
        txt = self.mgr.addonConfigHelp(self.addon)
        if txt:
            self.form.label.setText(txt)
        else:
            self.form.scrollArea.setVisible(False)

    def updateText(self, conf):
        self.form.editor.setPlainText(
            json.dumps(conf,sort_keys=True,indent=4, separators=(',', ': ')))

    def accept(self):
        txt = self.form.editor.toPlainText()
        try:
            new_conf = json.loads(txt)
        except Exception as e:
            showInfo(_("Invalid configuration: ") + repr(e))
            return

        if new_conf != self.conf:
            self.mgr.writeConfig(self.addon, new_conf)
            # does the add-on define an action to be fired?
            act = self.mgr.configUpdatedAction(self.addon)
            if act:
                act(new_conf)

        super(ConfigEditor, self).accept()

