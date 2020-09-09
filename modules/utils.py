# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from qgis.PyQt.QtCore import Qt, QRegExp, QVariant
from qgis.core import QgsVectorLayer
import re
import os
import itertools
import xml.etree.ElementTree as ET
from .models import FormElement
from . import dictionaries
import datetime
import uuid
import random


def validateDatasetId(datasetId):
    """sprawdza czy id ma poprawną formę"""
    pattern = r'PL.ZIPPZP.\d+/\d{1}[02468]{1}(\d{0}|\d{2}|\d{4})-(PZPW|MPZP|SUIKZP){1}'
    return True if re.fullmatch(pattern, datasetId) else False


def settingsValidateDatasetId(przestrzenNazw):
    """Walidacja idIIP pod kątem prawidłowej struktury przestrzeni nazw"""
    if not przestrzenNazw.startswith('PL.ZIPPZP.'):
        return False  # Brak wymaganej sekwencji - kod RP, kod dla zbioru
    try:
        numer = przestrzenNazw.split('.')[2].split('/')[0]
        teryt = przestrzenNazw.split('/')[1].split('-')[0]
    except:
        return False
    if not numer.isdigit():
        return False  # numer porządkowy nie jest liczbą całkowitą
    if not validate_teryt(teryt, rodzaj='None'):
        return False
    return True  # IIP prawidłowe


def validateDatasetUri(datasetUri):
    """sprawdza czy Uri ma poprawną formę"""
    pattern = r'http://zagospodarowanieprzestrzenne.gov.pl/app/AktPlanowaniaPrzestrzennego/PL.ZIPPZP.\d+/\d{1}[02468]{1}(\d{0}|\d{2}|\d{4})-(PZPW|MPZP|SUIKZP){1}/'
    return True if re.fullmatch(pattern, datasetUri) else False


def validateEmailAddress(email):
    """sprawdza czy adres email ma poprawną formę"""
    pattern = r'[a-zA-Z0-9_\-+]+@[a-zA-Z0-9\-\.]+.[a-zA-Z0-9]{2,10}'
    return True if re.fullmatch(pattern, email) else False


def generateUUID():
    """generuje UUID"""
    rd = random.Random()
    return str(uuid.UUID(int=rd.getrandbits(128)))


def oldestQDateTime(qDateTimelist):
    """zwraca najstarszą datę z listy dat QDateTime"""
    if type(qDateTimelist) == list and len(qDateTimelist) > 0:
        oldest = qDateTimelist[0]
        for date in qDateTimelist:
            if date > oldest:
                oldest == date
        return oldest


def getKeyByValue(dictionary, value):
    """Zwraca klucz słownika na podstawie wartości"""
    for key, v in dictionary.items():
        if v == value:
            return key
    return None


def showPopup(title, text, icon=QMessageBox.Information):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)
    msg.setStandardButtons(QMessageBox.Ok)
    return msg.exec_()


def validate_teryt_voivo(teryt):
    if int(teryt) % 2 == 1 or int(teryt) == 0:
        return False
    return True


def validate_teryt_county(teryt):
    if validate_teryt_voivo(teryt[0:2]):
        if 0 < int(teryt[2:4]) < 100:
            return True
    return False


def validate_teryt(teryt, rodzaj='None'):
    # Walidacja terytu
    if not teryt.isdigit():
        return False
    elif len(teryt) == 2 and validate_teryt_voivo(teryt):  # wojewodztwo
        if rodzaj != 'PZPW' and rodzaj != 'None':
            return False
        return True  # sprawdzić, czy rodzaj zbioru poprawny
    elif len(teryt) == 4 and validate_teryt_county(teryt) and rodzaj != 'None':
        # if rodzaj != 'RSZM':
        #     return False
        return True  # sprawdzić, czy rodzaj zbioru poprawny
    elif len(teryt) == 6 and validate_teryt_county(teryt):
        if rodzaj != 'MPZP' and rodzaj != 'SUIKZP' and rodzaj != 'None':
            return False
        if 0 < int(teryt[4:6]) < 100:
            return True
        return False
    else:
        return False


def validate_IIP(przestrzenNazw):
    """Walidacja idIIP pod kątem prawidłowej struktury przestrzeni nazw"""
    if not przestrzenNazw.startswith('PL.ZIPPZP.'):
        return False  # Brak wymaganej sekwencji - kod RP, kod dla zbioru
    try:
        numer = przestrzenNazw.split('.')[2].split('/')[0]
        rodzaj = przestrzenNazw.split('-')[1]
        teryt = przestrzenNazw.split('/')[1].split('-')[0]

    except:
        return False
    if not numer.isdigit():
        return False  # numer porządkowy nie jest liczbą całkowitą

    rodzaj_list = ['PZPW', 'SUIKZP', 'MPZP']
    if rodzaj not in rodzaj_list:
        # showPopup('Błąd identyfikatora', '')
        return False

    if not validate_teryt(teryt, rodzaj):
        return False

    return True  # IIP prawidłowe


def isAppOperative(gmlPath):
    """sprawdza czy zbiór APP jest obowiązującym zbiorem"""
    ns = {'xsi': "http://www.w3.org/2001/XMLSchema",
          'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gco': 'http://www.isotc211.org/2005/gco',
          'xlink': 'http://www.w3.org/1999/xlink',
          'gml': "http://www.opengis.net/gml/3.2",
          'wfs': 'http://www.opengis.net/wfs/2.0',
          'gmlexr': "http://www.opengis.net/gml/3.3/exr"}

    # statusPath = 'wfs:member/app:AktPlanowaniaPrzestrzennego/app:status[@xlink:title="prawnie wiążący lub realizowany"]'
    statusPath = 'wfs:member/app:AktPlanowaniaPrzestrzennego/app:status'

    root = ET.parse(gmlPath).getroot()
    find = root.find(statusPath, ns)
    if find is not None:
        if find.attrib['{http://www.w3.org/1999/xlink}title'] == 'prawnie wiążący lub realizowany':
            return True
    return False


def checkZbiorGeometryValidity(gmlFilesPath):
    """sprawdza integralność zbioru APP, czy np. obrysy się nie przecinają
    na podstawie listy ścieżek do plików GML"""
    geoms = []
    for gmlPath in gmlFilesPath:
        if isAppOperative(gmlPath):  # jest obowiązujący
            layer = QgsVectorLayer(gmlPath, "", 'ogr')
            if not layer.isValid():
                return [False, "Niepoprawna warstwa wektorowa w pliku %s" % gmlPath]
            if not layer.featureCount():
                return [False, "Brak obiektów przestrzennych w warstwie %s" % gmlPath]
            feat = next(layer.getFeatures())
            geoms.append((feat.geometry(), gmlPath))
    for a, b in itertools.combinations(geoms, 2):
        geom1 = a[0]
        path1 = a[1]
        geom2 = b[0]
        path2 = b[1]
        if geom1.overlaps(geom2):
            return [False, "Geometrie swóch APP w ramach jednego zbioru nie mogą na siebie nachodzić. Dotyczy plików\n\n%s\n%s" % (path1, path2)]
    return [True]


def getNamespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''


def createFormElements(attribute):
    """Tworzy listę obiektów klasy 'FormElement'
    na podstawie pliku xsd"""

    xsd = os.path.join(os.path.dirname(__file__),
                       'validator', 'planowaniePrzestrzenne.xsd')

    ns = {'glowny': "http://www.w3.org/2001/XMLSchema",
          'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gml': "http://www.opengis.net/gml/3.2",
          'gmlexr': "http://www.opengis.net/gml/3.3/exr"}
    formElements = []

    tree = ET.parse(xsd)
    root = tree.getroot()

    complexType = root.find(
        "glowny:complexType[@name='" + attribute + "']", ns)
    sequence = complexType[0][0][0]  # sekwencja z listą pól
    for element in sequence:

        if 'type' in element.attrib:
            elementType = element.attrib['type']
        else:
            elementComplexType = element.find("glowny:complexType", ns)
            elementAttrib = elementComplexType[0][0].attrib
            elementType = elementAttrib['base']

        elementName = element.attrib['name']
        formElement = FormElement(
            name=elementName,
            type=elementType,
            form=attribute
        )

        if 'minOccurs' in element.attrib:
            formElement.setMinOccurs(element.attrib['minOccurs'])
        if 'maxOccurs' in element.attrib:
            formElement.setMaxOccurs(element.attrib['maxOccurs'])

        # documentation
        documentation = element.find("glowny:annotation", ns).find(
            "glowny:documentation", ns)
        formElement.setDocumentation(documentation.text)

        # zdefiniowany w app complextype
        if elementType[:4] == 'app:':

            formElement.markAsComplex()  # ustawia .isComplex = True
            name = str(elementType).replace('Property', '').split(':')[-1]

            complexSequence = root.find(
                "glowny:complexType[@name='%s']" % name, ns)[0]

            for complexElement in complexSequence:
                if 'type' in complexElement.attrib:
                    # jeżeli jest atrybut 'type'
                    _formType = complexElement.attrib['type']
                else:
                    # jeżeli nie ma atrybutu 'type'
                    _formType = "anyURI"
                elementName = complexElement.attrib['name']

                innerFormElement = FormElement(
                    name=elementName,
                    type=_formType,
                    form=attribute
                )

                if elementName == 'wersjaId' and (
                        attribute == 'RysunekAktuPlanowniaPrzestrzenegoType'
                    or
                        attribute == 'AktPlanowaniaPrzestrzennegoType'
                ):
                    innerFormElement.setMinOccurs('1')
                else:
                    if 'minOccurs' in complexElement.attrib:
                        innerFormElement.setMinOccurs(
                            complexElement.attrib['minOccurs'])
                    if 'maxOccurs' in complexElement.attrib:
                        innerFormElement.setMaxOccurs(
                            complexElement.attrib['maxOccurs'])

                # complex documentation
                complexDocumentation = complexElement.find(
                    "glowny:annotation", ns).find("glowny:documentation", ns)
                innerFormElement.setDocumentation(complexDocumentation.text)
                formElement.setInnerFormElement(innerFormElement)

        formElements.append(formElement)

    return formElements


def createFormElementsRysunekAPP():
    """Tworzy listę obiektów klasy 'FormElement'
    na podstawie pliku xsd dla Rysunku APP"""

    return createFormElements('RysunekAktuPlanowniaPrzestrzenegoType')


def createFormElementsDokumentFormalny():
    """Tworzy listę obiektów klasy 'FormElement'
    na podstawie pliku xsd dla Rysunku APP"""

    return createFormElements('DokumentFormalnyType')


def createFormElementsAktPlanowaniaPrzestrzennego():
    """Tworzy listę obiektów klasy 'FormElement'
    na podstawie pliku xsd dla Rysunku APP"""

    return createFormElements('AktPlanowaniaPrzestrzennegoType')


def layout_widgets(layout):
    """lista widgetow/layoutow wewnątrz layoutu"""
    return (layout.itemAt(i) for i in range(layout.count()))


def layout_widget_by_name(layout, name):
    """wyszukuje widgeta wedlug nazwy wewnatrz layoutu
    Do wykorystania również w trakcie tworzenia layoutu (np. QHBoxLayout)"""
    for item in layout_widgets(layout):
        if isinstance(item, QLayout):   # zagnieżdzony layout
            result = layout_widget_by_name(layout=item, name=name)
            if result:
                return result
        elif isinstance(item, QWidgetItem):
            widget = item.widget()
            # print(widget.objectName())
            if name == widget.objectName():
                return widget
        else:
            raise NotImplementedError


def all_layout_widgets(layout):
    """lista wszystkich widgetow/layoutow wewnątrz layoutu uwzględniając zagnieżdzone elementy"""
    types = [QLineEdit, QLabel, QComboBox, QCheckBox, QDateEdit, QListWidget]
    allWidgets = []
    for item in layout_widgets(layout):
        if isinstance(item, QLayout):   # zagnieżdzony layout
            innerWidgets = all_layout_widgets(layout=item)
            allWidgets.extend(innerWidgets)
        elif isinstance(item, QWidgetItem):
            widget = item.widget()
            if isinstance(widget, QScrollArea):
                innerWidgets = all_layout_widgets(
                    layout=widget.widget().layout())
                allWidgets.extend(innerWidgets)
            elif isinstance(widget, QGroupBox):
                innerWidgets = all_layout_widgets(layout=widget.layout())
                allWidgets.extend(innerWidgets)
            else:   # zwykly widget
                allWidgets.append(widget)
        elif isinstance(item, QSpacerItem):
            pass
        else:
            raise NotImplementedError
    return allWidgets


def getWidgets(layout, types=[QPushButton, QLabel, QTextEdit, QLineEdit, QDateEdit, QComboBox, QListWidget]):
    wtypes = types
    qreg = QRegExp(r'.*')
    mywidgets = {}

    for t in wtypes:
        mywidgets[t] = layout.findChildren(t, qreg)
    return(mywidgets)


def getWidgetsByType(layout, searchObjectType):
    """zwraca listę widgeów danego typu wewnątrz layoutu"""
    qreg = QRegExp(r'.*')
    widgets = layout.findChildren(searchObjectType, qreg)
    return widgets


def getWidgetByName(layout, searchObjectType, name):
    """zwraca widget o zadanym typie i nazwie wewnątrz layoutu statycznego
    (np. wewnątrz całego okna formularza
    Do wykorzystania gdy już są zbudowane formularze/widoki"""
    widget = layout.findChild(searchObjectType, name)
    return widget


def makeXmlComplex(tag, item, element):
    ComplexItem = ET.SubElement(
        item, element.type.replace('PropertyType', ''))
    for inner in element.innerFormElements:
        if inner.refObject.text() != '':
            subItem = ET.SubElement(ComplexItem, tag + inner.name)
            subItem.text = inner.refObject.text()


def makeXmlListElements(tag, item, element, formData, slownik={}):
    # Tworzenie wewnętrzych elementów i wypełnianie ich
    nilReason = ["inapplicable", "missing", "template", "unknown", "withheld"]
    for fee in formData:
        if element.isComplex():
            subItem = ET.SubElement(item, tag + element.name)
            ComplexItem = ET.SubElement(
                subItem, element.type.replace('PropertyType', ''))
            for innerElement in element.innerFormElements:
                for fd in fee.keys():

                    # try:  # Sprawdzanie Nil == True
                    #     if fee[innerElement.name+'_lineEdit_nilReason_chkbx']:
                    #         makeNil(
                    #             innerItem, innerElement, nilReason[fee[innerElement.name+'_lineEdit_nilReason_cmbbx']])  # fee[innerElement.name+'_lineEdit_nilReason_cmbbx'])
                    # except:
                    #     pass
                    if innerElement.name in fd:

                        if fee[fd] != '':
                            innerItem = ET.SubElement(
                                ComplexItem, tag+innerElement.name)
                            if innerElement.type == 'date':
                                innerItem.text = fee[fd].replace(
                                    'Thh:mm:ss', '')
                            else:
                                innerItem.text = fee[fd]
                        break
        else:
            multiItem = ET.SubElement(
                item, tag+element.name)
            for fd in fee.keys():
                try:  # Sprawdzanie Nil == True
                    if fee[innerElement.name+'_lineEdit_nilReason_chkbx']:
                        makeNil(
                            innerItem, innerElement, fee[innerElement.name+'_lineEdit_nilReason_cmbbx'])
                except:
                    pass
                if element.name in fd:
                    multiItem.text = fee[fd]
                    break


def make_polygon(polygons):
    BoundaryList = []
    # pierwszy poligon jest outerBoundary, kolejne innerBoundary
    for polygon in polygons:
        Boundary = ''
        for point in polygon:

            Boundary = ' '.join(
                [Boundary, "{} {}".format(point.x(), point.y())])
        BoundaryList.append(Boundary[1:])
    return(BoundaryList)


def getCoordinates(obrysLayer):
    CoordinatesList = []
    coordinates = ''
    for f in obrysLayer.getFeatures():
        obrys = f.geometry()
    # getGeometry - wystąpił przypadek zmiany id, getFeatures jest bezpieczniejsze
    # obrys = obrysLayer.getGeometry(1)
    if obrys.isMultipart():
        for poligon in obrys.asMultiPolygon():
            CoordinatesList.append(make_polygon(poligon))
    else:
        # Poligon, który został multipoligonem utrzymuje typ multipoligona nawet jako zwykły poligon
        CoordinatesList.append(make_polygon(obrys.asPolygon()))
    return CoordinatesList


def makeSpatialExtent(node, CoordinatesList):
    for polygon in CoordinatesList:
        isBoundary = True  # 0 - True, >0 - False
        subItem2 = ET.SubElement(node, 'gml:surfaceMember')
        subItem3 = ET.SubElement(subItem2, 'gml:Polygon')
        for coordinates in polygon:
            if isBoundary == True:
                subItem4 = ET.SubElement(subItem3, 'gml:exterior')
            else:
                subItem4 = ET.SubElement(subItem3, 'gml:interior')
            subItem5 = ET.SubElement(subItem4, 'gml:LinearRing')
            subItem6 = ET.SubElement(subItem5, 'gml:posList')
            subItem6.text = coordinates
            isBoundary = False


def makeXML(docName, elements, formData, obrysLayer=None):
    # TODO Dodać obsługę nillable: https://inspire.ec.europa.eu/forum/discussion/view/61478/contents-of-attribute-nilreason-eg-unknown-vs-httpinspireeceuropaeucodelistvoidreasonvalueunknown
    # TODO Dodać iterację po obiektach z licznością *
    import datetime
    dict_map = {
        'status': dictionaries.statusListaKodowa,
        'poziomHierarchii': dictionaries.poziomyHierarchii,
        'nilReason': dictionaries.nilReasons,
        'zasiegPrzestrzenny': dictionaries.ukladyOdniesieniaPrzestrzennego,
        'typPlanu': dictionaries.typyPlanu,
        'dziennikUrzedowy': dictionaries.dziennikUrzedowyKod,
        'ukladOdniesieniaPrzestrzennego': dictionaries.ukladyOdniesieniaPrzestrzennego,
        'data': dictionaries.cI_DateTypeCode
    }
    IPP = formData['idIIP_lineEdit']
    if obrysLayer != None:
        CoordinatesList = getCoordinates(obrysLayer)
        epsg = str(obrysLayer.crs().authid()).split(':')[1]
        # Układ współrzędnych
        for crs in dict_map['ukladOdniesieniaPrzestrzennego'].values():
            if epsg in crs:
                srsName = crs
            else:
                # TODO co w przypadku, gdy CRS jest inny niż w słowniku - rozwiązanie tymczasowe
                srsName = "http://www.opengis.net/def/crs/EPSG/0/2180"
    else:
        CoordinatesList = None

    # Elementy, których wartości nie ma w formularzu
    pomijane_elementy = formSkippedElements(docName)

    # Strefa czasowa timezone jest ustawiona na sztywno
    root_data = {
        'timeStamp': datetime.datetime.utcnow().isoformat()+'Z',
        'numberReturned': "1",
        'numberMatched': "unknown",
    }
    # Przestrzenie nazw ustawione na sztywno
    namespaces = {
        'xmlns:gco': "http://www.isotc211.org/2005/gco",
        'xmlns:gmd': "http://www.isotc211.org/2005/gmd",
        'xmlns:gml': "http://www.opengis.net/gml/3.2",
        'xmlns:wfs': "http://www.opengis.net/wfs/2.0",
        'xmlns:xlink': "http://www.w3.org/1999/xlink",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xmlns:app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
        'xsi:schemaLocation': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0 ../appSchema/appSchema_app_v0_0_1/planowaniePrzestrzenne.xsd http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd"
    }
    # create the file structure
    data = ET.Element('wfs:FeatureCollection')
    datamember = ET.SubElement(data, 'wfs:member')

    for rd in root_data.keys():
        data.set(rd, root_data[rd])

    for ns in namespaces.keys():
        data.set(ns, namespaces[ns])

    tag = 'app:'
    items = ET.SubElement(datamember, tag + docName)
    items.set('gml:id', IPP)
    item = ET.SubElement(items, 'gml:identifier')
    codeSpace = 'http://zagospodarowanieprzestrzenne.gov.pl/app'
    item.set('codeSpace', codeSpace)
    item.text = '/'.join([codeSpace, docName, IPP.replace('_', '/')])

    for element in elements:
        if element.name not in pomijane_elementy:
            # if 'ReferenceType' not in element.type:
            item = ET.SubElement(items, tag + element.name)
            # Tworzenie wewnętrzego elementu obiektu złożonego
            if element.isComplex() == True:
                for fd in formData.keys():
                    if element.name in fd:
                        if type(formData[fd]) == list:
                            for params in formData[fd]:
                                makeXmlComplex(tag, item, element, params)
                        else:
                            makeXmlComplex(tag, item, element, formData)

            elif element.name == 'zasiegPrzestrzenny':
                subItem1 = ET.SubElement(item, 'gml:MultiSurface')
                subItem1.set('srsDimension', '2')
                subItem1.set('srsName', srsName)
                makeSpatialExtent(subItem1, CoordinatesList)
            else:  # Tworzenie elementów elementarnych
                for fd in formData.keys():
                    if element.name in fd:
                        if 'ReferenceType' in element.type:
                            slownik = dict_map[element.name]
                            try:
                                # TODO Sprawdzić dla wszystkich formularzy
                                if element.name == 'typPlanu':
                                    link = 'http://zagospodarowanieprzestrzenne.gov.pl/codelist/AktPlanowaniaPrzestrzennegoKod/'
                                elif element.name == 'dziennikUrzedowy':
                                    link = 'http://zagospodarowanieprzestrzenne.gov.pl/codelist/DziennikUrzedowyKod/'
                                else:
                                    link = ''
                                if 'http' in (link+slownik[formData[fd]]):
                                    item.set(
                                        'xlink:href', (link+slownik[formData[fd]]))
                                    item.set('xlink:title', formData[fd])
                            except:
                                item.set('xlink:href', formData[fd])
                                item.set('xlink:title', formData[fd])

                        elif element.name == 'ukladOdniesieniaPrzestrzennego':
                            slownik = dict_map[element.name]
                            item.text = slownik[formData[fd]]
                        elif element.type == 'date':
                            item.text = formData[fd].toString("yyyy-MM-dd")
                        elif element.type == 'gmd:CI_Date_PropertyType':
                            slownik = dict_map[element.name]
                            item1 = ET.SubElement(item, 'gml:CI_Date')
                            item2 = ET.SubElement(item1, 'gml:date')
                            item3 = ET.SubElement(item2, 'gco:Date')
                            item3.text = formData[fd].toString("yyyy-MM-dd")
                            # item4 = ET.SubElement(item2, 'gmd:DateType')
                            # item5 = ET.SubElement(item4, 'gmd:CI_DateTypeCode')
                            # item5.set(
                            #     'codeList', 'http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_DateTypeCode')
                            # item5.set('codeListValue', slownik[formData[fd]])
                            # item5.text = formData[fd]
                        elif element.type == 'dateTime':
                            item.text = formData[fd].toString(
                                "yyyy-MM-ddThh:mm:ss")
                        else:
                            item.text = formData[fd]
                        break
    return(data)


def formSkippedElements(docName):
    """Zwraca listę atrybutów dla poszczególnego dokumentu, które nie występują w formularzu"""
    pomijane = []
    if docName == 'AktPlanowaniaPrzestrzennego':
        pomijane = ['dokument', 'dokumentPrzystepujacy', 'dokumentUchwalajacy',
                    'dokumentZmieniajacy', 'dokumentUchylajacy', 'dokumentUniewazniajacy', 'rysunek']
    elif docName == 'RysunekAktuPlanowniaPrzestrzenego':
        pomijane = ['plan']
    elif docName == 'DokumentFormalny':
        pomijane = ['przystapienie', 'uchwala',
                    'zmienia', 'uchyla', 'uniewaznia']
    return(pomijane)


def formSkippedObjects(docName):
    """Zwraca listę nazw obiektów edytowalnych w formularzu, które nie podlegają umieszczeniu w xml"""
    pomijane = []
    if docName == 'AktPlanowaniaPrzestrzennego':
        pomijane = ['mapaPodkladowa_lineEdit', 'referencja_lineEdit',
                    'data_dateTimeEdit', 'lacze_lineEdit', 'lacze_lineEdit_nilReason_chkbx']
    elif docName == 'RysunekAktuPlanowniaPrzestrzenego':
        pomijane = []
    elif docName == 'DokumentFormalny':
        pomijane = []
    return(pomijane)


def checkForNillable(fe, element):
    nil = False  # Brak Nillable
    if fe.isNillable:
        widgets = all_layout_widgets(element[1])
        for widget in widgets:
            if type(widget).__name__ == 'QCheckBox':
                if widget.isChecked() == True:
                    nil = True
    return nil


def checkElement(fe, element):
    try:  # LineEdit
        if fe.minOccurs > 0 and (element.dateTime().toString() is None or element.dateTime().toString() == 'NULL' or element.dateTime().toString() == ''):
            return False
    except:
        try:
            if fe.minOccurs > 0 and (element.text() is None or element.text() == 'NULL' or element.text() == ''):
                return False

        except:
            try:  # Combobox
                if fe.minOccurs > 0 and (element.currentText() is None or element.currentText() == ''):
                    return False
            except:
                try:  # ListWidget
                    if fe.minOccurs > 0 and element.count() > 0:
                        return False
                except:
                    print('checkElement')
    return True


def getFormElementByName(formElements, name):
    for fe in formElements:
        if fe.name == name:
            return fe
        else:
            for inner in fe.innerFormElements:
                if inner.name == name:
                    return inner
    return None


def validate_typPlanu(formElements):
    """walidacja typPlanu"""
    typPlanu = getFormElementByName(formElements, 'typPlanu')
    mapaPodkladowa = getFormElementByName(formElements, 'mapaPodkladowa')
    przestrzenNazw = getFormElementByName(formElements, 'przestrzenNazw')
    rodzajZbioru = przestrzenNazw.refObject.text().split('-')[-1]
    if typPlanu is not None:
        rodzajZbioru_map = {
            'PZPW': ['plan zagospodarowania przestrzennego województwa'],
            'SUIKZP': ['studium uwarunkowań i kier. zagosp. przestrz. gminy'],
            'MPZP': ['miejscowy plan zagospodarowania przestrzennego', 'miejscowy plan odbudowy', 'miejscowy plan rewitalizacji']
        }

        typy = ["miejscowy plan zagospodarowania przestrzennego", "studium uwarunkowań i kier. zagosp. przestrz. gminy",
                "miejscowy plan odbudowy", "miejscowy plan rewitalizacji"]
        if typPlanu.refObject.currentText() in typy and len(getListWidgetItems(mapaPodkladowa.refObject)) == 0:
            showPopup('Brak mapy podkładowej', 'Mapa podkładowa jest wymagana dla wartości atrybutu typPlanu:\n - %s' %
                      '\n - '.join(typy))
            return False

        if typPlanu.refObject.currentText() not in rodzajZbioru_map[rodzajZbioru]:
            showPopup('Błąd wartości atrybutu', 'Atrybut typPlanu dla rodzaju zbioru %s przyjmuje wartości:\n - %s' %
                      (rodzajZbioru, '\n - '.join(rodzajZbioru_map[rodzajZbioru])))
            return False

    return True


def validate_status(formElements):
    """walidacja statusu"""
    obowiazujeOd = getFormElementByName(formElements, 'obowiazujeOd')
    obowiazujeDo = getFormElementByName(formElements, 'obowiazujeDo')
    status = getFormElementByName(formElements, 'status')
    if status is not None:
        if status.refObject.currentText() == 'prawnie wiążący lub realizowany' or status.refObject.currentText() == 'nieaktualny':
            if checkElement(obowiazujeOd, obowiazujeOd.refObject):
                if not obowiazujeOd.refObject.dateTime():
                    showPopup('Brak wartości atrybutu',
                              'Atrybut obowiazujeOd jest obowiązkowy dla statusów "prawnie wiążący lub realizowany" oraz "nieaktualny".')
                    return False
            if checkElement(obowiazujeDo, obowiazujeDo.refObject):
                if not obowiazujeDo.refObject.dateTime() and status.refObject.currentText() == 'nieaktualny':
                    showPopup('Brak wartości atrybutu',
                              'Atrybut obowiazujeDo jest obowiązkowy dla statusu "nieaktualny".')
                    return False
    return True


def validate_form_dates(formElements):
    """walidacja poprawności dat - rozpoczęcie, zakończenie"""
    daty_powiazane = {
        'poczatekWersjiObiektu': 'koniecWersjiObiektu',
        'obowiazujeOd': 'obowiazujeDo',
        'dataWejsciaWZycie': 'dataUchylenia'
    }
    for atrybut in daty_powiazane.keys():
        dataOd = getFormElementByName(formElements, atrybut)
        dataDo = getFormElementByName(formElements, daty_powiazane[atrybut])
        if dataOd is None or dataDo is None:
            continue
        if checkElement(dataOd, dataOd.refObject) and checkElement(dataDo, dataDo.refObject) and dataDo.refObject.text() != 'NULL':
            if not dataDo.refObject.dateTime():
                continue
            if dataOd.refObject.dateTime() > dataDo.refObject.dateTime():
                showPopup(title='Błąd wartości atrybutu %s' % atrybut,
                          text='Wartość atrybutu %s nie może być późniejsza od %s.' % (atrybut, daty_powiazane[atrybut]))
                return False
    return True


def isFormFilled(dialog):
    for fe in dialog.formElements:
        if fe.isComplex() and fe.minOccurs > 0:
            for inner in fe.innerFormElements:
                # Sprawdzanie poprawności przestrzeni nazw idIIP
                if inner.name == 'przestrzenNazw' and not validate_IIP(inner.refObject.text()):
                    showPopup(title='Błąd wartości atrybutu idIIP',
                              text='Błędna wartość dla atrybutu idIIP.')
                    return False
                if checkElement(inner, inner.refObject) == False:
                    showPopup(title='Błąd formularza',
                              text='Brak wartości dla wymaganego atrybutu (*).')
                    return False
        if fe.name in dialog.pomijane:
            continue
        # Sprawdza tylko czy wartość występuje co najmniej raz - brak specyfikacji dokładnej liczności
        if type(fe.refObject) == list:
            for element in fe.refObject:
                if checkElement(fe, element) == False:  # Brak wartości
                    showPopup(title='Błąd formularza',
                              text='Brak wartości dla wymaganego atrybutu (*).')
                    return False

        elif fe.refNilObject is not None:
            widgets = all_layout_widgets(fe.refNilObject)
            if checkElement(fe, fe.refObject) == False:  # Brak wartości
                for widget in widgets:
                    if type(widget).__name__ == 'QCheckBox':
                        if widget.isChecked() == False:  # Brak Nillable
                            showPopup(title='Błąd formularza',
                                      text='Brak wartości dla wymaganego atrybutu (*).')
                            return False

        else:
            if checkElement(fe, fe.refObject) == False:  # Brak wartości
                showPopup(title='Błąd formularza',
                          text='Brak wartości dla wymaganego atrybutu (*).')
                return False
    return True  # Wszystko wypełnione


def getListWidgetItems(element):
    itemList = []
    for i in range(element.count()):
        item = element.item(i).data(Qt.UserRole)
        for key in item.keys():
            if type(item[key]) == str or type(item[key]) == int:
                continue
            else:
                item[key] = item[key].toString("yyyy-MM-ddThh:mm:ss")
        itemList.append(item)
    return(itemList)


def retrieveFormData(elements, data, pomijane):

    form_data = {}
    for el in data:

        if el.objectName() in pomijane:
            continue
        if 'lineEdit' in el.objectName():
            try:
                form_data[el.objectName()] = el.text()
            except:
                if 'ComboBox' in type(el).__name__:
                    form_data[el.objectName()] = el.currentText()
        elif 'dateTimeEdit' in el.objectName():
            try:
                form_data[el.objectName()] = el.dateTime()
            except:
                if 'ComboBox' in type(el).__name__:
                    form_data[el.objectName()] = el.currentText()
        elif 'listWidget' in el.objectName():
            form_data[el.objectName()] = getListWidgetItems(el)
        else:
            try:
                if 'ComboBox' in type(el).__name__:
                    form_data[el.objectName()] = el.currentText()
            except:
                continue
    return(form_data)


def getListWidgetItems(listWidget):
    itemList = []
    for i in range(listWidget.count()):
        item = listWidget.item(i).data(Qt.UserRole)
        # print(item)
        for key in item.keys():
            if type(item[key]) == str or type(item[key]) == int:
                continue
            elif type(item[key]) == bool:
                continue
            else:
                # Uwaga - dla atrybutów typu date należy usuwać "Thh:mm:ss"
                item[key] = item[key].toString("yyyy-MM-ddThh:mm:ss")
        itemList.append(item)
    return(itemList)


def makeMapaPodkladowaNode(item, data):
    for i in data.keys():
        item1 = ET.SubElement(item, 'app:MapaPodkladowa')
        item1.text = data[i]


def makeListWidgetLaczeNode(item, data):
    for i in data.keys():
        item1 = ET.SubElement(item, 'app:lacze')
        item1.text = data[i]


def makeDataNode(item, data, slownik):
    item1 = ET.SubElement(item, 'gmd:CI_Date')
    item2 = ET.SubElement(item1, 'gmd:date')
    item3 = ET.SubElement(item2, 'gco:Date')
    item3.text = data[0].dateTime().toString("yyyy-MM-dd")
    item4 = ET.SubElement(item1, 'gmd:dateType')
    item5 = ET.SubElement(item4, 'gmd:CI_DateTypeCode')
    item5.set(
        'codeList', 'http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_DateTypeCode')
    item5.set('codeListValue', slownik[data[1].currentText()])
    item5.text = data[1].currentText()


def makeNil(item, element, nilReason):
    if element.isNillable:
        item.set('nilReason', str(nilReason))
        item.set('xsi:nil', 'true')


def checkForNoDateValue(element):
    if element.dateTime().toString() == '' or element.text() == 'NULL' or element.text() == None:
        return True
    return False  # jest wartość


def checkForNoValue(element):
    try:
        if element.text() == '' or element.text() == 'NULL' or element.text() == None:
            return True
        # print(element.text())
    except:
        try:
            if element.dateTime().toString() == '' or element.text() == 'NULL' or element.text() == None:
                return True
        except:
            try:
                if element.currentText() == '':
                    return True
                # print(element.currentText())
            except:
                try:
                    params = getListWidgetItems(element)
                    if params == []:
                        return True
                except:
                    # print(element)
                    pass
    return False  # jest wartość


def createXmlData(dialog, obrysLayer):  # NOWE

    dict_map = {
        'status': dictionaries.statusListaKodowa,
        'poziomHierarchii': dictionaries.poziomyHierarchii,
        'nilReason': dictionaries.nilReasons,
        'zasiegPrzestrzenny': dictionaries.ukladyOdniesieniaPrzestrzennego,
        'typPlanu': dictionaries.typyPlanu,
        'dziennikUrzedowy': dictionaries.dziennikUrzedowyKod,
        'ukladOdniesieniaPrzestrzennego': dictionaries.ukladyOdniesieniaPrzestrzennego,
        'data': dictionaries.cI_DateTypeCode
    }

    docNames = {
        'RasterFormularzDialog': 'RysunekAktuPlanowniaPrzestrzenego',
        'WektorFormularzDialog': 'AktPlanowaniaPrzestrzennego',
        'DokumentyFormularzDialog': 'DokumentFormalny'
    }

    docName = docNames[type(dialog).__name__]
    try:
        CoordinatesList = getCoordinates(obrysLayer)
        epsg = str(obrysLayer.crs().authid()).split(':')[1]
        # Układ współrzędnych
        for crs in dict_map['ukladOdniesieniaPrzestrzennego'].values():
            if epsg in crs:
                srsName = crs
            else:
                # TODO WYJĄTEK/POPUP DLA INNYCH CRS
                # TODO co w przypadku, gdy CRS jest inny niż w słowniku - rozwiązanie tymczasowe
                srsName = "http://www.opengis.net/def/crs/EPSG/0/"+epsg
    except:
        CoordinatesList = None

    # Strefa czasowa timezone jest ustawiona na sztywno
    root_data = {
        'timeStamp': datetime.datetime.utcnow().isoformat()+'Z',
        'numberReturned': "1",
        'numberMatched': "unknown",
    }

    # Przestrzenie nazw ustawione na sztywno
    namespaces = {
        'xmlns:gco': "http://www.isotc211.org/2005/gco",
        'xmlns:gmd': "http://www.isotc211.org/2005/gmd",
        'xmlns:gml': "http://www.opengis.net/gml/3.2",
        'xmlns:wfs': "http://www.opengis.net/wfs/2.0",
        'xmlns:xlink': "http://www.w3.org/1999/xlink",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xmlns:app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
        'xsi:schemaLocation': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0 ../appSchema/appSchema_app_v0_0_1/planowaniePrzestrzenne.xsd http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd"
    }
    # create the file structure
    data = ET.Element('wfs:FeatureCollection')
    datamember = ET.SubElement(data, 'wfs:member')

    for rd in root_data.keys():
        data.set(rd, root_data[rd])

    for ns in namespaces.keys():
        data.set(ns, namespaces[ns])

    tag = 'app:'
    items = ET.SubElement(datamember, tag + docName)

    itemid = ET.SubElement(items, 'gml:identifier')
    codeSpace = 'http://zagospodarowanieprzestrzenne.gov.pl/app'
    itemid.set('codeSpace', codeSpace)

    for fe in dialog.formElements:
        refObject = fe.refObject
        if checkForNoValue(refObject) and fe.minOccurs < 1:
            continue
        if (fe.type == 'date' or fe.type == 'dateTime') and checkForNoDateValue(refObject):
            continue
        if fe.name in dialog.pomijane and fe.name != 'zasiegPrzestrzenny':
            continue
        if fe.name in dict_map.keys():
            slownik = dict_map[fe.name]  # sprawdzać też na innerElements
        if fe.name == 'typPlanu':
            link = 'http://zagospodarowanieprzestrzenne.gov.pl/codelist/AktPlanowaniaPrzestrzennegoKod/'
        elif fe.name == 'dziennikUrzedowy':
            link = 'http://zagospodarowanieprzestrzenne.gov.pl/codelist/DziennikUrzedowyKod/'
        else:
            link = ''
        if fe.name == 'idIIP':
            IIP = refObject.text()
            items.set('gml:id', IIP)
            itemid.text = '/'.join([codeSpace, docName, IIP.replace('_', '/')])

        if fe.isComplex():

            if fe.maxOccurs == 'unbounded':  # Element jest wielokrotny
                params = getListWidgetItems(refObject)
                # print(params)
                makeXmlListElements(tag, items, fe, params)
                continue
            else:
                item = ET.SubElement(items, tag + fe.name)
                makeXmlComplex(tag, item, fe)
                continue
        elif fe.maxOccurs == 'unbounded':  # Element jest wielokrotny
            params = getListWidgetItems(refObject)
            if params == [] and fe.minOccurs == 0:
                continue
            makeXmlListElements(tag, items, fe, params)
            continue
        else:  # Element jest elementarny
            item = ET.SubElement(items, tag + fe.name)

        if fe.isNillable:
            refNilObject = fe.refNilObject
            nil = False
            widgets = all_layout_widgets(refNilObject)
            for widget in widgets:
                if type(widget).__name__ == 'QCheckBox':
                    if widget.isChecked() == True:
                        nil = True
                        for widget in widgets:
                            if type(widget).__name__ == 'QComboBox':
                                makeNil(item, fe, widget.currentText())
                                continue
                    else:
                        if fe.type == 'date':
                            item.text = refObject.dateTime().toString("yyyy-MM-dd")
                        elif fe.type == 'dateTime':
                            item.text = refObject.dateTime().toString(
                                "yyyy-MM-ddThh:mm:ss")
                        else:
                            try:
                                item.text = refObject.text()
                            except:
                                try:
                                    item.text = refObject.currentText()
                                except:
                                    pass

        elif fe.name == 'data':
            makeDataNode(item, refObject, slownik)
        elif fe.name == 'ukladOdniesieniaPrzestrzennego':
            item.text = slownik[refObject.currentText()]
        elif fe.type == 'date':
            item.text = refObject.dateTime().toString("yyyy-MM-dd")
        elif fe.type == 'dateTime':
            item.text = refObject.dateTime().toString(
                "yyyy-MM-ddThh:mm:ss")
        elif 'ReferenceType' in fe.type:
            try:
                item.set('xlink:href', (link+slownik[refObject.text()]))
                item.set('xlink:title', refObject.text())
            except:
                item.set('xlink:href',
                         (link+slownik[refObject.currentText()]))
                item.set('xlink:title', refObject.currentText())
        elif fe.name == 'zasiegPrzestrzenny':
            subItem1 = ET.SubElement(item, 'gml:MultiSurface')
            subItem1.set('srsDimension', '2')
            subItem1.set('srsName', srsName)
            makeSpatialExtent(subItem1, CoordinatesList)
        else:
            try:
                item.text = refObject.text()
            except:
                try:
                    item.text = refObject.currentText()
                except:
                    pass

    return data


def createXmlRysunekAPP(layout):
    """Tworzy szablon xml dla Rysunku APP"""
    docName = 'RysunekAktuPlanowniaPrzestrzenego'
    elements = createFormElements(docName+'Type')
    data = makeXML(docName=docName,
                   elements=elements,
                   formData=retrieveFormData(
                       elements,
                       all_layout_widgets(layout),
                       formSkippedObjects(docName)))

    return data


def createXmlDokumentFormalny(layout):
    """Tworzy szablon xml dla dokumentu formalnego"""
    docName = 'DokumentFormalny'
    elements = createFormElements(docName+'Type')
    data = makeXML(docName=docName,
                   elements=elements,
                   formData=retrieveFormData(
                       elements,
                       all_layout_widgets(layout),
                       formSkippedObjects(docName)))

    return data


def createXmlAktPlanowaniaPrzestrzennego(layout, obrysLayer):
    """Tworzy szablon xml dla aktu planowania przestrzennego"""
    docName = 'AktPlanowaniaPrzestrzennego'
    elements = createFormElements(docName+'Type')
    data = makeXML(docName=docName,
                   elements=elements,
                   formData=retrieveFormData(
                       elements,
                       all_layout_widgets(layout),
                       formSkippedObjects(docName)),
                   obrysLayer=obrysLayer)

    return data


def putElementAbove(element, subElementName, newElement):
    # Możemy umieścić nowy element nad starym elementem o określonej nazwie
    # element = root, subElementName = str element przed który wrzucamy, newElement = ET.Element
    idx = 0
    for elem in element:
        if subElementName in elem.tag:
            element.insert(idx, newElement)
            return True
        idx += 1
        # if len(list(elem)) > 0:
        #     if putElementAbove(elem, subElementName, newElement):
        #         return(putElementAbove(elem, subElementName, newElement))
    return False


def putElementBelow(element, subElementName, newElement):
    # Możemy umieścić nowy element pod starym elementem o określonej nazwie
    # element = root, subElementName = str element przed który wrzucamy, newElement = ET.Element
    idx = 0
    for elem in element:
        idx += 1
        if subElementName in elem.tag:
            element.insert(idx, newElement)
            return True

        # if len(list(elem)) > 0:
        #     if putElementBelow(elem, subElementName, newElement):
        #         return(putElementBelow(elem, subElementName, newElement))
    return False


def getDocType(filePath):
    docNames = ['AktPlanowaniaPrzestrzennego',
                'RysunekAktuPlanowniaPrzestrzenego',
                'DokumentFormalny']
    try:
        tree = ET.parse(filePath)
        root = tree.getroot()
        elemList = []
        # Sprawdzanie, czy plik
        if len(root) != 1:
            return ''
        for elem in root.iter():
            elemList.append(elem.tag)

        # usuwanie duplikatów
        elemList = list(set(elemList))

        for elem in elemList:
            for docName in docNames:
                if docName in elem:
                    return docName
    except:
        return ''
    return ''


def getDocIIP(rootDoc, IIP=''):
    for elem in rootDoc:
        for attr in elem.attrib.keys():
            if '{http://www.opengis.net/gml/3.2}id' in attr:  # szybka zmiana
                IIP = elem.attrib[attr]
                break
        if len(list(elem)) > 0:
            return(getDocIIP(elem, IIP))
    return IIP


def newItem(root, name, link, ns):
    """nowy obiekt typu gml:ReferenceType"""
    newElement = ET.SubElement(root, "{%s}%s" % (ns['app'], name))
    newElement.set('xlink:href', link)
    return newElement


def mergeDocsToAPP2(docList):  # Nowa wersja tworzenia APP - do dokończenia
    def initializeMember(data, docType, root, ns):
        # Inicjalizacja dokumentu
        dataMember = ET.SubElement(data, 'wfs:member')
        dataDoc = ET.SubElement(dataMember, 'app:%s' % docType)
        elementPath = 'wfs:member/app:%s' % (docType)
        idIIP = root.find(
            elementPath, ns).attrib['{http://www.opengis.net/gml/3.2}id']
        dataDoc.set('gml:id', idIIP)
        gmlIdentifier = ET.SubElement(dataDoc, 'gml:identifier')
        gmlIdentifier.set(
            'codeSpace', "http://zagospodarowanieprzestrzenne.gov.pl/app")
        gmlIdentifier.text = 'http://zagospodarowanieprzestrzenne.gov.pl/app/%s/%s' % (
            docType, idIIP.replace('_', '/'))
        return dataDoc

    def addElements(formElements, root, dataDoc, docType, relations=[]):
        for fe in formElements:
            elementPath = 'wfs:member/app:%s/app:%s' % (docType, fe.name)
            elements = root.findall(elementPath, ns)
            for element in elements:
                dataDoc.append(element)

    ns = {
        'xsi': "http://www.w3.org/2001/XMLSchema",
        'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
        'gmd': "http://www.isotc211.org/2005/gmd",
        'gco': 'http://www.isotc211.org/2005/gco',
        'xlink': 'http://www.w3.org/1999/xlink',
        'gml': "http://www.opengis.net/gml/3.2",
        'wfs': 'http://www.opengis.net/wfs/2.0',
        'gmlexr': "http://www.opengis.net/gml/3.3/exr"
    }

    # Strefa czasowa timezone jest ustawiona na sztywno
    root_data = {
        'timeStamp': datetime.datetime.utcnow().isoformat()+'Z',
        # liczba memberów w wfs:FeatureCollection
        'numberReturned': str(len(docList)),
        'numberMatched': "unknown",
    }

    for prefix, uri in ns.items():
        ET.register_namespace(prefix, uri)

    # Przestrzenie nazw ustawione na sztywno
    namespaces = {
        'xmlns:gco': "http://www.isotc211.org/2005/gco",
        'xmlns:gmd': "http://www.isotc211.org/2005/gmd",
        'xmlns:gml': "http://www.opengis.net/gml/3.2",
        'xmlns:wfs': "http://www.opengis.net/wfs/2.0",
        'xmlns:xlink': "http://www.w3.org/1999/xlink",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xmlns:app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
        'xsi:schemaLocation': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0 ../appSchema/appSchema_app_v0_0_1/planowaniePrzestrzenne.xsd http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd"
    }

    # create the file structure
    data = ET.Element('wfs:FeatureCollection')

    for attr, value in root_data.items():
        data.set(attr, value)

    for tag, uri in namespaces.items():
        data.set(tag, uri)

    docRoots = []
    docRelations = []
    rysRoots = []
    rysIIP = []

    for doc, relation in docList:
        docType = getDocType(doc)
        root = ET.parse(doc).getroot()
        formType = docType + 'Type'
        formElements = createFormElements(
            formType)  # odczytywanie atrybutów z xsd
        elementPath = 'wfs:member/app:%s' % (docType)
        idIIP = root.find(
            elementPath, ns).attrib['{http://www.opengis.net/gml/3.2}id']

        if docType == 'AktPlanowaniaPrzestrzennego':
            aktForm = formElements
            aktRoot = root

        if docType == 'RysunekAktuPlanowniaPrzestrzenego':
            rysForm = formElements
            rysIIP.append(idIIP)
            rysRoots.append(root)

        if docType == 'DokumentFormalny':
            if relation not in dictionaries.relacjeDokumentu.keys():
                return ''
            else:
                docForm = formElements
                docRelations.append(
                    {'id': idIIP, 'relation': dictionaries.relacjeDokumentu[relation]})
                docRoots.append(root)

    # Wypełnianie APP
    elementPath = 'wfs:member/app:AktPlanowaniaPrzestrzennego'
    aktIdIIP = aktRoot.find(
        elementPath, ns).attrib['{http://www.opengis.net/gml/3.2}id']
    docType = 'AktPlanowaniaPrzestrzennego'
    dataDoc = initializeMember(
        data, docType, aktRoot, ns)
    addElements(aktForm, aktRoot, dataDoc, docType)

    # Wypełnianie Rysunków APP
    for root in rysRoots:
        docType = 'RysunekAktuPlanowniaPrzestrzenego'
        dataDoc = initializeMember(
            data, docType, root, ns)
        addElements(rysForm, root, dataDoc, docType, relations=aktIdIIP)

    # Wypełnianie Dokumentów Formalnych
    for root in docRoots:
        docType = 'DokumentFormalny'
        dataDoc = initializeMember(
            data, docType, root, ns)
        addElements(docForm, root, dataDoc, docType, relations=aktIdIIP)

        # if fe.isComplex():
        #     for inner in fe.innerFormElements:
        #         innerElementPath = 'wfs:member/app:%s/app:%s/app:%s' % (
        #             docType, fe.name, inner.name)
        # if fe.maxOccurs == 'unbounded':

        # for elem in app_form:
        #     print(elem.name, elem.minOccurs, elem.maxOccurs, elem.value)

    # eksport APP
    # .replace(b'><', b'>\n\t<')
    mydata = ET.tostring(data, encoding="unicode")
    # from lxml import etree
    # root = etree.XML(mydata)
    # xml_string = etree.tostring(
    #     root,
    #     xml_declaration=True,
    #     encoding='utf-8',
    #     pretty_print=True).decode('utf-8')
    return mydata


def mergeDocsToAPP(docList):  # docList z getTableContent
    # docList[0] - ścieżka
    # docList[0] - relacja dokumentu / '' dla APP, Rysunek
    # Dodać liczbę zwracanych obiektów 'numberReturned': str(len(docList))
    ns = {
        'xsi': "http://www.w3.org/2001/XMLSchema",
        'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
        'gmd': "http://www.isotc211.org/2005/gmd",
        'gco': 'http://www.isotc211.org/2005/gco',
        'xlink': 'http://www.w3.org/1999/xlink',
        'gml': "http://www.opengis.net/gml/3.2",
        'wfs': 'http://www.opengis.net/wfs/2.0',
        'gmlexr': "http://www.opengis.net/gml/3.3/exr"
    }

    # Strefa czasowa timezone jest ustawiona na sztywno
    root_data = {
        'timeStamp': datetime.datetime.utcnow().isoformat()+'Z',
        # liczba memberów w wfs:FeatureCollection
        'numberReturned': str(len(docList)),
        'numberMatched': "unknown",
    }

    for prefix, uri in ns.items():
        ET.register_namespace(prefix, uri)

    # Przestrzenie nazw ustawione na sztywno
    namespaces = {
        'xmlns:gco': "http://www.isotc211.org/2005/gco",
        'xmlns:gmd': "http://www.isotc211.org/2005/gmd",
        'xmlns:gml': "http://www.opengis.net/gml/3.2",
        'xmlns:wfs': "http://www.opengis.net/wfs/2.0",
        'xmlns:xlink': "http://www.w3.org/1999/xlink",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xmlns:app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
        'xsi:schemaLocation': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0 ../appSchema/appSchema_app_v0_0_1/planowaniePrzestrzenne.xsd http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd"
    }

    # create the file structure
    data = ET.Element('wfs:FeatureCollection')

    # for attr, value in root_data.items():
    #     data.set(attr, value)

    # for tag, uri in namespaces.items():
    #     data.set(tag, uri)

    ##############################
    # ns = {
    #     'xsi': "http://www.w3.org/2001/XMLSchema",
    #     'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
    #     'gmd': "http://www.isotc211.org/2005/gmd",
    #     'gco': 'http://www.isotc211.org/2005/gco',
    #     'xlink': 'http://www.w3.org/1999/xlink',
    #     'gml': "http://www.opengis.net/gml/3.2",
    #     'wfs': 'http://www.opengis.net/wfs/2.0',
    #     'gmlexr': "http://www.opengis.net/gml/3.3/exr"
    # }
    # Przechowywanie elementów referencyjnych
    pomijane = {
        'AktPlanowaniaPrzestrzennego': {  # + zmiana
            "dokument": [],  # APP
            "dokumentPrzystepujacy": [],  # APP
            "dokumentUchwalajacy": [],  # APP
            "dokumentZmieniajacy": [],  # APP
            "dokumentUchylajacy": [],  # APP
            "dokumentUniewazniajacy": [],  # APP
            "rysunek": []  # APP
        },
        'DokumentFormalny': {
            "przystapienie": [],  # Dokument
            "uchwala": [],  # Dokument
            "zmienia": [],  # Dokument
            "uchyla": [],  # Dokument
            "uniewaznia": []  # Dokument
        },
        'RysunekAktuPlanowniaPrzestrzenego': {
            "plan": []  # Rysunek
        }
    }
    docRoots = {
        'AktPlanowaniaPrzestrzennego': [],
        'DokumentFormalny': [],
        'RysunekAktuPlanowniaPrzestrzenego': []
    }

    # for prefix, uri in ns.items():
    #     ET.register_namespace(prefix, uri)

    # Pozyskiwanie APP
    for doc, relation in docList:
        docType = getDocType(doc)
        root = ET.parse(doc).getroot()
        if docType == 'AktPlanowaniaPrzestrzennego':
            APProot = root
            appIIP = getDocIIP(root)
            APPrelLink = 'http://zagospodarowanieprzestrzenne.gov.pl/app/%s/%s' % (
                docType, appIIP)

    for doc, relation in docList:
        if relation == 'inna':
            relation = 'dokument'
        if relation == 'przystąpienie':
            relation = 'przystapienie'
        if relation == 'unieważnia':
            relation = 'uniewaznia'
        docType = getDocType(doc)
        root = ET.parse(doc).getroot()
        # słownik/tablica rootów poszczególnych dokumentów
        docRoots[docType].append(root)
        IIP = getDocIIP(root)
        relLink = 'http://zagospodarowanieprzestrzenne.gov.pl/app/%s/%s' % (
            docType, IIP)
        if docType == 'DokumentFormalny':
            if relation == 'przystapienie':
                pomijane['AktPlanowaniaPrzestrzennego']['dokumentPrzystepujacy'].append(
                    relLink)
                pomijane[docType]['przystapienie'].append(root)
            if relation == 'uchwala':
                pomijane['AktPlanowaniaPrzestrzennego']['dokumentUchwalajacy'].append(
                    relLink)
                pomijane[docType]['uchwala'].append(root)
            if relation == 'zmienia':
                pomijane['AktPlanowaniaPrzestrzennego']['dokumentZmieniajacy'].append(
                    relLink)
                pomijane[docType]['zmienia'].append(root)
            if relation == 'uchyla':
                pomijane['AktPlanowaniaPrzestrzennego']['dokumentUchylajacy'].append(
                    relLink)
                pomijane[docType]['uchyla'].append(root)
            if relation == 'uniewaznia':
                pomijane['AktPlanowaniaPrzestrzennego']['dokumentUniewazniajacy'].append(
                    relLink)
                pomijane[docType]['uniewaznia'].append(root)
            if relation == 'dokument':
                pomijane['AktPlanowaniaPrzestrzennego']['dokument'].append(
                    relLink)
        if docType == 'RysunekAktuPlanowniaPrzestrzenego':
            pomijane['AktPlanowaniaPrzestrzennego']['rysunek'].append(relLink)
            pomijane[docType]['plan'].append(root)
            # Dodaje atrybut do rysunku
            newItem(root=root[0][0], name='plan', link=APPrelLink, ns=ns)
    # Sprawdzanie relacji Dokumentu formalnego
    l_przystapienie = len(pomijane['DokumentFormalny']['przystapienie'])
    l_uchwala = len(pomijane['DokumentFormalny']['uchwala'])
    suma = l_przystapienie + l_uchwala
    if suma > 2 or suma == 0:
        # Wymagany jest co najmniej 1 dokument
        showPopup(title='Błąd liczności Dokumentów',
                  text='Nieprawidłowa liczba dokumentów.\n Przystąpienie: %i (0..*)\nUchwala: %i (0..1)' % (l_przystapienie, l_uchwala))
        return ''
    if len(docRoots['AktPlanowaniaPrzestrzennego']) != 1:
        showPopup(title='Błąd liczności dokumentu',
                  text='Liczba Aktów Planowania Przestrzennego: %i\nWymagana liczba: 1' % len(docRoots['AktPlanowaniaPrzestrzennego']))
        return ''
    if len(docRoots['DokumentFormalny']) < 1:
        showPopup(title='Błąd liczności dokumentu',
                  text='Liczba Dokumentów Formalnych: %i\nWymagana liczba: 1+' % len(docRoots['DokumentFormalny']))
        return ''
    # if len(docRoots['RysunekAktuPlanowniaPrzestrzenego']) < 1:
    #     showPopup(title='Błąd liczności dokumentu',
    #               text='Liczba Rysunków: %i\nWymagana liczba: 1+' % len(docRoots['RysunekAktuPlanowniaPrzestrzenego']))
    #     return ''

    # Dodawanie atrybutów do APP
    for atr in pomijane['AktPlanowaniaPrzestrzennego']:
        for value in pomijane['AktPlanowaniaPrzestrzennego'][atr]:
            newItem(APProot[0][0], name=atr, link=value, ns=ns)

    for atr in pomijane['DokumentFormalny']:
        for root in pomijane['DokumentFormalny'][atr]:
            newItem(root=root[0][0], name=atr, link=APPrelLink, ns=ns)

    for atr in pomijane['DokumentFormalny']:
        for root in pomijane['DokumentFormalny'][atr]:
            APProot.append(root[0])
    for atr in pomijane['RysunekAktuPlanowniaPrzestrzenego']:
        for root in pomijane['RysunekAktuPlanowniaPrzestrzenego'][atr]:
            APProot.append(root[0])

    zmiana_count = len(
        pomijane['AktPlanowaniaPrzestrzennego']['dokumentZmieniajacy'])
    if zmiana_count > 0:
        newElement = ET.Element("{%s}zmiana" % ns['app'])
        newElement.text = str(zmiana_count)
        aktPath = 'wfs:member/app:AktPlanowaniaPrzestrzennego'
        aktRoot = APProot.find(aktPath, ns)
        putElementBelow(element=aktRoot, subElementName='status',
                        newElement=newElement)
    numberReturned = str(len(docList))
    timeStamp = datetime.datetime.utcnow().isoformat()+'Z'
    APProot.attrib['timeStamp'] = timeStamp
    APProot.attrib['numberReturned'] = numberReturned
    # eksport APP
    # .replace(b'><', b'>\n\t<')
    for prefix, uri in ns.items():
        ET.register_namespace(prefix, uri)
    mydata = '<?xml version="1.0" encoding="utf-8"?>'+ET.tostring(APProot, encoding='unicode').replace(
        'ns1', 'xsi')  # xsi quickfix - do zweryfikowania
    return mydata
    # from lxml import etree
    # root = etree.XML(mydata)
    # xml_string = etree.tostring(
    #     root,
    #     xml_declaration=True,
    #     encoding='utf-8',
    #     pretty_print=True).decode('utf-8')
    # return xml_string


def mergeFormalDocuments(root, elements=[]):
    pomijane = ["przystapienie",
                "uchwala",
                "zmienia",
                "uchyla",
                "uniewaznia"]
    ns = "{http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0}"
    for element in root:
        el_name = element.tag.replace(ns, '')
        if el_name in pomijane:
            elements.append(element)
            root.remove(element)
        if len(list(element)) > 0:
            mergeFormalDocuments(element, elements)
    return elements


def sortDocRelations(relationList):
    DokumentFormalny = {
        "przystapienie": [],  # Dokument
        "uchwala": [],  # Dokument
        "zmienia": [],  # Dokument
        "uchyla": [],  # Dokument
        "uniewaznia": []  # Dokument
    }
    ns = "{http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0}"
    for relation in relationList:
        rel_name = relation.tag.replace(ns, '')
        DokumentFormalny[relationList].append(relation)
    return DokumentFormalny


def mergeAppToCollection(AppFiles, set={}):
    app_form = createFormElementsAktPlanowaniaPrzestrzennego()
    # for elem in app_form:
    #     print(elem.name)
    ns = {
        'xsi': "http://www.w3.org/2001/XMLSchema",
        'app': 'http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0',
        'gmd': "http://www.isotc211.org/2005/gmd",
        'gco': 'http://www.isotc211.org/2005/gco',
        'xlink': 'http://www.w3.org/1999/xlink',
        'gml': "http://www.opengis.net/gml/3.2",
        'wfs': 'http://www.opengis.net/wfs/2.0',
        'gmlexr': "http://www.opengis.net/gml/3.3/exr"
    }

    formalDocIIP = {}

    for prefix, uri in ns.items():
        ET.register_namespace(prefix, uri)

    main = True
    memberList = []
    numberReturned = 0
    for file in AppFiles:
        path = file.path
        root = ET.parse(path).getroot()  # APP
        for member in root:
            numberReturned = numberReturned + 1
            if 'DokumentFormalny' in member[0].tag:
                docAttributes = mergeFormalDocuments(
                    member[0], [])  # Lista atrybutów dokumentu
                IIP = getDocIIP(member)
                if IIP in formalDocIIP.keys():  # Sprawdzić czy atrybut nie występuje w liście
                    for attr in docAttributes:
                        for listElem in formalDocIIP[IIP]:
                            if attr.tag != listElem.tag:
                                formalDocIIP[IIP].append(attr)
                else:
                    formalDocIIP[IIP] = docAttributes
            memberList.append(member)
        if main:
            rootMain = root
            while len(list(rootMain)) > 0:
                member = rootMain[0]
                rootMain.remove(member)
            main = False

    for member in memberList:
        # print(member[0])
        skip = False  # Pomiń dokument, jeśli już istnieje w APP
        if 'DokumentFormalny' in member[0].tag:
            IIP = getDocIIP(member)
            for root in rootMain:
                rootIIP = getDocIIP(root)
                if rootIIP == IIP:
                    skip = True
                    break
            if skip:
                continue
            for element in formalDocIIP[IIP]:
                member[0].append(element)
        rootMain.append(member)

    timeStamp = datetime.datetime.utcnow().isoformat()+'Z'
    rootMain.attrib['timeStamp'] = timeStamp
    rootMain.attrib['numberReturned'] = str(numberReturned)
    # eksport APP
    # mydata = ET.tostring(rootMain)  # .replace(b'><', b'>\n\t<')
    mydata = '<?xml version="1.0" encoding="utf-8"?>'+ET.tostring(rootMain, encoding='unicode').replace(
        'ns1', 'xsi')  # xsi quickfix - do zweryfikowania
    return mydata
    # from lxml import etree
    # root = etree.XML(mydata)
    # xml_string = etree.tostring(
    #     root,
    #     xml_declaration=True,
    #     encoding='utf-8',
    #     pretty_print=True).decode('utf-8')
    # return xml_string


def getIPPapp(filePath):
    AppName = 'AktPlanowaniaPrzestrzennego'
    try:
        tree = ET.parse(filePath)
        root = tree.getroot()
        elemList = []
        for member in root:
            if AppName in member[0].tag:
                IIP = getDocIIP(member)
                return IIP
    except:
        return ''
    return ''


def findElementByTag(root, name, elem=None):
    for element in root:
        if '{http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0}'+name in element.tag:
            return element
        if len(list(element)) > 0:
            elem = findElementByTag(element, name)
    if elem is not None:
        return elem
    return None


def addToComboBox(formElement, value, formDict):
    feDict = formDict
    for key in feDict.keys():
        if value == key:
            formElement.refObject.setCurrentText(key)
            break
        if value == feDict[key]:
            formElement.refObject.setCurrentText(key)
            break


def setValueToWidget(formElement, value):
    """Dodawanie wartości do elementu w formularzu"""
    widgetType = type(formElement.refObject).__name__
    # print(formElement.name+' '+formElement.type+' '+widgetType)
    if widgetType == 'QgsFilterLineEdit':
        formElement.refObject.setText(value)
    if widgetType == 'NoScrollQgsDateTimeEdit' and formElement.type == 'dateTime':
        try:
            dateValue = value.replace('T', ' ')
            date_time_obj = datetime.datetime.strptime(
                dateValue, '%Y-%m-%d %H:%M:%S')
            formElement.refObject.setDateTime(date_time_obj)
        except:
            formElement.refObject.setDateTime(value)
    if widgetType == 'NoScrollQgsDateTimeEdit' and formElement.type == 'date':
        date_time_obj = datetime.datetime.strptime(
            value, '%Y-%m-%d')
        formElement.refObject.setDateTime(date_time_obj)
    if widgetType == 'NoScrollQgsDateEdit' and formElement.type == 'date':  # Brak typu?
        date_time_obj = datetime.datetime.strptime(value, '%Y-%m-%d')
        formElement.refObject.setDate(date_time_obj)
    if widgetType == 'NoScrollQComboBox':
        if formElement.name == 'ukladOdniesieniaPrzestrzennego':
            feDict = dictionaries.ukladyOdniesieniaPrzestrzennego
            addToComboBox(formElement, value, feDict)
        if formElement.name == 'dziennikUrzedowy':
            feDict = dictionaries.dziennikUrzedowyKod
            addToComboBox(formElement, value, feDict)
        if formElement.name == 'typPlanu':
            feDict = dictionaries.typyPlanu
            addToComboBox(formElement, value, feDict)
        if formElement.name == 'poziomHierarchii':
            feDict = dictionaries.poziomyHierarchii
            addToComboBox(formElement, value, feDict)
        if formElement.name == 'status':
            feDict = dictionaries.statusListaKodowa
            addToComboBox(formElement, value, feDict)


def setValueToListWidget(formElement, objVal):
    """Dodawanie elementów do obiektu ListWidget"""
    def addElement(formElement, objVal):
        listWidget = formElement.refObject
        newListWidgetItem = QListWidgetItem()
        data = {}
        textList = []

        for objName, objVal in objVal.items():
            # print(objName, objVal)
            if objName == 'data_dateTimeEdit':
                data[objVal.objectName()] = objVal.dateTime()
                # textList.append(objVal.dateTime().date().toString())
                objValue = objVal.dateTime().date().toString()
                textList.append(objValue)
            else:
                data[objName] = objVal
                textList.append(objVal)

        newListWidgetItem.setData(
            Qt.UserRole,
            QVariant(data)
        )
        newListWidgetItem.setText(" - ".join(textList))
        listWidget.addItem(newListWidgetItem)

    if formElement.name == 'lacze':
        addElement(formElement, objVal)
    elif formElement.name == 'tytulAlternatywny':
        addElement(formElement, objVal)
    elif formElement.name == 'mapaPodkladowa':
        addElement(formElement, objVal)
    else:
        print(formElement.name)  # Nieobsłużone atrybuty
        return


def loadItemsToForm(filePath, formElements):
    # TODO czyszczenie formularza przed wywołaniem
    root = ET.parse(filePath).getroot()

    ns = {
        'xsi': "http://www.w3.org/2001/XMLSchema",
        'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
        'gmd': "http://www.isotc211.org/2005/gmd",
        'gco': 'http://www.isotc211.org/2005/gco',
        'xlink': 'http://www.w3.org/1999/xlink',
        'gml': "http://www.opengis.net/gml/3.2",
        'wfs': 'http://www.opengis.net/wfs/2.0',
        'gmlexr': "http://www.opengis.net/gml/3.3/exr"
    }

    for prefix, uri in ns.items():
        ET.register_namespace(prefix, uri)

    for fe in formElements:
        # iteruje się po xml i szuka odpowiadającego atrybutu z formularza
        element = findElementByTag(root, fe.name, None)
        if element == None:
            continue
        value = element.text
        elementAttrib = element.attrib
        if len(elementAttrib) > 0:
            if fe.type == 'gml:ReferenceType':
                for key in elementAttrib.keys():
                    if 'title' in key:
                        value = elementAttrib[key]
        if fe.name == 'data':
            datePath = 'gmd:CI_Date/gmd:date/gco:Date'
            dateTypePath = 'gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode'
            dataDate = element.find(datePath, ns)
            dataDateTypeCode = element.find(dateTypePath, ns)
            date_time_obj = datetime.datetime.strptime(
                dataDate.text, '%Y-%m-%d')
            fe.refObject[0].setDate(date_time_obj)
            feDict = dictionaries.cI_DateTypeCode
            for key in feDict.keys():
                if dataDateTypeCode.text == key:
                    fe.refObject[1].setCurrentText(key)
        elif fe.isNillable and len(elementAttrib) > 0:
            if 'nilReason' in elementAttrib:
                refNilObject = fe.refNilObject
                widgets = all_layout_widgets(refNilObject)
                for widget in widgets:
                    if type(widget).__name__ == 'QCheckBox':
                        if widget.isChecked() == False:
                            widget.click()
                    if 'QComboBox' in type(widget).__name__:
                        feDict = dictionaries.nilReasons
                        widget.setEnabled(True)
                        for key in feDict.keys():
                            if elementAttrib['nilReason'] == key:
                                widget.setCurrentText(key)
        elif fe.maxOccurs == 'unbounded':
            formNames = ['AktPlanowaniaPrzestrzennego',
                         'RysunekAktuPlanowniaPrzestrzenego', 'DokumentFormalny']
            elements = []
            for formName in formNames:
                elementPath = 'wfs:member/app:%s/app:%s' % (formName, fe.name)
                elements = root.findall(elementPath, ns)
                if elements != []:
                    break
            for elem in elements:
                if fe.name == 'mapaPodkladowa':
                    val = []
                    objValues = {'data_dateTimeEdit': '',
                                 'referencja_lineEdit': '', 'lacze_lineEdit': ''}
                    for el in elem[0]:

                        objName = (el.tag.replace(
                            '{http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0}', ''))

                        for inner in fe.innerFormElements:
                            if inner.name == objName:
                                refObj = inner.refObject
                        if objName == 'data':
                            objValue = datetime.datetime.strptime(
                                el.text, '%Y-%m-%d')
                            refObj.setDateTime(objValue)
                            # objValue = input.dateTime().date().toString()
                            objValue = refObj
                            objName = objName+'_dateTimeEdit'

                        else:
                            objValue = el.text
                            objName = objName+'_lineEdit'
                        objValues[objName] = objValue
                        # print(objName)
                    setValueToListWidget(fe, objValues)
                else:
                    objName = (elem.tag.replace(
                        '{http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0}', ''))+'_lineEdit'
                    objValue = elem.text
                    setValueToListWidget(fe, {objName: objValue})

        else:
            setValueToWidget(fe, value)
        if fe.name == 'idIIP':
            for inner in fe.innerFormElements:
                try:
                    innerElement = findElementByTag(element, inner.name, None)
                    value = innerElement.text
                    setValueToWidget(inner, value)
                except:
                    print('\t Nieobsługiwany atrybut: ' +
                          inner.name+' '+inner.type)


def setAppId(setPath):
    """pozyskiwanie id IIP z aktów (APP) w zadanym zbiorze"""
    ns = {
        'xsi': "http://www.w3.org/2001/XMLSchema",
        'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
        'gmd': "http://www.isotc211.org/2005/gmd",
        'gco': 'http://www.isotc211.org/2005/gco',
        'xlink': 'http://www.w3.org/1999/xlink',
        'gml': "http://www.opengis.net/gml/3.2",
        'wfs': 'http://www.opengis.net/wfs/2.0',
        'gmlexr': "http://www.opengis.net/gml/3.3/exr"
    }
    root = ET.parse(setPath).getroot()
    appPath = 'wfs:member/app:AktPlanowaniaPrzestrzennego'
    appList = root.findall(appPath, ns)
    idIIPList = []
    for app in appList:
        idIIPList.append(app.attrib['{http://www.opengis.net/gml/3.2}id'])

    return idIIPList


def findElementInXmlFile(file, docName, elementName):
    ns = {
        'xsi': "http://www.w3.org/2001/XMLSchema",
        'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
        'gmd': "http://www.isotc211.org/2005/gmd",
        'gco': 'http://www.isotc211.org/2005/gco',
        'xlink': 'http://www.w3.org/1999/xlink',
        'gml': "http://www.opengis.net/gml/3.2",
        'wfs': 'http://www.opengis.net/wfs/2.0',
        'gmlexr': "http://www.opengis.net/gml/3.3/exr"
    }
    root = ET.parse(file).getroot()
    elementPath = 'wfs:member/app:%s/app:%s' % (docName, elementName)
    element = root.find(elementPath, ns)
    return element


def validateObjectNumber(files):
    ns = {'xsi': "http://www.w3.org/2001/XMLSchema",
          'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gco': 'http://www.isotc211.org/2005/gco',
          'xlink': 'http://www.w3.org/1999/xlink',
          'gml': "http://www.opengis.net/gml/3.2",
          'wfs': 'http://www.opengis.net/wfs/2.0',
          'gmlexr': "http://www.opengis.net/gml/3.3/exr"}
    docs = {
        'AktPlanowaniaPrzestrzennego': [],
        'RysunekAktuPlanowniaPrzestrzenego': [],
        'DokumentFormalny': []
    }

    for doc in files:
        docs[getDocType(doc[0])].append(ET.parse(doc[0]).getroot())

    if len(docs['AktPlanowaniaPrzestrzennego']) == 1:
        statusPath = 'wfs:member/app:AktPlanowaniaPrzestrzennego/app:status'
        statusFind = docs['AktPlanowaniaPrzestrzennego'][0].find(
            statusPath, ns)
        if statusFind.attrib['{http://www.w3.org/1999/xlink}title'] == 'prawnie wiążący lub realizowany' and len(docs['RysunekAktuPlanowniaPrzestrzenego']) == 0:
            showPopup('Błąd liczności obiektów',
                      'Wymagany jest co najmniej jeden obiekt RysunekAktuPlanowniaPrzestrzenego.\nWybrano obiektów: %d.' % len(docs['RysunekAktuPlanowniaPrzestrzenego']))
            return False
        if statusFind.attrib['{http://www.w3.org/1999/xlink}title'] == 'prawnie wiążący lub realizowany' or statusFind.attrib['{http://www.w3.org/1999/xlink}title'] == 'nieaktualny':
            for rys in docs['RysunekAktuPlanowniaPrzestrzenego']:
                obowiazujeOdPath = 'wfs:member/app:RysunekAktuPlanowniaPrzestrzenego/app:obowiazujeOd'
                obowiazujeOdFind = rys.find(obowiazujeOdPath, ns)
                obowiazujeDoPath = 'wfs:member/app:RysunekAktuPlanowniaPrzestrzenego/app:obowiazujeDo'
                obowiazujeDoFind = rys.find(obowiazujeDoPath, ns)
                if obowiazujeDoFind is None and statusFind.attrib['{http://www.w3.org/1999/xlink}title'] == 'nieaktualny':
                    showPopup('Błąd wartości atrybutu', 'Dla statusu "nieaktualny" obiektu AktPlanowaniaPrzestrzennego wartość atrybutu obowiazujeDo obiektu RysunekAktuPlanowniaPrzestrzenego jest wymagana.')
                    return False
                elif obowiazujeOdFind is None:  # Zawsze wymagane - schemat xsd
                    showPopup('Błąd wartości atrybutu', 'Dla statusów "prawnie wiążący lub realizowany" oraz "nieaktualny" obiektu AktPlanowaniaPrzestrzennego wartość atrybutu obowiazujeOd obiektu RysunekAktuPlanowniaPrzestrzenego jest wymagana.')
                    return False
    else:
        showPopup('Błąd liczności obiektów',
                  'Wymagany jest jeden obiekt AktPlanowaniaPrzestrzennego.\nWybrano obiektów: %d.' % len(docs['AktPlanowaniaPrzestrzennego']))
        return False

    return True


def validatePrzestrzenNazwAppSet(files):
    przestrzenNazw_list = []
    for doc in files:
        try:
            root = ET.parse(doc[0]).getroot()
        except:
            root = ET.parse(doc.path).getroot()
        for elem in root:
            przestrzenNazw = '_'.join(getDocIIP(elem, IIP='').split('_')[0:2])
            if przestrzenNazw not in przestrzenNazw_list:
                przestrzenNazw_list.append(przestrzenNazw)
    if len(przestrzenNazw_list) != 1:
        return False
    return True


def validateDokumentFormalnyDate(files):
    uchwala_dataWejsciaWZycie = None
    przystapienie_dataWejsciaWZycie = None
    for doc, relation in files:
        element = findElementInXmlFile(
            file=doc, docName='DokumentFormalny', elementName='dataWejsciaWZycie')
        if element is not None:
            data = datetime.datetime.strptime(element.text, '%Y-%m-%d')
            if relation == 'uchwala':
                if uchwala_dataWejsciaWZycie is None:
                    uchwala_dataWejsciaWZycie = data
                elif uchwala_dataWejsciaWZycie < data:
                    uchwala_dataWejsciaWZycie = data
            if relation == 'przystąpienie':
                if przystapienie_dataWejsciaWZycie is None:
                    przystapienie_dataWejsciaWZycie = data
                elif przystapienie_dataWejsciaWZycie < data:
                    przystapienie_dataWejsciaWZycie = data
    if uchwala_dataWejsciaWZycie is not None and przystapienie_dataWejsciaWZycie is not None and uchwala_dataWejsciaWZycie < przystapienie_dataWejsciaWZycie:
        return False
    return True


def checkIfAPP(file):
    ns = {
        'xsi': "http://www.w3.org/2001/XMLSchema",
        'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
        'gmd': "http://www.isotc211.org/2005/gmd",
        'gco': 'http://www.isotc211.org/2005/gco',
        'xlink': 'http://www.w3.org/1999/xlink',
        'gml': "http://www.opengis.net/gml/3.2",
        'wfs': 'http://www.opengis.net/wfs/2.0',
        'gmlexr': "http://www.opengis.net/gml/3.3/exr"
    }
    root = ET.parse(file).getroot()
    appPath = 'wfs:member/app:AktPlanowaniaPrzestrzennego'
    appList = root.findall(appPath, ns)
    if len(appList) != 1:
        return False
    return True
