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

###############################################################################
#    _______  _______  ______    _______  _______  _______ 
#   |       ||       ||    _ |  |       ||   _   ||       |
#   |_     _||   _   ||   | ||  |       ||  |_|  ||____   |
#     |   |  |  | |  ||   |_||_ |       ||       | ____|  |
#     |   |  |  |_|  ||    __  ||      _||       || ______|
#     |   |  |       ||   |  | ||     |_ |   _   || |_____ 
#     |___|  |_______||___|  |_||_______||__| |__||_______|
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
import template
from tab import HOJA

from util import DIALOG_OK_CANCEL
from util import NUEVO_DOC
from util import MENSAJE
from util import ABRIR_DIALOG
class MAIN_W(object):

    """La clase MAIM_W es la clase principal de TORCAZ.
        todos los eventos y la construcción del arbol de widget sale de aca
        el esquema de contenedores es el siguiente:

            main_windows
             |
              --> headerbar
             |       |
             |        --> button
             |       |      |
             |       |       --> popover
             |       |              |
             |       |               --> box_popover
             |       |                     |
             |       |                      --> boton_menu
             |       |                           |
             |       |                            --> box_boton_popover
             |       |                                 |
             |       |                                  --> label
             |       |                                 |
             |       |                                  --> image 
             |       |
             |        --> button_tab
             |               |
             |                --> box_boton
             |                       |
             |                        --> image 
              --> hbox
                   |
                    --> notebook 
    Notas:

    La variable global "grabar", habilita a la clase para poder capturar 
    el microfono y la pantalla de video 

    """

    def __init__(self,grabar):
        """TODO: to be defined1. """
        # Variable con la declaración, nombre, toolkit y metodo asociado
        # para cada boton del menu
        menues = [  ("Abrir",
                    "Abre un nuevo archivo",
                    'document-open',
                    lambda b: self.abrir()
                    ),
                    ("Abrir proyecto",
                    "Abre un proyecto",
                    'document-open',
                    lambda b: self.abrir_pry()
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
        self.proyecto = [] # almacena el nombre de cada archivo .py que se crea
        self.grabar=grabar # Si es True habilita la grabación del escritorio
        # declaro las variables de los archivos de configuración.
        # aca se guardan los CSV de las teclas pulsadas por el teclado
        # los puntos X/Y del mouse y un archivo de configuración para burrhus
        self.mouse_csv = None
        self.archivo_csv = None
        self.stalker_conf = None
        self.texto_template = template.texto 
        self.main_windows = Gtk.Window(title = "IDE python")
        self.main_windows.set_default_size(-1, 350)
        self.main_windows.connect("destroy", self.close_main)
        self.main_windows.connect("motion-notify-event", self.mouse_event)
        self.main_windows.show_all()
        self.headerbar = Gtk.HeaderBar()
        if self.grabar == True:
            self.headerbar.set_title("¡Advertencia!")
            self.headerbar.set_subtitle("el sistema esta grabando el"\
                                    " escritorio y el microfono")
        else:
            self.headerbar.set_title("grabación desactivada")
            self.headerbar.set_subtitle("el sistema NO esta grabando el"\
                                    " escritorio ni el microfono (solo interacciones de teclado dentro del IDE)")

        self.headerbar.set_show_close_button(True)
        self.main_windows.set_titlebar(self.headerbar)
        ## boton de barra de herramientas
        button = Gtk.Button("Menu")
        button.connect("clicked", self.on_popover_clicked)
        self.headerbar.pack_start(button)
        self.new_button("document-new","nueva pestaña",self.headerbar,self.new_tab)

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
            #print (iconname)
            label = Gtk.Label(text)
            image = Gtk.Image.new_from_icon_name(iconname,
                                                 Gtk.IconSize.LARGE_TOOLBAR
                                                 )
            box_boton_popover=Gtk.Box()
            box_boton_popover.set_homogeneous(False)
            box_boton_popover.set_orientation(Gtk.Orientation.HORIZONTAL)
            box_boton_popover.set_spacing(5)
            box_boton_popover.add(image)
            box_boton_popover.add(label)
            boton_menu = Gtk.Button()
            boton_menu.set_tooltip_text(tooltip)
            boton_menu.add(box_boton_popover)
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


        self.main_windows.connect('notify::is-active', self.cambia_el_foco)
        Gtk.main()
    def mouse_event(self, a,b):
        """TODO: Docstring for mouse_event.

        :a: TODO
        :returns: TODO

        """
        if self.mouse_csv !=None:
            fecha = str(datetime.now()).split(" ")
            cadena_final = str(b.x)+","+str(b.y) +"," + fecha[1]+","+fecha[0]+"\n"
            self.mouse_csv.write(cadena_final)


    def cambia_el_foco(self,window, param):
        if self.archivo_csv != None:
            fecha = str(datetime.now()).split(" ")
            cadena_final = "foco_"+ str(window.props.is_active) +"," + fecha[1]+","+fecha[0]+"\n"
            #print(cadena_final)
            self.archivo_csv.write(cadena_final)


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
                            "/espacio_de_trabajo/"+ruta+"/"
        os.mkdir(self.rutastalker_proy)
        self.rutastalker = self.rutastalker_proy + fecha_arch + "/"
        os.mkdir(self.rutastalker)
        self.stalker_conf = open(self.rutastalker + "stalker.config","w")

        self.archivo_csv = open(self.rutastalker+"main_windows.csv","w")
        self.archivo_csv.write("tecla,hora,fecha\n")
        self.mouse_csv = open(self.rutastalker+"main_windows_mouse.csv","w")
        self.mouse_csv.write("x,y,hora,fecha\n")
        if self.grabar == True:
            self.desktop_record_start()

    def abrir(self):
        """TODO: Docstring for abrir.
        :returns: TODO

        """
        print ("abrir")

    def abrir_pry(self):
        """TODO: Docstring for abrir.
        :returns: TODO

        """
        print ("abrir proyecto")
        pry = ABRIR_DIALOG()
        resultado=pry.abrir_pry("proyecto")
        print (resultado)

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
                            self.rutastalker_proy,
                            self.main_windows)
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
                            self.rutastalker_proy,
                            self.main_windows,
                            self.texto_template)
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
        cadena =[ "ffmpeg -video_size 1366x768 ",
                "-framerate 25 -f x11grab ",
                "-i :0.0+0,0 -f pulse -ac 2 -i ",
                "default ",cadena_final_grabacion, " -loglevel quiet"]
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
        #if self.stalker_conf != None:
        #    self.stalker_conf.close()
        if self.archivo_csv != None:
            self.archivo_csv.close()
        if self.mouse_csv != None:
            self.mouse_csv.close()
        if self.stalker_conf != None:
            self.stalker_conf.write("main_windows.csv\n")
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
 
grabar = False#True
win = MAIN_W(grabar)

