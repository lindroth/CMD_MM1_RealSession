from CMDChannelStripComponent import CMDChannelStripComponent
from _Framework.MixerComponent import MixerComponent


class CMDMixerComponent(MixerComponent):
	# def __init__(self, num_tracks, num_returns=0, with_eqs=False, with_filters=False):
	# 	MixerComponent.__init__(self, num_tracks, num_returns=0, with_eqs=False, with_filters=False)
	# 	self.logger = None

	def _create_strip(self):
		return CMDChannelStripComponent()

	def update(self):
		super(CMDMixerComponent, self).update()
		CMDMixerComponent.log_message("UPDATE!!")

	def setLog(self, logger):
		global log
		log = logger

	def _reassign_tracks(self):
		CMDMixerComponent.log_message("REASSIGN")
		super(CMDMixerComponent, self)._reassign_tracks()


	def on_track_list_changed(self):
		CMDMixerComponent.log_message("on track list changed")
		super(CMDMixerComponent, self).on_track_list_changed()

	@staticmethod
	def set_log(func):
		CMDMixerComponent.log_message = func
