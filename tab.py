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

from util import UTIL

class HOJA(UTIL):

    """Docstring for HOJA. """

    def __init__(self,notebook,nombre):
        """TODO: to be defined1. """
        self.nombre = nombre
        self.notebook = notebook
        self.create_textview(self.nombre)
        nombre_arch_py = nombre + ".py"
        self.archivo_py = open(nombre_arch_py,"w")
        nombre_arch_csv = nombre + ".csv"
        self.archivo_csv = open(nombre_arch_csv,"w")


    def create_textview(self,nombre):
        """
        create_textview es el metodo encargado de crear las pestañas dentro
        del notebook general, y detro de esa pestaña, es el encargado de crear
        el GtkSourceView para poder escribir y tener resaltado de sintaxis.
        """
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


    def execute(self,button,a,view):
        """TODO: Docstring for execute.

        :arg1: TODO
        :returns: TODO

        """

        start_iter = view.get_start_iter()
        end_iter = view.get_end_iter()
        text = view.get_text(start_iter, end_iter, True) 
        print(text)
        self.archivo_py.writelines(text)
