import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import csv


class TreeViewFilterWindow(Gtk.HBox):

    def __init__(self,archivo):
        super(TreeViewFilterWindow, self).__init__()

        self.upload_csv(archivo)
        #Gtk.Window.__init__(self, title="Treeview Filter Demo")
        #self.set_border_width(10)

        #Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        #Creating the ListStore model
        self.software_liststore = Gtk.ListStore(str, str, str)
        for software_ref in self.software_list:
            self.software_liststore.append(list(software_ref))
        self.current_filter_language = None

        #Creating the filter, feeding it with the liststore model
        self.language_filter = self.software_liststore.filter_new()
        #setting the filter function, note that we're not using the
        self.language_filter.set_visible_func(self.language_filter_func)

        #creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        for i, column_title in enumerate(["Punto de interes", "hora", "fecha"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        #creating buttons to filter by programming language, and setting up their events
        self.buttons = list()
        for prog_language in ["BackSpace", "None"]:
            button = Gtk.Button(prog_language)
            self.buttons.append(button)
            button.connect("clicked", self.on_selection_button_clicked)

        #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)
        self.scrollable_treelist.add(self.treeview)
        self.seg=0
        tree_selection = self.treeview.get_selection()
        #tree_selection.set_mode(gtk.SELECTION_MULTIPLE)
        tree_selection.connect("changed", self.onSelectionChanged)
        self.show_all()

    def onSelectionChanged(self, tree_selection):
        """TODO: Docstring for onSelectionChanged.

        :arg1: TODO
        :returns: TODO

        """
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,1)
            #print(value)
            value = value.split(".")
            value = value[0].split(":")
            h = int(value[0])*3600
            m = int(value[1])*60
            s = int(value[2])
            self.seg = h+m+s
            print(self.seg)

    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if self.current_filter_language is None or self.current_filter_language == "None":
            return True
        else:
            return model[iter][0] == self.current_filter_language

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        #we set the current language filter to the button's label
        self.current_filter_language = widget.get_label()
        print("%s language selected!" % self.current_filter_language)
        #we update the filter, which updates in turn the view
        self.language_filter.refilter()

    def upload_csv(self, arg1):
        """TODO: Docstring for upload_csv.

        :arg1: TODO
        :returns: TODO

        """
        self.software_list =[]
        with open(arg1) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            #line_count = ("","","")
            for row in csv_reader:
                l=(row[0],row[1],row[2])
                self.software_list.append(l)

#win = TreeViewFilterWindow()
#win.connect("destroy", Gtk.main_quit)
#win.show_all()
#Gtk.main()
