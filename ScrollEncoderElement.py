from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import InputControlElement
from _Framework.SessionComponent import SessionComponent

class ScrollEncoderElement(EncoderElement):
	def __init__(self, msg_type, channel, identifier, map_mode, session):
		EncoderElement.__init__(self, msg_type, channel, identifier, map_mode)
		self.set_report_values(True, True)
		self.session = session
	def notify_value(self, value):
		super(EncoderElement, self).notify_value(value)
		if value>63 and self.session._can_bank_down() == True:
				self.session._change_offsets(0, 1)
		elif self.session._can_bank_up() == True:
				self.session._change_offsets(0, -1)
		if self.normalized_value_listener_count():
			normalized = self.relative_value_to_delta(value) / 64.0 * self.encoder_sensitivity
			self.notify_normalized_value(normalized)