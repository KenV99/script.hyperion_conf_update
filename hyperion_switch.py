#!/usr/bin/python
#

import os
import sys
import subprocess
import xbmc

PARAMETER = str(sys.argv[1]).lower()
# xbmc.log('### hyperion_switcher arg=|%s|' % PARAMETER)

if PARAMETER == 'on':
    try:
        op = subprocess.check_output(['/storage/hyperion/bin/hyperiond.sh /storage/.config/hyperion.config.json </dev/null >/dev/null 2>&1 &'], shell=True)
    except subprocess.CalledProcessError as e:
        xbmc.log('### Hyperion ON Exception: %s' % e.output)
    except Exception as e:
        xbmc.log('### Hyperion ON Exception: %s' % e.message)
    else:
        xbmc.log('### Hyperion ON: %s'% op)
elif PARAMETER == 'off':
    try:
        op = subprocess.check_output(['killall hyperiond'], shell=True)
    except subprocess.CalledProcessError as e:
        xbmc.log('### Hyperion OFF Exception: %s' % e.output)
    except Exception as e:
        xbmc.log('### Hyperion OFF Exception: %s' % e.message)
    else:
        xbmc.log('### Hyperion OFF: %s' % op)


