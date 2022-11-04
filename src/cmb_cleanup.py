import os
# This script just runs through your directory and removes all CMB files.
# Useful if you've already converted them to another format, and are needing to cleanup.
# You can provide a directory to scan with 'scanDir'
# or leave it as is to scan the current directory that this py file exists in.
scanDir = '.'

# Checks the file
def cmb_delete():
    for root, dirs, files in os.walk(scanDir, topdown=False):
        for file in files:

            # GET FILENAMES
            f = os.path.join(root, file)
            f_split = os.path.splitext(f) # split the extension
            ext  = f_split[1] # get extension only, ex) '.txt'

            # Check if valid file format, ZSI
            match ext:
                case '.cmb':
                    os.remove(f)
                    print('Delete: ', f)
                case _:
                    # action-default
                    print(' >>> SKIP >>> ')

    print(' >>> Done >>> ')

# RUN FUNCTION
cmb_delete()