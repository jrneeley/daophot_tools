#!/usr/bin/env python


import re
import os
import numpy as np
import shutil
import pexpect
from astropy.io import fits
import sys


def allstar_init(dao_dir, target, fitsfile, mosaics=0):

	file_stem = re.sub(".fits","", fitsfile)

## Clean up previous runs

        extensions = ['.als', 's.coo']
        for ext in extensions:
                if (os.path.isfile(file_stem + ext)):
                        os.remove(file_stem + ext)
		if mosaics == 0: image=re.sub("data/",target+":", file_stem)
		if mosaics == 1: image=re.sub("mosaics/",target+"m:", file_stem)
    #    print "Working on " + image

## Running ALLSTAR
	allstar = pexpect.spawn(dao_dir+'allstar', timeout=240)
	#allstar.logfile = sys.stdout

	allstar.expect("OPT")
	allstar.sendline("")
	allstar.expect("Input image name")
	allstar.sendline(image)
	allstar.expect("File with the PSF")
	allstar.sendline("")
	allstar.expect("Input file")
	allstar.sendline("")
	allstar.expect("File for results")
	allstar.sendline("")
	allstar.expect("Name for subtracted image")
	allstar.sendline("")
	allstar.expect("stars")
	allstar.expect("Good bye")
	allstar.close()

def allstar_deep(dao_dir, fitsfile):

	file_stem = re.sub(".fits","", fitsfile)

## Clean up previous runs

        extensions = ['.als', 's.fits']
        for ext in extensions:
                if (os.path.isfile(file_stem + ext)):
                        os.remove(file_stem + ext)
    #    print "Working on " + image

## Running ALLSTAR
	allstar = pexpect.spawn(dao_dir+'allstar', timeout=240)
	allstar.logfile = sys.stdout

	allstar.expect("OPT")
	allstar.sendline("")
	allstar.expect("Input image name")
	allstar.sendline(fitsfile)
	allstar.expect("File with the PSF")
	allstar.sendline("")
	allstar.expect("Input file")
	allstar.sendline("")
	allstar.expect("File for results")
	allstar.sendline("")
	allstar.expect("Name for subtracted image")
	allstar.sendline("")
	allstar.expect("stars")
	allstar.expect("Good bye")
	allstar.close()
