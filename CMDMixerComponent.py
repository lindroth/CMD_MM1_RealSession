from CMDChannelStripComponent import CMDChannelStripComponent
from _Framework.MixerComponent import MixerComponent

class CMDMixerComponent(MixerComponent):
    def _create_strip(self):
        return CMDChannelStripComponent()