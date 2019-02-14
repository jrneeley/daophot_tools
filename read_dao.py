#!/usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as mp


def read_raw(raw_file):

    f = open(raw_file, 'r')
    lines = f.readlines()
    nstars = 0
    mags_all=[['header']]

    for line in lines:
        temp = line.split()
        if len(temp) == 15:
            nstars += 1
            mags_all.append(temp)
        if len(temp) < 15:
            mags_all[nstars]=mags_all[nstars]+temp

    star_ids = [item[0] for item in mags_all]
    star_ids.remove(star_ids[0])
    mags_all.remove(mags_all[0])

    return star_ids, mags_all

def read_coo(coo_file):

    dtype = np.dtype([('id', int), ('x', float), ('y', float), ('mag', float),
        ('sharp', float), ('round', float), ('round2', float)])
    data = np.loadtxt(coo_file, dtype=dtype, skiprows=3)

    return data


def read_ap(ap_file):
# Needs checking
    dtype = np.dtype([('id', float), ('x', float), ('y', float), ('mag', float)])
    data = np.loadtxt(ap_file, dtype=dtype, skiprows=3)

    ids = data['id'][0::2].astype(int)
    x = data['x'][0::2]
    y = data['y'][0::2]
    mags = data['mag'][0::2]
    err = data['mag'][1::2]
    return ids, mags, err

def read_mag(mag_file):

    dtype1 = np.dtype([('id', int), ('x', float), ('y', float), ('mag', float),
        ('err', float), ('err2', float), ('N frames', int), ('chi', float),
        ('sharp', float), ('var index', float), ('blunder index', float)])
    data = np.loadtxt(mag_file, dtype=dtype1, skiprows=3)

    return data

def read_mch(mch_file):

    f = open(mch_file, 'r')
    lines = f.readlines()
    n_lines = len(lines)

    dt = np.dtype([('file', 'S30'), ('x_offset', float), ('y_offset', float), ('transform_matrix', float, (4,))])
    simple_transform = np.zeros(n_lines, dtype=dt)

    file_list = np.zeros(n_lines, dtype='S30')
    x_offset = np.zeros(n_lines)
    y_offset = np.zeros(n_lines)
    transform = np.zeros((n_lines, 4))

    for ii, line in enumerate(lines):
        temp = line.split()
        file_name = temp[0].replace('\'','')
        file_name = file_name.split(':')
        if len(file_name) == 1:
            file_list[ii] = file_name[0]
        if len(file_name) != 1:
            file_list[ii] = file_name[1]
        x_offset[ii] = temp[2]
        y_offset[ii] = temp[3]
        transform[ii] = temp[4:8]

    simple_transform['file'] = file_list
    simple_transform['x_offset'] = x_offset
    simple_transform['y_offset'] = y_offset
    simple_transform['transform_matrix'] = transform

    return simple_transform

def read_nmg(nmg_file):

    data = ascii.read(nmg_file, delimiter=' ', data_start=2)

    id_num = np.array(data['col1'])
    x = np.array(data['col2'])
    y = np.array(data['col3'])
    mag = np.array(data['col4'])
    err = np.array(data['col5'])
    chi = np.array(data['col8'])
    sharp = np.array(data['col9'])

    return id_num, x, y, mag, err, chi, sharp

def read_lst(lst_file):

    dtype1 = np.dtype([('id', int), ('x', float), ('y', float)])
    data = np.loadtxt(lst_file, dtype = dtype1, usecols=(0,1,2), skiprows=3)

    ids = data['id']
    x = data['x']
    y = data['y']


    return ids, x, y

def read_alf(alf_file):

    dtype1 = np.dtype([('id', int), ('x', float), ('y', float), ('mag', float),
        ('err', float), ('sky', float), ('N iters', int), ('chi', float),
        ('sharp', float)])
    data = np.loadtxt(alf_file, dtype=dtype1, skiprows=3)

    return data


def read_add(add_file):

    dtype = np.dtype([('id', int), ('x', float), ('y', float), ('mag', float)])
    data = np.loadtxt(add_file, dtype=dtype, skiprows=3)

    return data
