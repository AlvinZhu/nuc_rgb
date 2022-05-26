# NUC RGB

CLI to control the RGB LED on Intel NUC 11/12 Extreme, for Linux and Windows

英特尔 NUC 11/12 Extreme 上的 RGB LED设置工具，适用于 Linux 和 Windows

## Requirements

Python3

pyserial~=3.5

## Build

### Arch Linux

```bash
makepkg -fCcs
```

### Windows

```shell
pyinstaller -F .\nuc_rgb.py --noupx
```

## Usage

```
usage: nuc_rgb [-h] [-p SERIAL_PORT] [-c CMD] [-s] [-l]

NUC RGB: CLI to control the RGB LED on Intel NUC 11/12 Extreme, for Linux and Windows

options:
  -h, --help            show this help message and exit
  -p SERIAL_PORT, --port SERIAL_PORT
                        serial port
  -c CMD, --execute CMD
                        execute comma-separated command string
  -s, --status          print RGB LED status
  -l, --list            print command list
```



## Command

```bash
RST   # reset default settings
BTN:x # enable or disable all RGB LED
        # x = 0:disable, 1:enable
################################################################################
      # n = A:Skull, B:Bottom_Left, C:Bottom_Right, D:Bottom_Front
nPx   # set Pattern
        # x = 0:Off, 1:Solid, 2:Pulse, 3:Breathing, 4:Strobing,
        #   5:PulseTrain1, 6:PulseTrain2, 7:PulseTrain3, 8:Rainbow1
nV:x  # set Brightness
        # x = [0-5], 0:disable
nR:x  # enable or disable Rainbow
        # x = 0:disable, 1:enable
nD:x  # set Frequency
        # x = [0-5], 0:disable
################################################################################
Ci:x  # set Color
        # i = 1:Skull, 2:Bottom_Left, 3:Bottom_Right, 4:Bottom_Front,
        #   5:Pulse_Train_Color1, 6:Pulse_Train_Color2, 7:Pulse_Train_Color3
        # x = [0-255], 0:Red, 32:Orange, 70:Yellow, 96:Green, 128:Cyan,
        #   160:Blue, 192:Purple, 224:Pink
################################################################################
# example:
nuc_rgb -c "DP1,DV:5,DR:0,C4:96"
  # Bottom_Front LED: Pattern:Solid, Brightness:5, Rainbow:disable, Color:Green
nuc_rgb -c "RST"
  # reset to default settings
```

