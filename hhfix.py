# hhfix - Fix Hexheld ROMs
# by minerobber

import argparse, struct

def crc16(data):
	crc=0xFFFF
	for c in data:
		for i in range(8):
			b=(c^crc)&1
			crc>>=1
			if b: crc^=0xd175
			c>>=1
	return (~crc)&0xFFFF

HEADER = struct.Struct("<128s96s16sBBBB4xHHHH")
assert HEADER.size==256,"Header not 256 bytes long"

def fixheader(data,**kwargs):
	title, developer, magic, romsize, cs1, cs2, min_soc, rev, copystart, copyend, crc = HEADER.unpack(data)
	if magic!=b'HEXHELD SOFTWARE':
		print("Fixing magic")
		magic = b'HEXHELD SOFTWARE'
	if kwargs.get("title"):
		title = kwargs["title"]
	if kwargs.get("developer"):
		developer = kwargs["developer"]
	if kwargs.get("romsize"):
		romsize = kwargs["romsize"]
	if kwargs.get("cs1"):
		cs1 = kwargs["cs1"]
	if kwargs.get("cs2"):
		cs2 = kwargs["cs2"]
	if kwargs.get("min_soc"):
		min_soc = kwargs["min_soc"]
	if kwargs.get("rev"):
		rev = kwargs["rev"]
	if kwargs.get("copyright"):
		copystart = kwargs["copyright"]
		copyend = kwargs["copyright"]
	if kwargs.get("copystart"):
		copystart = kwargs["copystart"]
	if kwargs.get("copyend"):
		copyend = kwargs["copyend"]
	crc_data = HEADER.pack(title,developer,magic,romsize,cs1,cs2,min_soc,rev,copystart,copyend,0)[:-2]
	crc = crc16(crc_data)
	data[:256] = HEADER.pack(title,developer,magic,romsize,cs1,cs2,min_soc,rev,copystart,copyend,crc)

def bcd(n):
	s = []
	x = 0
	while n>0:
		a, b = divmod(n,10)
		s.append(b)
		n = a
	while s:
		x<<=4
		x|=s.pop()
	return x

def main(*argv):
	parser = argparse.ArgumentParser(prog="hhfix.py",description="Fixes Hexheld ROM.")
	parser.add_argument("-t","--title",help="Overrides the title in the ROM.")
	parser.add_argument("-d","--developer",help="Overrides the developer in the ROM.")
	parser.add_argument("-s","--size",help="Overrides the ROM size in the ROM.")
	parser.add_argument("-1","--cs1",help="Overrides the CS1 version in the ROM.")
	parser.add_argument("-2","--cs2",help="Overrides the CS2 version in the ROM.")
	parser.add_argument("-m","--min-soc",help="Overrides the min SoC version in the ROM.")
	parser.add_argument("-r","--revision",help="Overrides the revision in the ROM.")
	parser.add_argument("--copystart",help="Overrides the copyright start year in the ROM.")
	parser.add_argument("--copyend",help="Overrides the copyright end year in the ROM.")
	parser.add_argument("-c","--copyright",help="Overrides the copyright start and end years in the ROM. Overriden by copystart and copyend.")
	parser.add_argument("rom",help="ROM file. Will be fixed in-place.")
	args = parser.parse_args(argv)
	print(args)
	kwargs = {}
	if args.title: kwargs['title']=args.title.encode('ascii')
	if args.developer: kwargs['developer']=args.developer.encode('ascii')
	if args.size: kwargs['romsize']=int(args.size,0)
	if args.cs1: kwargs['cs1']=int(args.cs1,0)
	if args.cs2: kwargs['cs2']=int(args.cs2,0)
	if args.min_soc: kwargs['min_soc']=int(args.min_soc,0)
	if args.revision: kwargs['revision']=int(args.revision,0)
	if args.copystart:
		year = int(args.copystart)
		kwargs['copystart']=bcd(year)
	if args.copyend:
		year = int(args.copyend)
		kwargs['copyend']=bcd(year)
	if args.copyright:
		year = int(args.copyright)
		kwargs['copyright']=bcd(year)
	with open(args.rom,"rb") as f: data=bytearray(f.read())
	fixheader(data,**kwargs)
	with open(args.rom,"wb") as f: f.write(data)

import sys
if __name__=="__main__": main(*sys.argv[1:])
