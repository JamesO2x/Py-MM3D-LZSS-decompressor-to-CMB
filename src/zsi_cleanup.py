import os
# This script just runs through your directory and removes any .ZSI files, or temp .zsidecomp files.
# You can provide a directory to scan with 'scanDir'
# or leave it as is to scan the current directory that this py file exists in.
scanDir = '.'

# Checks the file
def zsi_delete():
    for root, dirs, files in os.walk(scanDir, topdown=False):
        for file in files:

            # GET FILENAMES
            f = os.path.join(root, file)
            f_split = os.path.splitext(f) # split the extension
            ext  = f_split[1] # get extension only, ex) '.txt'

            # Check if valid file format, ZSI
            match ext:
                case '.zsi':
                    os.remove(f)
                    print('Delete: ', f)
                case '.zsidecomp':
                    os.remove(f)
                    print('Delete: ', f)
                case _:
                    # action-default
                    print(' >>> SKIP >>> ')

    print(' >>> Done >>> ')

# RUN FUNCTION
zsi_delete()