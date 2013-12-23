import Live
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.DeviceComponent import DeviceComponent


class CMDChannelStripComponent(ChannelStripComponent):
	""" Class extending CSC to have two buttons for toggling crossfader assign"""
	_active_instances = []

	@staticmethod
	def set_log(func):
		CMDChannelStripComponent.log_message = func

	def update(self):
		self._set_device_parameters()
		CMDChannelStripComponent.log_message("UPDATE Channel strip!!")
		super(CMDChannelStripComponent, self).update()

	def __init__(self):
		ChannelStripComponent.__init__(self)
		self._first_device = DeviceComponent()
		self._assign_a = None
		self._assign_b = None
		self._device_button1 = None
		self._device_button2 = None
		self._device_button3 = None
		self._device_button4 = None

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

	def set_device_buttons(self, button1, button2, button3, button4):
		self._device_button1 = button1
		self._device_button2 = button2
		self._device_button3 = button3
		self._device_button4 = button4

		self._set_device_parameters()
		self._track.add_devices_listener(self._on_change_devices)

	def _set_device_parameters(self):
		if self._track is not None and len(self._track.devices) > 0:
			self._first_device.set_device(self._track.devices[0])
			self._first_device.set_parameter_controls(
				tuple([self._device_button1, self._device_button2, self._device_button3, self._device_button4]))
		else:
			self._first_device.set_device(None)

	def _on_change_devices(self):
		CMDChannelStripComponent.log_message("DEVICE changed")
		self._set_device_parameters()

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
		elif self._assign_a != None and self._assign_b != None:
			self._assign_b.turn_off()
			self._assign_a.turn_off()

	def disconnect(self):
		if self._assign_a != None:
			self._assign_a.remove_value_listener(self._assign_a_value)
			self._assign_a.reset()
			self._assign_a = None
		if self._assign_b != None:
			self._assign_b.remove_value_listener(self._assign_b_value)
			self._assign_b.reset()
			self._assign_b = None
		super(CMDChannelStripComponent, self).update()
