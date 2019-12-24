#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#
# Utilidades para STALKER
# Copyright © 2019 Valentin Basel <valentinbasel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk
from gi.repository import GtkSource
import sys


class UTIL(object):

    """Docstring for UTIL. """

    def __init__(self):
        """TODO: to be defined1. """
        pass
    
    def new_button(self, imagen,text,vbox,func,a,b):
        """TODO: Docstring for botones_nuevo.

        :arg1: TODO
        :returns: TODO

        """
        ## boton de nueva pestaña
        button_tab = Gtk.Button()
        iconSize = Gtk.IconSize.LARGE_TOOLBAR
        img = imagen #"document-new"
        image = Gtk.Image.new_from_icon_name(img, iconSize)
        #label = Gtk.Label(text)

        box_boton=Gtk.VBox()
        box_boton.set_homogeneous(False)
        #box_boton.set_orientation(Gtk.Orientation.VERTICAL)
        box_boton.set_spacing(5)
        box_boton.add(image)
        #box_boton.add(label)
        button_tab.add(box_boton)
        button_tab.connect("clicked", func,a,b)
        vbox.pack_start(button_tab,False,True,5)

class DIALOG_OK_CANCEL(Gtk.Dialog):

    def __init__(self, parent,text,mensaje):
        Gtk.Dialog.__init__(self, 
                            text, 
                            parent, 
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK)
                            )
        self.set_default_size(150, 100)
        label = Gtk.Label(mensaje)
        box = self.get_content_area()
        box.add(label)
        self.show_all()

class NUEVO_DOC(object):

    """Docstring for NUEVO_DOC. """

    def __init__(self,parent):  #, message, title=''):
        # Returns user input as a string or None
        # If user does not input text it returns None, NOT AN EMPTY STRING.
        self.parent = parent 

    def run(self,message,title=''):
        dialogWindow = Gtk.MessageDialog(self.parent,
                              Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                              Gtk.MessageType.QUESTION,
                              Gtk.ButtonsType.OK_CANCEL,
                              message)

        dialogWindow.set_title(title)

        dialogBox = dialogWindow.get_content_area()
        userEntry = Gtk.Entry()
        userEntry.set_visibility(True)
        #userEntry.set_invisible_char("*")
        userEntry.set_size_request(250,0)
        dialogBox.pack_end(userEntry, False, False, 0)

        dialogWindow.show_all()
        response = dialogWindow.run()
        text = userEntry.get_text() 
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.OK) and (text != ''):
            return text
        else:
            return None

class MENSAJE(object):

    """Docstring for MENSAJE. """

    def __init__(self,men):
        """TODO: to be defined1. """
        
        self.main_windows = Gtk.Window(title = "salida de errores")
        self.main_windows.set_default_size(500,400)
        vbox = Gtk.VBox()
        self.main_windows.add(vbox)
        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        #self.grid.attach(scrolledwindow, 0, 1, 3, 1)
        boton = Gtk.Button("salir")

        boton.connect("clicked", self.close)
        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(men)
        self.scrolledwindow.add(self.textview)
        vbox.pack_start(self.scrolledwindow,True,True,0)
        vbox.pack_start(boton,False,False,0)
        self.main_windows.show_all()

    def close(self, arg1):
        self.main_windows.hide()

class ABRIR_DIALOG(object):
    
    """Docstring for ABRIR_DIALOG. """
    
    def __init__(self):
        """TODO: to be defined1. """
        self.dialog = Gtk.FileChooserDialog(
                            "Abrir",
                            None,
                            Gtk.FileChooserAction.OPEN,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.dialog.set_default_response(Gtk.ResponseType.OK)
        self.dialog.set_current_folder(sys.path[0])

    def abrir_pry(self,tipo):
        """TODO: Docstring for abrir_pry.
        :returns: TODO

        """
        if tipo =="proyecto":
            filter = Gtk.FileFilter()
            filter.set_name("torcaz")
            filter.add_pattern("*.stlkr")
            self.dialog.add_filter(filter)
            response = self.dialog.run()
            if response == Gtk.ResponseType.OK:
                cadena = self.dialog.get_filename()
                self.dialog.destroy()
                return cadena
            elif response == Gtk.ResponseType.CANCEL:
                self.dialog.destroy()
                return None
        self.dialog.destroy()
