import xbmc
import xbmcaddon
import os
import xbmcvfs

import sys
if sys.version > '3':
    xbmc.translatePath = xbmcvfs.translatePath


def getArgDict():
	argd = {}
	for i in range(1, len(sys.argv)):
		tok = sys.argv[i].split('=')
		argd[tok[0]] = tok[i]
	return argd


Addon = xbmcaddon.Addon('script.bluetooth.delay')

argsd = getArgDict()
# delay value provided by argument
requestedDelayValue = int(argsd['delay']) if 'delay' in argsd else None

firstRun = Addon.getSetting('firstRun')
if firstRun == "false" and requestedDelayValue is None:
	import xbmcgui
	dialog = xbmcgui.Dialog()
	dialog.ok(Addon.getLocalizedString(30013), Addon.getLocalizedString(30014))
	Addon.setSettingBool('firstRun', 1)

d1 = Addon.getSetting('Device1')
d2 = Addon.getSetting('Device2')
script = xbmc.translatePath(os.path.join('special://home/addons/script.bluetooth.delay/AudioDelay.py'))

if d2 == d1 and requestedDelayValue is None:
	xbmcaddon.Addon().openSettings()
else:
	import AudioDelay
	AudioDelay.main(requestedDelayValue)
