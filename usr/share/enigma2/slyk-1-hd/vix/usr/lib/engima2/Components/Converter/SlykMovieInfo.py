from Components.Converter.Converter import Converter
from Components.Element import cached, ElementError
from enigma import iServiceInformation, eServiceReference
from ServiceReference import ServiceReference

class SlykMovieInfo(Converter, object):
	MOVIE_META_DESCRIPTION = 1 # just meta description when available

	def __init__(self, type):
		if type == "MetaDescription":
			self.type = self.MOVIE_META_DESCRIPTION
		else:
			raise ElementError("'%s' is not <MetaDescription> for MovieInfo converter" % type)
		Converter.__init__(self, type)

	@cached
	def getText(self):
		service = self.source.service
		info = self.source.info
		event = self.source.event
		if info and service:	
			if self.type == self.MOVIE_META_DESCRIPTION:
				return ((event and (event.getExtendedDescription() or event.getShortDescription()))
				    or info.getInfoString(service, iServiceInformation.sDescription))
		return ""

 
	text = property(getText)