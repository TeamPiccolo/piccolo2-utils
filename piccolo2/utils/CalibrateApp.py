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

class Peaks(QtGui.QStandardItemModel):
    def __init__(self,*args,**keywords):
        self.pdata = keywords['data']
        del keywords['data']
        
        QtGui.QStandardItemModel.__init__(self,*args,**keywords)


    def selectLightSource(self,lightsource):
        peaks = self.pdata.peaks[self.pdata.peaks.lightSource==lightsource]
        self.clear()
        self.setHorizontalHeaderLabels(['pixel','wavelength','spectral line'])
        self.setColumnCount(3)
        self.setRowCount(len(peaks))
        i = 0
        for pixel,row in peaks.iterrows():
            item = QtGui.QStandardItem(str(pixel))
            item.setEditable(False)
            self.setItem(i,0,item)
            item = QtGui.QStandardItem(str(self.pdata.newWavelength(pixel)))
            item.setEditable(False)
            self.setItem(i,1,item)
            item = QtGui.QStandardItem(str(row.wavelength))
            self.setItem(i,2,item)
            i = i+1


class CalibrateApp(QtWidgets.QMainWindow, calibrate_ui.Ui_MainWindow):
    def __init__(self, calibrationData, parent=None):
        super(CalibrateApp, self).__init__()
        self.setupUi(self)

        self.calibrationData = calibrationData
        self.calibratePlot.data = calibrationData
        self.peaks = Peaks(data=self.calibrationData)
        
        # the light source selector
        self.lightSourceSelector.addItems(self.calibrationData.lightsources)
        self.lightSourceSelector.currentIndexChanged.connect(self.lightsourceChanged)

        # the peaks table
        self.tableView.setModel(self.peaks)

        # set the light source
        self.lightsourceChanged()

    def lightsourceChanged(self):
        ls = self.lightSourceSelector.currentText()
        self.calibratePlot.plotData(ls)
        self.peaks.selectLightSource(ls)
        
def main(calibrationData):
    app = QtWidgets.QApplication([])
    form = CalibrateApp(calibrationData)
    form.show()
    
    app.exec_()
