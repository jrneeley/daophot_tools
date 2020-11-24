import re
import os
import numpy as np
import pexpect
import sys
import matplotlib.pyplot as mp
from . import config
from . import read_dao
###############################################################################
#                          DAOPHOT
###############################################################################

def find(fitsfile, num_frames='1,1', coo_file='', opt_file='', new_thresh=0,
    verbose=0):

    dao_dir = config.dao_dir
    image = re.sub(".fits","", fitsfile)

## Running daophot
    daophot = pexpect.spawn(dao_dir+'daophot', encoding='utf-8')
    if verbose == 1:
        daophot.logfile = sys.stdout
    elif isinstance(verbose, str):
        daophot.logfile = open(verbose, 'w')

# Load appropriate opt file and edit threshold if necessary
    daophot.expect('Command:')
    daophot.sendline('op')
    daophot.expect('File with parameters')
    daophot.sendline(opt_file)
    daophot.expect('OPT>')
    if new_thresh > 0:
        daophot.sendline('th={}'.format(new_thresh))
        daophot.expect('OPT>')
    daophot.sendline('')

# ATTACH
    daophot.expect("Command:")
    daophot.sendline("at " + image)

    daophot.expect("Command:")
    daophot.sendline("find")
    daophot.expect("Number of frames averaged, summed:")
    daophot.sendline(num_frames)
    daophot.expect("File for positions")
    daophot.sendline(coo_file)
    check = daophot.expect(['Are you happy with this?', 'OVERWRITE'])
    if check == 1:
        daophot.sendline('')
        daophot.expect("Are you happy with this?")
        daophot.sendline("y")
    if check == 0:
        daophot.sendline("y")
    daophot.expect('Command:')
    daophot.sendline('exit')
    if isinstance(verbose, str):
        daophot.logfile.close()
    daophot.close(force=True)

def phot(fitsfile, phot_file='', coo_file='', ap_file='', opt_file='', verbose=1):

    dao_dir = config.dao_dir
    image = re.sub(".fits","", fitsfile)

## Running daophot
    daophot = pexpect.spawn(dao_dir+'daophot', encoding='utf-8')
    if verbose == 1:
        daophot.logfile = sys.stdout

# Load appropriate opt file and edit threshold if necessary
    daophot.expect('Command:')
    daophot.sendline('op')
    daophot.expect('File with parameters')
    daophot.sendline(opt_file)
    daophot.expect('OPT>')
    daophot.sendline('')

# ATTACH
    daophot.expect("Command:")
    daophot.sendline("at " + image)

# PHOT
    daophot.expect("Command:")
    daophot.sendline("phot")
    daophot.expect("File with aperture radii")
    daophot.sendline("")
    daophot.expect("PHO>")
    daophot.sendline("")
    check = daophot.expect(['Input position file', 'Profile-fitting photometry'])
    if check == 1:
        daophot.sendline('e')
        daophot.expect('Input position file')
        daophot.sendline(coo_file)
    if check == 0:
        daophot.sendline(coo_file)
    daophot.expect("Output file")
    daophot.sendline(ap_file)

## Exit Daophot
    check2 = daophot.expect(['Command:', 'OVERWRITE'])
    if check2 == 1:
        daophot.sendline('')
        daophot.expect('Command:')
        daophot.sendline('exit')
    if check2 == 0:
        daophot.sendline("exit")
    daophot.close(force=True)

# Not well tested....
def find_psf(fitsfile, opt_file=''):

    file_stem = re.sub(".fits","", fitsfile)

## Clean up previous runs

    extensions = ['.psf', '.nei']
    for ext in extensions:
        if (os.path.isfile(file_stem + ext)):
            os.remove(file_stem + ext)

    image = fitsfile
    print("Working on " + image)

#Running daophot
    daophot = pexpect.spawn(config.dao_dir+'daophot', encoding='utf-8')
    daophot.logfile = sys.stdout

# Load appropriate opt file and edit threshold if necessary
    daophot.expect('Command:')
    daophot.sendline('op')
    daophot.expect('File with parameters')
    daophot.sendline(opt_file)
    daophot.expect('OPT>')
    daophot.sendline('')

# attach the image
    daophot.expect("Command:")
    daophot.sendline("at " + file_stem)
## PSF
    daophot.expect("Command:")
    daophot.sendline("psf")
    daophot.expect("File with aperture results")
    daophot.sendline("")
    daophot.expect("File with PSF")
    daophot.sendline("")
    daophot.expect("File for the PSF")
    daophot.sendline("")
## Exit Daophot
    daophot.expect("Command:")
    daophot.sendline("exit")
    daophot.close(force=True)
    print("PSF complete")


def substar(fitsfile, leave_stars=1, verbose=1):

    daophot = pexpect.spawn(config.dao_dir+'daophot', encoding='utf-8')
    if verbose == 1:
        daophot.logfile = sys.stdout

    daophot.expect('Command:')
    daophot.sendline('at '+fitsfile)
    daophot.expect('Command:')
    daophot.sendline('substar')
    daophot.expect('File with the PSF')
    daophot.sendline('')
    daophot.expect('File with photometry')
    daophot.sendline('.als')
    daophot.expect('stars to leave in?')
    if leave_stars == 1:
        daophot.sendline('y')
        daophot.expect('File with star list')
        daophot.sendline('')
    daophot.expect('Name for subtracted image')
    daophot.sendline('')
    daophot.expect('Command:')
    daophot.sendline('ex')
    daophot.close(force=True)

def offset(filename, id_offset=0, x_offset=0.0, y_offset=0.0, mag_offset=0.0,
    verbose=1):

    daophot = pexpect.spawn(config.dao_dir+'daophot', encoding='utf-8')
    if verbose == 1:
        daophot.logfile = sys.stdout

    daophot.expect('Command')
    daophot.sendline('off')
    daophot.expect('Input file name')
    daophot.sendline(filename)
    daophot.expect('Additive offsets')
    off_string = '{} {} {} {}'.format(id_offset, x_offset, y_offset, mag_offset)
    daophot.sendline(off_string)
    daophot.expect('Output file name')
    daophot.sendline('')
    check = daophot.expect(['Command', 'OVERWRITE'])
    if check == 1:
        daophot.sendline('')
        daophot.expect('Command')
        daophot.sendline('ex')
    if check == 0:
        daophot.sendline('ex')
    daophot.close(force=True)


def append(file1, file2, out_file='', verbose=0):

    daophot = pexpect.spawn(config.dao_dir+'daophot', encoding='utf-8')
    if verbose == 1:
        daophot.logfile = sys.stdout
    daophot.expect('Command:')
    daophot.sendline('append')
    daophot.expect('First input file')
    daophot.sendline(file1)
    daophot.expect('Second input file')
    daophot.sendline(file2)
    daophot.expect('Output file')
    daophot.sendline(out_file)
    check = daophot.expect(['Command:', 'OVERWRITE'])
    if check == 1:
        daophot.sendline('')
        daophot.expect('Command:')
    daophot.sendline('exit')
    daophot.close(force=True)

def sort(in_file, out_file='', sort_option='3', renumber='y', verbose=0):

    # sort_option +- 1 -> increasing/decreasing ID number
    # sort option +- 2 -> increasing/decreasing X
    # sort option +- 3 -> increasing/decreasing Y
    # sort option +- 4 -> increasing/decreasing magnitude

    daophot = pexpect.spawn(config.dao_dir+'daophot', encoding='utf-8')
    if verbose == 1:
        daophot.logfile = sys.stdout
    daophot.expect('Command:')
    daophot.sendline('sort')
    daophot.expect('Which do you want')
    daophot.sendline(sort_option)
    daophot.expect('Input file name')
    daophot.sendline(in_file)
    daophot.expect('Output file name')
    daophot.sendline(out_file)
    check = daophot.expect(['stars renumbered?', 'OVERWRITE'])
    if check == 1:
        daophot.sendline('')
        daophot.expect('stars renumbered?')
        daophot.sendline(renumber)
    if check == 0:
        daophot.sendline(renumber)

    daophot.expect('Command:')
    daophot.sendline('exit')
    daophot.close(force=True)

def addstar(image, file_stem='fake', num_images = 1, seed=5, gain=999, star_list=None,
    min_mag=12, max_mag=18, num_stars=50, opt_file='', verbose=0):

    daophot = pexpect.spawn(config.dao_dir+'daophot', encoding='utf-8')
    if verbose == 1: daophot.logfile = sys.stdout

    # Make sure we are using the appropriate options file
    daophot.expect('Command:')
    daophot.sendline('opt')
    daophot.expect('File with parameters')
    daophot.sendline(opt_file)
    daophot.expect('OPT')
    daophot.sendline('')

    # First attach original image
    daophot.expect('Command:')
    daophot.sendline('at '+image)
    # start addstar
    daophot.expect('Command:')
    daophot.sendline('ad')
    daophot.expect('File with the PSF')
    daophot.sendline('')
    daophot.expect('Seed')
    daophot.sendline(str(seed))
    daophot.expect('Photons per ADU')
    daophot.sendline(str(gain))
    daophot.expect('Input data file')
    if star_list != None:
        daophot.sendline(star_list)
        daophot.expect('Output picture name')
        daophot.sendline(file_stem+'01')
        check = daophot.expect(['Input data file', 'really what you want?'])
        if check == 0:
            daophot.sendline('')
        if check == 1:
            daophot.sendline('y')
        daophot.expect('Input data file')
        daophot.sendline('')
        daophot.expect('Command')
        daophot.sendline('ex')
        daophot.close(force=True)
    else:
        daophot.sendline('')
        daophot.expect('Minimum, maximum magnitudes')
        daophot.sendline('{} {}'.format(min_mag, max_mag))
        daophot.expect('Number of stars to add')
        daophot.sendline(str(num_stars))
        daophot.expect('Number of new frames')
        daophot.sendline(str(num_images))
        daophot.expect('File-name stem')
        daophot.sendline(file_stem)
        check = daophot.expect(['Command', 'OVERWRITE'])
        if check == 0:
            daophot.sendline('ex')
            daophot.close(force=True)
        if check == 1:
            daophot.sendline('')
            for ii in range(num_images-1):
                daophot.expect('OVERWRITE')
                daophot.sendline('')
            daophot.expect('Command')
            daophot.sendline('ex')
            daophot.close(force=True)

###############################################################################
#                          ALLSTAR
###############################################################################

def allstar(fitsfile, new_options=0, sub_img='', suppress=0, verbose=0):

    file_stem = re.sub(".fits","", fitsfile)

## Running ALLSTAR
    allstar = pexpect.spawn(config.dao_dir+'allstar', encoding='utf-8', timeout=None)

    if verbose == 1:
        allstar.logfile = sys.stdout

    allstar.expect("OPT")
    if new_options == 0:
        allstar.sendline("")
    else:
        n_changes=len(new_options)
        for ii in range(n_changes):
            allstar.sendline(new_options[ii])
            allstar.expect("OPT")
        allstar.sendline("")
    allstar.expect("Input image name")
    allstar.sendline(file_stem)
    allstar.expect("File with the PSF")
    allstar.sendline("")
    allstar.expect("Input file")
    allstar.sendline("")
    allstar.expect("File for results")
    allstar.sendline("")
    check = allstar.expect(["Name for subtracted image", "OVERWRITE"])
    if check == 1:
        allstar.sendline("")
        allstar.expect("Name for subtracted image")
    if suppress == 0:
        allstar.sendline(sub_img)
        allstar.expect("Good bye")
        allstar.close(force=True)
    if suppress == 1:
        allstar.sendcontrol("d")
        allstar.expect("Good bye")
        #allstar.sendcontrol("c") - not working right now
        allstar.close(force=True)


###############################################################################
#                    DAOMATCH/ DAOMASTER
###############################################################################

# run daomatch on a list of images
def daomatch(image_list, output_file, verbose=0,
                    xy_limits=[], force_scale_rot=0, force_scale=0):

## run DAOMATCH on on fields
    daomatch = pexpect.spawn(config.dao_dir+'daomatch', encoding='utf-8')
    if verbose == 1:
        daomatch.logfile = sys.stdout

    daomatch.expect("Master input file")
    first_file = image_list[0]
    if len(xy_limits) == 4:
        daomatch.sendline(first_file+'*')
        daomatch.expect('Ymin, Ymax')
        xylim = '{} {} {} {}'.format(xy_limits[0], xy_limits[1], xy_limits[2], xy_limits[3])
        daomatch.sendline(xylim)
    elif len(xy_limits) == 0:
        daomatch.sendline(first_file)
    else:
        daomatch.close(force=True)
        print('Must provide 4 limits! (xmin, xmax, ymin, ymax)')
    daomatch.expect("Output file")
    daomatch.sendline(output_file)
    check = daomatch.expect(["Next input file", "OVERWRITE"])
    if check == 1:
        daomatch.sendline("")
        daomatch.expect("Next input file")
    # define appropriate suffix for images
    suffix = ''
    if force_scale_rot == 1:
        suffix = ';'
    if force_scale != 0:
        suffix = '/'+str(force_scale)
    if len(xy_limits) != 0:
        suffix += '!'

    for image in image_list:
        if image == first_file:
            continue
#            if check == 0:
        daomatch.sendline(image+suffix)
        check = daomatch.expect(["Next input file", "Write this transformation"])
        if check == 1:
            daomatch.sendline("y")
            daomatch.expect("Next input file")
        if check == 0:
            continue

    daomatch.sendline("")
    daomatch.expect("Good bye")
    daomatch.close()


def check_daomatch(mch_file, bright_only=True):

    #img_list, x_offsets, y_offsets, transform, dof = read_dao.read_mch(mch_file)
    tran = read_dao.read_mch(mch_file) 
    img_list = tran['filename']
    dof = tran['dof'][0]
    transform = tran['transform_matrix']
   
    n_imgs = len(img_list)
    master_frame = read_dao.read_alf(img_list[0])

    master_order = np.argsort(master_frame['mag'])
    if bright_only == True: 
        use = master_order[0:100]
    else: 
        use = master_order

    for ind in range(1,n_imgs):
        fig = mp.figure(figsize=(10,8))
        ax1 = fig.add_subplot(111)
        ax1.plot(master_frame['x'][use], master_frame['y'][use], 'b.', alpha=0.5, markersize=15)
        print(img_list[ind])
        data = read_dao.read_alf(img_list[ind])
        data_order = np.argsort(data['mag'])
        if bright_only == True: 
            use = data_order[0:100]
        else: 
            use = data_order

        # apply transformation 
        x_new = transform[ind][0] + transform[ind][2]*data['x'] + transform[ind][4]*data['y']
        y_new = transform[ind][1] + transform[ind][3]*data['x'] + transform[ind][5]*data['y']         
        
        if dof >= 12:
            head = read_dao.read_head(img_list[ind])
            ncol = head['NX']
            nrow = head['NY'] 
            xs = 2*(data['x']-1)/(ncol-1) - 1 
            ys = 2*(data['y']-1)/(nrow-1) - 1
            xy = xs*ys
            x2 = 1.5*xs**2-0.5
            y2 = 1.5*ys**2-0.5
            x_new += transform[ind][6]*x2 + transform[ind][8]*xy + transform[ind][10]*y2
            y_new += transform[ind][7]*x2 + transform[ind][9]*xy + transform[ind][11]*y2
        if dof >= 20: 
            x_new += (transform[ind][12]*xs + transform[ind][14]*ys)*x2 + (transform[ind][16]*xs + transform[ind][18]*ys)*y2
            y_new += (transform[ind][13]*xs + transform[ind][15]*ys)*x2 + (transform[ind][17]*xs + transform[ind][19]*ys)*y2  
        
        ax1.plot(x_new[use], y_new[use], 'r.', alpha=0.5, markersize=15)
        ax1.set_title(img_list[ind])
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        mp.show()

def daomaster(matchfile, frame_num='12, 0.5, 12', sigma='5',
            transformation='20', new_id='n', mag_file='n', corr_file='n',
            raw_file='n', new_trans='y', verbose=0,
            match_radii=[-4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1]):
# IN PROGRESS - FIX SO ALL OPTIONS WORK


    daomaster = pexpect.spawn(config.dao_dir+'daomaster', encoding='utf-8')
    if verbose == 1:
        daomaster.logfile = sys.stdout

    daomaster.expect("File with list of input files")
    daomaster.sendline(matchfile)
    daomaster.expect("Minimum number")
    daomaster.sendline(frame_num)
    daomaster.expect("Maximum sigma")
    daomaster.sendline(sigma)
    daomaster.expect("Your choice")
    daomaster.sendline(transformation)
    daomaster.expect("Critical match-up radius")
    daomaster.sendline(str(match_radii[0]))
    for radii in match_radii:
        if radii == match_radii[0]: continue
        daomaster.expect("New match-up radius")
        daomaster.sendline(str(radii))
    daomaster.expect("New match-up radius")
    daomaster.sendline("0")
    daomaster.expect("Assign new star IDs")
    daomaster.sendline(new_id)
    daomaster.expect("A file with mean magnitudes")
    daomaster.sendline(mag_file)
    check = daomaster.expect(['Output file name', 'A file with corrected magnitudes'])
    if check == 0:
        daomaster.sendline('')
        check2 = daomaster.expect(['OVERWRITE', 'A file with corrected magnitudes'])
        if check2 == 0:
            daomaster.sendline('')
            daomaster.expect('A file with corrected magnitudes')
    daomaster.sendline(corr_file)
    daomaster.expect("A file with raw magnitudes")
    daomaster.sendline(raw_file)
    check = daomaster.expect(['Output file name', 'A file with the new transformations'])
    if check == 0:
        daomaster.sendline('')
        check2 = daomaster.expect(['OVERWRITE', 'A file with the new transformations'])
        if check2 == 0:
            daomaster.sendline('')
            daomaster.expect('A file with the new transformations')
    daomaster.sendline(new_trans)
    daomaster.expect("Output file name")
    daomaster.sendline("")
    daomaster.expect("New output file name")
    daomaster.sendline("")
    daomaster.expect("A file with the transfer table")
    daomaster.sendline("e")

    daomaster.close(force=True)


def combine_mch_simple(mch_list, output_file='combine.mch'):

	o = open(output_file, 'w')
	for ii, mch in enumerate(mch_list):

		f = open(mch, 'r')
		lines = f.readlines()
		if ii == 0:
			o.write(lines[0])
		for jj in range(1, len(lines)):
			o.write(lines[jj])

		f.close()
	o.close()



###############################################################################
#                          ALLFRAME
###############################################################################
def allframe(image_list, star_list, verbose=1):

    # need very long timeout
    allframe = pexpect.spawn(config.dao_dir+'allframe', encoding='utf-8')
    if verbose == 1:
        allframe.logfile = sys.stdout

    allframe.expect('OPT')
    allframe.sendline('')
    allframe.expect('File with list of images')
    allframe.sendline(image_list)
    allframe.expect('File with list of stars')
    allframe.sendline(star_list)
    allframe.expect('Good bye.', timeout=None)
    allframe.close(force=True)
