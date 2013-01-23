import sys
from gi.repository import Gtk, Gdk, GLib

import gettext
gettext.install('endless_photos')

from photos_view import PhotosView
from photos_presenter import PhotosPresenter


class EndlessPhotos(Gtk.Application):
    """
    The photo application.

    This class ensures uniqueness (if a second photo application is started
    up, just switch to the first one instead.)

    Currently it is a Gtk.Application, but it should be an Endless.Application.
    """
    __gtype_name__ = 'EndlessPhotos'

    def __init__(self):
        Gtk.Application.__init__(self,
            application_id='com.endlessm.endless-photos')

    def do_startup(self):
        """
        Overrides the default Gio.Application.startup handler.

        This code is executed whenever the application starts up; we create the
        main window here.
        """
        # Chaining up is required
        Gtk.Application.do_startup(self)

        # Style CSS
        provider = Gtk.CssProvider()
        provider.load_from_path('../data/endless_photos.css')
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # The application has only one window; we create it here.
        # self._view = PhotosView()
        # self.add_window(self._view.get_window())
        # self._presenter = PhotosPresenter(view=self._window)
        self._window = Gtk.Window()
        self.add_window(self._window)
        self._window.show_all()

        # Run the main loop, to make sure the window is shown and therefore
        # seems responsive
        while Gtk.events_pending():
            Gtk.main_iteration()

    def do_activate(self):
        """
        Overrides the default Gio.Application.activate handler.

        It is required to override this in a subclass of Gio.Application, but it
        does not do anything right now.
        """
        pass

if __name__ == '__main__':
    app = EndlessPhotos()
    app.run(sys.argv)
