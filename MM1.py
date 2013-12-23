from __future__ import with_statement
import Live # This allows us (and the Framework methods) to use the Live API on occasion

from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.SliderElement import SliderElement # Class representing a slider on the controller

from ScrollEncoderElement import *
from ShiftableDeviceComponent import ShiftableDeviceComponent
from FlashingButtonElement import FlashingButtonElement # Custom code from Aumhaa/livid for creating flashing buttons
from MM1_Map import * # This contains your custom-tailored configuration/layout. This is really the only thing you should be editing.
from DetailViewControllerComponent import DetailViewControllerComponent
from CMDMixerComponent import CMDMixerComponent
from CMDChannelStripComponent import CMDChannelStripComponent
from SimpleButtonElement import *
from CMDVUMeters import *


#from CMDEncoderElement import CMDEncoderElement
# Global Variables
CHANNEL = 0 # assume channel is constant for everything

class MM1(ControlSurface):
	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		is_momentary = True
		self._timer = 0                             #used for flashing states, and is incremented by each call from self._update_display()
		self._touched = 0
		self.flash_status = 1 #

		with self.component_guard():
		# self._setup_transport_control()
			mixer = self.mixer_control()
			self.session_control(mixer)
			self.setup_device_control()

			self.vumeter = CMDVUMeters(self, EncoderElement(MIDI_CC_TYPE, CHANNEL, 80, Live.MidiMap.MapMode.absolute),
									   EncoderElement(MIDI_CC_TYPE, CHANNEL, 81, Live.MidiMap.MapMode.absolute))


	def mixer_control(self):
		is_momentary = True
		self.num_tracks = 4

		CMDMixerComponent.set_log(self.log_message)
		CMDChannelStripComponent.set_log(self.log_message)

		mixer = CMDMixerComponent(4, 0, False, False)
		mixer.name = 'Mixer'
		mixer.set_track_offset(0) #Sets start point for mixer strip (offset from left)
		for index in range(4):
			mixer.channel_strip(index).name = 'Mixer_ChannelStrip_' + str(index)
			mixer.channel_strip(index)._invert_mute_feedback = True
		crossfader = EncoderElement(MIDI_CC_TYPE, CHANNEL, 64, Live.MidiMap.MapMode.absolute)
		master_volume_control = SliderElement(MIDI_CC_TYPE, CHANNEL, 1)
		prehear_control = SliderElement(MIDI_CC_TYPE, CHANNEL, 4)
		crossfader.name = 'Crossfader'
		master_volume_control.name = 'Master_Volume_Control'
		prehear_control.name = 'Prehear_Volume_Control'
		mixer.set_crossfader_control(crossfader)
		mixer.set_prehear_volume_control(prehear_control)
		mixer.master_strip().set_volume_control(master_volume_control)

		count = 0
		for track in range(4):
			mixer.channel_strip(track).set_assign_buttons(
				SimpleButtonElement(False, MIDI_NOTE_TYPE, CHANNEL, 19 + count),
				SimpleButtonElement(False, MIDI_NOTE_TYPE, CHANNEL, 20 + count))
			mixer.channel_strip(track).set_device_buttons(
				EncoderElement(MIDI_CC_TYPE, CHANNEL, 6 + track, Live.MidiMap.MapMode.absolute),
				EncoderElement(MIDI_CC_TYPE, CHANNEL, 10 + track, Live.MidiMap.MapMode.absolute),
				EncoderElement(MIDI_CC_TYPE, CHANNEL, 14 + track, Live.MidiMap.MapMode.absolute),
				EncoderElement(MIDI_CC_TYPE, CHANNEL, 18 + track, Live.MidiMap.MapMode.absolute))

			count += 4

		if (USE_SELECT_BUTTONS == True):
			self.selectbuttons = [None for index in range(N_TRACKS)]
			for index in range(len(SELECT_BUTTONS)):
				self.selectbuttons[index] = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,
																  SELECT_BUTTONS[index], 'Select_Button', self)
				mixer.channel_strip(index).set_select_button(self.selectbuttons[index])
				self.selectbuttons[index].set_on_value(SELECT_BUTTON_ON_COLOR)
				self.selectbuttons[index].set_off_value(SELECT_BUTTON_OFF_COLOR)

		if (USE_SOLO_BUTTONS == True):
			self.solobuttons = [None for index in range(4)]
			for index in range(len(SOLO_BUTTONS)):
				self.solobuttons[index] = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,
																SOLO_BUTTONS[index], 'Solo_Button', self)
				mixer.channel_strip(index).set_solo_button(self.solobuttons[index])
				self.solobuttons[index].set_on_value(SOLO_BUTTON_ON_COLOR)
				self.solobuttons[index].set_off_value(SOLO_BUTTON_OFF_COLOR)

		if (USE_ARM_BUTTONS == True):
			self.armbuttons = [None for index in range(N_TRACKS)]
			for index in range(len(ARM_BUTTONS)):
				self.armbuttons[index] = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,
															   ARM_BUTTONS[index], 'Arm_Button', self)
				mixer.channel_strip(index).set_arm_button(self.armbuttons[index])
				self.armbuttons[index].set_on_value(ARM_BUTTON_ON_COLOR)
				self.armbuttons[index].set_off_value(ARM_BUTTON_OFF_COLOR)

		if (USE_MUTE_BUTTONS == True):
			self.mutebuttons = [None for index in range(N_TRACKS)]
			for index in range(len(MUTE_BUTTONS)):
				self.mutebuttons[index] = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL,
																MUTE_BUTTONS[index], 'Mute_Button', self)
				mixer.channel_strip(index).set_mute_button(self.mutebuttons[index])
				self.mutebuttons[index].set_on_value(MUTE_BUTTON_ON_COLOR)
				self.mutebuttons[index].set_off_value(MUTE_BUTTON_OFF_COLOR)

		if (USE_VOLUME_CONTROLS == True):
			self.volencoders = [None for index in range(len(VOLUME_ENCODERS))]
			for index in range(len(VOLUME_ENCODERS)):
				self.log_message("Setting up voulme")
				self.volencoders[index] = EncoderElement(MIDI_CC_TYPE, CHANNEL, VOLUME_ENCODERS[index],
														 Live.MidiMap.MapMode.absolute)
				mixer.channel_strip(index).set_volume_control(self.volencoders[index])
		return mixer


	def session_control(self, mixer):
		is_momentary = True
		self._timer = 0
		self.flash_status = 1
		self.session = SessionComponent(N_TRACKS, N_SCENES)
		self.session.name = "Session"
		self.session.set_mixer(mixer)
		self.session.set_offsets(0, 0)

		self.scene = [None for index in range(N_SCENES)]
		for row in range(N_SCENES):
			self.scene[row] = self.session.scene(row)
			self.scene[row].name = 'Scene_' + str(row)
			for column in range(N_TRACKS):
				clip_slot = self.scene[row].clip_slot(column)
				clip_slot.name = str(column) + '_Clip_Slot' + str(row)
				self.scene[row].clip_slot(column).set_triggered_to_play_value(CLIP_TRG_PLAY_COLOR)
				self.scene[row].clip_slot(column).set_stopped_value(CLIP_STOP_COLOR)
				self.scene[row].clip_slot(column).set_started_value(CLIP_STARTED_COLOR)
		self.set_highlighting_session_component(self.session)

		self.scrollencoder = ScrollEncoderElement(MIDI_CC_TYPE, CHANNEL, 3, Live.MidiMap.MapMode.absolute,
												  self.session)
		#assign a shift button so that we can switch states between the SessionComponent and the SessionZoomingComponent


		if USE_SESSION_NAV == True:
			self.navleft = SimpleButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, NAVBOX_LEFT_BUTTON)
			self.navleft.clear_send_cache()

			self.navright = SimpleButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, NAVBOX_RIGHT_BUTTON)
			self.navright.clear_send_cache()

			self.navup = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, NAVBOX_UP_BUTTON, 'Nav_Up_Button',
											   self)
			self.navup.clear_send_cache()
			self.navup.set_on_off_values(NAVBOX_UP_BUTTON_C, NAVBOX_UP_BUTTON_C)

			self.navdown = FlashingButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, NAVBOX_DOWN_BUTTON,
												 'Nav_Down_Button', self)
			self.navdown.clear_send_cache()
			self.navdown.set_on_off_values(NAVBOX_DOWN_BUTTON_C, NAVBOX_DOWN_BUTTON_C)

			self.session.set_track_bank_buttons(self.navright, self.navleft)
			self.session.set_scene_bank_buttons(self.navdown, self.navup)

		self.refresh_state()
		self.session.set_enabled(True)
		self.session.update()

	def setup_device_control(self):
		is_momentary = True
		device_bank_buttons = []
		#  device_param_controls = []
		bank_button_labels = ('Clip_Track_Button')
		for index in range(1):
			device_bank_buttons.append(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 18 + index))
			device_bank_buttons[-1].name = bank_button_labels[index]

		device = ShiftableDeviceComponent()
		device.name = 'Device_Component'
		self.set_device_component(device)
		detail_view_toggler = DetailViewControllerComponent(self)
		detail_view_toggler.name = 'Detail_View_Control'
		detail_view_toggler.set_device_clip_toggle_button(device_bank_buttons[0])

	def update_display(self):
		ControlSurface.update_display(self)
		self._timer = (self._timer + 1) % 256
		self.flash()

	def flash(self):
		pass


	def disconnect(self):
		self._hosts = []
		ControlSurface.disconnect(self)
		return None
