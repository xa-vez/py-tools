#!/usr/bin/python2
import argparse
import serial
import re
from datetime import datetime

parser = argparse.ArgumentParser(description='CLOE serial log filer. \r\n'
                                             ' Used to filter Sequans ASW CLOE logs from platfrom ones.\r\n'
                                             ' Only filtered logs are displayed, all logs are saved to log file.')

parser.add_argument('-p', '--port', default="/dev/ttyUSB0", type=str,
                    help='Log COM port')
parser.add_argument('-b', '--baud', default=115200, type=int,
                    help='Log COM port baudrate')
parser.add_argument('-f', '--file', default='cloe_log.txt', type=str,
                    help='Log file')
parser.add_argument('-o', '--override', action='store_true',
                    help='Override log file on script start')
parser.add_argument('-r', '--regexp', default='', type=str,
                    help='Regular expression to filter cloe output')

if __name__ == "__main__":
    args = parser.parse_args()
    ser = serial.Serial(args.port, args.baud)

    with open(args.file, 'w' if args.override else 'a+') as f:
        while True:
            line = ser.readline()
            if args.regexp:
                reg = re.compile(args.regexp)
                match = reg.search(line)
                if match:
                    print datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "  " + line.strip()
            elif "CLOE" in line or ">|" in line  or "ASSERT" in line or "assert" in line:
                print datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "  " + line.strip()
            f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "  " + line.strip() + "\n")
            f.flush()

