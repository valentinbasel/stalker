#! /usr/bin/python

#
# gtk3 example/widget for VLC Python bindings
# Copyright (C) 2017 Olivier Aubert <contact@olivieraubert.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#

"""VLC Gtk3 Widget classes + example application.

This module provides two helper classes, to ease the embedding of a
VLC component inside a pygtk application.

VLCWidget is a simple VLC widget.

DecoratedVLCWidget provides simple player controls.

When called as an application, it behaves as a video player.
"""

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from gi.repository import Gtk, GObject
from lista import TreeViewFilterWindow
Gdk.threads_init ()

import sys
import vlc

from gettext import gettext as _

# Create a single vlc.Instance() to be shared by (possible) multiple players.
if 'linux' in sys.platform:
    # Inform libvlc that Xlib is not initialized for threads
    instance = vlc.Instance("--no-xlib")
else:
    instance = vlc.Instance()


class VLCWidget(Gtk.DrawingArea):
    """Simple VLC widget.

    Its player can be controlled through the 'player' attribute, which
    is a vlc.MediaPlayer() instance.
    """
    __gtype_name__ = 'VLCWidget'

    def __init__(self, *p):
        Gtk.DrawingArea.__init__(self)
        self.player = instance.media_player_new()
        def handle_embed(*args):
            if sys.platform == 'win32':
                self.player.set_hwnd(self.get_window().get_handle())
            else:
                self.player.set_xwindow(self.get_window().get_xid())
            return True
        self.connect("realize", handle_embed)
        self.set_size_request(800, 600)

class DecoratedVLCWidget(Gtk.VBox):
    """Decorated VLC widget.

    VLC widget decorated with a player control toolbar.

    Its player can be controlled through the 'player' attribute, which
    is a Player instance.
    """
    __gtype_name__ = 'DecoratedVLCWidget'

    def __init__(self, *p):
        super(DecoratedVLCWidget, self).__init__()
        self._vlc_widget = VLCWidget(*p)
        self.player = self._vlc_widget.player 
        ad1 = Gtk.Adjustment(0, 0,100, 1, 20, 0)
        self.scaled = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1)
        self.scaled.connect("value-changed", self.scale_moved)
        self.pack_start(self._vlc_widget,True,True,0)
        self.pack_start(self.scaled,False,False,0)
        self._toolbar = self.get_player_control_toolbar()
        self.pack_start(self._toolbar, False, False, 0)
        #self.add(self.vbox)
        GObject.timeout_add(1000, self.on_timeout, None)
        self.show_all()

    def scale_moved(self, arg1):
        """TODO: Docstring for scale_moved.

        :arg1: TODO
        :returns: TODO

        """
        print("_")

    def on_timeout(self, arg1):
        """TODO: Docstring for on_timeout.

        :arg1: TODO
        :returns: TODO

        """
        s=self.player.get_state()
        if s != vlc.State.NothingSpecial and self.player.get_time() >-1:
            t=self.player.get_time()
            #print(t)
            l = self.player.get_length()
            if t >0:
                mm=float(int(t)*100/int(l))
                print(mm)
                self.scaled.set_value(mm)
        return True

    def get_player_control_toolbar(self):
        """Return a player control toolbar
        """
        tb = Gtk.Toolbar.new()
        for text, tooltip, iconname, callback in (
            ("Play", "Play", 'media-playback-start', lambda b: self.player.play()),
            (_("Pause"), _("Pause"), 'media-playback-pause', lambda b: self.player.pause()),
            (_("Stop"), _("Stop"), 'media-playback-stop', lambda b: self.player.stop()),
            (_("Quit"), _("Quit"), 'window-close-symbolic', Gtk.main_quit),
            ):
            i = Gtk.Image.new_from_icon_name(iconname, Gtk.IconSize.LARGE_TOOLBAR)
            b = Gtk.ToolButton()#i, text)
            b.set_icon_widget(i)
            b.set_tooltip_text(tooltip)
            b.connect("clicked", callback)
            tb.insert(b, -1)
        return tb

class VideoPlayer:
    """Example simple video player.
    """
    def __init__(self):
        self.vlc = DecoratedVLCWidget()
        
    def main(self, fname):
        
        self.tree = TreeViewFilterWindow("/home/vbasel/programa1.csv")
        fvideo=fname.split("/")
        fvideo = fvideo[-1]
        self.seg=self.convert_time(fvideo)

        self.vlc.player.set_media(instance.media_new(fname))

        w = Gtk.Window()
        hbox = Gtk.HBox()
        vbox = Gtk.VBox()
        boton = Gtk.Button(label = "PDI")
        boton.connect("clicked",self.boton_click)

        
        hbox.pack_start(self.vlc,True,True,10)
        vbox.pack_start(self.tree,True,True,0)

        vbox.pack_start(boton,False,False,0)
        
        hbox.pack_start(vbox,False,False,10)
        w.add(hbox)
        w.show_all()
        w.connect("destroy", Gtk.main_quit)
        Gtk.main()

    def boton_click(self, arg1):
        """TODO: Docstring for boton_click.

        :arg1: TODO
        :returns: TODO

        """
        if self.tree.seg >0:
            pdi = self.tree.seg - self.seg
            print(pdi)
            self.vlc.player.set_time(pdi*1000)
    def convert_time(self, hms):
        """TODO: Docstring for convert_time.

        :arg1: TODO
        :returns: TODO

        """

        hms = hms.split("_")
        h=int(hms[0])*3600
        m=int(hms[1])*60
        s=int(hms[2])
        seg=h+m+s
        print(seg)
        return seg 

if __name__ == '__main__':
    if not sys.argv[1:]:
       print('You must provide at least 1 movie filename')
       sys.exit(1)
    if len(sys.argv[1:]) == 1:
        p=VideoPlayer()
        p.main(sys.argv[1])
    instance.release()

