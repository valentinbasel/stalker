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
