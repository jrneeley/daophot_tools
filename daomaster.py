#!/usr/bin/env python

import sys
import pexpect
import re
import glob
import os


def daomaster(matchfile, dao_dir='/apps/daophot32/', frame_num='12, 0.5, 24',
            sigma='10', transformation='20', new_id='n', mag_file='n', corr_file='n',
            raw_file='n', new_trans='y', ):

## Clean up previous runs
    magfile=re.sub(".mch", ".mag", matchfile)
    if (os.path.isfile(magfile)):
            os.remove(magfile)
    daomaster = pexpect.spawn(dao_dir+'daomaster')
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
    daomaster.sendline("-5")
    daomaster.expect("New match-up radius")
    daomaster.sendline("4")
    daomaster.expect("New match-up radius")
    daomaster.sendline("3")
    daomaster.expect("New match-up radius")
    daomaster.sendline("2")
    daomaster.expect("New match-up radius")
    daomaster.sendline("2")
    daomaster.expect("New match-up radius")
    daomaster.sendline("2")
    daomaster.expect("New match-up radius")
    daomaster.sendline("1")
    daomaster.expect("New match-up radius")
    daomaster.sendline("1")
    daomaster.expect("New match-up radius")
    daomaster.sendline("1")
    daomaster.expect("New match-up radius")
    daomaster.sendline("1")
    daomaster.expect("New match-up radius")
    daomaster.sendline("0.5")
    daomaster.expect("New match-up radius")
    daomaster.sendline("0.5")
    daomaster.expect("New match-up radius")
    daomaster.sendline("0.5")
    daomaster.expect("New match-up radius")
    daomaster.sendline("0.5")
    daomaster.expect("New match-up radius")
    daomaster.sendline("0")
    daomaster.expect("Assign new star IDs")
    daomaster.sendline(new_id)
    daomaster.expect("A file with mean magnitudes")
    daomaster.sendline(mag_file)
    if mag_file == 'y':
        daomaster.expect("New output")
        daophot.sendline(magfile)
    daomaster.expect("A file with corrected magnitudes")
    daomaster.sendline(corr_file)
    daomaster.expect("A file with raw magnitudes")
    daomaster.sendline(raw_file)
    daomaster.expect("A file with the new transformations")
    daomaster.sendline(new_trans)
    daomaster.expect("Output file name")
    daomaster.sendline("")
    daomaster.expect("New output file name")
    daomaster.sendline("")
    daomaster.expect("A file with the transfer table")
    daomaster.sendline("e")

    daomaster.close(force=True)
