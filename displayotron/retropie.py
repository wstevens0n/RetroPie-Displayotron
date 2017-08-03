#!/usr/bin/env python

import math
import time
import os
import re
import dothat.backlight as backlight
import dothat.lcd as lcd
import fcntl
import socket
import struct
from datetime import datetime

def get_addr(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])
    except IOError:
        return 'Not Found!'

wlan0 = get_addr('wlan0')
eth0 = get_addr('eth0')

def get_cpu_temp():
   tempFile = open("/sys/class/thermal/thermal_zone0/temp")
   cpu_temp = tempFile.read()
   tempFile.close()
   return float(cpu_temp)/1000

def get_cpu_speed():
   tempFile = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
   cpu_speed = tempFile.read()
   tempFile.close()
   return float(cpu_speed)/1000

old_Temp = new_Temp = get_cpu_temp()
old_Speed = new_Speed = get_cpu_speed()

sec = 0
x = 0

pacman = [
    [0x0e, 0x1f, 0x1d, 0x1f, 0x18, 0x1f, 0x1f, 0x0e],
    [0x0e, 0x1d, 0x1e, 0x1c, 0x18, 0x1c, 0x1e, 0x0f]
]
def get_anim_frame(char, fps):
    return char[int(round(time.time() * fps) % len(char))]

while True:
    x += 3
    x %= 360
    backlight.sweep((x % 360) / 360.0)
    #backlight.set_graph(abs(math.cos(x / 100.0)))
    backlight.set_graph(0)

    lcd.create_char(1, get_anim_frame(pacman, 2))
    
    pos = int(x / 22)
    lcd.set_cursor_position(0,0)
    date = datetime.now().strftime("%b %e, %I:%M %p")
    lcd.write(date[:pos] + "  \x01")

    # cpu Temp & Speed information
    new_Temp = int(get_cpu_temp())
    new_Speed = int(get_cpu_speed())

    if old_Temp != new_Temp or old_Speed != new_Speed :
        old_Temp = new_Temp
        old_Speed = new_Speed

    text = " "+ str(new_Temp) + chr(223) + "C   " + str(new_Speed) + "Mhz"
    pos = int(x / 22)
    lcd.set_cursor_position(0,1)
    lcd.write(text[:pos] + "  \x01")

    wlan0 = get_addr('wlan0')
    eth0 = get_addr('eth0')

    pos = int(x / 22)
    lcd.set_cursor_position(0,2)
    if wlan0 != 'Not Found!':
        ip = "  " + wlan0
        lcd.write(ip[:pos] + "  \x01")
    else:
        ip = "  " + eth0
        lcd.write(ip[:pos] + "  \x02")
    
    time.sleep(0.01)
    sec = 0

    while (sec < 1):
        try:
            f = open('/dev/shm/runcommand.log', 'r')
        except IOError:
            break
        else:
            lcd.clear()
            system = f.readline()
            system = system.replace("\n","")
            systemMap = {
                "mame-mame4all" :   "MAME4ALL",
                "mame-advmame"  :   "AdvanceMAME",
                "mame-libretro" :   "MAME-libretro",
                "fba"           :   "FinalBurn Alpha",
                "gb"            :   "Game Boy",
                "gbc"           :   "Game Boy Color",
                "gba"           :   "Game Boy Advance",
                "nds"           :   "Nintendo DS",
                "virtualboy"    :   "VirtualBoy",
                "famicom"       :   "Famicom",
                "fds"           :   "Famicom Disk Sys",
                "nes"           :   "Nintendo",
                "sfc"           :   "Super Famicom",
                "snes"          :   "Super Nintendo",
                "n64"           :   "Nintendo 64",
                "gamegear"      :   "Sega Game Gear",
                "sg-1000"       :   "Sega SG-1000",
                "mastersystem"  :   "Sega Master Sys",
                "megadrive"     :   "Sega Megadrive",
                "megadrive-japan":  "Sega Megadrive",
                "sega32x"       :   "Sega 32x",
                "segacd"        :   "Sega CD",
                "dreamcast"     :   "Dreamcast",
                "ngp"           :   "Neo Geo Pocket",
                "ngpc"          :   "NG Pocket Color",
                "neogeo"        :   "Neo Geo",
                "pspminis"      :   "PSP Minis",
                "psp"           :   "PSPortable",
                "psx"           :   "Playstation",
                "atari800"      :   "Atari 800",
                "atari2600"     :   "Atari 2600",
                "atari5200"     :   "Atari 5200",
                "atari7800"     :   "Atari 7800",
                "atarilynx"     :   "Atari Lynx",
                "amiga"         :   "Amiga",
                "amigacd32"     :   "Amiga CD32",
                "coleco"        :   "Coleco",
                "c64"           :   "Commodore 64",
                "daphne"        :   "Daphne",
                "kodi"          :   "KODI",
                "pixel"         :   "Raspbian Pixel",
                "msx"           :   "MSX",
                "msx"           :   "MSX 2",
                "pc"            :   "DOSBOX / RPIX86",
                "pcengine"      :   "PC Engine",
                "pcenginecd"    :   "PC Engine CD",
                "scummvm"       :   "Scumm VM",
                "sgfx"          :   "NEC SuperGrafx",
                "tg16"          :   "NEC TurboGrafx 16",
                "tg16cd"        :   "NEC TurboGrafx 16 CD",
                "vectrex"       :   "Vectrex",
                "wonderswan"    :   "Wonderswan",
                "wonderswancolor":   "Wonderswan Color",
                "zmachine"      :   "Infocom Z-machine",
                "zxspectrum"    :   "Sinclair ZX Spectrum",
                "ports"         :   "Ports",
            }
            system = systemMap.get(system)
            rom = f.readline()
            rom = rom.replace("\n","")
            rom = "%s" %(rom)
            lcd.set_cursor_position(0,0)     
            lcd.write("%s" %(system))
            lcd.set_cursor_position(0,1)
            lcd.write(re.sub(r'\([^)]*\)', '', rom))
            time.sleep(3)
            f.close() 
            time.sleep(1)
  
