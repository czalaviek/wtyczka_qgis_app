# -*- coding: utf-8 -*-
"""
/***************************************************************************
 WtyczkaAPP
                                 A QGIS plugin
 Wtyczka QGIS wspomagająca przygotowanie aktów planowania przestrzennego zgodnych z rozporządzeniem Ministra Rozwoju.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-05-27
        git sha              : $Format:%H$
        copyright            : (C) 2020 by EnviroSolutions Sp. z o.o.
        email                : office@envirosolutions.pl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtWidgets import QDialog, QFileDialog

from qgis.PyQt import QtGui
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QToolButton, QMenu
#from qgis.core import QgsVectorLayer

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .modules.app.wtyczka_app import AppModule
from .modules.metadata import MetadaneDialog
from .modules.validator import WalidacjaDialog
from .modules.utils import showPopup

import os

PLUGIN_NAME = 'Wtyczka APP'
PLUGIN_VERSION = '0.1'


class WtyczkaAPP(AppModule):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # wczytanie modułów
        super(AppModule, self).__init__(iface)

        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)


        # Declare instance attributes
        self.actions = []

        self.listaPlikow = []

        # region okno moduł metadata
        self.metadaneDialog = MetadaneDialog()
        # endregion

        # region eventy moduł metadata
        self.metadaneDialog.prev_btn.clicked.connect(self.metadaneDialog_prev_btn_clicked)
        self.metadaneDialog.next_btn.clicked.connect(self.metadaneDialog_next_btn_clicked)

        self.metadaneDialog.send_btn.clicked.connect(self.showPopupSend)
        self.metadaneDialog.validateAndSave_btn.clicked.connect(self.showPopupValidateAndSave)

        self.metadaneDialog.newMetadata_radioButton.toggled.connect(self.newMetadataRadioButton_toggled)
        self.metadaneDialog.existingMetadata_radioButton.toggled.connect(self.existingMetadataRadioButton_toggled)

        self.metadaneDialog.server_checkBox.stateChanged.connect(self.server_checkBoxChangedAction)
        self.metadaneDialog.email_checkBox.stateChanged.connect(self.email_checkBoxChangedAction)

        self.metadaneDialog.newFile_widget.clicked.connect(self.saveMetaFile)
        self.metadaneDialog.chooseFile_widget.clicked.connect(self.openMetaFile)

        #self.metadaneDialog.chooseFile_widget.setFilter("*.xml")
        #self.metadaneDialog.chooseSet_widget.setFilter("*.gml")
        #self.metadaneDialog.newFile_widget.clicked.connect(self.getSaveFileName(filter="*.xml")[0])
        # endregion

        # region okno moduł validator
        self.walidacjaDialog = WalidacjaDialog()
        # endregion

        # region eventy moduł validator
        self.walidacjaDialog.prev_btn.clicked.connect(self.walidacjaDialog_prev_btn_clicked)

        self.walidacjaDialog.close_btn.setEnabled(False)
        self.walidacjaDialog.export_btn.clicked.connect(self.showPopupExport)
        self.walidacjaDialog.validate_btn.clicked.connect(self.walidacjaDialog_validate_btn_clicked)
        self.walidacjaDialog.validateGML_checkBox.stateChanged.connect(self.gml_checkBoxChangedAction)
        self.walidacjaDialog.validateXML_checkBox.stateChanged.connect(self.xml_checkBoxChangedAction)
        self.walidacjaDialog.close_btn.clicked.connect(self.walidacjaDialog.close)

        self.walidacjaDialog.chooseXML_widget.setFilter("*.xml")
        self.walidacjaDialog.chooseGML_widget.setFilter("*.gml")
        # endregion

    def addAction(self, icon_path, text, callback):
        m = self.toolButton.menu()
        action = QAction(
            icon=QIcon(icon_path),
            text=text,
            parent=self.iface.mainWindow()
        )
        action.triggered.connect(callback)
        self.actions.append(action)
        m.addAction(action)
        self.iface.addPluginToMenu(u'&' + PLUGIN_NAME, action)
        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.toolButton = QToolButton()
        self.toolButton.setDefaultAction(QAction(
            icon=QIcon(':/plugins/wtyczka_app/img/logo.png'),
            text=u'&' + PLUGIN_NAME,
            parent=self.iface.mainWindow()
        ))
        self.toolButton.clicked.connect(self.run_app)

        self.toolButton.setMenu(QMenu())
        self.toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.toolBtnAction = self.iface.addToolBarWidget(self.toolButton)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/praca_z_app.png',
                       text=u'Praca z APP / zbiorem APP',
                       callback=self.run_app)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/tworzenie.png',
                       text=u'Tworzenie / aktualizacja metadanych',
                       callback=self.run_metadata)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/walidacja.png',
                       text=u'Walidacja GML / XML',
                       callback=self.run_validator)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/ustawienia.png',
                       text=u'Ustawienia',
                       callback=self.run_settings)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(u'&' + PLUGIN_NAME, action)
            self.iface.removeToolBarIcon(action)

        self.iface.removeToolBarIcon(self.toolBtnAction)

    """Action handlers"""
    # region action handlers
    def run_app(self):
        self.openNewDialog(self.pytanieAppDialog)

    def run_metadata(self):
        self.openNewDialog(self.metadaneDialog)
        self.metadaneDialog.prev_btn.setEnabled(False)

    def run_settings(self):
        pass

    def run_validator(self):
        self.openNewDialog(self.walidacjaDialog)
        self.walidacjaDialog.prev_btn.setEnabled(False)
    # endregion

    """Event handlers"""

    # region metadaneDialog
    def metadaneDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def metadaneDialog_next_btn_clicked(self):
        self.openNewDialog(self.walidacjaDialog)
        self.listaOkienek.append(self.metadaneDialog)
        self.walidacjaDialog.prev_btn.setEnabled(True)

    def newMetadataRadioButton_toggled(self, enabled):
        if enabled:
            self.metadaneDialog.newFile_widget.setEnabled(True)
            self.metadaneDialog.chooseFile_widget.setEnabled(False)
            self.metadaneDialog.file_lbl.setText("...")

    def existingMetadataRadioButton_toggled(self, enabled):
        if enabled:
            self.metadaneDialog.newFile_widget.setEnabled(False)
            self.metadaneDialog.chooseFile_widget.setEnabled(True)
            self.metadaneDialog.file_lbl.setText("...")

    def server_checkBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.metadaneDialog.send_btn.setEnabled(True)
        else:
            if self.metadaneDialog.email_checkBox.isChecked():
                self.metadaneDialog.send_btn.setEnabled(True)
            else:
                self.metadaneDialog.send_btn.setEnabled(False)

    def email_checkBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.metadaneDialog.send_btn.setEnabled(True)
        else:
            if self.metadaneDialog.server_checkBox.isChecked():
                self.metadaneDialog.send_btn.setEnabled(True)
            else:
                self.metadaneDialog.send_btn.setEnabled(False)
    # endregion

    # region walidacjaDialog
    def walidacjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def walidacjaDialog_validate_btn_clicked(self):
        self.showPopupValidate()
        self.walidacjaDialog.close_btn.setEnabled(True)

    def xml_checkBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.walidacjaDialog.chooseXML_widget.setEnabled(True)
        else:
            self.walidacjaDialog.chooseXML_widget.setEnabled(False)

    def gml_checkBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.walidacjaDialog.chooseGML_widget.setEnabled(True)
        else:
            self.walidacjaDialog.chooseGML_widget.setEnabled(False)
    # endregion

    """Helper methods"""
    # region Helper methods


    #działa, ale trzeba dodać również inne rozszerzenia
    def openShpFile(self):
        shpFile = str(QFileDialog.getOpenFileName(filter=("Shapefiles (*.shp)"))[0])
        self.wektorInstrukcjaDialog.label.setText(shpFile)
        if shpFile is not None:
            self.iface.addVectorLayer(shpFile, str.split(os.path.basename(shpFile), ".")[0], "ogr")

    def saveMetaFile(self):
        self.outputPlik = QFileDialog.getSaveFileName(filter="*.xml")[0]
        if self.outputPlik != '':
            self.metadaneDialog.file_lbl.setText(self.outputPlik)

    def openMetaFile(self):
        self.plik = QFileDialog.getOpenFileName(filter="*.xml")[0]
        if self.plik != '':
            self.metadaneDialog.file_lbl.setText(self.plik)

    #niepotrzebne, było używane do QgsFileWidget - obecnie jest PushButton
    def openQgsFile(self):
        shpFile = self.wektorInstrukcjaDialog.chooseFile_btn.filePath()
        self.wektorInstrukcjaDialog.label.setText(shpFile)
        if shpFile is not None:
            self.iface.addVectorLayer(shpFile, str.split(os.path.basename(shpFile), ".")[0], "ogr")

    #wybór warstwy z QgsMapLayerComboBox
    def selectQgsLayer(self):
        # co jak użytkownik usunie wszystkie warstwy??
        aktywna_warstwa = self.wektorInstrukcjaDialog.layers_comboBox.currentLayer()
        if aktywna_warstwa:
            self.wektorInstrukcjaDialog.label.setText(aktywna_warstwa.name())
        else:
            self.wektorInstrukcjaDialog.label.setText("...")

    # endregion

    """Popup windows"""
    # region Popup windows

    def showPopupSaveLayer(self):
        showPopup("Zapisz warstwę", "Poprawnie zapisano warstwę.")

    def showPopupExport(self):
        showPopup("Wyeksportuj plik z błędami", "Poprawnie wyeksportowano plik z błędami.")

    def showPopupValidateAndSave(self):
        showPopup("Zwaliduj i zapisz plik XML", "Poprawnie zwalidowano oraz zapisano plik XML.")

    def showPopupSend(self):
        showPopup("Wyśli plik", "Wysłano plik XML zawierający metadane.")

    def showPopupValidate(self):
        showPopup("Waliduj pliki", "Poprawnie zwalidowano wszystkie wgrane pliki.")
    # endregion