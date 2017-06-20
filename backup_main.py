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
    
    
    def __init__(self, user):
        self._user = user
        self._start_dir = ''

    def drives(self):
        ext_drives = []
        for drive in os.listdir(self._my_path):
            ext_drives.append(os.path.join(self._my_path, drive))
        return ext_drives

class External_Mac(External):
    def __init__(self, user):
        super().__init__(self)
        self._start_dir = '/Volumes'
        print('Hello')
        
    
    def drives(self):
        ext_drives = []
        print('directory :' + self._start_dir)
        print(os.listdir('/Volumes'))
        for drive in os.listdir(self._start_dir):
            ext_drives.append(os.path.join(self._start_dir, drive))
        return ext_drives
       

def main():

    user = getpass.getuser()
    print('Hello ' + user)
    my_ext = External_Mac(user)
    
    select_drive = False
    ext_drive = ''

    if my_ext.drives():
        for drive in my_ext.drives():
                select = input('Backup on {} [y/n]: '.format(drive))
                if select == 'y':
                    ext_drive = drive
                    select_drive = True
                    break
    else:
        print('No external drives')

    if select_drive == False: sys.exit(0)
    print(ext_drive)

            
            
    

    default_src = os.environ['HOME']

    is_valid_root = False
    

    while not is_valid_root:
        my_root = input('Enter root directory {}: '.format(default_src))
        my_root = os.path.join(default_src, my_root)
        is_valid_root = os.path.isdir(my_root)
        print(my_root)

    my_dst = os.path.join(ext_drive, user + 'Backup')
'''   

    Backup(my_root, my_dst)

'''


if __name__=='__main__': main()
