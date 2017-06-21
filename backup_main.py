#!/usr/bin/python3
import os
import shutil
import getpass
import sys

class Backup:
    ''' Backup utility copies all files and directories
        from source to destination directory'''
    def __init__(self, my_root, my_dst):
        self._my_root = my_root
        self._my_dst = my_dst
        self.copying()


    def copying(self):

        for src_dir, dirs, files in os.walk(self._my_root):
            dst_dir = src_dir.replace(self._my_root, self._my_dst, 1) #replace source path with destination path
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_) #create the source path
                print('Copying file: ' + src_file)
                dst_file = os.path.join(dst_dir, file_) #create the destination path
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.copy(src_file, dst_dir)   


class External:
    '''Gets the path of the any external hard drives that are connected'''
    
    def __init__(self, user, start_dir):
        self._user = user
        self._start_dir = start_dir

    def drives(self):
        print(os.listdir(self._start_dir))
        ext_drives = []
        for drive in os.listdir(self._start_dir):
            ext_drives.append(os.path.join(self._start_dir, drive))
        return ext_drives

def main():

    user = getpass.getuser()
    print('Hello ' + user)
    
    platform = sys.platform
    if platform == 'linux' or platform == 'linux2':
    	# linux
        print('This is a Linux platform')
        start_dir = os.path.join('/media/', user)
    elif platform == 'darwin':
    	# Mac OS
        print('This is Mac OS')
        start_dir = '/Volumes'
    elif platform == 'win32':
    	# Windows
        print('This is a Windows platform')
        start_dir = None
    else:
        print('Platform is unknown. Aborting....')
        sys.exit(0)

    if os.path.isdir(start_dir):
        print('External drive is valid')
    else:
        print('External drive is invalid. Aborting')
        sys.exit(0)
        


    my_ext = External(user, start_dir) # create instance for external drives
    
    ext_drive = ''

    if my_ext.drives(): # If drive has found some drives
        for drive in my_ext.drives(): #Iterate through the dives to select one
                select = input('Backup on {} [y/n]: '.format(drive))
                if select == 'y':
                    ext_drive = drive
                    break
    else:
        print('No external drives') 
        sys.exit(0) # Exit if no drives found.

    default_src = os.environ['HOME'] # Set up the source directory starting from home directory

    is_valid_root = False

    while not is_valid_root: # Iterate through directory loop until a valid directory is chosen.
        my_root = input('Enter root directory {}: '.format(default_src))
        my_root = os.path.join(default_src, my_root)
        is_valid_root = os.path.isdir(my_root)
        print(my_root)

    my_dst = os.path.join(ext_drive, user + 'Backup')
  

    Backup(my_root, my_dst)




if __name__=='__main__': main()
