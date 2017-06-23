import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
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

class FileChooserWindow(Gtk.Window):

    def __init__(self):
        self.source_dir = None
        self.destination_dir = None
        self.sourced_selected = False
        self.destination_selected = False
        self.backup_complete = False
        
        Gtk.Window.__init__(self, title="Backup Utility")

        self.box = Gtk.Box(spacing=20, orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)

        
        self.button1 = Gtk.Button("Choose directory to back up")
        self.button1.connect("clicked", self.on_source_folder_clicked)
        self.box.add(self.button1)

        self.button2 = Gtk.Button("Choose destination directory")
        self.button2.connect("clicked", self.on_dest_folder_clicked)
        self.box.add(self.button2)

        self.button3 = Gtk.Button("Run Backup")
        self.button3.connect("clicked", self.back_up)
        self.box.add(self.button3)


    def on_source_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.sourced_selected = True
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
            self.source_dir = dialog.get_filename()
            self.button1.set_label(self.source_dir)
            button1 = Gtk.Button(self.source_dir)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def on_dest_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.destination_selected = True
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
            self.destination_dir = dialog.get_filename()
            self.button2.set_label(self.destination_dir)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def back_up(self, widget):
        if not self.backup_complete:
            if self.destination_selected & self.sourced_selected:
                self.button3.set_label("Backing up")
                Backup(self.source_dir, self.destination_dir)
                self.button3.set_label("Finished")
                self.backup_complete = True
            else:
                self.button3.set_label("Complete Directory Selection")
        else:
            self.button3.set_label("Finished")
        


win = FileChooserWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
