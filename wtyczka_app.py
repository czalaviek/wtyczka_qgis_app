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
from qgis.PyQt.QtWidgets import QAction, QToolButton, QMenu

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


        # okno moduł metadata
        self.metadaneDialog = MetadaneDialog()

        # eventy moduł metadata
        self.metadaneDialog.prev_btn.clicked.connect(self.metadaneDialog_prev_btn_clicked)
        self.metadaneDialog.next_btn.clicked.connect(self.metadaneDialog_next_btn_clicked)

        #okno moduł validator
        self.walidacjaDialog = WalidacjaDialog()

        #eventy moduł validator
        self.walidacjaDialog.prev_btn.clicked.connect(self.walidacjaDialog_prev_btn_clicked)
        self.walidacjaDialog.validate_btn.clicked.connect(self.walidacjaDialog.close)


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

        self.addAction(icon_path=':/plugins/wtyczka_app/img/logo.png',
                       text=u'Praca z APP / zbiorem APP',
                       callback=self.run_app)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/logo.png',
                       text=u'Tworzenie / aktualizacja metadanych',
                       callback=self.run_metadata)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/logo.png',
                       text=u'Walidacja plików',
                       callback=self.run_validator)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/logo.png',
                       text=u'Ustawienia',
                       callback=self.run_app)

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

    def run_settings(self):
        pass

    def run_validator(self):
        self.openNewDialog(self.walidacjaDialog)

    """Event handlers"""
    def pytanieAppDialog_app_btn_clicked(self):
        self.openNewDialog(self.rasterInstrukcjaDialog)

    def pytanieAppDialog_zbior_btn_clicked(self):
        self.openNewDialog(self.zbiorPrzygotowanieDialog)

    def rasterInstrukcjaDialog_next_btn_clicked(self):
        self.openNewDialog(self.rasterFormularzDialog)

    def rasterInstrukcjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.pytanieAppDialog)

    def rasterFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.rasterInstrukcjaDialog)

    def rasterFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.wektorInstrukcjaDialog)

    def wektorInstrukcjaDialog_next_btn_clicked(self):
        self.openNewDialog(self.wektorFormularzDialog)

    def wektorInstrukcjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.rasterFormularzDialog)

    def wektorFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.wektorInstrukcjaDialog)

    def wektorFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.dokumentyFormularzDialog)

    def dokumentyFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.wektorFormularzDialog)

    def dokumentyFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.generowanieGMLDialog)

    def generowanieGMLDialog_prev_btn_clicked(self):
        self.openNewDialog(self.dokumentyFormularzDialog)

    def generowanieGMLDialog_next_btn_clicked(self):
        self.openNewDialog(self.zbiorPrzygotowanieDialog)

    def zbiorPrzygotowanieDialog_prev_btn_clicked(self):
        self.openNewDialog(self.pytanieAppDialog)

    def zbiorPrzygotowanieDialog_next_btn_clicked(self):
        self.openNewDialog(self.metadaneDialog)

    def metadaneDialog_prev_btn_clicked(self):
        self.openNewDialog(self.zbiorPrzygotowanieDialog)

    def metadaneDialog_next_btn_clicked(self):
        self.openNewDialog(self.walidacjaDialog)

    def walidacjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.metadaneDialog)

    """Helper methods"""
    def openNewDialog(self, dlg):
        self.prevDlg = self.activeDlg
        self.activeDlg = dlg
        if self.prevDlg:
            self.prevDlg.close()
        self.activeDlg.show()

    def radioButtonStat(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Test")
