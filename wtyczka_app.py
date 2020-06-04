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
from PyQt5.QtWidgets import QDialog
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QToolButton, QMenu, QMessageBox

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .modules.app import PytanieAppDialog, ZbiorPrzygotowanieDialog, RasterInstrukcjaDialog, RasterFormularzDialog, WektorFormularzDialog, DokumentyFormularzDialog, WektorInstrukcjaDialog, GenerowanieGMLDialog
from .modules.metadata import MetadaneDialog
from .modules.validator import WalidacjaDialog

import os

PLUGIN_NAME = 'Wtyczka APP'
PLUGIN_VERSION = '0.1'

class WtyczkaAPP:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.activeDlg = None
        self.prevDlg = None
        # Declare instance attributes
        self.actions = []

        # okna moduł app
        self.pytanieAppDialog = PytanieAppDialog()
        self.zbiorPrzygotowanieDialog = ZbiorPrzygotowanieDialog()
        self.rasterInstrukcjaDialog = RasterInstrukcjaDialog()
        self.rasterFormularzDialog = RasterFormularzDialog()
        self.wektorFormularzDialog = WektorFormularzDialog()
        self.dokumentyFormularzDialog = DokumentyFormularzDialog()
        self.wektorInstrukcjaDialog = WektorInstrukcjaDialog()
        self.generowanieGMLDialog = GenerowanieGMLDialog()

        # eventy modul app
        self.pytanieAppDialog.zbior_btn.clicked.connect(self.pytanieAppDialog_zbior_btn_clicked)
        self.pytanieAppDialog.app_btn.clicked.connect(self.pytanieAppDialog_app_btn_clicked)
        self.rasterInstrukcjaDialog.next_btn.clicked.connect(self.rasterInstrukcjaDialog_next_btn_clicked)
        self.rasterInstrukcjaDialog.prev_btn.clicked.connect(self.rasterInstrukcjaDialog_prev_btn_clicked)
        self.rasterFormularzDialog.prev_btn.clicked.connect(self.rasterFormularzDialog_prev_btn_clicked)
        self.rasterFormularzDialog.next_btn.clicked.connect(self.rasterFormularzDialog_next_btn_clicked)
        self.wektorInstrukcjaDialog.next_btn.clicked.connect(self.wektorInstrukcjaDialog_next_btn_clicked)
        self.wektorInstrukcjaDialog.prev_btn.clicked.connect(self.wektorInstrukcjaDialog_prev_btn_clicked)
        self.wektorFormularzDialog.prev_btn.clicked.connect(self.wektorFormularzDialog_prev_btn_clicked)
        self.wektorFormularzDialog.next_btn.clicked.connect(self.wektorFormularzDialog_next_btn_clicked)
        self.dokumentyFormularzDialog.prev_btn.clicked.connect(self.dokumentyFormularzDialog_prev_btn_clicked)
        self.dokumentyFormularzDialog.next_btn.clicked.connect(self.dokumentyFormularzDialog_next_btn_clicked)
        self.generowanieGMLDialog.prev_btn.clicked.connect(self.generowanieGMLDialog_prev_btn_clicked)
        self.generowanieGMLDialog.next_btn.clicked.connect(self.generowanieGMLDialog_next_btn_clicked)
        self.zbiorPrzygotowanieDialog.prev_btn.clicked.connect(self.zbiorPrzygotowanieDialog_prev_btn_clicked)
        self.zbiorPrzygotowanieDialog.next_btn.clicked.connect(self.zbiorPrzygotowanieDialog_next_btn_clicked)

        self.rasterFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)
        self.wektorInstrukcjaDialog.saveLayer_btn.clicked.connect(self.showPopupSaveLayer)
        self.wektorInstrukcjaDialog.generateTemporaryLayer_btn.clicked.connect(self.showPopupGenerateLayer)
        self.wektorFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)
        self.dokumentyFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)
        self.generowanieGMLDialog.generate_btn.clicked.connect(self.showPopupGenerate)
        self.zbiorPrzygotowanieDialog.validateAndGenerate_btn.clicked.connect(self.showPopupGenerate2)

        self.generowanieGMLDialog.yesMakeAnotherApp_radioBtn.toggled.connect(self.yesMakeAnotherApp_radioBtn_clicked)
        self.generowanieGMLDialog.noMakeAnotherApp_radioBtn.toggled.connect(self.noMakeAnotherApp_radioBtn_clicked)
        self.generowanieGMLDialog.yesMakeSet_radioBtn.toggled.connect(self.yesMakeSet_radioBtn_clicked)
        self.generowanieGMLDialog.noMakeSet_radioBtn.toggled.connect(self.noMakeSet_radioBtn_clicked)


        # okno moduł metadata
        self.metadaneDialog = MetadaneDialog()

        # eventy moduł metadata
        self.metadaneDialog.prev_btn.clicked.connect(self.metadaneDialog_prev_btn_clicked)
        self.metadaneDialog.next_btn.clicked.connect(self.metadaneDialog_next_btn_clicked)

        self.metadaneDialog.send_btn.clicked.connect(self.showPopupSend)
        self.metadaneDialog.validateAndSave_btn.clicked.connect(self.showPopupValidateAndSave)

        self.metadaneDialog.newMetadata_radioButton.toggled.connect(self.newMetadataRadioButton_clicked)
        self.metadaneDialog.existingMetadata_radioButton.toggled.connect(self.existingMetadataRadioButton_clicked)

        self.metadaneDialog.server_checkBox.stateChanged.connect(self.server_checkBoxChangedAction)
        self.metadaneDialog.email_checkBox.stateChanged.connect(self.email_checkBoxChangedAction)

        #okno moduł validator
        self.walidacjaDialog = WalidacjaDialog()

        #eventy moduł validator
        self.walidacjaDialog.prev_btn.clicked.connect(self.walidacjaDialog_prev_btn_clicked)

        self.walidacjaDialog.export_btn.clicked.connect(self.showPopupExport)
        self.walidacjaDialog.validate_btn.clicked.connect(self.showPopupValidate)
        self.walidacjaDialog.validateGML_checkBox.stateChanged.connect(self.gml_checkBoxChangedAction)
        self.walidacjaDialog.validateXML_checkBox.stateChanged.connect(self.xml_checkBoxChangedAction)


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
                       text=u'Walidacja plików',
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

    """Event handlers"""
    listaOkienek = []

    def pytanieAppDialog_app_btn_clicked(self):
        self.openNewDialog(self.rasterInstrukcjaDialog)
        self.listaOkienek.append(self.pytanieAppDialog)

    def pytanieAppDialog_zbior_btn_clicked(self):
        self.openNewDialog(self.zbiorPrzygotowanieDialog)
        self.listaOkienek.append(self.pytanieAppDialog)

    def rasterInstrukcjaDialog_next_btn_clicked(self):
        self.openNewDialog(self.rasterFormularzDialog)
        self.listaOkienek.append(self.rasterInstrukcjaDialog)

    def rasterInstrukcjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def rasterFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def rasterFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.wektorInstrukcjaDialog)
        self.listaOkienek.append(self.rasterFormularzDialog)

    def wektorInstrukcjaDialog_next_btn_clicked(self):
        self.openNewDialog(self.wektorFormularzDialog)
        self.listaOkienek.append(self.wektorInstrukcjaDialog)

    def wektorInstrukcjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def wektorFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def wektorFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.dokumentyFormularzDialog)
        self.listaOkienek.append(self.wektorFormularzDialog)

    def dokumentyFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def dokumentyFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.generowanieGMLDialog)
        self.listaOkienek.append(self.dokumentyFormularzDialog)

    def generowanieGMLDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def generowanieGMLDialog_next_btn_clicked(self):
        if self.generowanieGMLDialog.yesMakeAnotherApp_radioBtn.isChecked():
            self.openNewDialog(self.rasterInstrukcjaDialog)
        if self.generowanieGMLDialog.yesMakeSet_radioBtn.isChecked():
            self.openNewDialog(self.zbiorPrzygotowanieDialog)
        if self.generowanieGMLDialog.noMakeSet_radioBtn.isChecked():
            self.generowanieGMLDialog.close()
        self.listaOkienek.append(self.generowanieGMLDialog)

    def zbiorPrzygotowanieDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def zbiorPrzygotowanieDialog_next_btn_clicked(self):
        self.openNewDialog(self.metadaneDialog)
        self.listaOkienek.append(self.zbiorPrzygotowanieDialog)

    def metadaneDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def metadaneDialog_next_btn_clicked(self):
        self.openNewDialog(self.walidacjaDialog)
        self.listaOkienek.append(self.metadaneDialog)

    def walidacjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    """Helper methods"""
    def openNewDialog(self, dlg):
        self.prevDlg = self.activeDlg
        self.activeDlg = dlg
        if self.prevDlg:
            self.prevDlg.close()
        self.activeDlg.show()

    def newMetadataRadioButton_clicked(self, enabled):
        if enabled:
            self.metadaneDialog.newFile_widget.setEnabled(True)
            self.metadaneDialog.chooseFile_widget.setEnabled(False)

    def existingMetadataRadioButton_clicked(self, enabled):
        if enabled:
            self.metadaneDialog.newFile_widget.setEnabled(False)
            self.metadaneDialog.chooseFile_widget.setEnabled(True)

    def yesMakeAnotherApp_radioBtn_clicked(self, enabled):
        if enabled:
            self.generowanieGMLDialog.next_btn.setText("Dalej")
            self.generowanieGMLDialog.yesMakeSet_radioBtn.setChecked(False)
            self.generowanieGMLDialog.noMakeSet_radioBtn.setChecked(False)
            self.generowanieGMLDialog.questionMakeSet_lbl.setEnabled(False)
            self.generowanieGMLDialog.yesMakeSet_radioBtn.setEnabled(False)
            self.generowanieGMLDialog.noMakeSet_radioBtn.setEnabled(False)

    def noMakeAnotherApp_radioBtn_clicked(self, enabled):
        if enabled:
            self.generowanieGMLDialog.next_btn.setText("Dalej")
            self.generowanieGMLDialog.questionMakeSet_lbl.setEnabled(True)
            self.generowanieGMLDialog.yesMakeSet_radioBtn.setEnabled(True)
            self.generowanieGMLDialog.noMakeSet_radioBtn.setEnabled(True)

    def yesMakeSet_radioBtn_clicked(self, enabled):
        if enabled:
            self.generowanieGMLDialog.next_btn.setText("Dalej")

    def noMakeSet_radioBtn_clicked(self, enabled):
        if enabled:
            self.generowanieGMLDialog.next_btn.setText("Zakończ")

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


    """Popup windows"""
    def showPopupSaveForm(self):
        msg = QMessageBox()
        msg.setWindowTitle("Zapisz aktualny formularz")
        msg.setText("Poprawnie zapisano formularz.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def showPopupSaveLayer(self):
        msg = QMessageBox()
        msg.setWindowTitle("Zapisz warstwę")
        msg.setText("Poprawnie zapisano warstwę.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def showPopupGenerateLayer(self):
        msg = QMessageBox()
        msg.setWindowTitle("Wygeneruj warstwę")
        msg.setText("Poprawnie wygenerowano warstwę tymczasową.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def showPopupGenerate(self):
        msg = QMessageBox()
        msg.setWindowTitle("Wygeneruj plik GML dla APP")
        msg.setText("Poprawnie wygenerowano plik GML.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def showPopupGenerate2(self):
        msg = QMessageBox()
        msg.setWindowTitle("Wygeneruj plik GML dla zbioru APP")
        msg.setText("Poprawnie wygenerowano plik GML.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def showPopupExport(self):
        msg = QMessageBox()
        msg.setWindowTitle("Wyeksportuj plik z błędami")
        msg.setText("Poprawnie wyeksportowano plik z błędami.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def showPopupValidateAndSave(self):
        msg = QMessageBox()
        msg.setWindowTitle("Zwaliduj i zapisz plik XML")
        msg.setText("Poprawnie zwalidowano oraz zapisano plik XML.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def showPopupSend(self):
        msg = QMessageBox()
        msg.setWindowTitle("Wyśli plik")
        msg.setText("Wysłano plik XML zawierający metadane.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def showPopupValidate(self):
        msg = QMessageBox()
        msg.setWindowTitle("Waliduj pliki")
        msg.setText("Poprawnie zwalidowano wszystkie wgrane pliki.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()