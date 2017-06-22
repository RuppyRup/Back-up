#!usr/bin/python3
import os, stat, sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

class Backup_GUI:

    def __init__(self, path):
        #set up window
        self._path = path
        self.window = Gtk.Window()
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.set_title("Backup Utility")
        self.window.set_border_width(10)
        self.window.set_default_size(800,800)
        # initialize the filesystem treestore
        fileSystemTreeStore = Gtk.TreeStore(str, Pixbuf, str)
        self.populateDirectorySystemTreeStore(fileSystemTreeStore, self._path) # populate the tree store  
        fileSystemTreeView = Gtk.TreeView(fileSystemTreeStore) # initialize the TreeView
        treeViewCol = Gtk.TreeViewColumn("Select Directory to Backup") # Create a TreeViewColumn
        # Create a column cell to display text
        colCellText = Gtk.CellRendererText()
        # Create a column cell to display an image
        colCellImg = Gtk.CellRendererPixbuf()
        # Add the cells to the column
        treeViewCol.pack_start(colCellImg, False)
        treeViewCol.pack_start(colCellText, True)
        # Bind the text cell to column 0 of the tree's model
        treeViewCol.add_attribute(colCellText, "text", 0)
        # Bind the image cell to column 1 of the tree's model
        treeViewCol.add_attribute(colCellImg, "pixbuf", 1)
        # Append the columns to the TreeView
        fileSystemTreeView.append_column(treeViewCol)
        # add "on expand" callback
        fileSystemTreeView.connect("row-expanded", self.onRowExpanded)
        # add "on collapse" callback
        fileSystemTreeView.connect("row-collapsed", self.onRowCollapsed)
        # get selected folder
        select = fileSystemTreeView.get_selection()
        select.connect("changed", self.on_tree_selection_changed)
        scrollView = Gtk.ScrolledWindow()
        scrollView.add(fileSystemTreeView)
        # append the scrollView to the window (this)
        self.window.add(scrollView)
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()

    def populateDirectorySystemTreeStore(self,treeStore, path, parent=None):
        itemCounter = 0
        # iterate over the items in the path
        for item in os.listdir(path):
            # Get the absolute path of the item
            itemFullname = os.path.join(path, item)
            # Extract metadata from the item
            itemMetaData = os.stat(itemFullname)
            # Determine if the item is a folder
            itemIsFolder = stat.S_ISDIR(itemMetaData.st_mode)
            # Generate an icon from the default icon theme
            itemIcon = Gtk.IconTheme.get_default().load_icon("folder" if itemIsFolder else "empty", 22, 0)
            # Append the item to the TreeStore
            #currentIter = treeStore.append(parent, [item, itemIcon, itemFullname])
            # add dummy if current item was a folder
            if itemIsFolder:
                currentIter = treeStore.append(parent, [item, itemIcon, itemFullname])
                treeStore.append(currentIter, [None, None, None])
            else:
                #currentIter = treeStore.append(parent, [None, None, None])
                pass
            #increment the item counter
            itemCounter += 1
        # add the dummy node back if nothing was inserted before
        if itemCounter < 1: treeStore.append(parent, [None, None, None])

    def onRowExpanded(self, treeView, treeIter, treePath):
        # get the associated model
        treeStore = treeView.get_model()
        # get the full path of the position
        newPath = treeStore.get_value(treeIter, 2)
        # populate the subtree on curent position
        self.populateDirectorySystemTreeStore(treeStore, newPath, treeIter)
        # remove the first child (dummy node)
        treeStore.remove(treeStore.iter_children(treeIter))


    def onRowCollapsed(self, treeView, treeIter, treePath):
        # get the associated model
        treeStore = treeView.get_model()
        # get the iterator of the first child
        currentChildIter = treeStore.iter_children(treeIter)
        # loop as long as some childern exist
        while currentChildIter:
            # remove the first child
            treeStore.remove(currentChildIter)
            # refresh the iterator of the next child
            currentChildIter = treeStore.iter_children(treeIter)
        # append dummy node
        treeStore.append(treeIter, [None, None, None])

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            print("You selected", model[treeiter][0])


def main():
    start_path = '/home'
    win = Backup_GUI(start_path)
    Gtk.main()

if __name__=='__main__':
    sys.exit(main())
