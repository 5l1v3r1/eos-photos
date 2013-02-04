from gi.repository import Gtk

from photos_top_toolbar import PhotosTopToolbar
from photos_left_toolbar import PhotosLeftToolbar
from photos_right_toolbar import PhotosRightToolbar
from photos_window import PhotosWindow
from photos_image_viewer import ImageViewer

class PhotosView(object):
    """
    The main view class for the photo application. Mainly just passes the
    presenter calls to the appropriate UI elements. PhotosWindow does the
    actual toplevel layout of the toolbars and central view.
    """
    def __init__(self):
        self._top_toolbar = PhotosTopToolbar()
        self._left_toolbar = PhotosLeftToolbar()
        self._right_toolbar = PhotosRightToolbar()
        self._image_viewer = ImageViewer()
        self._window = PhotosWindow(self._top_toolbar, self._left_toolbar, self._right_toolbar, self._image_viewer)

    def set_presenter(self, presenter):
        self._presenter = presenter
        self._top_toolbar.set_presenter(presenter)
        self._left_toolbar.set_presenter(presenter)
        self._right_toolbar.set_presenter(presenter)
        self._image_viewer.set_presenter(presenter)

    def get_window(self):
        return self._window

    def close_window(self):
        self._window.destroy()

    def minimize_window(self):
        self._window.iconify()

    def set_filter_names(self, filter_names, default):
        self._left_toolbar.set_filter_names(filter_names, default)

    def select_filter(self, filter_name):
        self._left_toolbar.select_filter(filter_name)

    def replace_image_from_file(self, image_name):
        self._image_viewer.load_from_file(image_name)

    def show_open_dialog(self):
        # Opens a dialog window where the user can choose an image file
        dialog = Gtk.FileChooserDialog ("Open Image", None, Gtk.FileChooserAction.OPEN);

        # Adds 'Cancel' and 'OK' buttons
        dialog.add_button(Gtk.STOCK_CANCEL, 0)
        dialog.add_button(Gtk.STOCK_OK, 1)

        # Sets default to 'OK'
        dialog.set_default_response(1)

        # Filters and displays files which can be opened by Gtk.Image
        filefilter = Gtk.FileFilter()
        filefilter.add_pixbuf_formats()
        dialog.set_filter(filefilter)

        if dialog.run() == 1:
            # Loads the image
            filename = dialog.get_filename()
            dialog.destroy()
            return filename
        else:
            dialog.destroy()
            return None

    def show_save_dialog(self):
        # Opens a dialog window where the user can choose an image file
        dialog = Gtk.FileChooserDialog ("Save Image", None, Gtk.FileChooserAction.SAVE);

        # Adds 'Cancel' and 'OK' buttons
        dialog.add_button(Gtk.STOCK_CANCEL, 0)
        dialog.add_button(Gtk.STOCK_OK, 1)

        # Sets default to 'OK'
        dialog.set_default_response(1)

        if dialog.run() == 1:
            # Loads the image
            filename = dialog.get_filename()
            dialog.destroy()
            return filename
        else:
            dialog.destroy()
            return None
