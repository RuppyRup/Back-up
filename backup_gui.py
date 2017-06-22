
import os
from gi.repository import Gtk

window = Gtk.Window()
window.connect("delete-event", Gtk.main_quit)


filesystemTreeStore = Gtk.TreeStore(str)
parents = {}

for (path, dirs, files) in os.walk("/home"):
    for subdir in dirs:
        parents[os.path.join(path, subdir)] = filesystemTreeStore.append(parents.get(path, None), [subdir])
    for item in files:
        filesystemTreeStore.append(parents.get(path, None), [item])

filesystemTreeView = Gtk.TreeView(filesystemTreeStore)
renderer = Gtk.CellRendererText()
filesystemColumn = Gtk.TreeViewColumn("Title", renderer, text=0)
filesystemTreeView.append_column(filesystemColumn)

window.add(filesystemTreeView)


window.show_all()
Gtk.main()
