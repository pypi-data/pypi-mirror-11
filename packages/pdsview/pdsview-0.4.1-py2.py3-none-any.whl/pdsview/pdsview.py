#! /usr/bin/env python

import sys
import os
import logging
try:
    import label
except:
    from pdsview import label
from glob import glob
from ginga.qtw.QtHelp import QtGui, QtCore
from ginga.qtw.ImageViewCanvasQt import ImageViewCanvas
from ginga.BaseImage import BaseImage
from ginga.LayerImage import LayerImage
from planetaryimage import PDS3Image
import argparse
import math
import numpy

STD_FORMAT = '%(asctime)s | %(levelname)1.1s | %(filename)s:%(lineno)d (%(funcName)s) | %(message)s'
#
#
app = QtGui.QApplication.instance()
if not app:
    app = QtGui.QApplication(sys.argv)


class ImageStamp(BaseImage):
    """A ginga BaseImage object that will be displayed in PDSViewer.

    Parameters
    ----------
    filepath: string
        A file and its relative path from the current working directory


    Attributes
    ----------
    image_name : string
        The filename of the filepath
    pds_image : planetaryimage object
        A planetaryimage object
    label : array
        The images label in an array
    cuts : tuple (int, int)
        The min and max pixel value scaling
    sarr : numpy array
        The color map of the array in an array
    zoom : float
        Zoom level of the image
    rotation : float
        The degrees the image is rotated
    transforms : tuple (bool, bool, bool)
        Whether the image is flipped across the x-axis, y-axis, or x/y is
        switched
    not_been_displayed : bool
        Whether the image has been displayed already
    """
    def __init__(self, filepath, name, pds_image, data_np, metadata=None,
                 logger=None):
        BaseImage.__init__(self, data_np=data_np, metadata=metadata,
                           logger=logger)
        self.set_data(data_np)
        with open(filepath, 'rb') as f:
            label_array = []
            for lineno, line in enumerate(f):
                line = line.decode().rstrip()
                label_array.append(line)
                if line.strip() == 'END':
                    break
        self.data = data_np
        self.image_name = name
        self.file_name = os.path.basename(filepath)
        self.pds_image = pds_image
        self.label = label_array
        self.cuts = None
        self.sarr = None
        self.zoom = None
        self.rotation = None
        self.transforms = None
        self.not_been_displayed = True

    def __repr__(self):
        return self.file_name


class CompositeLayer(BaseImage):
    """BaseImage object to act as a composite layer"""
    def __init__(self, data_np, metadata=None, logger=None):
        BaseImage.__init__(self, data_np=data_np, metadata=metadata,
                           logger=logger)
        self.set_data(data_np)


class CompositeImage(BaseImage, LayerImage):
    """A rgb colored image"""
    def __init__(self, composite_layers, names=None, data_np=None,
                 metadata=None, logger=None):
        BaseImage.__init__(self, data_np=data_np, metadata=metadata,
                           logger=logger)
        LayerImage.__init__(self)

        idx = 0
        if not names:
            names = [image.image_name for image in composite_layers]
        for composite_layer, name in zip(composite_layers, names):
            self.insert_layer(
                image=composite_layer, idx=idx, name=name)
            idx += 1
        self.rgb_compose()


class ChannelsDialog(QtGui.QDialog):
    """A Dialog box to adjust the channels and alpha values"""
    def __init__(self, current_image, main_window):
        super(ChannelsDialog, self).__init__()

        self.main_window = main_window
        self.current_image = current_image
        images = main_window.image_set.images
        image_names = [image.image_name for sub in images for image in sub]
        self.image_names = image_names
        rgb_names = [band.image_name for band in main_window.rgb]

        # Create display of image names and highlight the current image/channel
        self.image_list = QtGui.QTreeWidget()
        self.image_list.setColumnCount(1)
        self.image_list.setHeaderLabel('Channels')
        self.items = []
        for image_name in image_names:
            self.items.append(QtGui.QTreeWidgetItem(None, image_name))
        for index in range(len(self.items)):
            self.items[index].setText(0, image_names[index])
        self.image_list.insertTopLevelItems(1, self.items)
        # Do not allow selection of images from list
        self.image_list.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        # highlight the current image
        self.current_index = image_names.index(current_image.image_name)
        current_item = self.items[self.current_index]
        self.image_list.setItemSelected(current_item, True)
        self.image_list.setIndentation(0)
        self.image_list.setFixedWidth(400)

        # Create rgb check-box to toggle display of color or single band image
        # This rgb check box connects with the rgb check box in the main window
        self.rgb_check_box = QtGui.QCheckBox("RGB")
        self.rgb_check_box.stateChanged.connect(self.check_rgb)

        # Create Red Menu
        # Create the red menu drop down box
        self.red_menu = QtGui.QComboBox()
        red_label = QtGui.QLabel("Red")
        red_box = QtGui.QHBoxLayout()
        R_index = image_names.index(rgb_names[0])
        self.add_text_to_menu(self.red_menu, image_names, R_index)
        self.create_color_layout(red_label, self.red_menu, red_box)
        # Create red alpha slider
        self.red_alpha_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        red_alpha_value = QtGui.QLabel()
        red_alpha_value_container = QtGui.QHBoxLayout()
        red_alpha_label = QtGui.QLabel('Red %')
        red_alpha_slider_container = QtGui.QHBoxLayout()
        red_alpha_container = QtGui.QVBoxLayout()
        self.create_slider_layout(
            self.red_alpha_slider, red_alpha_value, red_alpha_label,
            red_alpha_slider_container, red_alpha_value_container,
            red_alpha_container)

        # Create Green Menu
        # Create the green menu drop down box
        self.green_menu = QtGui.QComboBox()
        green_label = QtGui.QLabel("Green")
        green_box = QtGui.QHBoxLayout()
        G_index = image_names.index(rgb_names[1])
        self.add_text_to_menu(self.green_menu, image_names, G_index)
        self.create_color_layout(green_label, self.green_menu, green_box)
        # Create green alpha slider
        self.green_alpha_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        green_alpha_value = QtGui.QLabel()
        green_alpha_value_container = QtGui.QHBoxLayout()
        green_alpha_label = QtGui.QLabel('Green %')
        green_alpha_slider_container = QtGui.QHBoxLayout()
        green_alpha_container = QtGui.QVBoxLayout()
        self.create_slider_layout(
            self.green_alpha_slider, green_alpha_value, green_alpha_label,
            green_alpha_slider_container, green_alpha_value_container,
            green_alpha_container)

        # Create Blue Menu
        # Create the blue menu drop down box
        self.blue_menu = QtGui.QComboBox()
        blue_label = QtGui.QLabel("Blue")
        blue_box = QtGui.QHBoxLayout()
        B_index = image_names.index(rgb_names[2])
        self.add_text_to_menu(self.blue_menu, image_names, B_index)
        self.create_color_layout(blue_label, self.blue_menu, blue_box)
        # Create blue alpha slider
        self.blue_alpha_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        blue_alpha_value = QtGui.QLabel()
        blue_alpha_value_container = QtGui.QHBoxLayout()
        blue_alpha_label = QtGui.QLabel('Blue %')
        blue_alpha_slider_container = QtGui.QHBoxLayout()
        blue_alpha_container = QtGui.QVBoxLayout()
        self.create_slider_layout(
            self.blue_alpha_slider, blue_alpha_value, blue_alpha_label,
            blue_alpha_slider_container, blue_alpha_value_container,
            blue_alpha_container)

        # Create a close button
        self.close_button = QtGui.QPushButton('Close')
        self.close_button.clicked.connect(self.close_dialog)

        containers = [self.image_list, self.rgb_check_box, red_box,
                      red_alpha_container, green_box,
                      green_alpha_container, blue_box, blue_alpha_container,
                      self.close_button]

        # Set items created above in a grid layout
        self.layout = QtGui.QGridLayout()
        row = 0
        for container in containers:
            try:
                self.layout.addLayout(container, row, 0)
                self.layout.setAlignment(container, QtCore.Qt.AlignLeft)
            except:
                self.layout.addWidget(container, row, 0)
                self.layout.setAlignment(container, QtCore.Qt.AlignHCenter)
            row += 1

        self.setLayout(self.layout)
        self.update_menus_index()
        # Match the rgb check box state from the main window
        state = main_window.rgb_check_box.checkState()
        self.rgb_check_box.setCheckState(state)

    def check_rgb(self, state):
        """Displays the rgb image when checked, single band otherwise"""
        if state == QtCore.Qt.Checked:
            self.main_window.rgb_check_box.setCheckState(QtCore.Qt.Checked)
            self.create_composite_image()
        elif state == QtCore.Qt.Unchecked:
            self.main_window.rgb_check_box.setCheckState(QtCore.Qt.Unchecked)

    def create_slider_layout(self, slider, value, label, slider_container,
                             value_container, container):
        """Creates the alpha slider layout"""
        slider.setRange(0, 100)
        slider.setValue(100)
        value_container.addWidget(value)
        slider.valueChanged.connect(
            lambda: self.update_alpha_value(slider, value, label))
        slider.sliderReleased.connect(self.create_composite_image)
        slider.setFixedWidth(100)
        value.setNum(slider.value())
        label.setFixedWidth(label.sizeHint().width())
        value.setIndent((slider.width()/100) * slider.value() + label.width())
        slider_container.addWidget(label)
        slider_container.addWidget(slider)
        container.addLayout(value_container)
        container.addLayout(slider_container)
        slider_container.setAlignment(label, QtCore.Qt.AlignLeft)
        slider_container.setAlignment(slider, QtCore.Qt.AlignLeft)
        value_container.setAlignment(value, QtCore.Qt.AlignHCenter)
        container.setAlignment(slider_container, QtCore.Qt.AlignLeft)
        container.setAlignment(value_container, QtCore.Qt.AlignLeft)

    def update_alpha_value(self, slider, slider_value, label):
        """Displays the slider value over the alpha slider cursor"""
        slider_value.setNum(slider.value())
        slider_value.setIndent((
            slider.width()/100) * slider.value() + label.width())

    def get_alphas(self):
        """Returns the alpha values from each alpha slider"""
        red_alpha = self.red_alpha_slider.value()/100.
        green_alpha = self.green_alpha_slider.value()/100.
        blue_alpha = self.blue_alpha_slider.value()/100.
        alphas = [red_alpha, green_alpha, blue_alpha]
        return alphas

    def add_text_to_menu(self, menu, names, index):
        """Adds the images to the menu & sets the current item in the menu"""
        for name in names:
            menu.addItem(name)
        menu.setCurrentIndex(index)
        menu.activated[int].connect(self.create_composite_image)

    def update_menus_index(self):
        """Updates indices so menu can return to default item"""
        red = self.red_menu.currentIndex()
        green = self.green_menu.currentIndex()
        blue = self.blue_menu.currentIndex()
        self.indices = [red, green, blue]

    def update_menus_current_item(self):
        """Change each menus current item to match the main windows rgb list"""
        rgb_names = [band.image_name for band in self.main_window.rgb]
        indices = [self.image_names.index(rgb_name) for rgb_name in rgb_names]
        menus = [self.red_menu, self.green_menu, self.blue_menu]
        for index, menu in zip(indices, menus):
            menu.setCurrentIndex(index)

    def menus_current_text(self):
        """Returns the text of each menu"""
        red = self.red_menu.currentText()
        green = self.green_menu.currentText()
        blue = self.blue_menu.currentText()
        bands = [red, green, blue]
        return bands

    def create_composite_image(self, index=None):
        """Creates the rgb composite image and displays it"""
        if self.rgb_check_box.checkState() == QtCore.Qt.Unchecked:
            return
        bands = self.menus_current_text()
        alphas = self.get_alphas()
        file_dict = self.main_window.image_set.file_dict
        names = []
        composite_layers = []
        try:
            for band, alpha in zip(bands, alphas):
                layer = file_dict[band]
                layer_data = layer.data * alpha
                composite_layer = CompositeLayer(layer_data)
                names.append(layer.image_name)
                composite_layers.append(composite_layer)
            composite_image = CompositeImage(composite_layers, names)
            rgb_data = composite_image.get_data()
            self.current_image.set_data(rgb_data)
            self.update_menus_index()
            self.main_window.next_channel.setEnabled(False)
            self.main_window.previous_channel.setEnabled(False)
        except ValueError:
            menus = [self.red_menu, self.green_menu, self.blue_menu]
            for menu, index in zip(menus, self.indices):
                menu.setCurrentIndex(index)
            print("Images must be the same size")
            self.rgb_check_box.setCheckState(QtCore.Qt.Unchecked)

    def create_color_layout(self, label, menu, box):
        """Set the menu and its label next to each other"""
        box.addWidget(label)
        box.addWidget(menu)

    def change_image(self, previous_channel):
        """Change the menu and image list when the image is changed"""
        last_item = self.items[self.current_index + previous_channel]
        channel = self.main_window.image_set.channel
        current_image = self.main_window.image_set.current_image[channel]
        self.current_image = current_image
        self.current_index = self.image_names.index(current_image.image_name)
        current_item = self.items[self.current_index]
        self.image_list.setItemSelected(current_item, True)
        self.image_list.setItemSelected(last_item, False)
        self.update_menus_current_item()
        self.create_composite_image()

    def change_channel(self, previous_channel):
        """Move to the next image when next channel is clicked"""
        channel = self.main_window.image_set.channel
        last_item = self.items[self.current_index + previous_channel]
        current_item = self.items[self.current_index + channel]
        self.image_list.setItemSelected(current_item, True)
        self.image_list.setItemSelected(last_item, False)

    def close_dialog(self):
        """Close the dialog and save the position"""
        self.main_window.channels_window_is_open = False
        self.main_window.channels_window_pos = self.pos()
        self.hide()


class ImageSet(object):
    """A set of ginga images to be displayed and methods to control the images.

    Parameters
    ----------
    filepaths: list
        A list of filepaths to pass through ImageStamp

    Attribute
    ---------
    images : list
        A list of ginga images with attributes set in ImageStamp that can be
        displayed in PDSViewer
    current_image : ImageStamp object
        The currently displayed image
    current_image_index : int
        Index value of the current image
    file_dict : dictionary
        dictionary of images list, makes accessing images by name easier
    channel : int
        Which channel in the image the view should be in
    next_prev_enabled : bool
        Whether the next and previous buttons should be enabled
    """
    def __init__(self, filepaths):
        # Remove any duplicate filepaths and sort the list alpha-numerically.
        filepaths = sorted(list(set(filepaths)))

        # Create image objects with attributes set in ImageStamp
        # These objects contain the data ginga will use to display the image
        self.images = []
        self.file_dict = {}
        self.create_image_set(filepaths)
        self.current_image_index = 0
        self.channel = 0
        if self.images:
            self.current_image = self.images[self.current_image_index]
        else:
            self.current_image = None
        self.enable_next_previous()

    def create_image_set(self, filepaths):
        rgb = ['R', 'G', 'B']
        for filepath in filepaths:
            try:
                channels = []
                pds_image = PDS3Image.open(filepath)
                bands = pds_image.label['IMAGE']['BANDS']
                if bands == 3:
                    for n in range(bands):
                        name = os.path.basename(filepath) + '(%s)' % (rgb[n])
                        data = pds_image.data[:, :, n]
                        image = ImageStamp(
                            filepath=filepath, name=name, data_np=data,
                            pds_image=pds_image)
                        self.file_dict[image.image_name] = image
                        channels.append(image)
                    self.images.append(channels)
                else:
                    name = os.path.basename(filepath)
                    data = pds_image.data
                    image = ImageStamp(
                        filepath=filepath, name=name, data_np=data,
                        pds_image=pds_image)
                    self.images.append([image])
                    self.file_dict[image.image_name] = image
            except:
                pass

    def enable_next_previous(self):
        """Set whether the next and previous buttons are enabled."""
        if len(self.images) > 1:
            self.next_prev_enabled = True
        else:
            self.next_prev_enabled = False

    def next(self):
        """Display next image, loop to first image if past the last image"""
        try:
            self.current_image_index += 1
            self.current_image = self.images[self.current_image_index]
        except:
            self.current_image_index = 0
            self.current_image = self.images[self.current_image_index]
        self.channel = 0

    def previous(self):
        """Display previous image and loop to last image if past first image"""
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = len(self.images) - 1
        self.current_image = self.images[self.current_image_index]
        self.channel = 0

    def next_channel(self):
        """Change to the next channel, restart if at the end of the channels"""
        number_channels = len(self.current_image)
        if number_channels == 1:
            return
        self.channel += 1
        if self.channel == number_channels:
            self.channel = 0

    def previous_channel(self):
        """Change to the previous channel, go to the end if at the beginning"""
        number_channels = len(self.current_image)
        if number_channels == 1:
            return
        self.channel -= 1
        if self.channel < 0:
            self.channel = number_channels - 1

    def append(self, new_files, dipslay_first_new_image):
        """Append a new image to the images list if it is pds compatible"""
        self.create_image_set(new_files)
        if dipslay_first_new_image == len(self.images):
            return
        self.enable_next_previous()
        self.current_image_index = dipslay_first_new_image
        self.current_image = self.images[self.current_image_index]

    def ROI_data(self, left, bottom, right, top):
        """Calculate the data in the Region of Interest

        Parameters
        ----------
        left : float
            The x coordinate value of the left side of the Region of Interest
        bottom : float
            The y coordinate value of the bottom side of the Region of Interest
        right : float
            The x coordinate value of the right side of the Region of Interest
        bottom : float
            The y coordinate value of the top side of the Region of Interest

        Returns
        -------
        data : array
            The data within the Region of Interest

        """

        data = self.current_image[self.channel].cutout_data(
            math.ceil(left), math.ceil(bottom), math.ceil(right),
            math.ceil(top))
        return data

    def ROI_pixels(self, left, bottom, right, top):
        """Calculate the number of pixels in the Region of Interest

        Parameters
        ----------
        See ROI_data

        Returns
        -------
        pixels : int
            The number of pixels in the Region of Interest

        """

        pixels = (right - left) * (top - bottom)
        return pixels

    def ROI_std_dev(self, left=None, bottom=None, right=None, top=None,
                    data=None):
        """Calculate the standard deviation in the Region of Interest

        Note
        ----
        If data is not provided, the left, bottom, right, and top parameters
        must be provided. Otherwise it will result in a TypeError.

        Parameters
        ----------
        left : Optional[float]
            The x coordinate value of the left side of the Region of Interest
        bottom : Optional[float]
            The y coordinate value of the bottom side of the Region of Interest
        right : Optional[float]
            The x coordinate value of the right side of the Region of Interest
        bottom : Optional[float]
            The y coordinate value of the top side of the Region of Interest
        data : Optional[array]
            The data within the Region of Interest

        Returns
        -------
        std_dev : float
            The standard deviation of the pixels in the Region of Interest

        """

        if data is None:
            data = self.ROI_data(left, bottom, right, top)
        std_dev = round(numpy.std(data), 6)
        return std_dev

    def ROI_mean(self, left=None, bottom=None, right=None, top=None,
                 data=None):
        """Calculate the mean of the Region of Interest

        Parameters
        ----------
        See ROI_std_dev

        Note
        ----
        See ROI_std_dev

        Returns
        -------
        mean : float
            The mean pixel value of the Region of Interest

        """

        if data is None:
            data = self.ROI_data(left, bottom, right, top)
        mean = round(numpy.mean(data), 4)
        return mean

    def ROI_median(self, left=None, bottom=None, right=None, top=None,
                   data=None):
        """Find the median of the Region of Interest

        Parameters
        ----------
        See ROI_std_dev

        Note
        ----
        See ROI_std_dev

        Returns
        -------
        median : float
            The median pixel value of the Region of Interest

        """

        if data is None:
            data = self.ROI_data(left, bottom, right, top)
        median = numpy.median(data)
        return median

    def ROI_min(self, left=None, bottom=None, right=None, top=None, data=None):
        """Find the minimum pixel value of the Region of Interest

        Parameters
        ----------
        See ROI_std_dev

        Note
        ----
        See ROI_std_dev

        Returns
        -------
        minimum : float
            The minimum pixel value of the Region of Interest

        """

        if data is None:
            data = self.ROI_data(left, bottom, right, top)
        minimum = numpy.nanmin(data)
        return minimum

    def ROI_max(self, left=None, bottom=None, right=None, top=None, data=None):
        """Find the maximum pixel value of the Region of Interest

        Parameters
        ----------
        See ROI_std_dev

        Note
        ----
        See ROI_std_dev

        Returns
        -------
        maximum : float
            The maximum pixel value of the Region of Interest

        """

        if data is None:
            data = self.ROI_data(left, bottom, right, top)
        maximum = numpy.nanmax(data)
        return maximum


class PDSViewer(QtGui.QMainWindow):
    """A display of a single image with the option to view other images

    Parameters
    ----------
    image_set: list
        A list of ginga objects with attributes set in ImageStamp"""

    def __init__(self, image_set):
        super(PDSViewer, self).__init__()

        self.image_set = image_set
        self.rgb = []

        # Set the sub window names here. This implementation will help prevent
        # the main window from spawning duplicate children. Even if the
        # duplication prevention is not set up for a window, this will be a
        # handy reference list of windows(or dialogs in most cases) that can
        # be spawned out of this window.
        self._label_window = None
        self._label_window_pos = None
        self.channels_window = None
        self.channels_window_is_open = False
        self.channels_window_pos = None

        self.pds_view = ImageViewCanvas(render='widget')
        self.pds_view.set_autocut_params('zscale')
        self.pds_view.enable_autozoom('override')
        self.pds_view.enable_autocuts('override')
        self.pds_view.set_callback('drag-drop', self.drop_file)
        self.pds_view.set_bg(0.5, 0.5, 0.5)
        self.pds_view.ui_setActive(True)
        self.pds_view.get_bindings().enable_all(True)
        # Activate left mouse click to display values
        self.pds_view.set_callback('cursor-down', self.display_values)
        # Activate click and drag to update values
        self.pds_view.set_callback('cursor-move', self.display_values)
        self.pds_view.set_callback('draw-down', self.start_ROI)
        self.pds_view.set_callback('draw-up', self.stop_ROI)
        self.pds_view.enable_draw(True)
        self.pds_view.set_drawtype('rectangle')

        pdsview_widget = self.pds_view.get_widget()
        pdsview_widget.resize(768, 768)

        vertical_align = QtGui.QVBoxLayout()
        vertical_align.setContentsMargins(QtCore.QMargins(2, 2, 2, 2))
        vertical_align.setSpacing(1)
        vertical_align.addWidget(pdsview_widget, stretch=1)

        horizontal_align = QtGui.QHBoxLayout()
        horizontal_align.setContentsMargins(QtCore.QMargins(4, 2, 4, 2))

        # self.open_label is need as an attribute to determine whether the user
        # should be able to open the label window. The other side of this
        # toggle is found in load_file().
        open_file = QtGui.QPushButton("Open File")
        open_file.clicked.connect(self.open_file)
        self.next_image = QtGui.QPushButton("Next")
        self.next_image.clicked.connect(
            lambda: self.display_image(next_image=True))
        self.next_image.setEnabled(image_set.next_prev_enabled)
        self.previous_image = QtGui.QPushButton("Previous")
        self.previous_image.clicked.connect(
            lambda: self.display_image(previous_image=True))
        self.previous_image.setEnabled(image_set.next_prev_enabled)
        self.open_label = QtGui.QPushButton("Label")
        self.open_label.clicked.connect(self.display_label)
        quit_button = QtGui.QPushButton("Quit")
        quit_button.clicked.connect(self.quit)
        self.rgb_check_box = QtGui.QCheckBox("RGB")
        self.rgb_check_box.stateChanged.connect(self.switch_rgb)
        self.next_channel = QtGui.QPushButton('CH +')
        self.next_channel.clicked.connect(
            lambda: self.display_image(next_channel=True))
        self.previous_channel = QtGui.QPushButton('CH -')
        self.previous_channel.clicked.connect(
            lambda: self.display_image(previous_channel=True))
        self.restore_defaults = QtGui.QPushButton("Restore Defaults")
        self.restore_defaults.clicked.connect(self.restore)
        self.channels_button = QtGui.QPushButton("Channels")
        self.channels_button.clicked.connect(self.channels_dialog)
        # Set Text so the size of the boxes are at an appropriate size
        self.x_value = QtGui.QLabel('X: #####')
        self.y_value = QtGui.QLabel('Y: #####')
        self.pixel_value = QtGui.QLabel('R: ######, G: ###### B: ######')

        horizontal_align.addStretch(1)
        for button in (
                self.x_value, self.y_value, self.pixel_value,
                self.previous_image, self.next_image, open_file,
                self.open_label, quit_button):
            horizontal_align.addWidget(button, stretch=0)
        # Region of Interest boxes
        self.pixels = QtGui.QLabel('#Pixels: #######')
        self.std_dev = QtGui.QLabel(
            'Std Dev: R: ######### G: ######### B: #########')
        self.mean = QtGui.QLabel(
            'Mean: R: ######## G: ######## B: ########')
        self.median = QtGui.QLabel(
            'Median: R: ######## G: ######## B: ########')
        self.min = QtGui.QLabel('Min: R: ### G: ### B: ###')
        self.max = QtGui.QLabel('Max: R: ### G: ### B: ###')
        # Set format for each information box to be the same
        for info_box in (self.x_value, self.y_value, self.pixel_value,
                         self.pixels, self.std_dev, self.mean, self.median,
                         self.min, self.max):
            info_box.setFrameShape(QtGui.QFrame.Panel)
            info_box.setFrameShadow(QtGui.QFrame.Sunken)
            info_box.setLineWidth(3)
            info_box.setMidLineWidth(1)
            info_box.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)
            info_box.setMinimumSize(info_box.sizeHint())
            info_box.setMaximumSize(info_box.sizeHint())

        horizontal_align_2 = QtGui.QHBoxLayout()
        horizontal_align_2.setContentsMargins(QtCore.QMargins(4, 2, 4, 2))
        for roi in (self.pixels, self.std_dev, self.mean):
            horizontal_align_2.addWidget(roi)
        horizontal_align_3 = QtGui.QHBoxLayout()
        horizontal_align_3.setContentsMargins(QtCore.QMargins(4, 2, 4, 2))
        for roi in (self.median, self.min, self.max, self.rgb_check_box):
            horizontal_align_3.addWidget(roi)
        horizontal_align_4 = QtGui.QHBoxLayout()
        horizontal_align_4.setContentsMargins(QtCore.QMargins(4, 2, 4, 2))
        for channel in (self.restore_defaults, self.previous_channel,
                        self.next_channel, self.channels_button):
            horizontal_align_4.addWidget(channel)

        hw = QtGui.QWidget()
        hw.setLayout(horizontal_align)
        hw_2 = QtGui.QWidget()
        hw_2.setLayout(horizontal_align_2)
        hw_3 = QtGui.QWidget()
        hw_3.setLayout(horizontal_align_3)
        hw_4 = QtGui.QWidget()
        hw_4.setLayout(horizontal_align_4)
        vertical_align.addWidget(hw, stretch=0)
        vertical_align.addWidget(hw_2, stretch=0)
        vertical_align.addWidget(hw_3, stretch=0)
        vertical_align.addWidget(hw_4, stretch=0)
        self.vertical_align = vertical_align
        self.horizontal_align = horizontal_align
        self.pdsview_widget = pdsview_widget

        vw = QtGui.QWidget()
        self.setCentralWidget(vw)
        vw.setLayout(vertical_align)

        if self.image_set.current_image:
            self.display_image()

    def switch_rgb(self, state):
        """Display rgb image when rgb box is checked, single band otherwise"""
        current_image = self.image_set.current_image
        index = self.image_set.channel
        if state == QtCore.Qt.Checked:
            if self.channels_window:
                self.channels_window.rgb_check_box.setCheckState(
                    QtCore.Qt.Checked)
            else:
                self.update_rgb()
                try:
                    datas = [band.data for band in self.rgb]
                    composite_layers = [CompositeLayer(data) for data in datas]
                    names = [band.image_name for band in self.rgb]
                    composite = CompositeImage(composite_layers, names)
                    rgb_data = composite.get_data()
                    current_image[index].set_data(rgb_data)
                    self.next_channel.setEnabled(False)
                    self.previous_channel.setEnabled(False)
                except ValueError:
                    print("Images must be the same size")
                    print("Use the channels button to select the bands")
                    self.rgb_check_box.setCheckState(QtCore.Qt.Unchecked)
        elif state == QtCore.Qt.Unchecked:
            self.update_rgb()
            current_image[index].set_data(current_image[index].data)
            self.next_channel.setEnabled(True)
            self.previous_channel.setEnabled(True)
            if self.channels_window:
                self.channels_window.rgb_check_box.setCheckState(
                    QtCore.Qt.Unchecked)
        if len(self.pds_view.objects) >= 1:
            self.stop_ROI(self.pds_view, None, None, None)

    def update_rgb(self):
        """Update the rgb list to have the 3 channels or the next 3 images"""
        self.rgb = []
        current_image = self.image_set.current_image
        if len(current_image) < 3:
            image_index = self.image_set.current_image_index
            while len(self.rgb) < 3:
                for image in self.image_set.images[image_index]:
                    self.rgb.append(image)
                    if len(self.rgb) == 3:
                        break
                image_index += 1
                if image_index == len(self.image_set.images):
                    image_index = 0
        else:
            for band in current_image:
                self.rgb.append(band)

    def display_values(self, pds_view, button, data_x, data_y):
        "Display the x, y, and pixel value when the mouse is pressed and moved"
        current_image = self.image_set.current_image[self.image_set.channel]
        try:
            # When clicking inside the image
            image = pds_view.get_image()
            x = round(data_x, 0)
            y = round(data_y, 0)
            value = image.get_data_xy(x, y)
            self.x_value.setText('X: %.0f' % (x))
            self.y_value.setText('Y: %.0f' % (y))
            if current_image.ndim == 3:
                # Show different band values for 3 band images
                R = str(round(value[0], 3))
                G = str(round(value[1], 3))
                B = str(round(value[2], 3))
                self.pixel_value.setText('R: %s G: %s B: %s' % (R, G, B))
            elif current_image.ndim == 2:
                # Show single pixel value for 2 band images
                self.pixel_value.setText('Value: %s' % (str(round(value, 3))))
        except:
            # When clicking outside the image
            x = pds_view.get_last_data_xy()[0]
            y = pds_view.get_last_data_xy()[1]
            self.x_value.setText('X: %.0f' % (x))
            self.y_value.setText('Y: %.0f' % (y))
            if current_image.ndim == 3:
                self.pixel_value.setText('R: 0 G: 0 B: 0')
            elif current_image.ndim == 2:
                self.pixel_value.setText('Value: 0')

    def display_label(self):
        """Display the label over the image"""
        # Utilizing the sub window variables to check if the label window has
        # been opened before. If not, the window is initialized.
        if self._label_window is None:
            self._label_window = label.LabelView(self)
        self._label_window.is_open = True
        self._label_window.show()
        self._label_window.activateWindow()

    def open_file(self):
        """Open a new image file from a file explorer"""
        file_name = QtGui.QFileDialog()
        file_name.setFileMode(QtGui.QFileDialog.ExistingFiles)
        new_files = file_name.getOpenFileNames(self)[0]
        if new_files:
            if self.image_set.current_image:
                self.save_parameters()
            first_new_image = len(self.image_set.images)
            self.image_set.append(new_files, first_new_image)
            # If there are no new images, don't continue
            if first_new_image == len(self.image_set.images):
                print ("The image(s) chosen are not PDS compatible")
                return
            self.next_image.setEnabled(self.image_set.next_prev_enabled)
            self.previous_image.setEnabled(self.image_set.next_prev_enabled)
            self.display_image()
        else:
            # integrate with logger
            print("No file selected!")
            return

    def channels_dialog(self):
        """Display the channels dialog box"""
        current_image = self.image_set.current_image[self.image_set.channel]
        if not self.channels_window:
            self.channels_window = ChannelsDialog(current_image, self)
        self.channels_window_is_open = True
        if self.channels_window_pos:
            self.channels_window.move(self.channels_window_pos)
        self.channels_window.show()

    def display_image(self, next_image=False, previous_image=False,
                      next_channel=False, previous_channel=False):
        """Display the current image and/or label"""
        last_channel = self.image_set.channel

        # Switch image and save parameters of previous image
        if next_image:
            self.save_parameters()
            self.image_set.next()
            if not self.channels_window_is_open:
                self.channels_window = None
        elif previous_image:
            self.save_parameters()
            self.image_set.previous()
            if not self.channels_window_is_open:
                self.channels_window = None
        elif next_channel:
            self.save_parameters()
            self.image_set.next_channel()
            if self.channels_window:
                self.channels_window.change_channel(last_channel)
        elif previous_channel:
            self.save_parameters()
            self.image_set.previous_channel()
            if self.channels_window:
                self.channels_window.change_channel(last_channel)

        current_image = self.image_set.current_image[self.image_set.channel]

        state = self.rgb_check_box.checkState()
        self.switch_rgb(state)

        # Update the channels window with the new image
        if next_image or previous_image:
            if self.channels_window:
                self.update_rgb()
                self.channels_window.change_image(last_channel)

        # Disable the next/previous channels buttons when there are no channels
        if len(self.image_set.current_image) < 3:
            self.next_channel.setEnabled(False)
            self.previous_channel.setEnabled(False)

        # Display image in viewer
        if current_image.not_been_displayed:
            # If it is the first time the image is shown, show with defaults
            self.pds_view.set_image(current_image)
            self.restore()
            self.pds_view.delayed_redraw()
            current_image.not_been_displayed = False
        else:
            # Set the current image with the images last parameters
            self.pds_view.set_image(current_image)
            self.apply_parameters(current_image, self.pds_view)
            self.pds_view.delayed_redraw()

        # Update the value box when the channel changes
        if next_channel or previous_channel:
            try:
                data_x = int(self.x_value.text()[3:])
                data_y = int(self.y_value.text()[3:])
                self.display_values(self.pds_view, None, data_x, data_y)
            except ValueError:
                pass
        else:
            # Reset the value boxes
            self.x_value.setText('X: ????')
            self.y_value.setText('Y: ????')
            if current_image.ndim == 3:
                self.pixel_value.setText('R: ???? G: ???? B: ????')
            elif current_image.ndim == 2:
                self.pixel_value.setText('Value: ????')

        if len(self.pds_view.objects) > 1:
            self.stop_ROI(self.pds_view, None, None, None)
            self.pds_view.update_canvas()
        else:
            self.set_ROI_text(
                0, 0, current_image.width, current_image.height)

        # Update label
        self.image_label = current_image.label

        # This checks to see if the label window exists and is open. If so,
        # this resets the label field so that the label being displayed is the
        # label for the current product. The label does not reset its position.
        if self._label_window is not None:
            pos = self._label_window.pos()
            label_text = '\n'.join(self.image_label)
            self._label_window.label_contents.setText(label_text)
            if self._label_window.is_open:
                self._label_window.cancel()
                self._label_window.move(pos)
                self._label_window.show()
                self._label_window.is_open = True
                self._label_window.activateWindow()

        self.setWindowTitle(current_image.image_name)

    def save_parameters(self):
        """Save the view parameters on the image"""
        last_image = self.image_set.current_image[self.image_set.channel]
        last_image.sarr = self.pds_view.get_rgbmap().get_sarr()
        last_image.zoom = self.pds_view.get_zoom()
        last_image.rotation = self.pds_view.get_rotation()
        last_image.transforms = self.pds_view.get_transforms()
        last_image.cuts = self.pds_view.get_cut_levels()

    def apply_parameters(self, image, view):
        """Display image with the images parameters"""
        if image.sarr is None:
            pass
        else:
            view.get_rgbmap().set_sarr(image.sarr)
        if image.zoom is None:
            pass
        else:
            view.zoom_to(image.zoom)
        if image.rotation is None:
            pass
        else:
            view.rotate(image.rotation)
        if image.transforms is None:
            pass
        else:
            flip_x = image.transforms[0]
            flip_y = image.transforms[1]
            switch_xy = image.transforms[2]
            view.transform(flip_x, flip_y, switch_xy)
        if image.cuts is None:
            pass
        else:
            loval, hival = image.cuts
            view.cut_levels(loval, hival, True)

    def restore(self):
        """Restore image to the default settings"""
        self.pds_view.get_rgbmap().reset_sarr()
        self.pds_view.enable_autocuts('on')
        self.pds_view.auto_levels()
        self.pds_view.enable_autocuts('override')
        self.pds_view.rotate(0.0)
        # The default transform/rotation of the image will be image specific so
        # transform bools will change in the future
        self.pds_view.transform(False, False, False)
        self.pds_view.zoom_fit()

    def start_ROI(self, pds_view, button, data_x, data_y):
        """Ensure only one Region of Interest (ROI) exists at a time

        Note
        ----
        This method is called when the right mouse button is pressed. Even
        though the arguments are not used, they are necessary to catch the
        right mouse button press event.

        Parameters
        ----------
        pds_view : ImageViewCanvas object
            The view that displays the image
        button : Qt.RightButton
            The right mouse button
        data_x : float
            The x-value of the location of the right button
        data_y : float
            The y-value of the location of the right button

        """

        if len(pds_view.objects) > 1:
            self.delete_ROI()

    def stop_ROI(self, pds_view, button, data_x, data_y):
        """Create a Region of Interest (ROI)

        When drawing stops (release of the right mouse button), the ROI border
        snaps to inclusive pixel (see top_right_pixel_snap and
        bottom_left_pixel_snap). The ROI's information is set as an attributes
        of the current image (see calculate_ROI_info).

        Note
        ----
        This method is called when the right mouse button is released. Even
        though only the pds_view argument is used, they are all necessary to
        catch the right mouse button release event.

        Parameters
        ----------
        See start_ROI parameters

        """

        # If there are no draw objects, stop
        current_image = self.image_set.current_image[self.image_set.channel]
        if len(pds_view.objects) == 1:
            self.set_ROI_text(0, 0, current_image.width, current_image.height)
            return

        draw_obj = pds_view.objects[1]

        # Retrieve the left, right, top, & bottom x and y values
        roi = self.left_right_bottom_top(
            draw_obj.x1, draw_obj.x2, draw_obj.y1, draw_obj.y2)
        left_x, right_x, bot_y, top_y, x2_is_right, y2_is_top = roi

        # Single right click deletes any ROI & sets the whole image as the ROI
        if left_x == right_x and bot_y == top_y:
            self.set_ROI_text(0, 0, current_image.width, current_image.height)
            self.delete_ROI()
            return

        # Determine if the ROI is outside the image.
        max_height = current_image.height
        max_width = current_image.width
        top_y, top_in_image = self.top_right_pixel_snap(top_y, max_height)
        bot_y, bot_in_image = self.bottom_left_pixel_snap(bot_y, max_height)
        right_x, right_in_image = self.top_right_pixel_snap(right_x, max_width)
        left_x, left_in_image = self.bottom_left_pixel_snap(left_x, max_width)

        # If the entire ROI is outside the ROI, delete the ROI and set the ROI
        # to the whole image
        if(not left_in_image or not right_in_image or not top_in_image
           or not bot_in_image):
            self.set_ROI_text(0, 0, current_image.width, current_image.height)
            self.delete_ROI()
            return

        # Snap the ROI to the edge of the image if it is outside the image
        if y2_is_top:
            draw_obj.y2 = top_y
            draw_obj.y1 = bot_y
        else:
            draw_obj.y1 = top_y
            draw_obj.y2 = bot_y
        if x2_is_right:
            draw_obj.x2 = right_x
            draw_obj.x1 = left_x
        else:
            draw_obj.x1 = right_x
            draw_obj.x2 = left_x

        # Calculate the ROI information

        self.set_ROI_text(left_x, bot_y, right_x, top_y)

    def top_right_pixel_snap(self, ROI_side, image_edge):
        """Snaps the top or right side of the ROI to the inclusive pixel

        Parameters
        ----------
        ROI_side : float
            Either the ROI's top-y or right-x value
        image_edge : float
            The top or right edge of the image

        Returns
        -------
        ROI_side : float
            The x or y value of the right or top ROI side respectively
        side_in_image : bool
            True if the side is in the image, False otherwise

        """

        # If the top/right ROI edge is outside the image, reset the top/right
        # ROI side value to the edge
        if ROI_side > image_edge:
            ROI_side = image_edge + .5
            side_in_image = True

        # If the right side is to the left of the image or the top side is
        # below the image, then the entire ROI is outside the image
        elif ROI_side < 0.0:
            side_in_image = False

        # If the top/right ROI values is inside the image, snap it the edge
        # of the inclusive pixel. If the value is already on the edge, pass
        else:
            if ROI_side - int(ROI_side) == .5:
                pass
            else:
                ROI_side = round(ROI_side) + .5
            side_in_image = True
        return (ROI_side, side_in_image)

    def bottom_left_pixel_snap(self, ROI_side, image_edge):
        """Snaps the bottom or left side of the ROI to the inclusive pixel

        Parameters
        ----------

        ROI_side : float
            Either the ROI's bottom-y or left-x value
        image_edge : float
            The top or right edge of the image

        Returns
        -------
        ROI_side : float
            The x or y value of the left or bottom ROI side respectively
        side_in_image : bool
            True if the side is in the image, False otherwise

        """

        # If the bottom/left ROI edge is outside the image, reset the
        # bottom/left ROI side value to the bottom/left edge (-0.5)
        if ROI_side < 0.0:
            ROI_side = -0.5
            side_in_image = True

        # If the left side is to the right of the image or the bottom side is
        # above the image, then the entire ROI is outside the image
        elif ROI_side > image_edge:
            side_in_image = False

        # If the bottom/left ROI values is inside the image, snap it the edge
        # of the inclusive pixel. If the value is already on the edge, pass
        else:
            if ROI_side - int(ROI_side) == .5:
                pass
            else:
                ROI_side = round(ROI_side) - 0.5
            side_in_image = True
        return (ROI_side, side_in_image)

    def left_right_bottom_top(self, x1, x2, y1, y2):
        """Determines the values for the left, right, bottom, and top vertices

        Parameters
        ----------
        x1 : float
            The x-value of where the right cursor was clicked
        x2 : float
            The x-value of where the right cursor was released
        y1 : float
            The y-value of where the right cursor was clicked
        y2 : float
            The y-value of where the right cursor was released

        Returns
        -------
        left_x : float
            The x-value of the left side of the ROI
        right_x : float
            The x-value of the right side of the ROI
        bot_y : float
            The y-value of the bottom side of the ROI
        top_y : float
            The y-value of the top side of the ROI
        x2_is_right : bool
            True if the x2 input is the right side of the ROI, False otherwise
        y2_is_top : bool
            True if the y2 input is the top side of the ROI, False otherwise

        """

        if x2 > x1:
            right_x = x2
            left_x = x1
            x2_is_right = True
        else:
            right_x = x1
            left_x = x2
            x2_is_right = False
        if y2 > y1:
            top_y = y2
            bot_y = y1
            y2_is_top = True
        else:
            top_y = y1
            bot_y = y2
            y2_is_top = False
        return (left_x, right_x, bot_y, top_y, x2_is_right, y2_is_top)

    def delete_ROI(self):
        """Deletes the Region of Interest"""
        try:
            self.pds_view.deleteObject(self.pds_view.objects[1])
        except:
            return

    def set_ROI_text(self, left, bottom, right, top):
        """Set the text of the ROI information boxes

        When the image has three bands (colored), the ROI value boxes will
        display the values for each band.

        Parameters
        ----------
        left : float
            The x coordinate value of the left side of the ROI
        bottom : float
            The y coordinate value of the bottom side of the ROI
        right : float
            The x coordinate value of the right side of the ROI
        bottom : float
            The y coordinate value of the top side of the ROI

        """

        data = self.image_set.ROI_data(
            left, bottom, right, top)
        # Calculate the number of pixels in the ROI
        ROI_pixels = self.image_set.ROI_pixels(left, bottom, right, top)
        self.pixels.setText('#Pixels: %s' % (str(ROI_pixels)))
        if data.ndim == 2:
            # 2 band image is a gray scale image
            self.set_ROI_gray_text(data)
        elif data.ndim == 3:
            # Three band image is a RGB colored image
            try:
                self.set_ROI_RGB_text(data)
            except:
                # If the ROI does not contain values for each band, treat the
                # ROI like a gray scale image
                self.set_ROI_gray_text(data)

    def set_ROI_gray_text(self, data):
        """Set the values for the ROI in the text boxes for a gray image

        Parameters
        ----------
        data : array
            The data from the Region of Interest

        """

        ROI_std_dev = self.image_set.ROI_std_dev(data=data)
        ROI_mean = self.image_set.ROI_mean(data=data)
        ROI_median = self.image_set.ROI_median(data=data)
        ROI_min = self.image_set.ROI_min(data=data)
        ROI_max = self.image_set.ROI_max(data=data)
        self.std_dev.setText('Std Dev: %s' % (str(ROI_std_dev)))
        self.mean.setText('Mean: %s' % (str(ROI_mean)))
        self.median.setText('Median: %s' % (str(ROI_median)))
        self.min.setText('Min: %s' % (str(ROI_min)))
        self.max.setText('Max: %s' % (str(ROI_max)))

    def set_ROI_RGB_text(self, data):
        """Set the values for the ROI in the text boxes for a RGB image

        Parameters
        ----------
        data : array
            The data from the Region of Interest

        """

        calc = self.image_set
        ROI_stdev = [calc.ROI_std_dev(data=data[:, :, n]) for n in range(3)]
        ROI_mean = [calc.ROI_mean(data=data[:, :, n]) for n in range(3)]
        ROI_median = [calc.ROI_median(data=data[:, :, n]) for n in range(3)]
        ROI_max = [int(calc.ROI_max(data=data[:, :, n])) for n in range(3)]
        ROI_min = [int(calc.ROI_min(data=data[:, :, n])) for n in range(3)]
        for item in ROI_stdev, ROI_mean, ROI_median, ROI_min, ROI_max:
            str(item)
        self.std_dev.setText(
            'Std Dev: R: %s G: %s B: %s' % (ROI_stdev[0], ROI_stdev[1],
                                            ROI_stdev[2]))
        self.mean.setText(
            'Mean: R: %s G: %s B: %s' % (ROI_mean[0], ROI_mean[1],
                                         ROI_mean[2]))
        self.median.setText(
            'Median: R: %s G: %s B: %s' % (ROI_median[0], ROI_median[1],
                                           ROI_median[2]))
        self.max.setText(
            'Max: R: %s G: %s B: %s' % (ROI_max[0], ROI_max[1],
                                        ROI_max[2]))
        self.min.setText(
            'Min: R: %s G: %s B: %s' % (ROI_min[0], ROI_min[1],
                                        ROI_min[2]))

    def drop_file(self, pdsimage, paths):
        """This function is not yet supported"""
        # file_name = paths[0]
        # self.load_file(file_name)
        pass

    def quit(self, *args):
        """Close pdsview"""
        if self._label_window is not None:
            self._label_window.cancel()
        if self.channels_window:
            self.channels_window.hide()
        self.close()


def pdsview(inlist=None):
    """Run pdsview from python shell or command line with arguments

    Parameters
    ----------
    inlist : list
        A list of file names/paths to display in the pdsview

    Examples
    --------

    From the command line:

    To view all images from current directory

    pdsview

    To view all images in a different directory

    pdsview path/to/different/directory/

    This is the same as:

    pdsview path/to/different/directory/*

    To view a specific image or types of images

    pdsview 1p*img

    To view images from multiple directories:

    pdsview * path/to/other/directory/

    From the (i)python command line:

    >>> from pdsview.pdsview import pdsview
    >>> pdsview()
    Displays all of the images from current directory
    >>> pdsview('path/to/different/directory')
    Displays all of the images in the different directory
    >>> pdsview ('1p*img')
    Displays all of the images that follow the glob pattern
    >>> pdsview ('a1.img, b*.img, example/path/x*img')
    You can display multiple images, globs, and paths in one window by
    separating each item by a command
    >>> pdsview (['a1.img, b3.img, c1.img, d*img'])
    You can also pass in a list of files/globs
    """
    files = []
    if isinstance(inlist, list):
        if inlist:
            for item in inlist:
                files += arg_parser(item)
        else:
            files = glob('*')
    elif isinstance(inlist, str):
        names = inlist.split(',')
        for name in names:
            files = files + arg_parser(name.strip())
    elif inlist is None:
        files = glob('*')

    image_set = ImageSet(files)
    w = PDSViewer(image_set)
    w.resize(780, 770)
    w.show()
    app.setActiveWindow(w)
    sys.exit(app.exec_())


def arg_parser(args):
    if os.path.isdir(args):
        files = glob(os.path.join('%s' % (args), '*'))
    elif args:
        files = glob(args)
    else:
        files = glob('*')
    return files


def cli():
    """Give pdsview ability to run from command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file', nargs='*',
        help="Input filename or glob for files with certain extensions"
        )
    args = parser.parse_args()
    pdsview(args.file)
