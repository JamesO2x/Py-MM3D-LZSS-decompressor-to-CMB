import os
import sys
# This script just runs through your directory and removes all CMB files.
# Useful if you've already converted them to another format, and are needing to cleanup.
# You can provide a directory to scan with 'scanDir'
# or leave it as is to scan the current directory that this py file exists in.

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.abspath(__file__))

print(f"The script is running from: {app_path}")

# Set path scan directory to the app path
scan_directory = app_path

# Checks the file
def crawl_dir_and_delete_files(dir_to_scan, filetypes_to_delete=None):

    if filetypes_to_delete == None:
        return print('ERROR: No filetypes specified.')

    for root, dirs, files in os.walk(dir_to_scan, topdown=False):
        
        for file in files:
            # GET FILENAMES
            file_to_delete  = os.path.join(root, file)
            f_split         = os.path.splitext(file_to_delete) # split the extension
            ext             = f_split[1] # get extension only, ex) '.txt'1

            # Check if valid file format
            if ext in filetypes_to_delete:
                os.remove(file_to_delete)
                print('Delete: ', file_to_delete)
            else:
                # action-default
                print(f' >>> SKIP >>> {file_to_delete}')

    print(' >>> Done >>> ')
    return


def confirm_user_choice(dir_to_scan, filetypes_to_delete=None):
    print(f'\n!!! Are you sure you want to delete all of the following file types:')
    print('  -> ', filetypes_to_delete)
    print('!!! from the following directory:')
    print('  -> ', dir_to_scan)
    print('!!! Are you sure? (This action can not be undone)\n')

    user_confirm = input('Confirm your choice (y/n): ')

    if user_confirm == 'y':
        crawl_dir_and_delete_files(scan_directory, filetypes_to_delete)
    else:
        print('# Action canceled.')

    return


# RUN FUNCTION
if __name__ == "__main__":

    print('''
#################################
#### LIST OF CLEANUP ACTIONS ####
#################################

This script will help you clean up unnecessary files from the directories after conversion.
The following actions are available:

    1. Delete all temporary ZSI Decompilation files 
         (*.zsi_lzs_decomp, *.zsidecomp).
    2. Delete all the old .ZSI files, AND delete temporary decomp files 
         (*.zsi, *.zsi_lzs_decomp, *.zsidecomp)
    3. Delete all newly created .CMB files and temp files 
         (*.cmb, *.zsi_lzs_decomp, *.zsidecomp) (basically undo the conversion)

Choose option 3 if you need to redo the entire ZSI to CMB conversion for some reason.
Choose option 2 if you no longer need the original ZSI files.

Choose option 1, if you are unsure which option you should choose.

NOTE: Make sure you have a backup copy of your files stored
      somewhere else on your computer before continuing.
      This script/program modifies files, and thus can result in 
      accidental data loss. This script/program is not intended for 
      any particular purpose. Use at your own risk.

''')

    user_action = input('Which action do you want to perform? ')
    
    match user_action:
        case '1':
            filetypes_to_delete = ['.zsi_lzs_decomp', '.zsidecomp']
            confirm_user_choice(scan_directory, filetypes_to_delete)
        case '2':
            filetypes_to_delete = ['.zsi', '.zsi_lzs_decomp', '.zsidecomp']
            confirm_user_choice(scan_directory, filetypes_to_delete)
        case '3':
            filetypes_to_delete = ['.cmb', '.zsi_lzs_decomp', '.zsidecomp']
            confirm_user_choice(scan_directory, filetypes_to_delete)
        case _:
            print('ERROR: Invalid option selected.')
            pass

    input('### Action Complete. You can close this terminal now.')
