# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wektor_instrukcja_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(580, 394)
        Dialog.setSizeGripEnabled(True)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_lbl = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title_lbl.setFont(font)
        self.title_lbl.setObjectName("title_lbl")
        self.verticalLayout.addWidget(self.title_lbl)
        self.instruction_scrollArea = QtWidgets.QScrollArea(Dialog)
        self.instruction_scrollArea.setWidgetResizable(True)
        self.instruction_scrollArea.setObjectName("instruction_scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 564, 245))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.instruction_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.instruction_lbl.setFont(font)
        self.instruction_lbl.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.instruction_lbl.setWordWrap(True)
        self.instruction_lbl.setObjectName("instruction_lbl")
        self.gridLayout.addWidget(self.instruction_lbl, 0, 0, 1, 1)
        self.instruction_scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.instruction_scrollArea)
        self.empty1_lbl = QtWidgets.QLabel(Dialog)
        self.empty1_lbl.setText("")
        self.empty1_lbl.setObjectName("empty1_lbl")
        self.verticalLayout.addWidget(self.empty1_lbl)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.addAppShp_lbl = QtWidgets.QLabel(Dialog)
        self.addAppShp_lbl.setObjectName("addAppShp_lbl")
        self.horizontalLayout_4.addWidget(self.addAppShp_lbl)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layers_comboBox = QgsMapLayerComboBox(Dialog)
        self.layers_comboBox.setObjectName("layers_comboBox")
        self.horizontalLayout.addWidget(self.layers_comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.empty2_lbl = QtWidgets.QLabel(Dialog)
        self.empty2_lbl.setText("")
        self.empty2_lbl.setObjectName("empty2_lbl")
        self.verticalLayout.addWidget(self.empty2_lbl)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.prev_btn = QtWidgets.QPushButton(Dialog)
        self.prev_btn.setEnabled(True)
        self.prev_btn.setObjectName("prev_btn")
        self.horizontalLayout_2.addWidget(self.prev_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.generateTemporaryLayer_btn = QtWidgets.QPushButton(Dialog)
        self.generateTemporaryLayer_btn.setObjectName("generateTemporaryLayer_btn")
        self.horizontalLayout_2.addWidget(self.generateTemporaryLayer_btn)
        self.skip_btn = QtWidgets.QPushButton(Dialog)
        self.skip_btn.setObjectName("skip_btn")
        self.horizontalLayout_2.addWidget(self.skip_btn)
        self.next_btn = QtWidgets.QPushButton(Dialog)
        self.next_btn.setObjectName("next_btn")
        self.horizontalLayout_2.addWidget(self.next_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title_lbl.setText(_translate("Dialog", "Przygotowanie granic APP"))
        self.instruction_lbl.setText(_translate("Dialog", "<html><head/><body><p>W kolejnym kroku tworzenia danych przestrzennych APP niezbędne jest posiadanie granic obszaru objętego danym aktem. </p><p><span style=\" font-weight:600;\">WAŻNE</span>: Dane przestrzenne muszą być zapisane w układzie PL-1992 lub PL-2000 i być reprezentowane geometrycznie przez jeden poligon lub multipoligon (w przypadku obiektów wieloczęściowych). </p><p>Jeżeli posiadasz w ten sposób przygotowane dane skorzystaj z opcji <span style=\" font-style:italic;\">Wybierz plik z granicami APP.</span></p><p>Jeżeli <span style=\" font-weight:600;\">nie posiadasz</span> danych przestrzennych dla APP musisz je przygotować. Zapoznaj się z instrukcją tworzenia danych przestrzennych dla APP: http…. <br/>oraz obejrzyj film: http… </p></body></html>"))
        self.addAppShp_lbl.setText(_translate("Dialog", "Wybierz plik z granicami APP (opcjonalne)"))
        self.prev_btn.setText(_translate("Dialog", "Wstecz"))
        self.generateTemporaryLayer_btn.setText(_translate("Dialog", "Stwórz pustą warstwę"))
        self.skip_btn.setToolTip(_translate("Dialog", "Pominięcie tworzenia formularza dla APP. Przeniesienie do formularza dla dokumentów formalnych."))
        self.skip_btn.setText(_translate("Dialog", "Pomiń"))
        self.next_btn.setText(_translate("Dialog", "Dalej"))
from qgsmaplayercombobox import QgsMapLayerComboBox


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
