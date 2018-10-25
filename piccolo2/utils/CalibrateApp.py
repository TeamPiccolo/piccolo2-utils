# Copyright 2014-2016 The Piccolo Team
#
# This file is part of piccolo2-utils.
#
# piccolo2-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# piccolo2-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with piccolo2-utils.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ['main']

from PyQt5 import QtCore, QtGui, QtWidgets
import calibrate_ui


class CalibrateApp(QtWidgets.QMainWindow, calibrate_ui.Ui_MainWindow):
    def __init__(self, calibrationData, parent=None):
        super(CalibrateApp, self).__init__()
        self.setupUi(self)

        self.calibrationData = calibrationData

        self.calibratePlot.data = calibrationData
        
        # the light source selector
        self.lightSourceSelector.addItems(self.calibrationData.lightsources)
        self.lightSourceSelector.currentIndexChanged.connect(self.replot)

        # plot current light source
        self.replot()

    def replot(self):
        self.calibratePlot.plotData(self.lightSourceSelector.currentText())
        
def main(calibrationData):
    app = QtWidgets.QApplication([])
    form = CalibrateApp(calibrationData)
    form.show()
    
    app.exec_()
