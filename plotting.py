from gi.repository import Gtk

from matplotlib.figure import Figure
from numpy import arange, pi, random, linspace
import matplotlib.cm as cm
#Possibly this rendering backend is broken currently
#from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas


# Data for plotting
def draw_chart_forcast(time_arr, val_arr):
    # t = np.arange(0.0, 2.0, 0.01)
    # s = 1 + np.sin(2 * np.pi * t)
    #
    # fig, ax = plt.subplots()
    # ax.plot(t, s)
    #
    # ax.set(xlabel='time (s)', ylabel='voltage (mV)',
    #        title='About as simple as it gets, folks')
    # ax.grid()
    # plt.show()


    myfirstwindow = Gtk.Window()
    myfirstwindow.connect("delete-event", Gtk.main_quit)
    myfirstwindow.set_default_size(400, 400)

    fig = Figure(figsize=(5,5), dpi=100)
    ax = fig.add_subplot(111)

    ax.plot(time_arr, val_arr)

    sw = Gtk.ScrolledWindow()
    myfirstwindow.add(sw)

    canvas = FigureCanvas(fig)
    canvas.set_size_request(400,400)
    sw.add_with_viewport(canvas)
    myfirstwindow.show_all()
    Gtk.main()