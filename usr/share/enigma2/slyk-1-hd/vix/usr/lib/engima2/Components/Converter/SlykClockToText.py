from Converter import Converter
from time import localtime, strftime
from Components.Element import cached


class SlykClockToText(Converter, object):
	DEFAULT = 0
	FORMAT = 1
	SLYK_AS_LENGTH = 2
	SLYK_Q_DATE = 3
	SLYK_HD_DATE = 4
	SLYK_HD_TIME = 5
	SLYK_HD_STARTPROGRESS = 6

	def __init__(self, type):
		Converter.__init__(self, type)

		self.fix = ""
		if ';' in type:
			type, self.fix = type.split(';')

		if type == "SlykAsLength":
			self.type = self.SLYK_AS_LENGTH
		elif type == "SlykQDate":
			self.type = self.SLYK_Q_DATE
		elif type == "SlykHDDate":
			self.type = self.SLYK_HD_DATE
		elif type == "SlykHDTime":
			self.type = self.SLYK_HD_TIME
		elif "Format" in type:
			self.type = self.FORMAT
			self.fmt_string = type[7:]
		else:
			self.type = self.DEFAULT

	@cached
	def getText(self):
		time = self.source.time
		
		if time is None:
			return ""

		def fix_space(string):
			if "Proportional" in self.fix and t.tm_hour < 10:
				return " " + string
			if "NoSpace" in self.fix:
				return string.lstrip(' ')
			return string

		if self.type == self.SLYK_AS_LENGTH:
		# below is 9 to not show duration on directories for movies
			if time <= 9:
				return ""
			else:
				if time / 3600 < 1:
					return ngettext("%d Min", "%d Mins", (time / 60)) % (time / 60)
				elif time / 60 % 60 == 0:
					return ngettext("%d Hour", "%d Hours", (time / 3600)) % (time / 3600)
				else:
					return "%dh %2dm" % (time / 3600, time / 60 % 60)
		
		t = localtime(time)
		
		if int(strftime("%H", t)) >= 12:
			timesuffix = _('pm')
		else:
			timesuffix = _('am')
			
		if self.type == self.DEFAULT:
			return fix_space(_("%2d:%02d") % (t.tm_hour, t.tm_min))
		elif self.type == self.SLYK_Q_DATE:
			d = _("%A, %l.%M") + _(timesuffix)
		elif self.type == self.SLYK_HD_DATE:
			d = _("%l.%M") + _(timesuffix) + _(" %a %d/%m")
		elif self.type == self.SLYK_HD_TIME:
			d = _("%l.%M") + _(timesuffix)
		elif self.type == self.FORMAT:
			d = self.fmt_string
		else:
			return "???"
			
		timetext = strftime(d, t) 
		
		return timetext.lstrip(' ')

	text = property(getText)
	