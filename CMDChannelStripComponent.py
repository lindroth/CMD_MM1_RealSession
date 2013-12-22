import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.DeviceComponent import DeviceComponent


class CMDChannelStripComponent(ChannelStripComponent):
	""" Class extending CSC to have two buttons for toggling crossfader assign"""
	_active_instances = []

	def __init__(self):
		ChannelStripComponent.__init__(self)
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

	def set_device_buttons(self, log, button1, button2, button3, button4):
		self.log = log
		self._first_device = DeviceComponent()
		self._device_button1 = button1
		self._device_button2 = button2
		self._device_button3 = button3
		self._device_button4 = button4

		self._set_device_parameters()

		self._track.add_devices_listener(self._on_add_devices)

	#Don't forget to implement remove device listener
	def _set_device_parameters(self):
		if len(self._track.devices) > 0:
			self.log.log_message("Setting parameters on device")
			self._first_device.set_device(self._track.devices[0])
			self._first_device.set_parameter_controls(
				tuple([self._device_button1, self._device_button2, self._device_button3, self._device_button4]))

	def _on_add_devices(self):
		self.log.log_message("Listener called")
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
        