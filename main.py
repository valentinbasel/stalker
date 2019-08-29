#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#
# Herramienta para investigación en el doctorado en educación en ciencia y
# tecnología
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

###############################################################################
#     _______  _______  _______  ___      ___   _  _______  ______   
#    |       ||       ||   _   ||   |    |   | | ||       ||    _ |  
#    |  _____||_     _||  |_|  ||   |    |   |_| ||    ___||   | ||  
#    | |_____   |   |  |       ||   |    |      _||   |___ |   |_||_ 
#    |_____  |  |   |  |       ||   |___ |     |_ |    ___||    __  |
#     _____| |  |   |  |   _   ||       ||    _  ||   |___ |   |  | |
#    |_______|  |___|  |__| |__||_______||___| |_||_______||___|  |_|                                                  
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

    def __init__(self,notebook):
        """TODO: to be defined1. """
        self.notebook = notebook 
        self.create_textview("programa_1.py")

 
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
        image = Gtk.Image()
        iconSize = Gtk.IconSize.SMALL_TOOLBAR
        image.set_from_stock(Gtk.STOCK_CLOSE, iconSize)
        close_button = Gtk.Button()
        close_button.set_image(image)
        #close_button.set_relief(Gtk.RELIEF_NONE)
        header.pack_start(title_label,
                          expand=True, fill=True, padding=0)
        header.pack_end(close_button,
                        expand=False, fill=True, padding=10)
        header.show_all()
        self.notebook.append_page(scrolledwindow,header)
        close_button.connect('clicked',
                                self.close_cb,
                                self.notebook,
                                scrolledwindow)


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
 
class MAIN_W(object):

    """Docstring for MAIN_W. """

    def __init__(self,grabar):
        """TODO: to be defined1. """
        self.grabar=grabar 
        self.main_windows = Gtk.Window(title = "IDE python")
        self.main_windows.set_default_size(-1, 350)
        self.main_windows.connect("destroy", self.close_main)
        self.main_windows.show_all()
        self.notebook = Gtk.Notebook()
        
        pagina = HOJA(self.notebook)
        pagina = HOJA(self.notebook)
        pagina = HOJA(self.notebook)

        self.main_windows.add(self.notebook)
        self.main_windows.show_all()
        if self.grabar==True:
            self.desktop_record_start()
        Gtk.main()
    
    def desktop_record_start(self):
        """TODO: Docstring for grabacion.
        :returns: TODO

        """

        fecha = str(datetime.now()).split(" ")
        cadena_final = fecha[1]+"_"+fecha[0] 
        cadena_final = cadena_final.replace(".","_")

        cadena_final = cadena_final.replace(";","_")
        cadena_final = cadena_final.replace(":","_")
        cadena_final = cadena_final + ".mkv"
        cadena =[ "ffmpeg -video_size 1024x768 ",
                "-framerate 25 -f x11grab ",
                "-i :0.0+0,0 -f pulse -ac 2 -i ",
                "default ",cadena_final]
        video=""
        for linea in cadena:
            video = video + linea 
        self.proc1 = subprocess.Popen(video, shell = True)

    def record_desktop_stop(self):
        """TODO: Docstring for record_desktop_stop.
        :returns: TODO

        """
        time.sleep(1)
        subprocess.Popen.kill(self.proc1) 
        time.sleep(1)

    def close_main(self, arg1):
        """TODO: Docstring for close_main.

        :arg1: TODO
        :returns: TODO

        """
        if self.grabar==True:
            self.record_desktop_stop()
        Gtk.main_quit()

grabar = True 
win = MAIN_W(grabar)

