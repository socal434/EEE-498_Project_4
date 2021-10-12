################################################################################
# Project 4                                                                    #
# Chance Hope                                                                  #
# Run hspice to determine the tphl of a circuit                                #
################################################################################

import numpy as np  # package needed to read the results file
import subprocess  # package needed to launch hspice
import shutil

n = 1  # number of inverters
tphl_data = []  # stores delay data
n_list = []  # stores number of inverters
fan_list = []  # stores fan out factor
while n <= 11:
    fan = 2  # fan out number of inverters
    while fan <= 10:  # this loop appends the base InvChain.sp file for the appropriate number of inverters
        shutil.copy('InvChain_base.sp', 'InvChain_inv_%d_%d.sp' % (n, fan))
        file = open('InvChain_inv_%d_%d.sp' % (n, fan), 'a')  # open for writing
        if n == 1:
            file.writelines(['.param fan = %d' % fan, '\nXinv1 a z inv M = 1', '\n.end'])
        if n == 3:
            file.writelines(['.param fan = %d' % fan, '\nXinv1 a b inv M = 1', '\nXinv2 b c inv M = %d' % fan**1,
                             '\nXinv3 c z inv M = %d' % fan**2, '\n.end'])
        if n == 5:
            file.writelines(['.param fan = %d' % fan, '\nXinv1 a b inv M = 1', '\nXinv2 b c inv M = %d' % fan**1,
                             '\nXinv3 c d inv M = %d' % fan**2, '\nXinv4 d e inv M = %d' % fan**3,
                             '\nXinv5 e z inv M = %d' % fan**4, '\n.end'])
        if n == 7:
            file.writelines(['.param fan = %d' % fan, '\nXinv1 a b inv M = 1', '\nXinv2 b c inv M = %d' % fan**1,
                             '\nXinv3 c d inv M = %d' % fan**2, '\nXinv4 d e inv M = %d' % fan**3,
                             '\nXinv5 e f inv M = %d' % fan**4, '\nXinv6 f g inv M = %d' % fan**5,
                             '\nXinv7 g z inv M = %d' % fan**6, '\n.end'])
        if n == 9:
            file.writelines(['.param fan = %d' % fan, '\nXinv1 a b inv M = 1', '\nXinv2 b c inv M = %d' % fan**1,
                             '\nXinv3 c d inv M = %d' % fan**2, '\nXinv4 d e inv M = %d' % fan**3,
                             '\nXinv5 e f inv M = %d' % fan**4, '\nXinv6 f g inv M = %d' % fan**5,
                             '\nXinv7 g h inv M = %d' % fan**6, '\nXinv8 h i inv M = %d' % fan**7,
                             '\nXinv9 i z inv M = %d' % fan**8, '\n.end'])
        if n == 11:
            file.writelines(['.param fan = %d' % fan, '\nXinv1 a b inv M = 1', '\nXinv2 b c inv M = %d' % fan**1,
                             '\nXinv3 c d inv M = %d' % fan**2, '\nXinv4 d e inv M = %d' % fan**3,
                             '\nXinv5 e f inv M = %d' % fan**4, '\nXinv6 f g inv M = %d' % fan**5,
                             '\nXinv7 g h inv M = %d' % fan**6, '\nXinv8 h i inv M = %d' % fan**7,
                             '\nXinv9 i j inv M = %d' % fan**8, '\nXinv10 j k inv M = %d' % fan**9,
                             '\nXinv11 k z inv M = %d' % fan**10, '\n.end'])
        file.close()
        # launch hspice. Note that both stdout and stderr are captured so
        # they do NOT go to the terminal!
        proc = subprocess.Popen(['hspice', 'InvChain_inv_%d_%d.sp' % (n, fan)], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        output, err = proc.communicate()
        # extract tphl from the output file
        data = np.recfromcsv('InvChain_inv_%d_%d.mt0.csv' % (n, fan), comments="$", skip_header=3)
        tphl = data["tphl_inv"]
        tphl_data.append(tphl)  # append to list for reporting
        n_list.append(n)  # append to list for reporting
        fan_list.append(fan)  # append to list for reporting
        print('N', n, 'fan', fan, 'tphl', tphl)
        fan += 1
    n += 2
tphl_min_index = tphl_data.index(min(tphl_data))  # finds index of lowest delay for printing
print('\nBest Values are:')
print('Fan =', fan_list[tphl_min_index])
print('Number of Inverters =', n_list[tphl_min_index])
print('tphl = ', tphl_data[tphl_min_index])
