script.hyperion_conf_update
=======================
A Kodi AddOn to write changes made by a hyperion remote program into the permanent json file.

Changes made by remote programs to the transform matrix for hyperion are usually lost when hyperion restarts because
those changes are not written into hyperion.config.json. This AddOn can be run under 'Programs' in Kodi to store
those changes in the json file without having to edit it manually. It can also be added to the keyboard.xml or
remote.xml files to allow it to run via a keyboard command or remote button (see example_keyboard.xml).

Limitations:
The LED set 'id' can only contain alphanumerics - no dashes, dots, etc.
Currently written only for OpenELEC as it stands.
Expects that the current hyperion.config.json file is formatted similar to that produced by hyperioncon.jar.

Also included is:
1) a script to turn the LEDs on/off (hyperion_switch.py) - see example_keyboard.xml for usage.
2) an mp4 file containing solid colors for use while configuring the LEDs using a remote program