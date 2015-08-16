#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2015 KenV99
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
import datetime
import json
import subprocess
import re
pattern = re.compile('[\W_]+')

debug = False
if debug:
    filepath = r'C:\Users\Ken User\AppData\Roaming\Kodi\addons\script.hyperion_conf_update'
    date_append = True
    restart = True
    class xbmc:
        @staticmethod
        def log(p):
            print p
else:
    import xbmc
    import xbmcgui
    import xbmcaddon
    filepath = r'/storage/.config'
    _settings = xbmcaddon.Addon("script.hyperion_conf_update")
    date_append = _settings.getSetting('date_append') == 'true'
    restart = _settings.getSetting('restart') == 'true'

def get_current():
    if debug:
        with open(os.path.join(filepath,'output.json'), 'r') as l:
            filetxt = ''.join(l.readlines()[3:])
    else:
        try:
            filetxt = subprocess.check_output(['/storage/hyperion/bin/hyperion-remote.sh -l'], shell=True)        
            fl = filetxt.split('\n')
            fl = fl[3:]
            filetxt = "\n".join(fl)
            xbmc.log(filetxt)
        except Exception as e:
            xbmc.log('#### hyperion_config_update ERROR: %s' % e.message)
            raise
    try:
        jd = json.loads(filetxt)
    except Exception as e:
        xbmc.log('#### hyperion_config_update ERROR: %s' % e.message)
        filetxt = ''
        raise
    else:
        td = {}
        t = {}
        tl =  jd['transform']
        tl_cnt = len(tl)
        for i in xrange(0, tl_cnt):
            td[tl[i]['id']] = tl[i]
        return td

def writejson(newjson):
    n = ''.join(newjson)
    if date_append:
        ds = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        bakfn = 'hyperion.config.json_%s.bak' % ds
    else:
        bakfn = 'hyperion.config.json.bak'
    if os.path.exists(bakfn):
        os.remove(bakfn)
    bakfn = os.path.join(filepath, bakfn)
    try:
        os.rename(os.path.join(filepath,'hyperion.config.json'), bakfn)
    except Exception as e:
        xbmc.log('#### hyperion_config_update ERROR: %s' % e.message)
        filetxt = ''
        raise
    try:
        with open(os.path.join(filepath, 'hyperion.config.json'), 'w') as l:
            l.write(n)
    except Exception as e:
        xbmc.log('#### hyperion_config_update ERROR: %s' % e.message)
        raise
    else:
        if not debug:
            dialog = xbmcgui.Dialog()
            dialog.notification('hyperion_conf_update', 'json file updated successfully', time=2000)
            try:
                op = subprocess.check_output(['killall hyperiond'], shell=True)
            except subprocess.CalledProcessError as e:
                xbmc.log('### Hyperion OFF Exception: %s' % e.output)
            except Exception as e:
                xbmc.log('### Hyperion OFF Exception: %s' % e.message)
            try:
                op = subprocess.check_output(['/storage/hyperion/bin/hyperiond.sh /storage/.config/hyperion.config.json </dev/null >/dev/null 2>&1 &'], shell=True)
            except subprocess.CalledProcessError as e:
                xbmc.log('### Hyperion ON Exception: %s' % e.output)
            except Exception as e:
                xbmc.log('### Hyperion ON Exception: %s' % e.message)


def main():
    td = get_current()
    try:
        newjson = []
        l = open(os.path.join(filepath, 'hyperion.config.json'), 'r')
        jsonl = l.readlines()
        l.close()
        tflag = False
        idflag = False
        cidx = -1
        for line in jsonl:
            x = line.strip()
            if x == '' or x[0:2] == '//':
                newjson.append(line)
            else:
                if line.strip()[0:11] == '"transform"':
                    tflag = True
                if tflag:
                    y = line.strip().split(':')
                    if y[0].strip() == '"id"':
                        newjson.append(line)
                        z = y[1].strip()
                        k = pattern.sub('', z)
                        if k in td.keys():
                            t = td[k]
                            idflag = True
                        else:
                            idflag = False
                    elif idflag:
                        ys = y[0].strip()
                        if ys == '"saturationGain"':
                            x = t['saturationGain']
                            r = ''.join(['%.4f' % t['saturationGain'], ','])
                            ln = line.replace(y[1], r)
                            newjson.append(ln)
                        elif ys == '"valueGain"':
                            r = ''.join(['%.4f' % t['valueGain'], ''])
                            ln = line.replace(y[1], r)
                            newjson.append(ln)
                        elif ys == '"red"':
                            cidx = 0
                            newjson.append(line)
                        elif ys == '"green"':
                            cidx = 1
                            newjson.append(line)
                        elif ys == '"blue"':
                            cidx = 2
                            newjson.append(line)
                        elif cidx != -1:
                            if ys == '"threshold"':
                                r = ''.join(['%.4f' % t['threshold'][cidx],","])
                                ln = line.replace(y[1], r)
                                newjson.append(ln)
                            elif ys == '"gamma"':
                                r = ''.join(['%.4f' % t['gamma'][cidx],","])
                                ln = line.replace(y[1], r)
                                newjson.append(ln)
                            elif ys == '"blacklevel"':
                                r = ''.join(['%.4f' % t['blacklevel'][cidx],","])
                                ln = line.replace(y[1], r)
                                newjson.append(ln)
                            elif ys == '"whitelevel"':
                                r = ''.join(['%.4f' % t['whitelevel'][cidx],""])
                                ln = line.replace(y[1], r)
                                newjson.append(ln)
                            else:
                                newjson.append(line)
                        elif ys == "]":
                            tflag = False
                            newjson.append(line)
                        else:
                            newjson.append(line)
                    else:
                        newjson.append(line)


                else:
                    newjson.append(line)
        writejson(newjson)
    except Exception as e:
        xbmc.log('#### hyperion_config_update ERROR: %s' % e.message)
        filetxt = ''
        raise


if __name__ == '__main__':
    main()

