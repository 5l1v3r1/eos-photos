from gi.repository import Gtk
from widgets.list_button import ListButton
import random


class PhotosLeftToolbar(Gtk.VBox):
    """
    The left filter selection toolbar for the photo app.
    """
    def __init__(self, images_path="", **kw):
        super(PhotosLeftToolbar, self).__init__(homogeneous=False, spacing=0, **kw)
        self._images_path = images_path

        self._categories = {}

        self._categories["borders"] = Category(
            images_path=self._images_path, label_name="BORDERS", category_name="borders",
            expanded_callback=lambda: self.change_category("borders"))

        self._categories["filters"] = Category(
            images_path=self._images_path, label_name="FILTROS", category_name="filters",
            expanded_callback=lambda: self.change_category("filters"))

        self._categories["text"] = Category(
            images_path=self._images_path, label_name="TEXTO", category_name="text",
            expanded_callback=lambda: self.change_category("text"))

        self._categories["transforms"] = Category(
            images_path=self._images_path, label_name="TRANSFORMS", category_name="transforms",
            expanded_callback=lambda: self.change_category("transforms"))

        self._filter_options = {}

        for category in self._categories.values():
            self.pack_start(category, expand=False, fill=True, padding=20)

        self.show_all()

    def set_filter_names(self, filter_names, default):
        map(self._add_filter_option, filter_names)
        self._filter_options[default].select()

    def _add_filter_option(self, filter_name):
        category = self._categories[random.choice(self._categories.keys())]
        path = "filter_thumbnails/filter_" + filter_name + ".jpg"
        option = ListButton(
            images_path=self._images_path, path=path, name="filter", label_name=filter_name,
            clicked_callback=lambda: self._presenter.on_filter_select(filter_name), vertical=True)
        self._filter_options[filter_name] = option

        category.add_to_scroll(option)

    def select_filter(self, filter_name):
        for name, option in self._filter_options.items():
            if not name == filter_name:
                option.deselect()

    def set_presenter(self, presenter):
        self._presenter = presenter

    def change_category(self, category_name):
        for name, category in self._categories.items():
            if not name == category_name:
                category.deselect()


class Category(Gtk.Expander):
    def __init__(self, images_path="", label_name="", category_name="", expanded_callback=None, **kw):
        super(Category, self).__init__(**kw)

        self._expanded_callback = expanded_callback
        self._images_path = images_path
        self._title_box = ListButton(
            images_path=self._images_path, path="Filter-icon.png", name="filter",
            label_name=label_name, vertical=False)
        self.set_label_widget(self._title_box)
        #self._title_allign = Gtk.HBox(homogeneous=False, spacing=0)
        #self._title_allign.pack_start(borders_title_box, expand=False, fill=False, padding=10)

        self._scroll_contents = Gtk.VBox(homogeneous=False, spacing=8)
        self._scroll_area = Gtk.ScrolledWindow(name="filters-scroll-area")
        self._scroll_area.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self._scroll_area.add_with_viewport(self._scroll_contents)
        self._scroll_area.set_vexpand(True)

        # self._separator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
        # self.add(self._separator)

        # self._drop_shadow = Gtk.Image.new_from_file(images_path + "Filter-mask-shadow.png")
        # self._drop_shadow.set_halign(Gtk.Align.CENTER)
        # self._drop_shadow.set_valign(Gtk.Align.START)
        # self._overlay = Gtk.Overlay()
        # self._overlay.add(self._scroll_area)
        # self._overlay.add_overlay(self._drop_shadow)

        self.connect('notify::expanded', self.expanded_cb)
        self.set_resize_toplevel(True)

    def expanded_cb(self, widget, event):
        if self.get_expanded():
            self._title_box.select()
            self.add(self._scroll_area)
            self._expanded_callback()
        else:
            self.remove(self._scroll_area)
            self._title_box.deselect()
        self.show_all()

    def select(self):
        self.set_expanded(True)

    def deselect(self):
        self.set_expanded(False)

    def is_selected(self):
        return self.get_expanded()

    def add_to_scroll(self, object_):
        align = Gtk.HBox(homogeneous=False, spacing=0)
        align.pack_start(object_, expand=False, fill=False, padding=30)
        self._scroll_contents.pack_start(align, expand=False, fill=False, padding=0)
        self.show_all()
