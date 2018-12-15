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

        i = 0
        #print (forecasts)
        for k, v in forecasts.items():
            print()
            degrees_dict[i].set_text(str(v['main']['cel_temp']) + ' C')
            time_dict[i].set_text(v['dt_txt'][12:16])
            icon_dict[i].set_from_file('icons/small/%s.png' % v['weather'][0]['icon'])
            if i == 0:
                icon_dict[i].set_from_file('icons/large/%s.png' % v['weather'][0]['icon'])
            i += 1
            if i > 8:
                break

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

# get element of ui designed
window = builder.get_object("win1")

# degree labels
degrees_dict = {
    0: builder.get_object("degree0"),
    1: builder.get_object("degree1"),
    2: builder.get_object("degree2"),
    3: builder.get_object("degree3"),
    4: builder.get_object("degree4"),
    5: builder.get_object("degree5"),
    6: builder.get_object("degree6"),
    7: builder.get_object("degree7"),
    8: builder.get_object("degree8"),
}

# icons
icon_dict = {
    0: builder.get_object("icon0"),
    1: builder.get_object("icon1"),
    2: builder.get_object("icon2"),
    3: builder.get_object("icon3"),
    4: builder.get_object("icon4"),
    5: builder.get_object("icon5"),
    6: builder.get_object("icon6"),
    7: builder.get_object("icon7"),
    8: builder.get_object("icon8"),
}

# time
time_dict = {
    0: builder.get_object("time0"),
    1: builder.get_object("time1"),
    2: builder.get_object("time2"),
    3: builder.get_object("time3"),
    4: builder.get_object("time4"),
    5: builder.get_object("time5"),
    6: builder.get_object("time6"),
    7: builder.get_object("time7"),
    8: builder.get_object("time8"),
}

####

window.show_all()

Gtk.main()

