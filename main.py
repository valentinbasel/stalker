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
from util import NUEVO_DOC

class MAIN_W(object):

    """Docstring for MAIN_W. """

    def __init__(self,grabar):
        """TODO: to be defined1. """
        menues = [ ("Abrir",
                    "Abre un nuevo archivo",
                    'document-open',
                    lambda b: self.abrir()
                    ),
                    ("Nuevo",
                    "Crea una nueva pestaña",
                    'document-new',
                    lambda b: self.new_tab(None)
                    ),
                    ("Guardar",
                    "Guarda el archivo",
                    'document-save',
                    lambda b: self.guardar()
                    ),
                    ("salir",
                    "Salir del programa",
                    'application-exit',
                    lambda b: self.close_main(None)
                    ),
                    ]
        self.proyecto = []

        self.grabar=grabar
        self.main_windows = Gtk.Window(title = "IDE python")
        self.main_windows.set_default_size(-1, 350)
        self.main_windows.connect("destroy", self.close_main)
        self.main_windows.show_all()
        headerbar = Gtk.HeaderBar()
        headerbar.set_title("¡Advertencia!")
        headerbar.set_subtitle("el sistema esta grabando el"\
                                " escritorio y el microfono")
        headerbar.set_show_close_button(True)
        self.main_windows.set_titlebar(headerbar)
        ## boton de barra de herramientas
        button = Gtk.Button("Menu")
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
        for item in menues:
            text, tooltip, iconname, callback = item
            print (iconname)
            label = Gtk.Label(text)
            image = Gtk.Image.new_from_icon_name(iconname,
                                                 Gtk.IconSize.LARGE_TOOLBAR
                                                 )
            box_boton=Gtk.Box()
            box_boton.set_homogeneous(False)
            box_boton.set_orientation(Gtk.Orientation.HORIZONTAL)
            box_boton.set_spacing(5)
            box_boton.add(image)
            box_boton.add(label)
            boton_menu = Gtk.Button()
            boton_menu.set_tooltip_text(tooltip)
            boton_menu.add(box_boton)
            boton_menu.connect("clicked", callback)
            box_popover.add(boton_menu)
        self.hbox = Gtk.HBox(spacing = 6)
        self.notebook = Gtk.Notebook()
        self.hbox.pack_start(self.notebook,True,True,0)
        self.main_windows.add(self.hbox)
        self.main_windows.show_all()
        mensaje = DIALOG_OK_CANCEL(self.main_windows,"advertencia","hola")
        respuesta = mensaje.run()
        if respuesta == Gtk.ResponseType.OK and self.grabar==True:
            pass
        elif respuesta == Gtk.ResponseType.CANCEL:
            self.grabar = False
            self.close_main(None)
            exit()
        mensaje.destroy()
        Gtk.main()

    def crear_proyecto(self,ruta):
        """TODO: Docstring for crear_proyecto.
        :returns: TODO

        """
        fecha = str(datetime.now()).split(" ")
        fecha_arch = fecha[1]+"_"+fecha[0]
        #self.ruta_trabajo
        fecha_arch = fecha_arch.replace(":","_")
        fecha_arch = fecha_arch.replace(".","-")
        self.rutastalker_proy = os.getenv("HOME")+ \
                            "/.espacio_de_trabajo/"+ruta+"/"
        os.mkdir(self.rutastalker_proy)
        self.rutastalker = self.rutastalker_proy + fecha_arch + "/"
        os.mkdir(self.rutastalker)
        self.stalker_conf = open(self.rutastalker + "stalker.config","w")
        if self.grabar == True:
            self.desktop_record_start()

    def abrir(self):
        """TODO: Docstring for abrir.
        :returns: TODO

        """
        print ("abrir")

    def new_tab(self,button):
        """TODO: Docstring for new_tab.
        :returns: TODO

        """

        nuevo_arch = NUEVO_DOC(self.main_windows)
        if len(self.proyecto)>0:

            nombre = nuevo_arch.run("Elija un nombre para su archivo",
                                    "nuevo archivo")
            for dat in self.proyecto:
                if dat == nombre:
                    print ("nombre duplicado") #aca poner un dialogo de error
                    return

            self.proyecto.append(nombre)
            pagina = HOJA(self.notebook,nombre,
                            self.rutastalker,
                            self.rutastalker_proy)
            self.stalker_conf.write(nombre+".csv\n")
            self.main_windows.show_all()
        else:
            nuevo_proyecto = NUEVO_DOC(self.main_windows)
            nombre = nuevo_arch.run("Elija un nombre para el proyecto",
                                    "nuevo proyecto")
            self.crear_proyecto(str(nombre))
            nuevo_arch = NUEVO_DOC(self.main_windows)
            nombre = nuevo_arch.run("Elija un nombre para su archivo",
                                    "nuevo archivo")
            pagina = HOJA(self.notebook,nombre,
                            self.rutastalker,
                            self.rutastalker_proy)
            self.proyecto.append(nombre)
            self.stalker_conf.write(nombre+".csv\n")
            self.main_windows.show_all()



    def on_popover_clicked(self, button):
        self.popover.show_all()

    def desktop_record_start(self):
        """TODO: Docstring for grabacion.
        :returns: TODO

        """

        fecha = str(datetime.now()).split(" ")
        cadena_final = fecha[1]+"_"+fecha[0] 
        cadena_final = cadena_final.replace(".","_")

        cadena_final = cadena_final.replace(";","_")
        cadena_final = cadena_final.replace(":","_")

        cadena_final_grabacion = self.rutastalker+ cadena_final + ".mkv"
        cadena =[ "ffmpeg -video_size 800x600 ",
                "-framerate 25 -f x11grab ",
                "-i :0.0+0,0 -f pulse -ac 2 -i ",
                "default ",cadena_final_grabacion]
        video=""
        for linea in cadena:
            video = video + linea 
        self.proc1 = subprocess.Popen(video, shell = True)
        self.stalker_conf.write(cadena_final+".mkv\n")

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
        self.stalker_conf.close()
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

