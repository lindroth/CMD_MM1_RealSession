import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.ChannelStripComponent import ChannelStripComponent


class CMDChannelStripComponent(ChannelStripComponent):
	""" Class extending CSC to have two buttons for toggling crossfader assign"""
	_active_instances = []

	def __init__(self):
		ChannelStripComponent.__init__(self)
		self._assign_a = None
		self._assign_b = None

	def set_assign_buttons(self, button1, button2):
		if button1 != self._assign_a:
			if self._assign_a != None:
				self._assign_a.remove_value_listener(self._assign_a_value)
				self._assign_a.reset()
			self._assign_a = button1
			self._assign_a != None and self._assign_a.add_value_listener(self._assign_a_value)
		if button2 != self._assign_b:
			if self._assign_b != None:
				self._assign_b.remove_value_listener(self._assign_b_value)
				self._assign_b.reset()
			self._assign_b = button2
			self._assign_b != None and self._assign_b.add_value_listener(self._assign_b_value)
		self.update()

	def _assign_a_value(self, value):

		if value > 0:
			if self._track.mixer_device.crossfade_assign == 0:
				self._track.mixer_device.crossfade_assign = 1
				self._assign_a.turn_off()
				self._assign_b.turn_off()
			else:
				self._track.mixer_device.crossfade_assign = 0
				self._assign_a.turn_on()
				self._assign_b.turn_off()
			if not self._assign_a != None:
				raise AssertionError
				if not isinstance(value, int):
					raise AssertionError
					if self.is_enabled():
						pass
						#self._track.mixer_device.crossfade_assign = 2

	def _assign_b_value(self, value):
		if value > 0:
			if self._track.mixer_device.crossfade_assign == 2:
				self._track.mixer_device.crossfade_assign = 1
				self._assign_a.turn_off()
				self._assign_b.turn_off()
			else:
				self._track.mixer_device.crossfade_assign = 2
				self._assign_b.turn_on()
				self._assign_a.turn_off()
			if not self._assign_b != None:
				raise AssertionError
				if not isinstance(value, int):
					raise AssertionError
					if self.is_enabled():
						pass
						#self._track.mixer_device.crossfade_assign = 127

	def _on_cf_assign_changed(self):
		if self._track != None and self._track != self.song().master_track and self._assign_a != None and self._assign_b != None:
			if self._track.mixer_device.crossfade_assign == 2:
				self._assign_a.turn_off()
				self._assign_b.turn_on()
			elif self._track.mixer_device.crossfade_assign == 1:
				self._assign_b.turn_off()
				self._assign_a.turn_off()
			else:
				self._assign_a.turn_on()
				self._assign_b.turn_off()


	def disconnect(self):
		if self._assign_a != None:
			self._assign_a.remove_value_listener(self._assign_a_value)
			self._assign_a.reset()
			self._assign_a = None
		if self._assign_b != None:
			self._assign_b.remove_value_listener(self._assign_b_value)
			self._assign_b.reset()
			self._assign_b = None
		super(CMDChannelScriptComponent, self).disconnect()
        