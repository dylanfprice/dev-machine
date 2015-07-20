#!/usr/bin/python
import argparse
import dbus
import datetime

# Level settings:
day_level = 75
night_level = 20

bus = dbus.SessionBus()

proxy = bus.get_object(
    'org.gnome.SettingsDaemon',
    '/org/gnome/SettingsDaemon/Power'
)

iface = dbus.Interface(
    proxy,
    dbus_interface='org.gnome.SettingsDaemon.Power.Screen'
)


# Description
parser = argparse.ArgumentParser(description='Sets the Monitor Brightness')
# nargs='?' wont make error if missing argument
parser.add_argument('level', nargs='?', type=int, help='Integer from 1 to 100')
args = parser.parse_args()

if not args.level and args.level != 0:
    print 'Setting brightness based on Time'

    now = datetime.datetime.now()

    if now.hour > 7 and now.hour < 20:
        level = day_level
    else:
        level = night_level
else:
    level = args.level

print 'Setting brightness to: ', level

# Set brightness:
iface.SetPercentage(level)
