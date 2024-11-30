import sys
import random
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class NumberSelectorApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="BuckShot Helper" if random.randint(0, 9) != 0 else "BackShot Helper")

        self.set_default_size(500, 300)
        self.set_border_width(10)
        
        self.removed_from_order = ""
        
        # Create the main layout
        main_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_layout)

        # Create Lives section
        lives_layout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lives_label = Gtk.Label(label="Lives:")
        self.lives_spinbutton = Gtk.SpinButton.new_with_range(0, 10, 1)
        self.lives_spinbutton.set_value(0)
        self.lives_spinbutton.connect("value-changed", self.on_spinbox_value_changed)
        self.last_lives_value = 0
        lives_layout.pack_start(lives_label, False, False, 0)
        lives_layout.pack_start(self.lives_spinbutton, False, False, 0)

        # Create Blanks section
        blanks_layout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        blanks_label = Gtk.Label(label="Blanks:")
        self.blanks_spinbutton = Gtk.SpinButton.new_with_range(0, 10, 1)
        self.blanks_spinbutton.set_value(0)
        self.blanks_spinbutton.connect("value-changed", self.on_spinbox_value_changed)
        self.last_blanks_value = 0
        blanks_layout.pack_start(blanks_label, False, False, 0)
        blanks_layout.pack_start(self.blanks_spinbutton, False, False, 0)

        # Create Button Grid (10 buttons side by side)
        button_layout = Gtk.Grid()
        self.buttons = []
        for i in range(10):
            button = Gtk.Button(label=" ")
            button.set_sensitive(False)
            button.set_size_request(40, 40)
            button.connect("clicked", self.on_button_click, i)
            self.buttons.append(button)
            button_layout.attach(button, i, 0, 1, 1)

        # Clear button
        clear_button = Gtk.Button(label="Clear")
        clear_button.connect("clicked", self.clear)

        # Add widgets to main layout
        main_layout.pack_start(lives_layout, False, False, 0)
        main_layout.pack_start(blanks_layout, False, False, 0)
        main_layout.pack_start(button_layout, True, True, 0)
        main_layout.pack_start(clear_button, False, False, 0)

        # Set the window properties
        self.set_resizable(False)

    def clear(self, widget):
        self.lives_spinbutton.set_value(0)
        self.blanks_spinbutton.set_value(0)

    def on_button_click(self, button, button_index):
        if button.get_label() == "#":
            self.set_button_letter(button, "L")
        elif button.get_label() == "L":
            self.set_button_letter(button, "B")
        else:
            self.set_button_letter(button, "#")
        
    def set_button_letter(self, button, letter):
        button.set_label(letter)
        if letter == "L":
            button.get_style_context().add_class('lives')
        elif letter == "B":
            button.get_style_context().add_class('blanks')
        else:
            button.get_style_context().add_class('default')

    def get_string_from_button(self):
        order = ""
        for button in self.buttons:
            text = button.get_label()
            if text != " ":
                order += text
        return order

    def set_buttons_from_string(self, order):
        i = 0
        for button in self.buttons:
            if i < len(order) and len(order) != 0:
                button.set_sensitive(True)
                self.set_button_letter(button, order[i])
            else:
                button.set_sensitive(False)
                self.set_button_letter(button, " ")
            i += 1

    def on_spinbox_value_changed(self, widget):
        lives_value = self.lives_spinbutton.get_value_as_int()
        blanks_value = self.blanks_spinbutton.get_value_as_int()
        possible_shells = 10 - (lives_value + blanks_value)
        
        if possible_shells == 0:
            self.lives_spinbutton.set_adjustment(Gtk.Adjustment(0, 0, lives_value, 1, 1, 0))
            self.blanks_spinbutton.set_adjustment(Gtk.Adjustment(0, 0, blanks_value, 1, 1, 0))
        else:
            self.lives_spinbutton.set_adjustment(Gtk.Adjustment(0, 0, 10, 1, 1, 0))
            self.blanks_spinbutton.set_adjustment(Gtk.Adjustment(0, 0, 10, 1, 1, 0))
        
        known_order = self.get_string_from_button()
        if abs(lives_value - self.last_lives_value) > 1:
            change_amount = abs(lives_value - self.last_lives_value)
        elif abs(blanks_value - self.last_blanks_value) > 1:
            change_amount = abs(blanks_value - self.last_blanks_value)
        else:
            change_amount = 1

        if lives_value < self.last_lives_value or blanks_value < self.last_blanks_value:
            for i in range(change_amount):
                self.removed_from_order = known_order[:1] + self.removed_from_order
                known_order = known_order[1:]
        else:
            for i in range(change_amount):
                if self.removed_from_order != "":
                    known_order = self.removed_from_order[:1] + known_order
                    self.removed_from_order = self.removed_from_order[1:]
                else:
                    known_order = '#' + known_order
        
        self.set_buttons_from_string(known_order)
        self.last_lives_value = self.lives_spinbutton.get_value_as_int()
        self.last_blanks_value = self.blanks_spinbutton.get_value_as_int()

        if lives_value == 0 and blanks_value == 0:
            print("New Round")
            self.removed_from_order = ""


if __name__ == '__main__':
    app = NumberSelectorApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
