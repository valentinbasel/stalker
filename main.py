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


## librerias generales
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk
from gi.repository import GtkSource
from datetime import datetime
import time
import os
import subprocess

## librerias internas
from tab import HOJA
from util import DIALOG_OK_CANCEL

class MAIN_W(object):

    """Docstring for MAIN_W. """

    def __init__(self,grabar):
        """TODO: to be defined1. """
        self.grabar=grabar
        self.main_windows = Gtk.Window(title = "IDE python")
        self.main_windows.set_default_size(-1, 350)
        self.main_windows.connect("destroy", self.close_main)
        self.main_windows.show_all()

        headerbar = Gtk.HeaderBar()
        #headerbar.set_title("HeaderBar Example")
        #headerbar.set_subtitle("HeaderBar Subtitle")
        headerbar.set_show_close_button(True)
        self.main_windows.set_titlebar(headerbar)

        ## boton de barra de herramientas
        button = Gtk.Button("Open")
        button.connect("clicked", self.on_popover_clicked)
        headerbar.pack_start(button)

        self.new_button("document-new","nueva pestaña",headerbar,self.new_tab)
        
        ##  popover
        self.popover = Gtk.Popover()
        self.popover.set_relative_to(button)
        ## Box donde se guardan los botones del menu popover
        box_popover = Gtk.Box()
        box_popover.set_spacing(5)
        box_popover.set_orientation(Gtk.Orientation.VERTICAL)
        self.popover.add(box_popover)
        ## creo los botones que van dentro del popover
        for a in range(2):
            label = Gtk.Label("boton")
            image = Gtk.Image.new_from_file("icaro.png")
            box_boton=Gtk.Box()
            box_boton.set_homogeneous(False)
            box_boton.set_orientation(Gtk.Orientation.HORIZONTAL)
            box_boton.set_spacing(5)
            box_boton.add(image)
            box_boton.add(label)
            
            boton_menu = Gtk.Button()
            boton_menu.set_tooltip_text(str(a))
            boton_menu.add(box_boton)
            boton_menu.connect("clicked", self.on_boton_menu_clicked,a,"f")
            box_popover.add(boton_menu)

        self.hbox = Gtk.HBox(spacing = 6)
        self.notebook = Gtk.Notebook()
        self.hbox.pack_start(self.notebook,True,True,0)

        pagina = HOJA(self.notebook,"programa1")



        self.main_windows.add(self.hbox)

        self.main_windows.show_all()
        
        mensaje = DIALOG_OK_CANCEL(self.main_windows,"advertencia","hola")
        respuesta = mensaje.run()
        if respuesta == Gtk.ResponseType.OK and self.grabar==True:
            self.desktop_record_start()
        elif respuesta == Gtk.ResponseType.CANCEL:
            self.grabar = False
            self.close_main(None)
            exit()
        
        mensaje.destroy()

        Gtk.main()

    def new_tab(self,button):
        """TODO: Docstring for new_tab.
        :returns: TODO

        """
        pagina = HOJA(self.notebook,"programa1.py")
        self.main_windows.show_all()

    def on_popover_clicked(self, button):
        self.popover.show_all()
        
    def on_boton_menu_clicked(self,button,a,f):
        print("%i,%s",a,f)

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


    def new_button(self, imagen,text,headerbar,func):
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
        button_tab.connect("clicked", func)
        headerbar.pack_start(button_tab)
 
grabar = True
win = MAIN_W(grabar)

