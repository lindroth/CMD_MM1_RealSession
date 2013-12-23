CMD_MM1_RealSession
===================

This is a Ableton Live 9 Remote Script for the Behringer CMD MM1 that moves the faders with the moving box in live.
Knobs is assigned to the first device for each track by magic.

If you don't know how to install 3rd party remote scripts see
http://sonicbloom.net/en/ableton-live-tutorial-how-to-install-midi-remote-scripts/

If this script does not work for you, it might me that your CMD-MM1 does not send on MIDI channel 1

In the file MM1.py change CHANNEL = 0 to CHANNEL = 4

You can easily check which channel your CMD MM1 sends on in live by mapping a knob on the MM-1 to something and then check the channel in the midi mappings window in Live.

A big thanks too Behringer for releasing the CMD MM-1 and for releasing their remote scripts.