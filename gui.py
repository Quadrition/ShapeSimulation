from PyQt4.QtGui import QWidget, QGridLayout, QPushButton, QLabel, QSpinBox, QComboBox
from PyQt4.QtCore import QObject, SIGNAL
import globals


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        self.setWindowTitle('Parameters')

        self.fps_label = QLabel('FPS')
        self.fps_spinbox = QSpinBox()
        self.fps_spinbox.setRange(1, 1000)
        self.fps_spinbox.setSingleStep(1)
        self.fps_spinbox.setValue(globals.FPS)

        self.force_label = QLabel('Key force')
        self.force_spinbox = QSpinBox()
        self.force_spinbox.setRange(1, 1000)
        self.force_spinbox.setSingleStep(1)
        self.force_spinbox.setValue(globals.KEY_FORCE)

        self.friction_label = QLabel('Friction')
        self.friction_spinbox = QSpinBox()
        self.friction_spinbox.setRange(1, 1000)
        self.friction_spinbox.setSingleStep(1)
        self.friction_spinbox.setValue(globals.FRICTION)

        self.shape_type_label = QLabel('New shape type')
        self.shape_type_combobox = QComboBox()
        self.shape_type_combobox.addItem('Polygon')
        self.shape_type_combobox.addItem('Circle')
        self.shape_type_combobox.setCurrentIndex(0)

        self.shape_radius_label = QLabel('New shape radius')
        self.shape_radius_spinbox = QSpinBox()
        self.shape_radius_spinbox.setRange(1, 500)
        self.shape_radius_spinbox.setSingleStep(1)
        self.shape_radius_spinbox.setValue(globals.NEW_SHAPE_RADIUS)

        self.shape_mass_label = QLabel('New shape mass')
        self.shape_mass_spinbox = QSpinBox()
        self.shape_mass_spinbox.setRange(1, 500)
        self.shape_mass_spinbox.setSingleStep(1)
        self.shape_mass_spinbox.setValue(globals.NEW_SHAPE_MASS)

        self.shape_degree_label = QLabel('New shape degree')
        self.shape_degree_spinbox = QSpinBox()
        self.shape_degree_spinbox.setRange(1, 500)
        self.shape_degree_spinbox.setSingleStep(1)
        self.shape_degree_spinbox.setValue(globals.NEW_SHAPE_DEGREE)

        self.confirm_button = QPushButton('Confirm')
        QObject.connect(self.confirm_button, SIGNAL('clicked()'), self.change_parameters)

        grid_layout.addWidget(self.fps_label, 0, 0)
        grid_layout.addWidget(self.fps_spinbox, 0, 1)
        grid_layout.addWidget(self.force_label, 0, 2)
        grid_layout.addWidget(self.force_spinbox, 0, 3)
        grid_layout.addWidget(self.friction_label, 0, 4)
        grid_layout.addWidget(self.friction_spinbox, 0, 5)
        grid_layout.addWidget(self.shape_type_label, 1, 0)
        grid_layout.addWidget(self.shape_type_combobox, 1, 1)
        grid_layout.addWidget(self.shape_radius_label, 1, 2)
        grid_layout.addWidget(self.shape_radius_spinbox, 1, 3)
        grid_layout.addWidget(self.shape_mass_label, 2, 0)
        grid_layout.addWidget(self.shape_mass_spinbox, 2, 1)
        grid_layout.addWidget(self.shape_degree_label, 2, 2)
        grid_layout.addWidget(self.shape_degree_spinbox, 2, 3)
        grid_layout.addWidget(self.confirm_button, 2, 4, 1, 2)

    def change_parameters(self):
        globals.FPS = self.fps_spinbox.value()
        globals.KEY_FORCE = self.force_spinbox.value()
        globals.NEW_SHAPE_TYPE = (
            globals.ShapeType.POLYGON if self.shape_type_combobox.currentIndex() == 0 else globals.ShapeType.CIRCLE)
        globals.NEW_SHAPE_RADIUS = self.shape_radius_spinbox.value()
        globals.NEW_SHAPE_MASS = self.shape_mass_spinbox.value()
        globals.NEW_SHAPE_DEGREE = self.shape_degree_spinbox.value()
