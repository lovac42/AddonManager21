# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2019 Lovac42
# Support: https://github.com/lovac42/AddonManager21
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# Original Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# Files are backported from anki-2.1.5 src with a few mods here and there.

import aqt, os, re, sys
from aqt import mw
from aqt.qt import *
from aqt.utils import getText, tooltip, showText, showInfo
from codecs import open
from anki.utils import json
from aqt.addons import AddonManager
from .dialog import AddonsDialog
import urllib2


USER_AGENT='Anki 2.0 Forever'


class AddonManager21(AddonManager):
    _configButtonActions = {}
    _configUpdatedActions = {}

    def __init__(self, mw):
        self.mw = mw
        self._menus = []
        action = QAction('Addon Configurations...', mw)
        action.triggered.connect(self.onAddonsDialog)
        mw.form.menuTools.addAction(action)


    def rebuildAddonsMenu(self):
        return

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
        # config.update(userConf)
        config=nestedUpdate(config,userConf) #update nested dicts
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

    def addonName(self, dir):
        return self.addonMetaID(dir).get("name", dir)

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

#Use for writing addonID from custom input
    def writeAddonMetaID(self, dir, meta):
        path = os.path.join(self.addonsFolder(dir), "meta_id.json")
        with open(path, "w", encoding="utf8") as f:
            json.dump(meta, f)

    def addonFromModule(self, module):
        return module.split(".")[0]

    def addonsFolder(self, dir=None):
        root = self.mw.pm.addonFolder()
        if not dir:
            return root
        return os.path.join(root, dir)

    def managedAddons(self):
        self.addonSID={}
        addons=[]
        for dir in self.allAddons():
            try:
                meta = self.addonMetaID(dir)
                aoid=meta.get('addonID',None)
                assert aoid
                addons.append(aoid)
                self.addonSID[aoid]=dir
            except:
                continue
        return addons


    # Updating
    ######################################################################

    def checkForUpdates(self):
        # get mod times
        self.mw.progress.start(immediate=True)
        try:
            # ..of enabled items downloaded from ankiweb
            addons = self.managedAddons()
            mods = []
            while addons:
                chunk = addons[:25]
                del addons[:25]
                mods.extend(self._getModTimes(None, chunk))
            return self._updatedIds(mods)
        finally:
            self.mw.progress.finish()

    def _getModTimes(self, client, chunk):
        try:
            url=aqt.appShared + "updates/" + ",".join(chunk)
            crawler = urllib2.build_opener()
            crawler.addheaders = [('User-agent', USER_AGENT)]
            c = crawler.open(url)
            data=c.read()
            return json.loads(data)
        except ValueError:
           utils.showInfo("Not a valid url")
           return
        except urllib2.HTTPError as error:
            showWarning('The remote server has returned an error:'
                        ' HTTP Error {} ({})'.format(error.code,error.reason))
            return

    def _updatedIds(self, mods):
        updated = []
        for dir, ts in mods:
            if not ts: continue #null for anki 2.0 only addons, use a fake __init__ file to set time on server.

            sid = self.addonSID.get(str(dir),None)
            if not sid: continue

            meta=self.addonMeta(sid)
            mod=int(meta.get("mod","-1"))
            if mod < ts:
                updated.append(sid)
                #Mark as updated
                meta['mod'] = str(ts)
                self.writeAddonMeta(sid, meta)
        return updated



#MODS FROM: https://github.com/Arthur-Milchior/anki-debug-json/blob/master/jsonErrorMessage.py
    def addonConfigDefaults(self, dir):
        path = os.path.join(self.addonsFolder(dir), "config.json")
        try:
            with open(path, encoding="utf8") as f:
                t=f.read()
                try:
                    return json.loads(t)
                except Exception as e:
                    print "Here is a JSON error in default config of addon {dir}:".format(dir=sys.stderr)
                    print str(e)
                    print "\n\n===================\n\nCopy and save past config to be sure that it is not overwritten by accident. Past config was {t}".format(t=sys.stderr)
                    return dict()
        except:
            return None


#MODS FROM: https://github.com/Arthur-Milchior/anki-debug-json/blob/master/jsonErrorMessage.py
    def addonMeta(self, dir):
        path = self._addonMetaPath(dir)
        try:
            with open(path, encoding="utf8") as f:
                t=f.read()
                try:
                    return json.loads(t)
                except Exception as e:
                    print "Here is a JSON error in current config of addon {dir}:".format(dir=sys.stderr)
                    print str(e)
                    print "\n\n===================\n\n \
Copy and save past config to be sure that it is not overwritten by accident. Past config was {t}".format(t=sys.stderr)
        except: pass
        return dict()

    def addonMetaID(self, dir):
        path = os.path.join(self.addonsFolder(dir), "meta_id.json")
        try:
            with open(path, encoding="utf8") as f:
                t=f.read()
                try:
                    return json.loads(t)
                except Exception as e:
                    print "Here is a JSON error in current config of addon {dir}:".format(dir=sys.stderr)
                    print str(e)
                    print "\n\n===================\n\n \
Copy and save past config to be sure that it is not overwritten by accident. Past config was {t}".format(t=sys.stderr)
        except: pass
        return dict()



#update nested dicts ===============================
# https://stackoverflow.com/questions/3232943/
import collections
def nestedUpdate(d,u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            d[k] = nestedUpdate(d.get(k, {}), v)
        else:
            d[k] = v
    return d
