import numpy as np



def write_mag(ids, x, y, mags, out_file, errs=None, err1=None, frames=None,
    chi=None, sharp=None, var=None, blunder=None):

    header_line1 = ' NL    NX    NY  LOWBAD HIGHBAD  THRESH     AP1  PH/ADU  RNOISE    FRAD\n'
    header_line2 = '  1  4013  4766  -500.0 32766.5   0.000   0.000   0.000   0.000   0.000\n\n'
    head = header_line1+'\n'+header_line2+'\n'

    f = open(out_file, 'w')
    f.write(header_line1)
    f.write(header_line2)
    f.close()

    f = open(out_file, 'a')

    n_stars = len(ids)

    if errs == None:
        errs = np.repeat(0.0001, n_stars)
    if err1 == None:
        err1 = np.repeat(0.0000, n_stars)
    if frames == None:
        frames = np.repeat(1., n_stars)
    if chi == None:
        chi = np.repeat(0.000, n_stars)
    if sharp == None:
        sharp = np.repeat(0.000, n_stars)
    if var == None:
        var = np.repeat(0.00, n_stars)
    if blunder == None:
        blunder = np.repeat(1.000, n_stars)
    #dtype = np.dtype([('1', int), ('2', float), ('3', float), ('4', float), \
    #    ('5', float), ('6', float), ('7', float), ('8')])
    data_save = np.array(zip(ids, x, y, mags, errs, err1, frames, chi, sharp, \
        var, blunder))

    np.savetxt(f, data_save,
        fmt='%8i %8.3f %8.3f %8.3f %8.4f %8.4f %8.0f %8.3f %8.3f %8.2f %8.3f')
    f.close()
