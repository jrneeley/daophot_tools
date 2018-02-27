#!/usr/bin/env python

import re
import shutil
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as mp
import sys
from matplotlib.ticker import ScalarFormatter

def folder_setup():
	daophot_dir = raw_input("Enter path to Daophot executables: ")
	optical_dir = raw_input("Enter path to optical catalogs: ")
	opt_dir = raw_input("Enter path to OPT files: ")
	return daophot_dir, optical_dir, opt_dir

def spitzer_flux2dn(image, newname="", exptime=None, fluxconv=None):

	if (newname == ""):
		newname = re.sub(".fits", "_dn.fits", image)
	shutil.copy(image, newname)
	hdulist = fits.open(newname, mode='update')
	prihdr = hdulist[0].header
	scidata = hdulist[0].data
	if exptime == None : exptime = prihdr['exptime']
	if fluxconv == None : fluxconv = prihdr['fluxconv']
	scidata *= exptime/fluxconv


def set_opt_files(opt_dir, channel, exptime, warm=1):

	if warm == 1:
		opt_dir2 = opt_dir+'warm/'
	if warm == 0:
		opt_dir2 = opt_dir+'cryo/'

	if (channel == 'I1'):
		optfile = opt_dir2+'ch1-'+str(exptime)+'s.opt'
	if (channel == 'I2'):
		optfile = opt_dir2+'ch2-'+str(exptime)+'s.opt'
	shutil.copy(optfile, 'daophot.opt')
	shutil.copy(opt_dir+'photo.opt', 'photo.opt')
	shutil.copy(opt_dir+'allstar.opt', 'allstar.opt')
	shutil.copy(opt_dir+'allframe.opt', 'allframe.opt')

def set_opt_files_mosaic(opt_dir, channel, exptime, warm=1):

	if warm == 0:
		opt_dir2 = opt_dir+'cryo/'
	if warm == 1:
		opt_dir2 = opt_dir+'warm/'
	if (channel == 'I1'):
		optfile = opt_dir2+'ch1-'+str(exptime)+'s-mosaic.opt'
	if (channel == 'I2'):
		optfile = opt_dir2+'ch2-'+str(exptime)+'s-mosaic.opt'
	shutil.copy(optfile, 'daophot.opt')
	shutil.copy(opt_dir+'photo-mosaic.opt', 'photo.opt')
	shutil.copy(opt_dir+'allstar-mosaic.opt', 'allstar.opt')
	shutil.copy(opt_dir+'allframe.opt', 'allframe.opt')

def find_fields(image_list, channel):
	off_list = []
	on_list = []
	center_ra = []
	center_dec = []
	for image in image_list:
		hdulist = fits.open(image)
		prihdr = hdulist[0].header
		fovid = prihdr['fovid']
# If not a map, we can determine fields directly from header
		if fovid != 81:
			if channel == 'I1':
				if fovid == 74:
					off_list.append(image)
					center_ra.append(prihdr['crval1'])
					center_dec.append(prihdr['crval2'])
				if fovid == 67:
					on_list.append(image)
					center_ra.append(prihdr['crval1'])
					center_dec.append(prihdr['crval2'])
			if channel == 'I2':
				if fovid == 67:
					off_list.append(image)
					center_ra.append(prihdr['crval1'])
					center_dec.append(prihdr['crval2'])
				if fovid == 74:
					on_list.append(image)
					center_ra.append(prihdr['crval1'])
					center_dec.append(prihdr['crval2'])
# If it is a map, we need to find the fields from the coordinates
		if fovid == 81:
			center_ra.append(prihdr['crval1'])
			center_dec.append(prihdr['crval2'])
# Plot to count number of fields
	mp.plot(center_ra, center_dec,'ro')
	mp.ylabel('Dec')
	mp.xlabel('RA')
	x_formatter = ScalarFormatter(useOffset=False)
	mp.gca().xaxis.set_major_formatter(x_formatter)
#	mp.savefig('mapping-positions.eps', format='eps')
	mp.show()
# Ask user how many separate fields there are
	num_fields = input('How many fields exist for this data set?: ')
	if fovid != 81:
		if channel == 'I1':
			field_lists = [off_list, on_list]
		if channel == 'I2':
			field_lists = [on_list, off_list]
	if fovid == 81:
		field_lists = []
		list_of_fields = raw_input('Enter file with list of fields: ')
		f = open(list_of_fields, 'r')
		lists = f.readlines()
		if len(lists) != num_fields:
			sys.exit("Wrong number of fields!")
		for lst in lists:
			lst = lst.strip()
			f2 = open(lst, 'r')
			field_images = f2.readlines()
			field_n = []
			for image in field_images:
				image = image.strip()
				field_n.append(image)
			field_lists.append(field_n)
			f2.close()
		f.close()

	return num_fields, field_lists
