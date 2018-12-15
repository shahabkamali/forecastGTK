import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from fetch_data import get_24h_forecast_temps
from plotting import draw_chart_forcast
import cache_helper as ch



class Handler(Gtk.Window):

    def onDestroy(self, *args):
        Gtk.main_quit()

    def on_btn_fetch_clicked(self, widget):
        city_id = '2643743'#self.combo.get_active_id()
        cached_forecasts = ch.get(city_id)

        forecasts = get_24h_forecast_temps(city_id)
        if cached_forecasts:
            cached_forecasts = {**cached_forecasts, **forecasts}
        ch.set(city_id, cached_forecasts)

        list_items = ['temp: %s  time:%s' % (forecast['main']['cel_temp'],
                                            forecast['dt_txt']) for forecast in forecasts.values()]

        degree_label.set_text(str(list_items[0]))

    def draw_chart_clicked(self, widget):
        city_id = self.combo.get_active_id()
        cached_forecasts = ch.get(city_id)
        if not cached_forecasts:
            return None

        val_list = [forecast['main']['cel_temp'] for forecast in cached_forecasts.values()]

        time_list = [forecast['dt_txt'] for forecast in cached_forecasts.values()]

        draw_chart_forcast(time_list, val_list)

builder = Gtk.Builder()
builder.add_from_file("home.glade")
builder.connect_signals(Handler())

window = builder.get_object("win1")
degree_label = builder.get_object("degree1")
window.show_all()

Gtk.main()

