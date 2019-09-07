#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#
# class new page 
# Copyright © 2019 Valentín Basel <valentinbasel@gmail.com>
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
from datetime import datetime

import time
import os
import subprocess

class HOJA(object):

    """Docstring for HOJA. """

    def __init__(self,notebook,nombre):
        """TODO: to be defined1. """
        self.nombre = nombre
        self.notebook = notebook
        self.create_textview(self.nombre)

    def create_textview(self,nombre):

        lm = GtkSource.LanguageManager.get_default()
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        #self.grid.attach(scrolledwindow, 0, 1, 3, 1)
        self.textview = GtkSource.View() # Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("")
        # Selecciono como código fuente a resaltar el lenguaje PYTHON
        self.textbuffer.set_language(lm.get_language("python"))
        # activo el resaltado de imagen
        self.textbuffer.set_highlight_syntax(True)
        # activo el numero de linea de código en el margen izquierdo
        self.textview.set_show_line_numbers(True)
        # cuando se apriete el tabulador o los Spaces, conservar la identación
        self.textview.set_auto_indent(True)
        # cuando se teclea TAB, lo remplaza por espacios
        self.textview.set_insert_spaces_instead_of_tabs(True)
        # remplaza el TAB con 4 espacios
        self.textview.set_tab_width(4)
        scrolledwindow.add(self.textview)
        self.tag_found = self.textbuffer.create_tag("found",
                                                    background="yellow")
        self.textview.connect("key-press-event",self.textpress)
        header = Gtk.HBox()
        title_label = Gtk.Label(nombre)
        # image = Gtk.Image()
        # iconSize = Gtk.IconSize.SMALL_TOOLBAR
        # image.set_from_stock(Gtk.STOCK_CLOSE, iconSize)
        # close_button = Gtk.Button()
        # close_button.set_image(image)
        #close_button.set_relief(Gtk.RELIEF_NONE)


        header.pack_start(title_label,
                          expand=True, fill=True, padding=0)
        # header.pack_end(close_button,
                        # expand=False, fill=True, padding=10)

        self.new_button("media-playback-start","ejecutar",header,self.execute,None,None)

        self.new_button("window-close-symbolic","cerrar",header,self.close_cb,self.notebook,scrolledwindow)
        header.show_all()

        self.notebook.append_page(scrolledwindow,header)
        # close_button.connect('clicked',
                                # self.close_cb,
                                # self.notebook,
                                # scrolledwindow)


    def close_cb(self,a,b,c):
        """TODO: Docstring for close_cb.
        :returns: TODO

        """
        page_num = b.page_num(c)
        b.remove_page( page_num )
        c.destroy()

    def textpress(self,widget, event):
        """TODO: Docstring for textpress.

        :widget: textview
        :event: tecla presionada
        :returns: None

        """
        fecha = str(datetime.now()).split(" ")
        tecla = Gdk.keyval_name(event.keyval)

        cadena_final = tecla +"," + fecha[1]+","+fecha[0]
        print(cadena_final)
        #print()

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

    def execute(self,button,a,b):
        """TODO: Docstring for execute.

        :arg1: TODO
        :returns: TODO

        """
        print ("ejecuto")
        print(a)
        print(b)
