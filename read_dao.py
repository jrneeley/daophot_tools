import sys
import numpy as np
import matplotlib.pyplot as mp


def read_raw(raw_file, filters=[], mjds=[]):

    f = open(raw_file, 'r')
    lines = f.readlines()
    nstars = 0
    data_all=[['header']]

    for i, line in enumerate(lines):
        # skip header lines
        if i <= 2:
            continue
        temp = line.split()
        if i == 3:
            nmax = len(temp)
        if len(temp) == 15:
            nstars += 1
            data_all.append(temp)
        if len(temp) < 15:
            if len(temp) == nmax:
                nstars += 1
                data_all.append(temp)
            else:
                data_all[nstars]=data_all[nstars]+temp

    #star_ids = [item[0] for item in mags_all]
    #star_ids.remove(star_ids[0])
    data_all.remove(data_all[0])
    star_ids = [item[0] for item in data_all]
    star_x = [item[1] for item in data_all]
    star_y = [item[2] for item in data_all]
    star_chi = [item[-2] for item in data_all]
    star_sharp = [item[-1] for item in data_all]

    nstars = len(star_ids)
    nobs = int(len(data_all[0][3:-2])/2)

    dt = np.dtype([('ids', int), ('x', float), ('y', float),
        ('filters', 'U10', nobs), ('mjds', float, nobs),
        ('mags', float, nobs), ('errs', float, nobs),
        ('chi', float), ('sharp', float)])
    data = np.zeros(nstars, dtype=dt)
    data['ids'] = star_ids
    data['x'] = star_x
    data['y'] = star_y
    data['chi'] = star_chi
    data['sharp'] = star_sharp
    for i in range(nstars):
        data['mags'][i] = data_all[i][3:-2:2]
        data['errs'][i] = data_all[i][4:-2:2]

        if len(filters) == 0:
            data['filters'][i] = np.repeat('F', nobs)
        else:
            data['filters'][i] = filters
        if len(mjds) == 0:
            data['mjds'][i] = np.repeat(np.nan, nobs)
        else:
            data['mjds'][i] = mjds
    return data

def read_coo(coo_file):

    dtype = np.dtype([('id', int), ('x', float), ('y', float), ('mag', float),
        ('sharp', float), ('round', float), ('round2', float)])
    data = np.loadtxt(coo_file, dtype=dtype, skiprows=3)

    return data

def read_ap_long(ap_file):

    f = open(ap_file, 'r')
    lines = f.readlines()
    nstars = 0
    data_all=[]

    for i, line in enumerate(lines):
        # skip header lines
        if i <= 2:
            continue
        # get array from line
        temp = line.split()
        if len(temp) == 0:
            nstars += 1
            start = 1
            continue
        if start == 1:
            data_all.append(temp)
            start = 0
        elif start == 0:
            data_all[nstars-1]=data_all[nstars-1]+temp

    n = len(data_all[0])
    n_aps = int((n - 6)/2)


    dt = np.dtype([('ids', int), ('x', float), ('y', float),
        ('mags', float, n_aps), ('errs', float, n_aps),
        ('modal_sky', float), ('std_sky', float), ('skew_sky', float)])
    data = np.zeros(nstars, dtype=dt)
    data['ids'] = [item[0] for item in data_all]
    data['x'] = [item[1] for item in data_all]
    data['y'] = [item[2] for item in data_all]
    data['modal_sky'] = [item[n_aps+3] for item in data_all]
    data['std_sky'] = [item[n_aps+4] for item in data_all]
    data['skew_sky'] = [item[n_aps+5] for item in data_all]

    data['mags'] = [item[3:3+n_aps] for item in data_all]
    data['errs'] = [item[n_aps+6:] for item in data_all]

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

def read_head(mag_file):
     
    f = open(mag_file, 'r')
    line0 = f.readline()
    line1 = f.readline()
    temp = line1.split()

    dt = np.dtype([('NL', int), ('NX', int), ('NY', int), ('LOWBAD', float), 
                   ('HIGHBAD', float), ('THRESH', float), ('AP1', float), 
                   ('PHPADU', float), ('RNOISE', float), ('FRAD', float)])
    head = np.zeros(1, dtype=dt)
    head['NL'] = temp[0]
    head['NX'] = temp[1]
    head['NY'] = temp[2]
    head['LOWBAD'] = temp[3]
    head['HIGHBAD'] = temp[4]
    head['THRESH'] = temp[5]
    head['AP1'] = temp[6]
    head['PHPADU'] = temp[7]
    head['RNOISE'] = temp[8]
    head['FRAD'] = temp[9]

    return head

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
    
    # determine degrees of freedom in transformation
    line1 = lines[0].split()
    dof = len(line1[2:-2])

    dt = np.dtype([('filename', 'U30'), ('dof', int),
                ('transform_matrix', float, (dof,))])
    data = np.zeros(n_lines, dtype=dt)
    for i in range(n_lines):
        data['dof'][i] = dof
        temp = lines[i].split()
        file_name = temp[0].replace('\'', '')
        file_name = file_name.split(':')
        if len(file_name) == 1:
            data['filename'][i] = file_name[0]
        else:
            data['filename'][i] = file_name[1]
        data['transform_matrix'][i] = temp[2:-2]

    return data

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
        ('err', float), ('sky', float), ('N iters', float), ('chi', float),
        ('sharp', float)])
    data = np.loadtxt(alf_file, dtype=dtype1, skiprows=3)

    return data


def read_add(add_file):

    dtype = np.dtype([('id', int), ('x', float), ('y', float), ('mag', float)])
    data = np.loadtxt(add_file, dtype=dtype, skiprows=3)

    return data
