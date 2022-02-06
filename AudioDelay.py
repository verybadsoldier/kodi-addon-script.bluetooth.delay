import xbmc
from xml.dom import minidom
import xbmcaddon
import xbmcgui
import os
import time
import xbmcvfs

import sys
if sys.version > '3':
    xbmc.translatePath = xbmcvfs.translatePath

integer_types = (int)

Addon = xbmcaddon.Addon('script.bluetooth.delay')

line1 = Addon.getSetting('line1')
line2 = Addon.getSetting('line2')
t = 1000


def calcNumSteps(current, requested):
    requested = requested / 1000.0

    current = round(float(current), 3)
    xbmc.log('calcNumSteps - current: {}, requested: {}'.format(current, requested), xbmc.LOGINFO)

    return int(((float(requested) * 1000000) - (float(current) * 1000000)) / 25000)


def waitForMtimeChange(filepath, refmtime):
    while True:
        curmtime = os.path.getmtime(filepath)
        if curmtime != refmtime:
            return
        time.sleep(0.01)


def getGuisettingsPath():
    return xbmc.translatePath('special://profile/guisettings.xml')


def showDelayInfo():
    sourcesXML = minidom.parse(getGuisettingsPath())
    sources = sourcesXML.getElementsByTagName('audiodelay')[0].firstChild.nodeValue
    
    if float(sources) > 0:
        n = Addon.getLocalizedString(30021)
    elif float(sources) < 0:
        n = Addon.getLocalizedString(30022)
    elif float(sources) == 0:
        n = Addon.getLocalizedString(30023)
    
    if float(sources) == -0.000000:
        sources = "0.000000"
    
    xbmcgui.Dialog().notification(format(float(sources), '.3f') + n,line2, "",t)


def setDelayValue(delayVal):
    guisettings_path = getGuisettingsPath()
    time1 = os.path.getmtime(guisettings_path)

    xbmc.executebuiltin('ActivateWindow(osdaudiosettings)')
    xbmc.executebuiltin('SetFocus(-73)')
    xbmc.executebuiltin("Action(select)")
    xbmc.executebuiltin('SetFocus(11)')
    xbmc.executebuiltin("Action(select)", wait=True)

    waitForMtimeChange(guisettings_path, time1)

    sourcesXML = minidom.parse(guisettings_path)
    sources = sourcesXML.getElementsByTagName('audiodelay')[0].firstChild.nodeValue

    numSteps = calcNumSteps(sources, delayVal)

    xbmc.log('numSteps: {}'.format(numSteps), xbmc.LOGINFO)

    for _ in range(abs(numSteps)):
        if numSteps > 0.0:
            xbmc.executebuiltin("Action(AudioDelayPlus)")
        else:
            xbmc.executebuiltin("Action(AudioDelayMinus)")

    time3 = os.path.getmtime(guisettings_path)
    xbmc.executebuiltin('SetFocus(-73)')
    xbmc.executebuiltin("Action(select)")
    xbmc.executebuiltin('SetFocus(11)')
    xbmc.executebuiltin("Action(select)", wait=True)
    time.sleep(1.0)
    xbmc.executebuiltin("Action(close)", wait=True)

    waitForMtimeChange(guisettings_path, time3)
    
    showDelayInfo()


def main(requestedDelayValue):
    xbmc.log('########### 1: {}'.format(requestedDelayValue), xbmc.LOGINFO)

    if (xbmc.getCondVisibility('Player.HasMedia') == False):
        xbmcgui.Dialog().notification("",Addon.getLocalizedString(30015), "",t)
        return


    check = getGuisettingsPath()
    time1 = os.path.getmtime(check)

    xbmc.executebuiltin('ActivateWindow(osdaudiosettings)')
    xbmc.executebuiltin('SetFocus(-73)')
    xbmc.executebuiltin("Action(select)")
    xbmc.executebuiltin('SetFocus(11)')
    xbmc.executebuiltin("Action(select)", wait=True)

    waitForMtimeChange(check, time1)

    sourcesXML = minidom.parse(getGuisettingsPath())
    sources = sourcesXML.getElementsByTagName('audiodelay')[0].firstChild.nodeValue

    if requestedDelayValue is not None:
        # use delay value provided by arguments
        setDelayValue(requestedDelayValue)
    else:
        s = float(Addon.getSetting('Mode'))
        d1 =  float(Addon.getSetting('Device1'))
        d2 =  float(Addon.getSetting('Device2'))

        sources = round(.0025000 * round(float(sources)/.0025000),6)

        y = ((float(d2) * 1000000) - (float(d1) * 1000000)) / 25000
        y = int(y)
        y = abs(y)

        if d2 == d1:
            xbmc.executebuiltin("Action(close)")
            Addon.openSettings()
        elif float(sources) == d1:
            for x in range(y):
                if float(d2) > float(d1):
                    xbmc.executebuiltin("Action(AudioDelayPlus)")
                if float(d2) < float(d1):
                    xbmc.executebuiltin("Action(AudioDelayMinus)")
            time3 = os.path.getmtime(check)
            xbmc.executebuiltin('SetFocus(-73)')
            xbmc.executebuiltin("Action(select)")
            xbmc.executebuiltin('SetFocus(11)')
            xbmc.executebuiltin("Action(select)", wait=True)
            time.sleep(s)
            xbmc.executebuiltin("Action(close)", wait=True)

            waitForMtimeChange(check, time3)

            sourcesXML = minidom.parse(getGuisettingsPath())
            sources = sourcesXML.getElementsByTagName('audiodelay')[0].firstChild.nodeValue
            if float(sources) > 0:
                n = Addon.getLocalizedString(30021)
            if float(sources) < 0:
                n = Addon.getLocalizedString(30022)
            if float(sources) == 0:
                n = Addon.getLocalizedString(30023)
            if float(sources) == -0.000000:
                sources = "0.000000"
            xbmcgui.Dialog().notification(format(float(sources), '.3f') + n,line2, "",t)


        elif float(sources) == d2:
            for x in range(y):
                if float(d1) > float(d2):
                    xbmc.executebuiltin("Action(AudioDelayPlus)")
                if float(d1) < float(d2):
                    xbmc.executebuiltin("Action(AudioDelayMinus)")
            time3 = os.path.getmtime(check)
            xbmc.executebuiltin('SetFocus(-73)')
            xbmc.executebuiltin("Action(select)")
            xbmc.executebuiltin('SetFocus(11)')
            xbmc.executebuiltin("Action(select)", wait=True)
            time.sleep(s)
            xbmc.executebuiltin("Action(close)", wait=True)

            waitForMtimeChange(check, time3)

            sourcesXML = minidom.parse(getGuisettingsPath())
            sources = sourcesXML.getElementsByTagName('audiodelay')[0].firstChild.nodeValue
            if float(sources) > 0:
                n = Addon.getLocalizedString(30021)
            if float(sources) < 0:
                n = Addon.getLocalizedString(30022)
            if float(sources) == 0:
                n = Addon.getLocalizedString(30023)
            if float(sources) == -0.000000:
                sources = "0.000000"
            xbmcgui.Dialog().notification(format(float(sources), '.3f') + n,line1, "",t)
        else:
            y = ((float(sources) * 1000000) - (float(d2) * 1000000)) / 25000
            y = str(y)[-2:] == '.0'  and int(y) or y
            if isinstance(y, float):
                if float(sources) > 0:
                    n = Addon.getLocalizedString(30021)
                if float(sources) < 0:
                    n = Addon.getLocalizedString(30022)
                if float(sources) == 0:
                    n = Addon.getLocalizedString(30023)
                sources = sourcesXML.getElementsByTagName('audiodelay')[0].firstChild.nodeValue
                xbmcgui.Dialog().notification(format(float(sources), '.6f') + n," ", "",t*6)
                dialog = xbmcgui.Dialog()
                ok = dialog.ok(Addon.getLocalizedString(30016), Addon.getLocalizedString(30017))
                if ok == True:
                    xbmc.executebuiltin('PlayerControl(stop)')
                    xbmc.executebuiltin('ActivateWindow(osdaudiosettings)')
                    xbmc.executebuiltin('SetFocus(-73)')
                    xbmc.executebuiltin("Action(select)")
                    xbmc.executebuiltin('SetFocus(11)')
                    xbmc.executebuiltin("Action(select)", wait=True)
                    time.sleep(s)
                    xbmc.executebuiltin("Action(close)", wait=True)
                    sourcesXML = minidom.parse(getGuisettingsPath())
                    sources = sourcesXML.getElementsByTagName('audiodelay')[0].firstChild.nodeValue
                    xbmcgui.Dialog().notification(format(float(sources), '.3f') + Addon.getLocalizedString(30019),"","", t*6)
                    dialog.ok(Addon.getLocalizedString(30016), Addon.getLocalizedString(30018))
                    return
                else:
                    xbmc.executebuiltin("Action(close)")
                    return
            if isinstance(y, integer_types):
                y = int(y)
                y = abs(y)

                if float(sources) > float(d2):
                    for x in range(y):
                        xbmc.executebuiltin("Action(AudioDelayMinus)")
                if float(sources) < float(d2):
                    for x in range(y):
                        xbmc.executebuiltin("Action(AudioDelayPlus)")
            time3 = os.path.getmtime(check)
            xbmc.executebuiltin('SetFocus(-73)')
            xbmc.executebuiltin("Action(select)")
            xbmc.executebuiltin('SetFocus(11)')
            xbmc.executebuiltin("Action(select)", wait=True)
            time.sleep(s)
            xbmc.executebuiltin("Action(close)", wait=True)

            waitForMtimeChange(check, time3)

            sourcesXML = minidom.parse(getGuisettingsPath())
            sources = sourcesXML.getElementsByTagName('audiodelay')[0].firstChild.nodeValue
            if float(sources) > 0:
                n = Addon.getLocalizedString(30021)
            if float(sources) < 0:
                n = Addon.getLocalizedString(30022)
            if float(sources) == 0:
                n = Addon.getLocalizedString(30023)
            if float(sources) == -0.000000:
                sources = "0.000000"
            xbmcgui.Dialog().notification(format(float(sources), '.3f') + n,line2, "",t)
