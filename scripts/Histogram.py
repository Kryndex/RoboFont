# Glyph Width Histogram
# by Jens 2014-09-08

from math import ceil
import vanilla
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.canvas import Canvas
from mojo.drawingTools import *
from lib.tools.defaults import getDefault


class UnitizationInfo(object):
    def __init__(self):
        self.systems = {}
    
    def add_system(self, system):
        if system.upm in self.systems:
            self.systems[system.upm].append(system)
        else:
            self.systems[system.upm] = [system]
    
    def get_systems_by_upm(self, upm):
        if upm in self.systems:
            return self.systems[upm]
        else:
            return []
    
    def get_all_units(self):
        return self.systems.keys()
    
    def get_ui_list(self):
        # return a list that can be used in vanilla.List
        ui_list = ["-"]
        for upm in sorted(self.systems.keys()):
            for system in sorted(self.systems[upm]):
                ui_list.append(system.name)
        return ui_list
    
    def get_system_by_name(self, name):
        for system_list in self.systems.itervalues():
            for system in system_list:
                if system.name == name:
                    return system
        return None


class UnitSystem(object):
    def __init__(self, name, units, min_units=None, max_units=None, strategy="free", unit_dict={}):
        self.name = name
        self.upm = units
        self.min_units = min_units
        self.max_units = max_units
        
        # unitization strategies
        if strategy == "alleq":
            self.set_all_equal()
        elif strategy == "fixed":
            if unit_dict:
                self.set_fixed_units(unit_dict)
            else:
                raise "Must supply unit_dict when using fixed units"
        elif strategy == "free":
            self.set_free_units()
        else:
            raise "Unknown unitization strategy."
    
    def set_fixed_units(self, unit_dict):
        self.all_equal = False
        self.fixed_units = unit_dict
        self.free_units = False
    
    def set_all_equal(self, all_equal=True):
        self.all_equal = all_equal
        self.fixed_units = {}
        self.free_units = False
    
    def set_free_units(self, free_units=True):
        self.all_equal = False
        self.fixed_units = {}
        self.free_units = free_units

# define known unit systems
# sources: <http://www.quadibloc.com/comp/propint.htm>
#          Osterer, Stamm (Hrsg.): Adrian Frutiger Schriften. Das Gesamtwerk. Birkhaeuser 2009

unitization_info = UnitizationInfo()

unitization_info.add_system(UnitSystem("Monospaced", 1, 0, 1, "alleq"))
unitization_info.add_system(UnitSystem("IBM Executive Typewriter", 5, 2, 5, "fixed", {
    2: ["f", "i", "j", "l", "t", "I",
        "period", "comma", "colon", "semicolon", "quotesingle", "exclam", "parenleft", "parenright", "space"],
    3: ["a", "b", "c", "d", "e", "g", "h", "k", "n", "o", "p", "q", "r", "s", "u", "v", "x", "y", "z", "J", "S",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        'quotedbl', "question", "numbersign", "plus", "hyphen", "asterisk", "slash", "equal"],
    4: ["w", "A", "B", "C", "D", "E", "F", "G", "H", "K", "L", "N", "O", "P", "Q", "R", "T", "U", "V", "X", "Y", "Z",
        "ampersand"],
    5: ["m", "W", "M",
        "at", "percent", "underscore", "onehalf", "onequarter"],
}))
unitization_info.add_system(UnitSystem("IBM Mag Card Executive (1972)", 7, 3, 7, "fixed", {
    3: ["i", "j", "l"],
    4: ["f", "t", "I", "quotesingle"],
    5: ["a", "c", "e", "h", "k", "n", "o", "r", "s", "u", "v", "x", "z", "J",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "period", "comma", "colon", "semicolon", "exclam", "question", "quotedbl", "at", "numbersign", "dollar", "ampersand", "cent", "parenleft", "parenright", "+", "-", "*", "/", "=", "_", "onehalf", "onequarter", "space"],
    6: ["b", "d", "g", "p", "q", "y", "E", "F", "L", "P", "S", "Z"],
    7: ["m", "w", "A", "B", "C", "D", "G", "H", "K", "M", "N", "O", "Q", "R", "T", "U", "V", "W", "X", "Y"],
}))
unitization_info.add_system(UnitSystem("IBM Selectric Composer (1966)", 9, 3, 9, "fixed", {
    3: ["i", "j", "l",
        "period", "comma", "semicolon", "grave", "quotesingle", "hyphen", "space"],
    4: ["f", "t", "r", "s", "I",
        "colon", "exclam", "parenleft", "parenright", "slash"],
    5: ["a", "c", "e", "g", "z", "J", "bracketleft"],
    6: ["b", "d", "h", "k", "n", "p", "q", "u", "v", "x", "y", "P", "S",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "bracketright", "plus", "asterisk", "equal", "dollar", "dagger"],
    7: ["B", "C", "E", "F", "L", "T", "Z"],
    8: ["w", "A", "D", "G", "H", "K", "N", "O", "Q", "R", "U", "V", "X", "Y",
        "ampersand", "at", "percent", "onehalf", "onequarter", "threequarters", "emdash"],
    9: ["m", "W", "M"],
}))
unitization_info.add_system(UnitSystem("Linotype early photo typesetting", 18, 0, 18, "free"))
unitization_info.add_system(UnitSystem("Monotype hot metal and Monophoto Filmsetter", 18, 4, 18, "free"))
unitization_info.add_system(UnitSystem("Lumitype", 36, 0, None, "free"))
unitization_info.add_system(UnitSystem("Berthold photo typesetting", 48, 0, None, "free"))
unitization_info.add_system(UnitSystem("Linotype later photo typesetting (3 x 18)", 54, 0, 54, "free"))
unitization_info.add_system(UnitSystem("URW photo typesetting", 54, 0, 54, "free"))


"""
HistogramUI - the main window (RoboFont-specific)
"""


class HistogramUI(BaseWindowController):

    def __init__(self):
        
        self.histogram_width = 608
        self.histogram_height = 380
        histogram_x_offset = 10
        histogram_y_offset = 10
        window_width = 630
        window_height = 500
        
        # how much of the em is shown?
        self.ems_horizontal = 1.3
        
        # how many pixels on the canvas per letter?
        self.scale_vertical = 10.0
        
        self.units = 18
        self.known_units = unitization_info.get_all_units()
        self.system = None
        self.show_fixed = True
        
        self.glyphs = []
        
        # show glyphs or lines?
        self.show_glyphs = True
        
        y = 10
        self.w = vanilla.Window((window_width, window_height), "Glyph Width Histogram")
        self.w.histogram = Canvas((histogram_x_offset, histogram_y_offset, -10, self.histogram_height),
                                canvasSize=(self.histogram_width, self.histogram_height),
                                hasHorizontalScroller=False,
                                hasVerticalScroller=False,
                                delegate=self)
        y += self.histogram_height + histogram_y_offset + 8
        self.w.unit_label = vanilla.TextBox((histogram_x_offset, y, 90, 20), "Units per em:")
        self.w.unit_display = vanilla.TextBox((histogram_x_offset + 90, y, 30, 20), self.units)
        self.w.system_selection = vanilla.PopUpButton((histogram_x_offset + 120, y-1, 300, 20),
            [],
            callback = self._systemCallback,
            #sizeStyle = "small",
        )
        self.w.show_fixed = vanilla.CheckBox((histogram_x_offset + 462, y-1, 300, 20),
            "Show system widths",
            value=self.show_fixed,
            callback = self._showFixedCallback,
        )
        y += 28
        self.w.unit_slider = vanilla.Slider((histogram_x_offset, y, -10, 20),
            minValue = 1,
            maxValue = 64,
            value = self.units,
            tickMarkCount = 64,
            callback = self._unitCallback,
            stopOnTickMarks = True,
        )
        y += 33
        self.w.glyph_selection_label = vanilla.TextBox((histogram_x_offset, y, 120, 20), "Analyze glyphs:")
        self.w.glyph_selection = vanilla.RadioGroup((histogram_x_offset + 110, y, 210, 20),
            ["Selected", "All", "Charset:"],
            isVertical = False,
            callback = self._glyphSelectionCallback,
            sizeStyle = "small",
        )
        
        self.w.charset_selection = vanilla.PopUpButton((histogram_x_offset + 320, y, -110, 20),
            [],
            callback = self._charsetCallback,
            #sizeStyle = "small",
        )
        
        self.w.update_button = vanilla.Button((-100, y, -10, 20),
            "Update",
            callback = self._updateButtonCallback
        )
        
        self._unitCallback()
        self.w.system_selection.setItems(unitization_info.get_ui_list())
        if self.units in self.known_units:
            self.system = unitization_info.get_systems_by_upm(self.units)[0]
            self.w.system_selection.set(unitization_info.get_ui_list().index(self.system.name))
        else:
            self.system = None
            self.w.system_selection.set(0)
        self.w.glyph_selection.set(0)
        self.w.charset_selection.enable(False)
        self.update_charset_selection()
        self.glyphs = self.get_glyphnames_for_histogram()
        self.calculate_histogram()
        self.setUpBaseWindowBehavior()
        
        #addObserver(self, "glyphChanged", "currentGlyphChanged")
        #addObserver(self, "glyphChanged", "draw")
        #addObserver(self, "removeFontFromList", "fontWillClose")
        #addObserver(self, "updateFontList", "fontDidOpen")
        self.w.open()
    
    def _unitCallback(self, sender=None):
        self.units = int(self.w.unit_slider.get())
        if sender is not None:
            if self.units in self.known_units:
                self.system = unitization_info.get_systems_by_upm(self.units)[0]
                self.w.system_selection.set(unitization_info.get_ui_list().index(self.system.name))
            else:
                self.system = None
                self.w.system_selection.set(0)
        text = "%i" % self.units
        self.w.unit_display.set(self.units)
        self._check_fixed()
        self.w.histogram.update()
    
    def _systemCallback(self, sender=None):
        # a unit system has been selected
        name = self.w.system_selection.getItems()[sender.get()]
        if name != "-":
            self.system = unitization_info.get_system_by_name(name)
            self.w.unit_slider.set(self.system.upm)
            self._unitCallback()
        self._check_fixed()
    
    def _check_fixed(self):
        if self.system is not None:
            if self.system.fixed_units:
                self.w.show_fixed.enable(True)
            else:
                self.w.show_fixed.enable(False)
        else:
            self.w.show_fixed.enable(False)
    
    def _showFixedCallback(self, sender=None):
        self.show_fixed = sender.get()
        self.w.histogram.update()
    
    def _glyphSelectionCallback(self, sender=None):
        if self.w.glyph_selection.get() == 2:
            self.w.charset_selection.enable(True)
        else:
            self.w.charset_selection.enable(False)
        self.glyphs = self.get_glyphnames_for_histogram()
        self.calculate_histogram()
    
    def _charsetCallback(self, sender=None):
        self.glyphs = self.get_glyphnames_for_histogram()
        self.calculate_histogram()
    
    def _updateButtonCallback(self, sender=None):
        charset_index = self.w.charset_selection.get()
        self.update_charset_selection()
        if charset_index <= len(self.w.charset_selection.getItems()):
            self.w.charset_selection.set(charset_index)
        else:
            self.w.charset_selection.set(-1)
        self.glyphs = self.get_glyphnames_for_histogram()
        self.calculate_histogram()
    
    def update_charset_selection(self):
        self.charsets = getDefault("charsets")
        self.w.charset_selection.setItems(sorted(self.charsets.keys()))
    
    def get_glyphnames_for_histogram(self):
        font = CurrentFont()
        mode = self.w.glyph_selection.get()
        if mode == 0:
            #print "Analyze Selection"
            names = font.selection
        elif mode == 1:
            #print "Analyze All Glyphs"
            names = font.glyphOrder
        else:
            #print "Analyze Charset"
            all_glyphs = font.glyphOrder
            selected_charset_name = self.w.charset_selection.getItems()[self.w.charset_selection.get()]
            names = [name for name in self.charsets[selected_charset_name] if name in all_glyphs]
        return names
    
    def calculate_histogram(self, sender=None):
        #print "calculate_histogram"
        font = CurrentFont()
        #names = self.get_glyphnames_for_histogram()
        histogram = {}
        max_width = 0
        for name in self.glyphs:
            width = font[name].width
            if width > max_width:
                max_width = width
            if width in histogram:
                histogram[width].append(name)
            else:
                histogram[width] = [name]
        self.max_width = max_width
        self.histogram = histogram
        #print self.histogram
        self.w.histogram.update()
    
    def draw(self):
        # canvas draw callback
        save()
        self._drawGrid()
        restore()
        font = CurrentFont()
        if self.show_fixed and self.system is not None and self.system.fixed_units:
            # display the fixed widths of the current unitization system
            self.draw_histogram(font, self.system.upm, (0, 0, 1, 0.5), True, histogram=self.system.fixed_units)
        # draw the histogram for the current font
        self.draw_histogram(font, font.info.unitsPerEm, (1, 0, 0, 1), True)
    
    def draw_histogram(self, font, upm, color, show_glyphs=False, histogram=None):
        if histogram is None:
            histogram = self.histogram
        save()
        fill(1, 0.5, 0.2, 1.0)
        stroke(color[0], color[1], color[2], color[3])
        for width in sorted(histogram.keys()):
            num = len(histogram[width])
            x = 10 + width * self.histogram_width / (upm * self.ems_horizontal)
            save()
            if show_glyphs:
                save()
                fill(color[0], color[1], color[2], 0.2)
                fontsize(self.scale_vertical)
                for i in range(len(histogram[width])):
                    glyph_name = histogram[width][i]
                    if glyph_name in font:
                        u = font[glyph_name].unicode
                        if u:
                            text("%s" % unichr(u), x + 4, 18 + i * self.scale_vertical)
                        else:
                            text("%s" % glyph_name, x + 4, 18 + i * self.scale_vertical)
                    else:
                        text("%s" % glyph_name, x + 4, 18 + i * self.scale_vertical)
                restore()
                strokewidth(2)
            else:
                strokewidth(6)
            # draw bars
            line(x, 20, x, 20 + num * self.scale_vertical)
            strokewidth(0)
            text("%s" % (num), x - 3 * len(str(num)), 22 + num * self.scale_vertical)
            restore()
        restore()
    
    def _drawGrid(self):
        label_every = 1
        if self.units > 24:
            label_every = 2
        save()
        strokeWidth(0)
        stroke(None)
        fill(0.88, 0.92, 0.98)
        if self.system is not None:
            if self.system.min_units is not None:
                rect(0, 0, 10 + self.system.min_units * self.histogram_width / (self.units * self.ems_horizontal), self.histogram_height)
            if self.system.max_units is not None:
                rect(10 + self.system.max_units * self.histogram_width / (self.units * self.ems_horizontal), 0, self.histogram_width, self.histogram_height)
        
        strokeWidth(1.0)
        stroke(0.8, 0.8, 0.8)
        fill(0.6, 0.6, 0.6)
        for u in range(0, int(ceil(self.units * self.ems_horizontal))):
            x = 10 + u * self.histogram_width / (self.units * self.ems_horizontal)
            if u == self.units:
                # mark the full em
                stroke(0, 0, 0)
                line(x, 20, x, self.histogram_height-10)
                strokeWidth(0)
                text("1 em", x + 4, self.histogram_height - 21)
                strokeWidth(1.0)
            elif u % 10 == 0:
                # make every 10th line darker
                stroke(0.5, 0.5, 0.5)
                line(x, 20, x, self.histogram_height - 20)
            else:
                stroke(0.8, 0.8, 0.8)
                line(x, 20, x, self.histogram_height - 30)
            if u % label_every == 0:
                strokeWidth(0)
                text("%s" % (u), x - 3 * len(str(u)), 5)
        restore()


if __name__ == "__main__":
    OpenWindow(HistogramUI)