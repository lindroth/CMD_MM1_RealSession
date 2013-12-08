from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import InputControlElement
from _Framework.NotifyingControlElement import NotifyingControlElement

COLOR_MAP = [0, 1, 2, 3, 4, 5, 6]

MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
MIDI_PB_TYPE = 2
MIDI_MSG_TYPES = (MIDI_NOTE_TYPE,
				  MIDI_CC_TYPE,
				  MIDI_PB_TYPE)
MIDI_NOTE_ON_STATUS = 144
MIDI_NOTE_OFF_STATUS = 128
MIDI_CC_STATUS = 176
MIDI_PB_STATUS = 224


class SimpleButtonElement(ButtonElement):
	__module__ = __name__
	__doc__ = ' Special button class that can be configured with custom on- and off-values, some of which flash at specified intervals called by _Update_Display'

	def __init__(self, is_momentary, msg_type, channel, identifier):
		ButtonElement.__init__(self, is_momentary, msg_type, channel, identifier)

	def turn_on(self):
		self.send_value(1)

	def turn_off(self):
		self.send_value(0)

	def flash(self):
		self.send_value(2)
		