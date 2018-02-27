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

def read_ap(ap_file):

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
        ('err', float)])
    data = np.loadtxt(mag_file, dtype=dtype1, usecols=(0,1,2,3,4), skiprows=3)

    return data

def read_mch(mch_file):

    file_list = []
    x_offset = []
    y_offset = []
    transform_matrix = []
    f = open(mch_file, 'r')
    for line in f:
        temp = line.split()
        n=len(temp[0])
        file_name = temp[0].replace('\'','')
        file_name = file_name.split(':')
        if len(file_name) == 1:
            file_list.append(file_name[0])
        if len(file_name) != 1:
            file_list.append(file_name[1])
        x_offset.append(temp[2])
        y_offset.append(temp[3])
        transform_matrix.append(temp[4:-2])
    dof = len(transform_matrix[1])

    return file_list, x_offset, y_offset, transform_matrix, dof

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

    dtype1 = np.dtype([('id', int), ('x', float), ('y', float), ('mag', float), ('err', float)])
    data = np.loadtxt(alf_file, dtype=dtype1, usecols=(0,1,2,3,4), skiprows=3)

    ids = data['id']
    x = data['x']
    y = data['y']
    mag = data['mag']
    err = data['err']


    return data

def read_coo_new(coo_file):

    dtype1 = np.dtype([('id', int), ('x', float), ('y', float), ('mag1', float),
        ('err', float), ('mag2', float)])
    data = np.loadtxt(coo_file, dtype=dtype1, usecols=(0,1,2,3,4,5), skiprows=3)

    return data
