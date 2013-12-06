import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.SessionComponent import SessionComponent 
import math


# Constants. Tweaking these would let us work with different grid sizes or different templates

#Index of the columns used for VU display
A_COL = [4]
B_COL = [5]
C_COL = [6]
D_COL = [7]
# Which channels we are monitoring for RMS
A_SOURCE = 0
B_SOURCE  = 1
C_SOURCE = 2
D_SOURCE  = 3

# Grid size
CLIP_GRID_X = 6
CLIP_GRID_Y = 6

# Velocity values for clip colours. Different on some devices
LED_RED = 4
LED_ON = 5
LED_OFF = 0
LED_ORANGE = 3

# Scaling constants. Narrows the db range we display to 0db-21db or thereabouts
CHANNEL_SCALE_MAX = 0.92
CHANNEL_SCALE_MIN = 0.3
CHANNEL_SCALE_INCREMENTS = 4

MASTER_SCALE_MAX = 0.94
MASTER_SCALE_MIN = 0.1
MASTER_SCALE_INCREMENTS = 15

RMS_FRAMES = 10
USE_RMS = False

class VUMeter():
  'represents a single VU to store RMS values etc in'
  def __init__(self, parent, track, top, bottom, 
              increments, vu_set, master = False):


    self.frames = [0.0] * RMS_FRAMES
    self.parent = parent
    self.track = track
    self.top = top
    self.bottom = bottom
    self.multiplier = self.calculate_multiplier(top, bottom, increments)
    self.current_left_level = 0
    self.current_right_level = 0
    self.master = master

  def observe(self):
    new_frame = self.mean_peak() 
    self.store_frame(new_frame)

    #if USE_RMS:
      #level = self.scale(self.rms(self.frames))
    #else:
    self.left_level = self.scale(self.left_peak())
    self.right_level = self.scale(self.right_peak())
    # Only update LEDs when value changes
    if self.left_level != self.current_left_level or self.right_level != self.current_right_level:
      self.current_left_level = self.left_level
      self.current_right_level = self.right_level
      if self.master:
          self.parent.set_master_leds(self.left_level, self.right_level)

  def store_frame(self, frame):
    self.frames.pop(0)
    self.frames.append(frame)

  def rms(self, frames):
    return math.sqrt(sum(frame*frame for frame in frames)/len(frames))

  # return the mean of the L and R peak values
  def mean_peak(self):
    return (self.track.output_meter_left + self.track.output_meter_right) / 2
  def right_peak(self):
    return self.track.output_meter_right
  def left_peak(self):
    return self.track.output_meter_left

  # Perform the scaling as per params. We reduce the range, then round it out to integers
  def scale(self, value):
    if (value > self.top):
      value = self.top
    elif (value < self.bottom):
      value = self.bottom
    value = value - self.bottom
    value = value * self.multiplier #float, scale 0-10
    return int(round(value))
  
  def calculate_multiplier(self, top, bottom, increments):
    return (increments / (top - bottom))



class CMDVUMeters(ControlSurfaceComponent):
    'standalone class used to handle VU meters'

    def __init__(self, parent, lightsleft, lightsright):
        # Boilerplate
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
        self.lightsleft = lightsleft
        self.lightsright = lightsright
        # Default the L/R/Master levels to 0
        self._meter_level = 0
        self.clear_master_leds()

        
        #setup classes
        
        self.master_meter = VUMeter(self, self.song().master_track,
                                    MASTER_SCALE_MAX,
                                    MASTER_SCALE_MIN, MASTER_SCALE_INCREMENTS,
                                    None, True)
        # Listeners!
        self.song().master_track.add_output_meter_left_listener(self.master_meter.observe)

    # If you fail to kill the listeners on shutdown, Ableton stores them in memory and punches you in the face
    def disconnect(self):
        self.clear_master_leds()
        self.song().master_track.remove_output_meter_left_listener(self.master_meter.observe)
        

    # Called when the Master clips. Makes the entire clip grid BRIGHT RED 
    def clip_warning(self):
        pass

    def set_master_leds(self, left_level, right_level):
        self.lightsleft.send_value(left_level+48, True)
        self.lightsright.send_value(right_level+48, True)
    def clear_master_leds(self):
        self.lightsleft.send_value(48,True)
        self.lightsright.send_value(48,True)
    # boilerplate
    def update(self):
        pass

    def on_enabled_changed(self):
        self.update()

    def on_selected_track_changed(self):
        self.update()

    def on_track_list_changed(self):
        self.update()

    def on_selected_scene_changed(self):
        self.update()

    def on_scene_list_changed(self):
        self.update()









