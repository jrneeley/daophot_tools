import numpy as np
import sys
import AstroTools as at
from . import read_dao

def dao2reg(infile, outfile, ids=1, color='green', radius=10):


    data = np.loadtxt(infile, skiprows=3, usecols=(0,1,2))

    f = open(outfile+'.reg', 'w')
    f.write('global color={}\n'.format(color))
    f.write('image \n')
    for ii in range(len(data[:,0])):
        if ids == 1:
            f.write('circle {:7.2f} {:7.2f} {} # text= {{ {} }}\n'.format(\
                data[ii,1], data[ii,2], radius, int(data[ii,0])))
        else:
            f.write('circle {:7.2f} {:7.2f} {} \n'.format(data[ii,1],data[ii,2], radius))
    f.close()

#### DO NOT USE - NOT COMPLETE
def make_catalog(filters, star_list='median.off', mch_file='alf.mch'):

    n_filters = len(filters)

    # Setup array structures using input star list
    input_list = read_dao.read_mag(star_list)
    file_list = read_dao.read_mch()
    n_images = len(file_list['file'])

    ids = input_list['id']
    sort_ids = ids.argsort()
    n_stars = len(input_list['id'])

    multiepoch_mags = np.zeros((n_stars, n_images))
    multiepoch_errs = np.zeros((n_stars, n_images))
    multiepoch_chi = np.zeros((n_stars, n_images))
    multiepoch_sharp = np.zeros((n_stars, n_images))
    multiepoch_times = np.zeros((n_stars, n_images))
