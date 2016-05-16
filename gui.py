#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from numpy import sin, linspace
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

from newton import Newton, AbsoluteError, RelativeError

def _parse_error(err_str):
    """Parses a string representing an error type (Absoluto or Relativo)"""
    return AbsoluteError if err_str == 'Absoluto' else RelativeError

def _parse_function(func_str):
    """Parses a string representing a function"""
    pass

class Gui:
    def run(self): Gtk.main()
    def destroy(self, _): Gtk.main_quit()

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('newton.glade')
        self.table = Gtk.Table(2,2)
        self.main_window_init()
        self.box_init()
        self.grid_init()
        self.func_entry_init()
        self.interval_entry_init()
        self.iter_entry_init()
        self.error_entry_init()
        self.error_drop_init()
        self.statusbar_init()
        self.button_init()
        self.window.show_all()

    def calculate(self, widget):
        self.box.pack_start(self.table, True, True, 0)
        data = self.get_relevant_data()
        # self.newton = Newton(data['function'], df, data['interval'], data['maxError'], data['maxIter'], data['errorType'])
        # stop_reason = self.newton.run()
        # self.draw_table(widget, data)
        # msg = "Após %d iterações, obtemos um valor aproximado de 0.0015392" % (data['maxIter'])
        # ctx_id = self.statusbar.get_context_id('test')
        # self.statusbar_update(widget, ctx_id, msg)

    def draw_table(self, data):
        pass

    def get_relevant_data(self):
        """Returns a dict with all the user input data"""
        from ast import literal_eval
        data = { 'function': self.funcEntry.get_text(), # _parse_function(self.funcEntry.get_text())
                 'interval': literal_eval(self.intervalEntry.get_text()),
                 'maxError': literal_eval(self.errorEntry.get_text()),
                 'maxIter': literal_eval(self.iterEntry.get_text()),
                 'errorType': _parse_error(self.errorDrop.get_active_text()) }
        print 'Debug:\n' + str(data) # debug
        return data

    def main_window_init(self):
        self.window = self.builder.get_object('window1')
        self.window.connect('destroy', self.destroy)

    def func_entry_init(self):
        self.funcEntry = self.builder.get_object('funcEntry')

    def box_init(self):
        self.box = self.builder.get_object('box1')

    def grid_init(self):
        self.grid = self.builder.get_object('grid1')

    def statusbar_init(self):
        self.statusbar = self.builder.get_object('statusbar')

    def interval_entry_init(self):
        self.intervalEntry = self.builder.get_object('intervaloEntry')

    def iter_entry_init(self):
        self.iterEntry = self.builder.get_object('iterEntry')

    def error_entry_init(self):
        self.errorEntry = self.builder.get_object('errorEntry')

    def error_drop_init(self):
        self.errorDrop = self.builder.get_object('errorDrop')

    def button_init(self):
        self.calcBtn = self.builder.get_object('calcularButton')
        self.calcBtn.connect('clicked', self.calculate)
        #self.calcBtn.connect('clicked', self.statusbar_update, ctx_id, msg)

    def statusbar_update(self, button, ctx_id, msg):
        # print self.funcEntry.get_text()
        self.statusbar.push(ctx_id, msg)

if __name__ == '__main__':
    Gui().run()
