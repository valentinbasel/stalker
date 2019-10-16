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
import sys

from util import UTIL

class HOJA(UTIL):

    """Docstring for HOJA. """

    def __init__(self,notebook,nombre,ruta,ruta_py):
        """TODO: to be defined1. """

        self.rutastalker = ruta
        self.rutastalker_py = ruta_py
        self.nombre = nombre
        self.notebook = notebook
        self.create_textview(self.nombre)
        self.nombre_arch_py = self.rutastalker_py+nombre + ".py"
        self.nombre_arch_salida = self.rutastalker +nombre+ ".py"
        nombre_arch_csv = self.rutastalker + nombre + ".csv"
        self.archivo_csv = open(nombre_arch_csv,"w")


    def create_textview(self,nombre):
        """
        create_textview es el metodo encargado de crear las pestañas dentro
        del notebook general, y detro de esa pestaña, es el encargado de crear
        el GtkSourceView para poder escribir y tener resaltado de sintaxis.
        """
        self.archivo_py = None
        header = Gtk.HBox()
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        title_label = Gtk.Label(nombre)
        lm = GtkSource.LanguageManager.get_default()
        self.textview = GtkSource.View() # Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        # agrego un texto con dentro del textview
        self.textbuffer.set_text("") #aca puedo poner un template
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
        self.textview.connect("key-press-event",self.textpress)
        header.pack_start(title_label,
                          expand=True, 
                          fill=True, 
                          padding=0
                          )
        self.new_button("media-playback-start",
                        "ejecutar",
                        header,
                        self.execute,
                        self.notebook,
                        self.textbuffer,
                        )
        self.new_button("window-close-symbolic",
                        "cerrar",
                        header,
                        self.close_cb,
                        self.notebook,
                        scrolledwindow
                        )
        header.show_all()
        self.notebook.append_page(scrolledwindow,header)
    
    def close_cb(self,a,b,c):
        """TODO: Docstring for close_cb.
        :returns: TODO

        """
        self.archivo_csv.close()
        if self.archivo_py != None: 
            self.archivo_py.close()
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

        cadena_final = tecla +"," + fecha[1]+","+fecha[0]+"\n"
        print(cadena_final)
        self.archivo_csv.write(cadena_final)

        #print()

    def actualizar_arch(self, view,nombre):
        """TODO: Docstring for actualizar_arch.

        :arg1: TODO
        :returns: TODO

        """
        
        self.archivo_py = open(nombre,"w")
        start_iter = view.get_start_iter()
        end_iter = view.get_end_iter()
        text = view.get_text(start_iter, end_iter, True) 
        print(text)
        self.archivo_py.writelines(text)
        self.archivo_py.close()

    def execute(self,button,a,view):
        """TODO: Docstring for execute.

        :arg1: TODO
        :returns: TODO

        """
        fecha = str(datetime.now()).split(" ")

        cadena_final = self.nombre_arch_salida + "," + fecha[1]+","+fecha[0]+"\n"
        self.actualizar_arch(view,self.nombre_arch_py)
        self.actualizar_arch(view,cadena_final)
        proceso = subprocess.Popen(["python3", 
                            self.nombre_arch_py], 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
        i = proceso.wait()
        print(i)
        nombre_arch_out = ".stout.txt" + "," + fecha[1]+","+fecha[0]+"\n"
        nombre_arch_out = self.nombre_arch_salida + nombre_arch_out 
        nombre_arch_err = ".sterr.txt" + "," + fecha[1]+","+fecha[0]+"\n"
        nombre_arch_err = self.nombre_arch_salida + nombre_arch_err 


        archivo_salidas = open(nombre_arch_out,"w")
        archivo_err = open(nombre_arch_err,"w")

        errores = proceso.stderr.read()
        salida = proceso.stdout.read()
        proceso.stderr.close()
        proceso.stdout.close() 
        print("salida estandar: ", salida.decode(sys.getdefaultencoding()))
        archivo_salidas.writelines(salida.decode(sys.getdefaultencoding()))
        archivo_salidas.close()

        if errores != None:
            archivo_err.write("err:\n")
            print("salida errores: ",errores.decode(sys.getdefaultencoding()))
            archivo_err.writelines(errores.decode(sys.getdefaultencoding()))
            archivo_err.close()
        
        self.archivo_csv.write("err_"+str(i)+ "," + fecha[1]+","+fecha[0]+"\n")
        #self.archivo_csv.write(cadena_final)
        #self.archivo_csv.write(nombre_arch_out)
        #self.archivo_csv.write(nombre_arch_err)
