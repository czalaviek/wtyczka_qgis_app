# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pytanie_dialog_base.ui'
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
        Dialog.setMinimumSize(QtCore.QSize(0, 196))
        Dialog.setSizeGripEnabled(True)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.settings_btn = QtWidgets.QPushButton(Dialog)
        self.settings_btn.setMaximumSize(QtCore.QSize(27, 16777215))
        self.settings_btn.setObjectName("settings_btn")
        self.horizontalLayout_2.addWidget(self.settings_btn)
        self.help_btn = QtWidgets.QPushButton(Dialog)
        self.help_btn.setMaximumSize(QtCore.QSize(27, 16777215))
        self.help_btn.setObjectName("help_btn")
        self.horizontalLayout_2.addWidget(self.help_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.empty1_lbl = QtWidgets.QLabel(Dialog)
        self.empty1_lbl.setText("")
        self.empty1_lbl.setObjectName("empty1_lbl")
        self.verticalLayout.addWidget(self.empty1_lbl)
        self.title_lbl = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title_lbl.setFont(font)
        self.title_lbl.setWordWrap(True)
        self.title_lbl.setObjectName("title_lbl")
        self.verticalLayout.addWidget(self.title_lbl)
        self.empty2_lbl = QtWidgets.QLabel(Dialog)
        self.empty2_lbl.setText("")
        self.empty2_lbl.setObjectName("empty2_lbl")
        self.verticalLayout.addWidget(self.empty2_lbl)
        self.instruction_scrollArea = QtWidgets.QScrollArea(Dialog)
        self.instruction_scrollArea.setWidgetResizable(True)
        self.instruction_scrollArea.setObjectName("instruction_scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 564, 274))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.instruction_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.instruction_lbl.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.instruction_lbl.setWordWrap(True)
        self.instruction_lbl.setObjectName("instruction_lbl")
        self.gridLayout.addWidget(self.instruction_lbl, 0, 0, 1, 1)
        self.instruction_scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.instruction_scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.zbior_btn = QtWidgets.QPushButton(Dialog)
        self.zbior_btn.setObjectName("zbior_btn")
        self.horizontalLayout.addWidget(self.zbior_btn)
        self.app_btn = QtWidgets.QPushButton(Dialog)
        self.app_btn.setObjectName("app_btn")
        self.horizontalLayout.addWidget(self.app_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.settings_btn.setText(_translate("Dialog", "U"))
        self.help_btn.setText(_translate("Dialog", "?"))
        self.title_lbl.setText(_translate("Dialog", "Czy będziesz pracować ze zbiorem danych przestrzennych aktów planowania przestrzennego (zbiór APP), czy z danymi przestrzennymi dla pojedynczego aktu planowania przestrzennego (APP)?"))
        self.instruction_lbl.setText(_translate("Dialog", "<html><head/><body><p>APP – obejmuje dane przestrzenne dla jednego aktu planowania przestrzennego np. dla wybranego miejscowego planu zagospodarowania przestrzennego. </p><p>Zbiór APP – obejmuje zestaw danych przestrzennych dla wielu (co najmniej jednego) aktów planowania przestrzennego tego samego rodzaju, występujących w danej jednostce podziału terytorialnego np. miejscowe plany zagospodarowania przestrzennego gminy XXX. </p><p>Szczegółowe informacje nt. zakresu danych ujętych w zbiorze znajdziesz w specyfikacji danych.  </p><p>Aby utworzyć zbiór APP, należy wcześniej przygotować pojedyncze pliki GML dla każdego APP, który zostanie włączony do tego zbioru.   </p><p>Dane przestrzenne dla jednego APP obejmują: <br/><span style=\" font-family:\'Symbol\';\">· </span>rysunek lub rysunki APP, w postaci plików rastrowych z nadaną georeferencją, w formacie GeoTIFF, wraz z informacją o adresie internetowym pod którym jest on opublikowany, <br/><span style=\" font-family:\'Symbol\';\">· </span>granicę obszaru objętego APP określoną w układzie PL-1992 lub PL-2000, posiadającą reprezentację geometryczną w postaci jednego poligonu lub multipoligonu (w przypadku obiektów wieloczęściowych), <br/><span style=\" font-family:\'Symbol\';\">· </span>informacje nt. dokumentów powiązanych z danym APP (np. uchwała o przystąpieniu do sporządzenia APP, czy uchwała uchwalająca APP). </p></body></html>"))
        self.zbior_btn.setText(_translate("Dialog", "Zbiór APP"))
        self.app_btn.setText(_translate("Dialog", "APP"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
