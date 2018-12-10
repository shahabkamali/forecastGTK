import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from fetch_data import get_24h_forecast_temps
from plotting import draw_chart_forcast
import cache_helper as ch


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Forecast Program")
        self.set_border_width(10)
        self.set_default_size(400, 500)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        # location label
        self.label = Gtk.Label("City:")

        # location combo
        self.combo = Gtk.ComboBoxText()
        self.combo.insert(0, "2643743", "London")
        self.combo.insert(1, "2950159", "Berlin")
        self.combo.insert(2, "2761369", "Vienna")
        self.combo.set_active(0)
        # add to box
        self.box.pack_start(self.label, True, True, 0)
        self.box.pack_start(self.combo, True, True, 0)

        # add button
        self.fetch_btn = Gtk.Button(label="Fetch Forecast")
        self.box.pack_start(self.fetch_btn, True, True, 0)
        self.fetch_btn.connect("clicked", self.fetch_btn_clicked)

        # add list box
        self.forecast_listbox = Gtk.ListBox()
        self.box.pack_start(self.forecast_listbox, True, True, 0)

        # chart btn
        self.chart_btn = Gtk.Button(label="show Chart")
        self.box.pack_start(self.chart_btn, True, True, 0)
        self.chart_btn.connect("clicked", self.draw_chart_clicked)

    def fetch_btn_clicked(self, widget):
        city_id = self.combo.get_active_id()
        cached_forecasts = ch.get(city_id)

        forecasts = get_24h_forecast_temps(city_id)
        if cached_forecasts:
            cached_forecasts = {**cached_forecasts, **forecasts}
        ch.set(city_id, cached_forecasts)

        list_items = ['temp: %s  time:%s' % (forecast['main']['cel_temp'],
                                            forecast['dt_txt']) for forecast in forecasts.values()]

        for w in self.forecast_listbox:
            self.forecast_listbox.remove(w)

        for item in list_items:
            self.listitem = Gtk.Label(item)
            self.forecast_listbox.add(self.listitem)

        self.forecast_listbox.show_all()

    def draw_chart_clicked(self, widget):
        city_id = self.combo.get_active_id()
        cached_forecasts = ch.get(city_id)
        if not cached_forecasts:
            return None

        val_list = [forecast['main']['cel_temp'] for forecast in cached_forecasts.values()]

        time_list = [forecast['dt_txt'] for forecast in cached_forecasts.values()]

        draw_chart_forcast(time_list, val_list)


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
