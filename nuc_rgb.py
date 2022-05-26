#!/usr/bin/env python
# coding: utf-8

import platform
from time import sleep
import serial
import json
import argparse

SERIAL_PORT_LINUX = '/dev/ttyACM0'
SERIAL_PORT_WINDOWS = 'COM3'

TIME_START = 2
TIME_CMD = 0.1

CMD_HELP = '''\
--------------------------------------------------------------------------------
RST   | reset default settings
BTN:x | enable or disable all RGB LED
          x = 0:disable, 1:enable
--------------------------------------------------------------------------------
        n = A:Skull, B:Bottom_Left, C:Bottom_Right, D:Bottom_Front
nPx   | set Pattern
          x = 0:Off, 1:Solid, 2:Pulse, 3:Breathing, 4:Strobing,
            5:PulseTrain1, 6:PulseTrain2, 7:PulseTrain3, 8:Rainbow1
nV:x  | set Brightness
          x = [0-5], 0:disable
nR:x  | enable or disable Rainbow
          x = 0:disable, 1:enable
nD:x  | set Frequency
          x = [0-5], 0:disable
--------------------------------------------------------------------------------
Ci:x  | set Color
          i = 1:Skull, 2:Bottom_Left, 3:Bottom_Right, 4:Bottom_Front,
            5:Pulse_Train_Color1, 6:Pulse_Train_Color2, 7:Pulse_Train_Color3
          x = [0-255], 0:Red, 32:Orange, 70:Yellow, 96:Green, 128:Cyan,
            160:Blue, 192:Purple, 224:Pink
--------------------------------------------------------------------------------
example: 
nuc_rgb -c "DP1,DV:5,DR:0,C4:96"
    Bottom_Front LED: Pattern:Solid, Brightness:5, Rainbow:disable, Color:Green
nuc_rgb -c "RST"
    reset to default settings
--------------------------------------------------------------------------------\
'''

PATTERN = {
    0: 'Off',
    1: 'Solid',
    2: 'Pulse',
    3: 'Breathing',
    4: 'Strobing',
    5: 'PulseTrain1',
    6: 'PulseTrain2',
    7: 'PulseTrain3',
    8: 'Rainbow1'
}

COLOR = {x: str(x) for x in range(256)}
COLOR[0] = 'Red'
COLOR[32] = 'Orange'
COLOR[70] = 'Yellow'
COLOR[96] = 'Green'
COLOR[128] = 'Cyan'
COLOR[160] = 'Blue'
COLOR[192] = 'Purple'
COLOR[224] = 'Pink'


def send(ser, cmd):
    ser.write(cmd)
    sleep(TIME_CMD)


def recv(ser):
    return ser.read_until()


def run_cmds(ser, cmds: str):
    cmd_list = cmds.strip().split(',')
    for cmd in cmd_list:
        send(ser, cmd.upper().encode()+b'\n')


def get_id(ser):
    send(ser, b'ID?\n')
    return recv(ser).decode().strip()


def get_status(ser):
    send(ser, b'STA?\n')
    ret = recv(ser).decode().strip().split(',')
    r = [int(x) for x in ret]
    ap, bp, cp, dp, c1, c2, c3, c4, c5, c6, c7, av, bv, cv, dv, ad, bd, cd, dd, ar, br, cr, dr, btn = r
    status = {
        'Enabled': btn == 1,
        'Skull': {
            'Pattern': PATTERN[ap],
            'Color': COLOR[c1],
            'Brightness': av,
            'Frequency': ad,
            'Rainbow': ar == 1,
        },
        'Bottom_Left': {
            'Pattern': PATTERN[bp],
            'Color': COLOR[c2],
            'Brightness': bv,
            'Frequency': bd,
            'Rainbow': br == 1,
        },
        'Bottom_Right': {
            'Pattern': PATTERN[cp],
            'Color': COLOR[c2],
            'Brightness': cv,
            'Frequency': cd,
            'Rainbow': cr == 1,
        },
        'Bottom_Front': {
            'Pattern': PATTERN[dp],
            'Color': COLOR[c4],
            'Brightness': dv,
            'Frequency': dd,
            'Rainbow': dr == 1,
        },
        'Pulse_Train_Color': [COLOR[c5], COLOR[c6], COLOR[c7]]
    }
    return status


def main():
    parser = argparse.ArgumentParser(
        description='NUC RGB: CLI to control the RGB LED on Intel NUC 11/12 Extreme, for Linux and Windows')
    parser.add_argument('-p', '--port', metavar='SERIAL_PORT', type=str, default='', help='serial port')
    parser.add_argument('-c', '--execute', metavar='CMD', type=str, help='execute comma-separated command string')
    parser.add_argument('-s', '--status', action='store_true', help='print RGB LED status')
    parser.add_argument('-l', '--list', action='store_true', help='print command list')
    args = parser.parse_args()

    if args.list:
        print(CMD_HELP)
        exit()

    if args.port:
        serial_port = args.port
    elif platform.system() == 'Linux':
        serial_port = SERIAL_PORT_LINUX
    elif platform.system() == 'Windows':
        serial_port = SERIAL_PORT_WINDOWS
    else:
        serial_port = None
    ser = serial.Serial(serial_port, timeout=3)
    sleep(TIME_START)

    if args.execute:
        run_cmds(ser, args.execute)

    if args.status or not args.execute:
        print('Controller ID:', get_id(ser))
        status = get_status(ser)
        print(json.dumps(status, indent=4))

    ser.close()


if __name__ == '__main__':
    main()
