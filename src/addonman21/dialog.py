# -*- coding: utf-8 -*-
# Files are backported from anki-2.1.5 src with a few mods here and there.
# Support: https://github.com/lovac42/AddonManager21
# //------------------------------------------------
# //------------------------------------------------

# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import aqt, os, re
from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from aqt.utils import getText, tooltip, showText, showInfo, showWarning, openLink
from codecs import open
from anki.utils import json
from aqt.addons import GetAddons
from .forms.addons import AddonsDialog_Ui_Dialog
from .confEd import ConfigEditor


class AddonsDialog(QDialog):

    def __init__(self, addonsManager):
        QDialog.__init__(self, mw)
        self.mgr = addonsManager
        self.mw = mw

        f = self.form = AddonsDialog_Ui_Dialog()
        f.setupUi(self)
        f.getAddons.clicked.connect(self.onGetAddons)
        f.checkForUpdates.clicked.connect(self.onCheckForUpdates)
        # f.toggleEnabled.clicked.connect(self.onToggleEnabled)
        f.viewPage.clicked.connect(self.onViewPage)
        # f.viewFiles.clicked.connect(self.onViewFiles)
        # f.delete_2.clicked.connect(self.onDelete)
        f.config.clicked.connect(self.onConfig)
        self.form.addonList.currentRowChanged.connect(self._onAddonItemSelected)
        self.form.addonList.itemDoubleClicked.connect(self.onConfig)




        self.redrawAddons()
        self.show()

    def redrawAddons(self):
        self.addons = [(self.annotatedName(d), d) for d in self.mgr.allAddons()]
        self.addons.sort()
        self.form.addonList.clear()
        self.form.addonList.addItems([r[0] for r in self.addons])
        if self.addons:
            self.form.addonList.setCurrentRow(0)

    def _onAddonItemSelected(self, row_int):
        try:
            addon = self.addons[row_int][1]
        except IndexError:
            addon = ''
        # self.form.viewPage.setEnabled(bool (re.match(r"^\d+$", addon)))

    def annotatedName(self, dir):
        meta = self.mgr.addonMeta(dir)
        buf = self.mgr.addonName(dir)
        if meta.get('disabled'):
            buf += _(" (disabled)")
        return buf

    def selectedAddons(self):
        idxs = [x.row() for x in self.form.addonList.selectedIndexes()]
        return [self.addons[idx][1] for idx in idxs]

    def onlyOneSelected(self):
        dirs = self.selectedAddons()
        if len(dirs) != 1:
            showInfo(_("Please select a single add-on first."))
            return
        return dirs[0]

    def onToggleEnabled(self):
        for dir in self.selectedAddons():
            self.mgr.toggleEnabled(dir)
        self.redrawAddons()

    def onViewPage(self):
        addon = self.onlyOneSelected()
        if not addon: return

        try:
            meta = self.mgr.addonMetaID(addon)
            aoid=meta.get('addonID',None)
            assert aoid
        except:
            meta = self.mgr.addonMeta(addon)
            id,ok=getText('Enter missing addonID')
            if not ok: return
            meta['addonID'] = aoid = id
            self.mgr.writeAddonMetaID(addon, meta)

        if re.match(r"^\d+$", aoid):
            openLink(aqt.appShared + "info/{}".format(aoid))
        else:
            showWarning(_("Add-on was not downloaded from AnkiWeb."))

    def onViewFiles(self):
        # if nothing selected, open top level folder
        selected = self.selectedAddons()
        if not selected:
            openFolder(self.mgr.addonsFolder())
            return

        # otherwise require a single selection
        addon = self.onlyOneSelected()
        if not addon:
            return
        path = self.mgr.addonsFolder(addon)
        openFolder(path)

    def onDelete(self):
        selected = self.selectedAddons()
        if not selected:
            return
        if not askUser(ngettext("Delete the %(num)d selected add-on?",
                                "Delete the %(num)d selected add-ons?",
                                len(selected)) %
                               dict(num=len(selected))):
            return
        for dir in selected:
            self.mgr.deleteAddon(dir)
        self.redrawAddons()

    def onGetAddons(self):
        GetAddons(self.mw)

    def onCheckForUpdates(self):
        updated = self.mgr.checkForUpdates()
        if not updated:
            tooltip(_("No updates available."))
        else:
            names = [self.mgr.addonName(d) for d in updated]
            showText('New Updates:\n'+"\n  ".join(names))
            # if askUser(_("Update the following add-ons?") +
                               # "\n" + "\n".join(names)):
                # log, errs = self.mgr.downloadIds(updated)
                # if log:
                    # tooltip("\n".join(log), parent=self)
                # if errs:
                    # showWarning("\n".join(errs), parent=self)
                # self.redrawAddons()

    def onConfig(self):
        addon = self.onlyOneSelected()
        if not addon:
            return

        # does add-on manage its own config?
        act = self.mgr.configAction(addon)
        if act:
            act()
            return

        conf = self.mgr.getConfig(addon)
        if conf is None:
            showInfo(_("Add-on has no configuration."))
            return

        ConfigEditor(self, addon, conf)

