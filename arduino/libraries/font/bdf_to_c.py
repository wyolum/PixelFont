import re
from numpy import *
from pylab import *
import sys

ascii = '''STARTCHAR C
ENCODING 67
SWIDTH 640 0
DWIDTH 6 0
BBX 6 9 0 -2
BITMAP
00
30
48
40
40
48
30
00
00
ENDCHAR
'''
ascii = '''STARTCHAR C
ENCODING 67
SWIDTH 640 0
DWIDTH 6 0
BBX 6 9 0 -2
BITMAP
00
30
48
40
40
48
30
00
00
ENDCHAR
'''
x = re.compile(r'BITMAP\n([0-9a-fA-F\n]*?)\nENDCHAR', re.MULTILINE)
assert x.search(ascii)
char = re.compile(r'STARTCHAR[-a-zA-Z0-9 \n]*?ENCODING ([0-9]+)[-a-zA-Z0-9 \n]*?BITMAP\n([0-9a-fA-F\n]*?)\nENDCHAR', re.MULTILINE)
match = char.search(ascii)

usage = Exception("python bdf_to_c.py width height bdf_file.bdf")
if len(sys.argv) < 4:
    raise usage

width = int(sys.argv[1])
height = int(sys.argv[2])
fn = sys.argv[3]
t = open(fn).read()

def tobits(b):
    out = []
    for i in range(8):
        out.append(b >> i & 1)
    return out

def format(bytes):
    out = []
    for b in bytes:
        out.append('0x%02x' % b)
    return out
i = 0
out = []

print('const byte FONT%dx%d_N_ROW = 16;' % (width, height))
print('const byte FONT%dx%d_N_COL = 8;' % (width, height))
print('const byte FONT%dx%d_N_CHAR = 128;'% (width, height))

print('byte font%dx%d[] = {' % (width, height))

chars = [[] for i in range(128)]
for m in char.finditer(t):
    # print m.group(0)]
    enc = int(m.group(1))
    bytes = m.group(2).strip()
    bytes = [int(s.strip(), 16) for s in bytes.splitlines()]
    if enc < len(chars):
        chars[enc] = bytes
for char in chars:
    char += [0 for i in range(height - len(char))]
    print (','.join(format(char)) + ',')
print('};')
