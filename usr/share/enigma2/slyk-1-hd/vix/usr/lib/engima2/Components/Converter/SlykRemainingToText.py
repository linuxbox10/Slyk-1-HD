from Components.Converter.Converter import Converter
from Poll import Poll
from Components.Element import cached
from Components.config import config

class SlykRemainingToText(Poll, Converter, object):
	ONLY_MINUTE = 5

	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		if type == "OnlyMinute":
			self.type = self.ONLY_MINUTE
			
		if config.usage.swap_time_display_on_osd.value == "1" or config.usage.swap_time_display_on_osd.value == "3" or config.usage.swap_time_display_on_osd.value == "5":
			self.poll_interval = 1000
			self.poll_enabled = True
		if config.usage.swap_time_display_on_osd.value == "2" or config.usage.swap_time_display_on_osd.value == "4":
			self.poll_interval = 1000
			self.poll_enabled = True

	@cached
	def getText(self):
		time = self.source.time
		if time is None:
			return ""

		duration = 0
		elapsed = 0
		remaining = 0

		(duration, remaining) = self.source.time
				
		l = duration # Length
		p = elapsed # Position
		r = remaining  # Remaining

		if self.type == self.ONLY_MINUTE:
			if remaining is not None:
				return ngettext(_("Started %d min ago"), _("Started %d mins ago"), (r/60)) % (r/60)
		else:
			return "%d" % l

	text = property(getText)