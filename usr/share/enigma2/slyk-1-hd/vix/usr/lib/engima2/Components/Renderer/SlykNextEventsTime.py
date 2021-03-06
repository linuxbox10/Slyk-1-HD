from Components.VariableText import VariableText
from Components.Element import cached
from Renderer import Renderer
from enigma import eLabel, eEPGCache
from time import localtime, strftime


class SlykNextEventsTime(VariableText, Renderer):
    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.epgcache = eEPGCache.getInstance()

    def applySkin(self, desktop, parent):
        self.number = 3
        attribs = []
        for (attrib, value) in self.skinAttributes:
            if attrib == "number":
                self.number = int(value)
            else:
                attribs.append((attrib, value))
        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = eLabel

    def connect(self, source):
        Renderer.connect(self, source)
        self.changed((self.CHANGED_DEFAULT,))

    def changed(self, what):
        if what[0] == self.CHANGED_CLEAR:
            self.text = ""
        else:
            list = self.epgcache.lookupEvent(['BDT', (self.source.text, 0, -1, 360)])
            text = ""
            if len(list):
                i = 1
                for event in list:
                    if len(event) == 3 and i == int(self.number):
                        t = localtime(event[0])
                        if int(strftime("%H", t)) >= 12:
                            timesuffix = _('pm')
                        else:
                            timesuffix = _('am')
                        text = strftime("%l", t) + "." + strftime("%M", t) + timesuffix
                        break
                    i = i + 1
                    if i >= len(list):
                        break
            self.text = text
