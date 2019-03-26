#!/usr/bin/python

import re
import time
from pyswip import *

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty, ListProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string('''
#:import NoTransition kivy.uix.screenmanager.NoTransition

<PortsScreen>
    add: add
    list: list
    BoxLayout:
        id: box
        spacing: 25
        padding: (25, 25)
        orientation: 'vertical'
        canvas.before:
            Color:
                rgb: 0.15, 0.15, 0.15,
            Rectangle:
                pos: box.pos
                size: box.size
        AddPort:
            id: add
        PortList:
            id: list

<AddPort>
    id: box
    id_f: id
    name_f: name
    height: 40
    spacing: 5
    padding: 5
    orientation: 'horizontal'
    size_hint_y: None
    canvas.before:
        Color:
            rgb: 0.2, 0.2, 0.2
        Rectangle:
            pos: box.pos
            size: box.size
    TextInput:
        id: id
        hint_text: 'code'
        foreground_color: (1, 0, 0, 1) if root.error else (0, 0, 0, 1)
    TextInput:
        id: name
        hint_text: 'city'
    Button:
        text: 'Agregar'
        on_release: root.submit_port()

<PortList>
    container: container
    scroll_type: ['bars']
    bar_color: 1, 1, 1, 0.75
    on_parent: root.update_ports()
    BoxLayout:
        id: container
        padding: 0
        spacing: 10
        size_hint_y: None
        height: container.minimum_height
        orientation: 'vertical'

<PortItem>
    id: item
    height: 50
    padding: 10
    spacing: 10
    size_hint_y: None
    orientation: 'horizontal'
    canvas.before:
        Color:
            rgb: 0.2, 0.2, 0.2
        Rectangle:
            pos: item.pos
            size: item.size
    Label:
        id: id
        size_hint_x: None
        text: root._id
        canvas.before:
            Color:
                rgb: 0.3, 0.3, 0.3
            Rectangle:
                pos: id.pos
                size: id.size
    TextInput:
        id: i_name
        text: root._name
        disabled: root.lock
        multiline: False
    Button:
        size_hint_x: None
        text: 'Cambiar' if root.lock else 'Aceptar'
        on_release: root.toggle_lock() if root.lock else root.update_prolog(i_name.text)
    Button:
        id: delete
        size_hint_x: None
        disabled: not root.lock
        opacity: 1 if root.lock else 0
        text: 'Eliminar'
        on_release: root.delete()

<FlightsScreen>
    add: add
    list: list
    BoxLayout:
        id: box
        spacing: 25
        padding: (25, 25)
        orientation: 'vertical'
        canvas.before:
            Color:
                rgb: 0.15, 0.15, 0.15,
            Rectangle:
                pos: box.pos
                size: box.size
        AddFlight:
            id: add
        FlightList:
            id: list

<AddFlight>
    id: box
    id_f: id
    fr_f: fr
    to_f: to
    co_f: co
    height: 40
    spacing: 5
    padding: 5
    orientation: 'horizontal'
    size_hint_y: None
    canvas.before:
        Color:
            rgb: 0.2, 0.2, 0.2
        Rectangle:
            pos: box.pos
            size: box.size
    TextInput:
        id: id
        hint_text: 'code'
        foreground_color: (1, 0, 0, 1) if root.error else (0, 0, 0, 1)
    TextInput:
        id: fr
        hint_text: 'from'
        foreground_color: (1, 0, 0, 1) if root.f_error else (0, 0, 0, 1)
    TextInput:
        id: to
        hint_text: 'to'
        foreground_color: (1, 0, 0, 1) if root.t_error else (0, 0, 0, 1)
    TextInput:
        id: co
        hint_text: 'cost'
        foreground_color: (1, 0, 0, 1) if root.c_error else (0, 0, 0, 1)
    Button:
        text: 'Agregar'
        on_release: root.submit_flight()

<FlightList>
    container: container
    scroll_type: ['bars']
    bar_color: 1, 1, 1, 0.75
    on_parent: root.update_flights()
    BoxLayout:
        id: container
        padding: 0
        spacing: 10
        size_hint_y: None
        height: container.minimum_height
        orientation: 'vertical'

<FlightItem>
    id: item
    height: 50
    padding: 10
    spacing: 10
    size_hint_y: None
    orientation: 'horizontal'
    canvas.before:
        Color:
            rgb: 0.2, 0.2, 0.2
        Rectangle:
            pos: item.pos
            size: item.size
    Label:
        id: id
        size_hint_x: None
        text: root._id
        canvas.before:
            Color:
                rgb: 0.3, 0.3, 0.3
            Rectangle:
                pos: id.pos
                size: id.size
    TextInput:
        id: i_from
        text: root._from
        disabled: root.lock
        multiline: False
    TextInput:
        id: i_to
        text: root._to
        disabled: root.lock
        multiline: False
    TextInput:
        id: i_cost
        text: root._cost
        disabled: root.lock
        multiline: False
    Button:
        size_hint_x: None
        text: 'Cambiar' if root.lock else 'Aceptar'
        on_release: root.toggle_lock() if root.lock else root.update_prolog(i_from.text, i_to.text, i_cost.text)
    Button:
        id: delete
        size_hint_x: None
        disabled: not root.lock
        opacity: 1 if root.lock else 0
        text: 'Eliminar'
        on_release: root.delete()

<PathsScreen>
    _from: _from
    _to: _to
    BoxLayout:
        id: box
        padding: 25
        orientation: 'vertical'
        canvas:
            Color:
                rgb: 0.15, 0.15, 0.15
            Rectangle:
                size: box.size
                pos: box.pos
        BoxLayout:
            id: add
            size_hint_y: None
            padding: 5
            spacing: 5
            height: 40
            canvas.before:
                Color:
                    rgb: 0.2, 0.2, 0.2
                Rectangle:
                    pos: add.pos
                    size: add.size
            TextInput:
                id: _from
                hint_text: 'from'
            TextInput:
                id: _to
                hint_text: 'to'
            Button:
                text: 'query'
                on_release: root.find_paths()
        Label:
            height: 50
            size_hint_y: None
            text: 'Sin niveles (directo):'
        Label:
            id: l0
            text: root.text_0
            canvas.before:
                Color:
                    rgb: 0.2, 0.2, 0.2
                Rectangle:
                    size: l0.size
                    pos: l0.pos
        Label:
            height: 50
            size_hint_y: None
            text: 'A 1 nivel:'
        Label:
            id: l1
            text: root.text_1
            canvas.before:
                Color:
                    rgb: 0.2, 0.2, 0.2
                Rectangle:
                    size: l1.size
                    pos: l1.pos
        Label:
            height: 50
            size_hint_y: None
            text: 'A 2 niveles:'
        Label:
            id: l2
            text: root.text_2
            canvas.before:
                Color:
                    rgb: 0.2, 0.2, 0.2
                Rectangle:
                    size: l2.size
                    pos: l2.pos
        Label:
            height: 50
            size_hint_y: None
            text: 'A 3 niveles:'
        Label:
            id: l3
            text: root.text_3
            canvas.before:
                Color:
                    rgb: 0.2, 0.2, 0.2
                Rectangle:
                    size: l3.size
                    pos: l3.pos

<MainScreen>
    manager: manager
    ports_s: s_po
    flights_s: s_fl
    orientation: 'vertical'
    Label:
        id: title
        text: 'no homo bro ;-)'
        color: 1, 1, 1
        font_size: '40sp'
        size_hint_y: None
        canvas.before:
            Color:
                rgb: 0.345, 0.345, 0.345
            Rectangle:
                pos: title.pos
                size: title.size
    ScreenManager:
        id: manager
        transition: NoTransition()
        PortsScreen:
            id: s_po
            name: 'po'
        FlightsScreen:
            id: s_fl
            name: 'fl'
        PathsScreen:
            id: s_pa
            name: 'pa'
    BoxLayout:
        padding: 2.5
        size_hint_y: None
        orientation: 'horizontal'
        Button:
            text: 'Aeropuertos'
            screen: s_po.name
            on_release: root.switch_to(s_po.name, self)
        Button:
            text: 'Vuelos'
            screen: s_fl.name
            on_release: root.switch_to(s_fl.name, self)
        Button:
            text: 'Caminos'
            screen: s_pa.name
            on_release: root.switch_to(s_pa.name, self)
''')

# Information consult screen
class PortsScreen(Screen):
    add = ObjectProperty(None)
    list = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PortsScreen, self).__init__(**kwargs)

# Container and controller for new Airport
class AddPort(BoxLayout):
    error = BooleanProperty(False)
    id_f = ObjectProperty(None)
    name_f = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AddPort, self).__init__(**kwargs)

    def submit_port(self):
        if (self.id_f.text == None or self.name_f.text == None):
            return
        app = App.get_running_app()
        ids = []
        # at least one airport exists
        try:
            ids = app.prolog.query('airport(X).')
            ids = [id['X'] for id in ids]
        # no airports exist
        except:
            pass
        if (not self.id_f.text in ids):
            self.error = False
            app.create_airport(self.id_f.text, self.name_f.text)
            self.id_f.text = ''
            self.name_f.text = ''
        else:
            self.error = True

# Container and controller for new Airport
class PortList(ScrollView):
    container = ObjectProperty(None)
    ports = ListProperty([])

    def __init__(self, **kwargs):
        super(PortList, self).__init__(**kwargs)

    def update_ports(self):
        self.ports = []
        self.container.children.clear()
        prolog = App.get_running_app().prolog
        # at least one airport exists
        try:
            for port in prolog.query('airport(X), name(X, Y).'):
                self.ports.append({ 'id': str(port['X']), 'name': port['Y'] })
        # no airports exist
        except:
            print('<ERROR> no airports registered')

        for port in self.ports:
            item = PortItem(port['id'], port['name'])
            self.container.add_widget(item)

# Container and controller for new Airport
class PortItem(BoxLayout):
    _id = StringProperty('')
    _name = StringProperty('')
    lock = BooleanProperty(True)

    def __init__(self, _id = '-1', _name = '_NAME_'):
        super(PortItem, self).__init__()
        self._id = _id
        self._name = _name

    def toggle_lock(self):
        self.lock = not self.lock

    def update_prolog(self, _name):
        app = App.get_running_app()
        self.toggle_lock()
        if (self._name != _name):
            app.replace_airport_name(self._id, self._name, _name)

    def delete(self):
        App.get_running_app().delete_airport(self.id, self.name)

# Addition (or insertion) screen
class FlightsScreen(Screen):
    add = ObjectProperty(None)
    list = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FlightsScreen, self).__init__(**kwargs)

class AddFlight(BoxLayout):
    error = BooleanProperty(False)
    t_error = BooleanProperty(False)
    f_error = BooleanProperty(False)
    c_error = BooleanProperty(False)
    id_f = ObjectProperty(None)
    fr_f = ObjectProperty(None)
    to_f = ObjectProperty(None)
    co_f = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AddFlight, self).__init__(**kwargs)

    def submit_flight(self):
        if (self.id_f.text == '' or self.fr_f.text == '' or self.to_f.text == '' or self.co_f.text == ''):
            return
        app = App.get_running_app()
        ids = []
        p_ids = []

        # at least one flight exists
        try:
            ids = app.prolog.query('flight(X).')
            ids = [id['X'] for id in ids]

            p_ids = app.prolog.query('airport(X).')
            p_ids = [p_id['X'] for p_id in p_ids]
        # no flights exist
        except:
            pass

        # set all error flags to false
        error = False
        self.error = False
        self.f_error = False
        self.t_error = False
        self.c_error = False

        # check errors for each field
        if (self.id_f.text in ids):
            error = True
            self.error = True
        if (not self.fr_f.text in p_ids):
            error = True
            self.f_error = True
        if (not self.to_f.text in p_ids):
            error = True
            self.t_error = True
        # cost error will be given on float parsing
        cost = None
        try:
            cost = float(self.co_f.text)
        except ValueError:
            error = True
            self.c_error = True
            return

        # only create records if there were no errors
        if (not error):
            self.co_f.text = str(cost)
            self.c_error = False
            app.create_flight(self.id_f.text, self.fr_f.text, self.to_f.text, self.co_f.text)
            self.id_f.text = ''
            self.fr_f.text = ''
            self.to_f.text = ''
            self.co_f.text = ''

class FlightList(ScrollView):
    container = ObjectProperty(None)
    flights = ListProperty([])

    def __init__(self, **kwargs):
        super(FlightList, self).__init__(**kwargs)

    def update_flights(self):
        self.flights = []
        self.container.children.clear()
        prolog = App.get_running_app().prolog
        # at least one flight exists
        try:
            for flight in prolog.query('flight(W), path(W, X, Y, Z).'):
                self.flights.append({ 'id': str(flight['W']), 'from': flight['X'], 'to': flight['Y'], 'cost': flight['Z'] })
        # no flights exist
        except:
            print('<ERROR> no flights registered')

        for flight in self.flights:
            item = FlightItem(flight['id'], flight['from'], flight['to'], flight['cost'])
            self.container.add_widget(item)

class FlightItem(BoxLayout):
    _id = StringProperty('')
    _from = StringProperty('')
    from_dd = ObjectProperty(None)
    _to = StringProperty('')
    to_dd = ObjectProperty(None)
    _cost = StringProperty('')
    lock = BooleanProperty(True)

    def __init__(self, _id = '-1', _from = '_FROM_', _to = '_TO_', _cost = '_COST_'):
        super(FlightItem, self).__init__()
        self._id = _id
        self._from = _from
        self._to = _to
        self._cost = str(_cost)

    def toggle_lock(self):
        self.lock = not self.lock

    def update_prolog(self, n_from, n_to, n_cost):
        app = App.get_running_app()
        self.toggle_lock()
        if (self._from != n_from or self._to != n_to or self._cost != n_cost):
            app.replace_flight_data(self._id, self._from, self._to, self._cost, n_to, n_from, n_cost)

    def delete(self):
        App.get_running_app().delete_flight(self._id, self._from, self._to, self._cost)

# Information-modification screen
class PathsScreen(Screen):
    _from = ObjectProperty(None)
    _to = ObjectProperty(None)
    text_0 = StringProperty('')
    text_1 = StringProperty('')
    text_2 = StringProperty('')
    text_3 = StringProperty('')

    # NoHomoApp._purge_str proxy (I'm lazy like that)
    def _sanitize(self, string, identifier = True):
        app = App.get_running_app()
        return app._purge_str(string, identifier)

    # query knowledge base on posible paths from (0 to 4 levels)
    def find_paths(self):
        app = App.get_running_app()

        # make sure fields represent valid input
        self._from.text = self._sanitize(self._from.text)
        self._to.text = self._sanitize(self._to.text)

        # shorthands
        _from = self._from.text
        _to = self._to.text

        # actually run the queries
        self.text_0 = app.query_paths(_from, _to, 0)
        self.text_1 = app.query_paths(_from, _to, 1)
        self.text_2 = app.query_paths(_from, _to, 2)
        self.text_3 = app.query_paths(_from, _to, 3)

# Main class
class NoHomoApp(App):
    prolog_file = StringProperty('knowledge_base.pl')
    prolog = Prolog()
    main_s = None

    def build(self):
        self.load_prolog()
        self.main_s = MainScreen()
        return self.main_s

    # Prolog stuff
    def load_prolog(self):
        self.prolog.consult(self.prolog_file)

    # load file contents to buffer
    def _get_file_content(self):
        pl = open(self.prolog_file)
        pl_str = pl.read()
        pl.close()
        return pl_str

    # write buffer to file
    def _write_file_content(self, pl_str):
        pl = open(self.prolog_file, 'w')
        pl.write(pl_str)
        pl.close()
        self._trigger_prolog_change()

    # trigger updates on this data's dependants
    def _trigger_prolog_change(self):
        self.load_prolog()
        self.main_s.ports_s.list.update_ports()
        self.main_s.flights_s.list.update_flights()

    # sanitize string to only contain lowercase letters
    def _purge_str(self, string = '0', identifier = True):
        string = str(string)
        string = string.lower()
        if identifier:
            string = re.sub(r'[^a-z0-9]', '', string)
            string = string.lstrip('0123456789')
        else:
            string = re.sub(r'[^a-z0-9.]', '', string)

        return string

    # replace instance of an airport's detail with new data
    def replace_airport_name(self, id = '', f = '', t = ''):
        id = self._purge_str(id)
        t = self._purge_str(t)

        if (id == '' or f == '' or t == ''):
            self._trigger_prolog_change()
            return

        pl_str = self._get_file_content()
        pl_str = re.sub('name\(%s, %s\)' % (id, f), 'name(%s, %s)' % (id, t), pl_str)
        self._write_file_content(pl_str)

    # create airport records above definition and detail tags
    def create_airport(self, id = '', name = ''):
        id = self._purge_str(id)
        name = self._purge_str(name)

        if (id == '' or name == ''):
            self._trigger_prolog_change()
            return

        pl_str = self._get_file_content()
        pl_str = re.sub('\% --po_def--', 'airport(%s).\n%% --po_def--' % id, pl_str)
        pl_str = re.sub('\% --po_det--', 'name(%s, %s).\n%% --po_det--' % (id, name), pl_str)
        self._write_file_content(pl_str)

    # remove instances of airport definition and detail
    def delete_airport(self, id = '', name = ''):
        id = self._purge_str(id)
        name = self._purge_str(name)

        if (id == '' or name == ''):
            self._trigger_prolog_change()
            return

        pl_str = self._get_file_content()
        pl_str = re.sub('airport\(%s\).\n' % id, '', pl_str)
        pl_str = re.sub('name\(%s, %s\).\n' % (id, name), '', pl_str)
        self._write_file_content(pl_str)

    # replace instance of an flight's detail with new data
    def replace_flight_data(self, _id = '', p_from = '', p_to = '', p_cost = '', _from = '', _to = '', _cost = ''):
        _id = self._purge_str(_id)
        _from = self._purge_str(_from)
        _to = self._purge_str(_to)
        _cost = self._purge_str(_cost, False)

        if (_id == '' or p_from == '' or p_to == '' or p_cost == '' or _from == '' or _to == '' or _cost == ''):
            self._trigger_prolog_change()
            return

        pl_str = self._get_file_content()
        pl_str = re.sub('path\(%s, %s, %s, %s\)' % (_id, p_from, p_to, p_cost), 'path(%s, %s, %s, %s)' % (_id, _from, _to, _cost), pl_str)
        self._write_file_content(pl_str)

    def create_flight(self, _id = '', _from = '', _to = '', _cost = ''):
        _id = self._purge_str(_id)
        _from = self._purge_str(_from)
        _to = self._purge_str(_to)
        _cost = self._purge_str(_cost, False)

        if (_id == '' or _from == '' or _to == '' or _cost == ''):
            self._trigger_prolog_change()
            return

        pl_str = self._get_file_content()
        pl_str = re.sub('\% --fl_def--', 'flight(%s).\n%% --fl_def--' % _id, pl_str)
        pl_str = re.sub('\% --fl_det--', 'path(%s, %s, %s, %s).\n%% --fl_det--' % (_id, _from, _to, _cost), pl_str)
        self._write_file_content(pl_str)

    # remove instances of flight definition and detail
    def delete_flight(self, _id = '', _from = '', _to = '', _cost = ''):
        _id = self._purge_str(_id)
        _from = self._purge_str(_from)
        _to = self._purge_str(_to)
        _cost = self._purge_str(_cost, False)

        if (_id == '' or _from == '' or _to == '' or _cost == ''):
            self._trigger_prolog_change()
            return

        pl_str = self._get_file_content()
        pl_str = re.sub('flight\(%s\).\n' % _id, '', pl_str)
        pl_str = re.sub('path\(%s, %s, %s, %s\).\n' % (_id, _from, _to, _cost), '', pl_str)
        self._write_file_content(pl_str)

    def query_paths(self, _from, _to, level = 0):
        try:
            s = ''
            if (level == 0):
                t = self.prolog.query('path_to_0(%s, %s, X, P).' % (_from, _to))
                for _t in t:
                    s = s + '[%s] -(%s)-> [%s] { $%s }\n' % (_from, _t['X'], _to, str(_t['P']))

            elif (level == 1):
                t = self.prolog.query('path_to_1(%s, %s, X, A, Y, P).' % (_from, _to))
                for _t in t:
                    s = s + '[%s] -(%s)-> [%s] -(%s)-> [%s] { $%s }\n' % (_from, _t['X'], _t['A'], _t['Y'], _to, str(_t['P']))

            elif (level == 2):
                t = self.prolog.query('path_to_2(%s, %s, X, A, Y, B, Z, P).' % (_from, _to))
                for _t in t:
                    s = s + '[%s] -(%s)-> [%s] -(%s)-> [%s] -(%s)-> [%s] { $%s }\n' % (_from, _t['X'], _t['A'], _t['Y'], _t['B'], _t['Z'], _to, str(_t['P']))

            elif (level == 3):
                t = self.prolog.query('path_to_3(%s, %s, W, A, X, B, Y, C, Z, P).' % (_from, _to))
                for _t in t:
                    s = s + '[%s] -(%s)-> [%s] -(%s)-> [%s] -(%s)-> [%s] { $%s }\n' % (_from, _t['W'], _t['A'], _t['X'], _t['B'], _t['Y'], _t['C'], _t['Z'], _to, str(_t['P']))

            if (s == ''):
                s = 'NO PATH'
        except:
            s = 'NO PATH (error)'
        finally:
            return s

# Main screen
class MainScreen(BoxLayout):
    manager = ObjectProperty(None)
    ports_s = ObjectProperty(None)
    flights_s = ObjectProperty(None)

    def switch_to(self, screen, button):
        if self.manager.current != screen:
            self.manager.current = screen

# Entry point
if __name__ == '__main__':
    NoHomoApp().run()

