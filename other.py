import numpy as np


def dao2reg(infile, outfile, ids=1, color='green'):


    data = np.loadtxt(infile, skiprows=3, usecols=(0,1,2))

    f = open(outfile+'.reg', 'w')
    f.write('global color={}\n'.format(color))
    f.write('image \n')
    for ii in range(len(data[:,0])):
        if ids == 1:
            f.write('circle {:7.2f} {:7.2f} 10 # text= {{ {} }}\n'.format(\
                data[ii,1], data[ii,2], int(data[ii,0])))
        else:
            f.write('circle {:7.2f} {:7.2f} 10 \n'.format(data[ii,1],data[ii,2]))
    f.close()
