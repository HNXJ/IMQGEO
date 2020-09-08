from PyQt5.QtGui import QKeySequence, QPalette, QColor
from PyQt5.QtCore import QDateTime, Qt, QTimer, QRect
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

import IMQImageViewer as ImageViewer
import IMQShapeFile as Shape
import IMQProcessRun as Run
import threading
import sys


class WidgetGallery(QDialog):
    
    def __init__(self, parent=None):
        
        super(WidgetGallery, self).__init__(parent)
        self.originalPalette = QApplication.palette()
        self.resize(1600, 900)           
        
        self.originalPalette.setColor(QPalette.Window, QColor(53, 53, 53))
        self.originalPalette.setColor(QPalette.WindowText, Qt.white)
        self.originalPalette.setColor(QPalette.Base, QColor(25, 25, 25))
        self.originalPalette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        
        # palette.setColor(QPalette.ToolTipBase, Qt.white)
        # palette.setColor(QPalette.ToolTipText, Qt.white)
        # palette.setColor(QPalette.Text, Qt.white)
        # palette.setColor(QPalette.Button, QColor(53, 53, 53))
        
        # palette.setColor(QPalette.ButtonText, Qt.white)
        # palette.setColor(QPalette.BrightText, Qt.red)
        # palette.setColor(QPalette.Link, QColor(42, 130, 218))
        # palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        
        # palette.setColor(QPalette.HighlightedText, Qt.black)
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.imageViewer = ImageViewer.QImageViewer()
        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeft2GroupBox()
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        self.createProgressBar()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        
        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topLeft2GroupBox, 1, 1)
        mainLayout.addWidget(self.topRightGroupBox, 1, 2, 1, 2)
        
        mainLayout.addWidget(self.bottomLeftTabWidget, 1, 4, 1, 1)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 0, 1, 4)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 4)
        mainLayout.setRowStretch(1, 1)
        
        mainLayout.setRowStretch(2, 4)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        mainLayout.setColumnStretch(2, 2)
        mainLayout.setColumnStretch(3, 2)
        
        self.setLayout(mainLayout)
        self.setWindowTitle("Map parser")
        self.changeStyle('Fusion')
        self.imageViewer.show()
        
        return

    def changeStyle(self, styleName):
        
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()
        return

    def changePalette(self):
        
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)
        
        return

    def advanceProgressBar(self):
        
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)
        return

    def createTopLeft2GroupBox(self):
        
        self.topLeft2GroupBox = QGroupBox("Custom Detail")
        # self.radioButton1 = QRadioButton("Water Channels")
        # self.radioButton2 = QRadioButton("Borders")
        
        # self.radioButton3 = QRadioButton("Rivers")
        # self.radioButton4 = QRadioButton("Low borders")
        flo = QFormLayout()
        
        self.RlineEdit1 = QLineEdit()
        self.RlineEdit1.setMaxLength(3)
        # self.Rlanel1 = QLabel("Red")
        
        self.GlineEdit1 = QLineEdit()
        self.GlineEdit1.setMaxLength(3)
        # self.Rlanel1 = QLabel("Green")
        
        self.BlineEdit1 = QLineEdit()
        self.BlineEdit1.setMaxLength(3)
        # self.Rlanel1 = QLabel("Blue")
        
        self.RlineEdit2 = QLineEdit()
        self.RlineEdit2.setMaxLength(3)
        # self.Rlanel1 = QLabel("Red")
        
        self.GlineEdit2 = QLineEdit()
        self.GlineEdit2.setMaxLength(3)
        # self.Rlanel1 = QLabel("Green")
        
        self.BlineEdit2 = QLineEdit()
        self.BlineEdit2.setMaxLength(3)
        # self.Rlanel1 = QLabel("Blue")
        
        flo.addRow("Red min", self.RlineEdit1)
        flo.addRow("Green min", self.GlineEdit1)
        flo.addRow("Blue min", self.BlineEdit1)
        
        flo.addRow("Red max", self.RlineEdit2)
        flo.addRow("Green max", self.GlineEdit2)
        flo.addRow("Blue max", self.BlineEdit2)
        
        layout = QVBoxLayout()
        # layout.addWidget(self.radioButton1)
        # layout.addWidget(self.radioButton2)
        # layout.addWidget(self.radioButton3)
        
        # layout.addWidget(self.radioButton4)
        # layout.addWidget(self.radioButton5)
        
        # layout.addWidget(self.RlineEdit1, alignment=Qt.AlignRight)
        # layout.addWidget(self.GlineEdit1, alignment=Qt.AlignRight)
        # layout.addWidget(self.BlineEdit1, alignment=Qt.AlignRight)
        
        # layout.addWidget(self.RlineEdit2, alignment=Qt.AlignRight)
        # layout.addWidget(self.GlineEdit2, alignment=Qt.AlignRight)
        # layout.addWidget(self.BlineEdit2, alignment=Qt.AlignRight)
        
        layout.addStretch(1)
        
        self.topLeft2GroupBox.setLayout(flo)    
        return
    
    def createTopLeftGroupBox(self):
        
        self.topLeftGroupBox = QGroupBox("Detail")
        self.radioButton1 = QRadioButton("Water Channels")
        self.radioButton2 = QRadioButton("Borders")
        
        self.radioButton3 = QRadioButton("Rivers")
        self.radioButton4 = QRadioButton("Low borders")
        self.radioButton5 = QRadioButton("Custom thresholding")
        
        
        self.radioButton1.toggled.connect(self.topLeft2GroupBox.setDisabled)
        self.radioButton2.toggled.connect(self.topLeft2GroupBox.setDisabled)
        self.radioButton3.toggled.connect(self.topLeft2GroupBox.setDisabled)
        self.radioButton4.toggled.connect(self.topLeft2GroupBox.setDisabled)
        
        # self.RlineEdit = QLineEdit()
        # self.GlineEdit = QLineEdit()
        # self.BlineEdit = QLineEdit()
        
        self.radioButton1.setChecked(True)

        checkBox = QCheckBox("Remove rednoise")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(self.radioButton1)
        layout.addWidget(self.radioButton2)
        layout.addWidget(self.radioButton3)
        
        layout.addWidget(self.radioButton4)
        layout.addWidget(self.radioButton5)
        
        # layout.addWidget(self.RlineEdit)
        # layout.addWidget(self.GlineEdit)
        # layout.addWidget(self.BlineEdit)
        
        layout.addWidget(checkBox)
        layout.addStretch(1)
        
        self.topLeftGroupBox.setLayout(layout)    
        return
    
    def ShowPlots(self, args):
        self.Consule.setPlainText(" - ")
        fp = self.lineEdit.text()
        sp = self.slider_ratio.value()
        
        r1 = self.RlineEdit1.text()
        g1 = self.GlineEdit1.text()
        b1 = self.RlineEdit1.text()
        
        r2 = self.RlineEdit2.text()
        g2 = self.GlineEdit2.text()
        b2 = self.RlineEdit2.text()
        
        self.progressBar.setValue(0)
        self.Consule.append("Loading image, ratio = " + str(sp))
        if self.radioButton1.isChecked():
            # I = threading.Thread(target=Run.channels
                                 # ,args=(None, "default", sp, fp))
            I = Run.channels(scale_percent=sp, filepath=fp)
            self.label1.setText("Channels")
        elif self.radioButton2.isChecked():
            I = Run.Borders(scale_percent=sp, filepath=fp)
            self.label1.setText("Borders")
        elif self.radioButton3.isChecked():
            I = Run.Rivers(scale_percent=sp, filepath=fp)
            self.label1.setText("Rivers")
        elif self.radioButton4.isChecked():
            I = Run.Roads(scale_percent=sp, filepath=fp)
            self.label1.setText("Low borders")
        elif self.radioButton5.isChecked():
            try:
                r1 = max(min(int(r1), 255), 0)
                g1 = max(min(int(g1), 255), 0)
                b1 = max(min(int(b1), 255), 0)
                
                r2 = max(min(int(r2), 255), 0)
                g2 = max(min(int(g2), 255), 0)
                b2 = max(min(int(b2), 255), 0)
                
            except Exception:
                self.Consule.append("RGB color values must be integer numbers")
                # QtGui.QMessageBox.about(self, 'Error','Input can only be a number')
                return
            
            I = Run.Custom(scale_percent=sp, filepath=fp, lr=r1, lg=g1, lb=b1
                           ,hr=r2, hg=g2, hb=b2)
            self.label1.setText("Custom threshold")
        
        # plt.figure('Plots')
        # imgplot = plt.imshow(I)
        # plt.show()
        J = I
        # J = I.start()
        self.progressBar.setValue(40)
        self.Consule.append("Processing ...")
        self.progressBar.setValue(75)

        
        self.Consule.append("Done.")
        self.progressBar.setValue(100)
        
        self.imageViewer.show()
        self.imageViewer.showMap(J)
        return
    
    def SavePlots(self, args):
        
        self.Consule.setPlainText(" - ")
        print(self.radioButton1.isChecked())
        self.progressBar.setValue(100)
        return
    
    def ShapeFile(self, args):
        
        self.Consule.setPlainText(" Converting ...")
        self.progressBar.setValue(20)        
        
        try:
            if self.radioButton1.isChecked():
                Shape.run("dblues.dxf")
            elif self.radioButton2.isChecked():
                Shape.run("darks.dxf")
            elif self.radioButton3.isChecked():
                Shape.run("lblues.dxf")
            elif self.radioButton4.isChecked():
                Shape.run("pinks.png")
        except:
            self.Consule.setPlainText(" Converting failed ! type error")
            
        return
        
    def createTopRightGroupBox(self):
        
        self.topRightGroupBox = QGroupBox("Actions")
        self.ShowPlots_ = QPushButton("Show plots")
        self.ShapeFile_ = QPushButton("Covert to shape file")
        self.ShowPlots_.clicked.connect(self.ShowPlots)
        self.ShapeFile_.clicked.connect(self.ShapeFile)
        self.ShowPlots_.setDefault(False)

        # self.SavePlots_ = QPushButton("Save plots")
        # self.SavePlots_.clicked.connect(self.SavePlots)
        # self.SavePlots_.setDefault(False)
        # self.SavePlots_.setCheckable(True)
        # self.SavePlots_.setChecked(False)
        
        fname_label = QLabel("Filepath")
        self.lineEdit = QLineEdit('CyprusGeologyMapTaurus.tif')
        
        # self.lineEdit.setEchoMode(QLineEdit.Password)
        # spinBox = QSpinBox(self.bottomRightGroupBox)
        # spinBox.setValue(50)
        
        # dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        # dateTimeEdit.setDateTime(QDateTime.currentDateTime())
            
        slider_label = QLabel("Ratio")
        self.slider_ratio = QSlider(Qt.Horizontal, self.topRightGroupBox)
        self.slider_ratio.setValue(10)

        # scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        # scrollBar.setValue(60)

        # dial = QDial(self.bottomRightGroupBox)
        # dial.setValue(30)
        # dial.setNotchesVisible(True)

        # layout.setRowStretch(5, 1)
        
        layout = QVBoxLayout()
        layout.addWidget(fname_label)
        layout.addWidget(self.lineEdit)
        
        # layout.addWidget(spinBox, 1, 0, 1, 2)
        # layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        # slider_label = QLabel("Ratio")
        
        layout.addWidget(slider_label)
        layout.addWidget(self.slider_ratio)
        # layout.addWidget(scrollBar, 4, 0)
        # layout.addWidget(dial, 3, 1, 2, 1)
        
        layout.addWidget(self.ShowPlots_)
        layout.addWidget(self.ShapeFile_)
        # layout.addWidget(self.SavePlots_)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)
        return
    
    def createBottomLeftTabWidget(self):
    
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        self.Consule = QTextEdit()
        self.Consule.setPlainText("Consule")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(self.Consule)
        tab2.setLayout(tab2hbox)

        # self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Consule")
        return
    
    def createBottomRightGroupBox(self):
        
        self.bottomRightGroupBox = QGroupBox("Plot")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        # self.lineEdit = QLineEdit('CyprusGeologyMapTaurus.tif')
        # self.lineEdit.setEchoMode(QLineEdit.Password)

        # spinBox = QSpinBox(self.bottomRightGroupBox)
        # spinBox.setValue(50)

        # dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        # dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        # slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        # slider.setValue(40)

        # scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        # scrollBar.setValue(60)

        # dial = QDial(self.bottomRightGroupBox)
        # dial.setValue(30)
        # dial.setNotchesVisible(True)

        layout = QGridLayout()
        # layout.addWidget(self.lineEdit, 0, 0, 1, 2)
        # layout.addWidget(spinBox, 1, 0, 1, 2)
        # layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        self.label1 = QLabel("Type")
        
        layout.addWidget(self.label1)
        # label2 = QLabel(" ")
        # layout.addWidget(label2)
        # label3 = QLabel(" ")
        layout.addWidget(self.imageViewer, 1, 0, 3, 4)
  
        # layout.addWidget(slider, 3, 0)
        # layout.addWidget(scrollBar, 4, 0)
        # layout.addWidget(dial, 3, 1, 2, 1)
        
        layout.setRowStretch(1, 4)
        layout.setColumnStretch(0, 3)
        self.bottomRightGroupBox.setLayout(layout)
        
        return
    
    def createProgressBar(self):
        
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        
        # timer = QTimer(self)
        # timer.timeout.connect(self.advanceProgressBar)
        # timer.start(1000)
        
        return
    

if __name__ == '__main__':

    # app = QApplication(sys.argv)
    # imageViewer = ImageViewer.QImageViewer()
    # imageViewer.show()
    # sys.exit(app.exec_())
    
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_()) 