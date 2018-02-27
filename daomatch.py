#!/usr/bin/env python

import sys
import pexpect
import read_dao
import matplotlib.pyplot as mp
import numpy as np

# run daomatch on a list of images
def daomatch(image_list, output_file, dao_dir='/apps/daophot32/',
                    xy_limits=None, force_scale_rot=0, force_scale=0):

## run DAOMATCH on on fields
    daomatch = pexpect.spawn(dao_dir+'daomatch')
    daomatch.logfile = sys.stdout

    daomatch.expect("Master input file")
    first_file = image_list[0]
    if xy_limits != None:
        daomatch.sendline(first_file+'*')
        daomatch.expect('Ymin, Ymax')
        daomatch.sendline(xy_limits)
    if xy_limits == None:
        daomatch.sendline(first_file)
    daomatch.expect("Output file")
    daomatch.sendline(output_file)
    check = daomatch.expect(["Next input file", "New output file"])
    if check == 1:
        daomatch.sendline("")

    # define appropriate suffix for images
    suffix = ''
    if force_scale_rot == 1:
        suffix = ';'
    if force_scale != 0:
        suffix = '/'+str(force_scale)
    if xy_limits != None:
        suffix += '!'

    for image in image_list:
        if image == first_file:
            continue
#            if check == 0:
        daomatch.sendline(image+suffix)
        check = daomatch.expect(["Next input file", "Write this transformation"])

        if check == 1:
            daomatch.sendline('y')
        if check == 0:
            continue
#            daomatch.expect('Next input file')
#            daomatch.sendline(image+suffix)

#    daomatch.expect("Next input file")
    daomatch.sendline("")
    daomatch.expect("Good bye")
    daomatch.close()


def check_daomatch(mch_file):

    img_list, x_offsets, y_offsets, transform, dof = read_dao.read_mch(mch_file)

    n_imgs = len(img_list)
    master_frame = read_dao.read_alf(img_list[0])

    master_order = np.argsort(master_frame['mag'])
    master_brightest = master_order[0:100]

    for ind in range(1,n_imgs):
        fig = mp.figure(figsize=(10,8))
        ax1 = fig.add_subplot(111)
        ax1.plot(master_frame['x'][master_brightest], master_frame['y'][master_brightest], 'b.', alpha=0.5, markersize=15)
        data = read_dao.read_alf(img_list[ind])
        data_order = np.argsort(data['mag'])
        data_brightest = data_order[0:100]
        x_new = float(x_offsets[ind]) + float(transform[ind][0])*data['x'] + float(transform[ind][1])*data['y']
        y_new = float(y_offsets[ind]) + float(transform[ind][2])*data['x'] + float(transform[ind][3])*data['y']
        ax1.plot(x_new[data_brightest], y_new[data_brightest], 'r.', alpha=0.5, markersize=15)
        ax1.set_title(img_list[ind])
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        mp.show()
