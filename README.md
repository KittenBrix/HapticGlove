# HapticGlove

unfortunately, recording keypresses for use as blip or vibration outputs depends on pygame.
even worse, on some machines, holding a key down is interpretted as multiple keydown and keyup 
events, which prevents me from matching the key press duration properly. (this is why it'll be
blips and not exact note durations) I'm unsure if this is a pygame fault.

playback on vibration motors depends on having the RPi.GPIO library and the appropriate setup for
motors. [TODO: drop parts list and schematic for my build]

playback via audio requires an audio device and the pyAudio library.
