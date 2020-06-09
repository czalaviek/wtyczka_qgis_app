# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'metadane_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(574, 600)
        font = QtGui.QFont()
        font.setKerning(True)
        Dialog.setFont(font)
        self.gridLayout_3 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_lbl = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.title_lbl.setFont(font)
        self.title_lbl.setObjectName("title_lbl")
        self.verticalLayout.addWidget(self.title_lbl)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.existingMetadata_radioButton = QtWidgets.QRadioButton(Dialog)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.existingMetadata_radioButton.setFont(font)
        self.existingMetadata_radioButton.setChecked(True)
        self.existingMetadata_radioButton.setObjectName("existingMetadata_radioButton")
        self.verticalLayout_2.addWidget(self.existingMetadata_radioButton)
        self.chooseFile_widget = QgsFileWidget(Dialog)
        self.chooseFile_widget.setObjectName("chooseFile_widget")
        self.verticalLayout_2.addWidget(self.chooseFile_widget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.vertical_line = QtWidgets.QFrame(Dialog)
        self.vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_line.setObjectName("vertical_line")
        self.horizontalLayout.addWidget(self.vertical_line)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.newMetadata_radioButton = QtWidgets.QRadioButton(Dialog)
        self.newMetadata_radioButton.setEnabled(True)
        self.newMetadata_radioButton.setObjectName("newMetadata_radioButton")
        self.verticalLayout_3.addWidget(self.newMetadata_radioButton)
        self.newFile_widget = QgsFileWidget(Dialog)
        self.newFile_widget.setEnabled(False)
        self.newFile_widget.setObjectName("newFile_widget")
        self.verticalLayout_3.addWidget(self.newFile_widget)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontal_line = QtWidgets.QFrame(Dialog)
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontal_line.setObjectName("horizontal_line")
        self.verticalLayout.addWidget(self.horizontal_line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addSet_lbl = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.addSet_lbl.setFont(font)
        self.addSet_lbl.setObjectName("addSet_lbl")
        self.horizontalLayout_2.addWidget(self.addSet_lbl)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.chooseSet_widget = QgsFileWidget(Dialog)
        self.chooseSet_widget.setObjectName("chooseSet_widget")
        self.horizontalLayout_2.addWidget(self.chooseSet_widget)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.titleForm_lbl = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.titleForm_lbl.setFont(font)
        self.titleForm_lbl.setObjectName("titleForm_lbl")
        self.verticalLayout.addWidget(self.titleForm_lbl)
        self.form_scrollArea = QtWidgets.QScrollArea(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.form_scrollArea.sizePolicy().hasHeightForWidth())
        self.form_scrollArea.setSizePolicy(sizePolicy)
        self.form_scrollArea.setWidgetResizable(True)
        self.form_scrollArea.setObjectName("form_scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 558, 359))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.streszczenie_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.streszczenie_lbl.setObjectName("streszczenie_lbl")
        self.gridLayout_2.addWidget(self.streszczenie_lbl, 2, 0, 1, 1)
        self.typZbioru_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.typZbioru_lbl.setObjectName("typZbioru_lbl")
        self.gridLayout_2.addWidget(self.typZbioru_lbl, 3, 0, 1, 1)
        self.adresZbioruDanych_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.adresZbioruDanych_lbl.setObjectName("adresZbioruDanych_lbl")
        self.gridLayout_2.addWidget(self.adresZbioruDanych_lbl, 4, 0, 1, 1)
        self.tytulZbioru_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.tytulZbioru_lbl.setObjectName("tytulZbioru_lbl")
        self.gridLayout_2.addWidget(self.tytulZbioru_lbl, 0, 0, 1, 1)
        self.dataUtworzenia_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.dataUtworzenia_lbl.setObjectName("dataUtworzenia_lbl")
        self.gridLayout_2.addWidget(self.dataUtworzenia_lbl, 5, 0, 1, 1)
        self.tytulZbioru_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tytulZbioru_lineEdit.sizePolicy().hasHeightForWidth())
        self.tytulZbioru_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.tytulZbioru_lineEdit.setFont(font)
        self.tytulZbioru_lineEdit.setObjectName("tytulZbioru_lineEdit")
        self.gridLayout_2.addWidget(self.tytulZbioru_lineEdit, 0, 1, 1, 4)
        self.streszczenie_textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_2)
        self.streszczenie_textEdit.setObjectName("streszczenie_textEdit")
        self.gridLayout_2.addWidget(self.streszczenie_textEdit, 2, 1, 1, 5)
        self.typZbioru_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.typZbioru_lineEdit.setFont(font)
        self.typZbioru_lineEdit.setObjectName("typZbioru_lineEdit")
        self.gridLayout_2.addWidget(self.typZbioru_lineEdit, 3, 1, 1, 4)
        self.dataUtworzenia_dateEdit = QtWidgets.QDateEdit(self.scrollAreaWidgetContents_2)
        self.dataUtworzenia_dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 5, 22), QtCore.QTime(0, 0, 0)))
        self.dataUtworzenia_dateEdit.setObjectName("dataUtworzenia_dateEdit")
        self.gridLayout_2.addWidget(self.dataUtworzenia_dateEdit, 5, 1, 1, 1)
        self.adresZbioruDanych_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.adresZbioruDanych_lineEdit.setFont(font)
        self.adresZbioruDanych_lineEdit.setObjectName("adresZbioruDanych_lineEdit")
        self.gridLayout_2.addWidget(self.adresZbioruDanych_lineEdit, 4, 1, 1, 4)
        self.form_scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.form_scrollArea)
        self.empty1_lbl = QtWidgets.QLabel(Dialog)
        self.empty1_lbl.setText("")
        self.empty1_lbl.setObjectName("empty1_lbl")
        self.verticalLayout.addWidget(self.empty1_lbl)
        self.send_lbl = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.send_lbl.setFont(font)
        self.send_lbl.setObjectName("send_lbl")
        self.verticalLayout.addWidget(self.send_lbl)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        self.server_checkBox = QtWidgets.QCheckBox(Dialog)
        self.server_checkBox.setObjectName("server_checkBox")
        self.gridLayout.addWidget(self.server_checkBox, 0, 2, 1, 1)
        self.email_checkBox = QtWidgets.QCheckBox(Dialog)
        self.email_checkBox.setObjectName("email_checkBox")
        self.gridLayout.addWidget(self.email_checkBox, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 3, 1, 1)
        self.server_toolBtn = QtWidgets.QToolButton(Dialog)
        self.server_toolBtn.setObjectName("server_toolBtn")
        self.gridLayout.addWidget(self.server_toolBtn, 1, 2, 1, 1)
        self.email_toolBtn = QtWidgets.QToolButton(Dialog)
        self.email_toolBtn.setObjectName("email_toolBtn")
        self.gridLayout.addWidget(self.email_toolBtn, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.empty2_lbl = QtWidgets.QLabel(Dialog)
        self.empty2_lbl.setText("")
        self.empty2_lbl.setObjectName("empty2_lbl")
        self.verticalLayout.addWidget(self.empty2_lbl)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.prev_btn = QtWidgets.QPushButton(Dialog)
        self.prev_btn.setObjectName("prev_btn")
        self.horizontalLayout_3.addWidget(self.prev_btn)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.validateAndSave_btn = QtWidgets.QPushButton(Dialog)
        self.validateAndSave_btn.setObjectName("validateAndSave_btn")
        self.horizontalLayout_3.addWidget(self.validateAndSave_btn)
        self.send_btn = QtWidgets.QPushButton(Dialog)
        self.send_btn.setEnabled(False)
        self.send_btn.setObjectName("send_btn")
        self.horizontalLayout_3.addWidget(self.send_btn)
        self.next_btn = QtWidgets.QPushButton(Dialog)
        self.next_btn.setEnabled(True)
        self.next_btn.setObjectName("next_btn")
        self.horizontalLayout_3.addWidget(self.next_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title_lbl.setText(_translate("Dialog", "Metadane"))
        self.existingMetadata_radioButton.setText(_translate("Dialog", "Wybierz istniejący plik z metadanymi"))
        self.newMetadata_radioButton.setText(_translate("Dialog", "Utwórz nowy plik z metadanymi"))
        self.addSet_lbl.setText(_translate("Dialog", "Wybierz plik GML dla zbioru APP (opcjonalne)"))
        self.titleForm_lbl.setText(_translate("Dialog", "Formularz metadanych:"))
        self.streszczenie_lbl.setText(_translate("Dialog", "Streszczenie"))
        self.typZbioru_lbl.setText(_translate("Dialog", "Typ zbioru"))
        self.adresZbioruDanych_lbl.setText(_translate("Dialog", "Adres zbioru danych"))
        self.tytulZbioru_lbl.setText(_translate("Dialog", "Tytuł zbioru"))
        self.dataUtworzenia_lbl.setText(_translate("Dialog", "Data utworzenia"))
        self.adresZbioruDanych_lineEdit.setText(_translate("Dialog", "Podaj adres URI"))
        self.send_lbl.setText(_translate("Dialog", "Wybierz, gdzie chcesz wysłać plik z metadanymi (opcjonalne):"))
        self.server_checkBox.setText(_translate("Dialog", "Wyślij na serwer katalogowy"))
        self.email_checkBox.setText(_translate("Dialog", "Wyślij na adres email"))
        self.server_toolBtn.setText(_translate("Dialog", "..."))
        self.email_toolBtn.setText(_translate("Dialog", "..."))
        self.prev_btn.setText(_translate("Dialog", "Wstecz"))
        self.validateAndSave_btn.setText(_translate("Dialog", "Waliduj/zapisz"))
        self.send_btn.setText(_translate("Dialog", "Wyślij"))
        self.next_btn.setText(_translate("Dialog", "Dalej"))
from qgsfilewidget import QgsFileWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
