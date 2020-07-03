#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------
# Tim Hancock 2017

"""
Series of functions to deal with restrictionsInProposals. Defined as static functions to allow them to be used in forms ... (not sure if this is the best way ...)

"""
from qgis.PyQt.QtWidgets import (
    QMessageBox,
    QAction,
    QDialogButtonBox,
    QLabel,
    QDockWidget,
    QDialog,
    QLabel,
    QPushButton,
    QApplication
)

from qgis.PyQt.QtGui import (
    QIcon,
    QPixmap,
    QImage
)

from qgis.PyQt.QtCore import (
    QObject,
    QTimer,
    QThread,
    pyqtSignal,
    pyqtSlot
)

from qgis.PyQt.QtSql import (
    QSqlDatabase
)

from qgis.core import (
    Qgis,
    QgsExpressionContextScope,
    QgsExpressionContextUtils,
    QgsExpression,
    QgsFeatureRequest,
    QgsMessageLog,
    QgsFeature,
    QgsGeometry,
    QgsTransaction,
    QgsTransactionGroup,
    QgsProject,
    QgsSettings
)

from qgis.gui import *
import functools
import time, datetime
import os
#import cv2

from abc import ABCMeta
from TOMs.generateGeometryUtils import generateGeometryUtils
from TOMs.restrictionTypeUtilsClass import (TOMsParams, TOMsLayers, originalFeature, RestrictionTypeUtilsMixin)

from TOMs.ui.TOMsCamera import (formCamera)
try:
    import cv2
    cv2_available = True
except ImportError:
    QgsMessageLog.logMessage("Not able to import cv2 ...", tag="TOMs panel")
    cv2_available = False

import uuid
from TOMs.core.TOMsMessageLog import TOMsMessageLog

class gpsLayers(TOMsLayers):
    def __init__(self, iface):
        TOMsLayers.__init__(self, iface)
        self.iface = iface
        #TOMsMessageLog.logMessage("In gpsLayers.init ...", level=Qgis.Info)
        # TODO: Load these from a local file - or database
        self.TOMsLayerList = [
            "Bays",
            "Lines",
            "Signs",
            "RestrictionPolygons",
            # "ConstructionLines",
            # "CPZs",
            # "ParkingTariffAreas",
            # "StreetGazetteerRecords",
            "RoadCentreLine",
            "RoadCasement",
            # "RestrictionTypes",
            "BayLineTypes",
            # "BayTypes",
            # "LineTypes",
            # "RestrictionPolygonTypes",
            "LengthOfTime",
            "PaymentTypes",
            "RestrictionShapeTypes",
            "SignTypes",
            "TimePeriods",
            "UnacceptabilityTypes"
                         ]
        self.TOMsLayerDict = {}

class gpsParams(TOMsParams):
    def __init__(self):
        TOMsParams.__init__(self)
        #self.iface = iface

        #TOMsMessageLog.logMessage("In gpsParams.init ...", level=Qgis.Info)

        self.TOMsParamsList.extend([
                          "gpsPort",
                          "cameraNr"
                               ])

class FieldRestrictionTypeUtilsMixin():
    def __init__(self, iface):
        #RestrictionTypeUtilsMixin.__init__(self, iface)
        self.iface = iface
        self.settings = QgsSettings()

        #self.TOMsUtils = RestrictionTypeUtilsMixin(self.iface)

    def setDefaultFieldRestrictionDetails(self, currRestriction, currRestrictionLayer, currDate):
        TOMsMessageLog.logMessage("In setDefaultFieldRestrictionDetails: ", level=Qgis.Info)

        # TODO: Need to check whether or not these fields exist. Also need to retain the last values and reuse
        # gis.stackexchange.com/questions/138563/replacing-action-triggered-script-by-one-supplied-through-qgis-plugin

        try:
            currRestriction.setAttribute("CreateDateTime", currDate)
        except Exception as e:
            None

        try:
            generateGeometryUtils.setRoadName(currRestriction)
        except Exception as e:
            None

        """if currRestrictionLayer.geometryType() == 1:  # Line or Bay
            generateGeometryUtils.setAzimuthToRoadCentreLine(currRestriction)
            currRestriction.setAttribute("RestrictionLength", currRestriction.geometry().length())"""


        #currentCPZ, cpzWaitingTimeID = generateGeometryUtils.getCurrentCPZDetails(currRestriction)

        #currRestriction.setAttribute("CPZ", currentCPZ)

        #currDate = self.proposalsManager.date()

        if currRestrictionLayer.name() == "Lines":
            currRestriction.setAttribute("RestrictionTypeID", self.readLastUsedDetails("Lines", "RestrictionTypeID", 201))  # 10 = SYL (Lines)
            currRestriction.setAttribute("GeomShapeID", self.readLastUsedDetails("Lines", "GeomShapeID", 10))   # 10 = Parallel Line
            currRestriction.setAttribute("NoWaitingTimeID", self.readLastUsedDetails("Lines", "NoWaitingTimeID", None))
            currRestriction.setAttribute("NoLoadingTimeID", self.readLastUsedDetails("Lines", "NoLoadingTimeID", None))
            #currRestriction.setAttribute("NoWTimeID", cpzWaitingTimeID)
            #currRestriction.setAttribute("CreateDateTime", currDate)
            currRestriction.setAttribute("UnacceptableTypeID", self.readLastUsedDetails("Lines", "UnacceptableTypeID", None))

            generateGeometryUtils.setAzimuthToRoadCentreLine(currRestriction)
            currRestriction.setAttribute("RestrictionLength", currRestriction.geometry().length())

        elif currRestrictionLayer.name() == "Bays":
            currRestriction.setAttribute("RestrictionTypeID", self.readLastUsedDetails("Bays", "RestrictionTypeID", 101))  # 28 = Permit Holders Bays (Bays)
            currRestriction.setAttribute("GeomShapeID", self.readLastUsedDetails("Bays", "GeomShapeID", 1)) # 21 = Parallel Bay (Polygon)
            currRestriction.setAttribute("NrBays", -1)
            currRestriction.setAttribute("TimePeriodID", self.readLastUsedDetails("Bays", "TimePeriodID", None))

            #currRestriction.setAttribute("MaxStayID", ptaMaxStayID)
            #currRestriction.setAttribute("NoReturnID", ptaNoReturnTimeID)
            #currRestriction.setAttribute("ParkingTariffArea", currentPTA)
            #currRestriction.setAttribute("CreateDateTime", currDate)
            generateGeometryUtils.setAzimuthToRoadCentreLine(currRestriction)
            currRestriction.setAttribute("RestrictionLength", currRestriction.geometry().length())

        elif currRestrictionLayer.name() == "Signs":
            currRestriction.setAttribute("SignType_1", self.readLastUsedDetails("Signs", "SignType_1", 28))  # 28 = Permit Holders Only (Signs)

        elif currRestrictionLayer.name() == "RestrictionPolygons":
            currRestriction.setAttribute("RestrictionTypeID", self.readLastUsedDetails("RestrictionPolygons", "RestrictionTypeID", 4))  # 28 = Residential mews area (RestrictionPolygons)


    def storeLastUsedDetails(self, layer, field, value):
        entry = '{layer}/{field}'.format(layer=layer, field=field)
        TOMsMessageLog.logMessage("In storeLastUsedDetails: " + str(entry) + " (" + str(value) + ")", level=Qgis.Info)
        self.settings.setValue(entry, value)

    def readLastUsedDetails(self, layer, field, default):
        entry = '{layer}/{field}'.format(layer=layer, field=field)
        TOMsMessageLog.logMessage("In readLastUsedDetails: " + str(entry) + " (" + str(default) + ")", level=Qgis.Info)
        return self.settings.value(entry, default)

    def setupFieldRestrictionDialog(self, restrictionDialog, currRestrictionLayer, currRestriction):

        #self.restrictionDialog = restrictionDialog
        #self.currRestrictionLayer = currRestrictionLayer
        #self.currRestriction = currRestriction
        #self.restrictionTransaction = restrictionTransaction

        # Create a copy of the feature
        self.origFeature = originalFeature()
        self.origFeature.setFeature(currRestriction)

        if restrictionDialog is None:
            reply = QMessageBox.information(None, "Error",
                                            "setupFieldRestrictionDialog. Correct form not found",
                                            QMessageBox.Ok)
            TOMsMessageLog.logMessage(
                "In setupRestrictionDialog. dialog not found",
                level=Qgis.Warning)
            return

        restrictionDialog.attributeForm().disconnectButtonBox()
        button_box = restrictionDialog.findChild(QDialogButtonBox, "button_box")

        if button_box is None:
            TOMsMessageLog.logMessage(
                "In setupRestrictionDialog. button box not found",
                level=Qgis.Warning)
            return

        button_box.accepted.connect(functools.partial(self.onSaveFieldRestrictionDetails, currRestriction,
                                      currRestrictionLayer, restrictionDialog))

        button_box.rejected.connect(functools.partial(self.onRejectFieldRestrictionDetailsFromForm, restrictionDialog, currRestrictionLayer))

        restrictionDialog.attributeForm().attributeChanged.connect(functools.partial(self.onAttributeChangedClass2_local, currRestriction, currRestrictionLayer))

        self.photoDetails_field(restrictionDialog, currRestrictionLayer, currRestriction)

        """def onSaveRestrictionDetailsFromForm(self):
        TOMsMessageLog.logMessage("In onSaveRestrictionDetailsFromForm", level=Qgis.Info)
        self.onSaveRestrictionDetails(self.currRestriction,
                                      self.currRestrictionLayer, self.restrictionDialog, self.restrictionTransaction)"""

    def onAttributeChangedClass2_local(self, currFeature, layer, fieldName, value):

        #self.TOMsUtils.onAttributeChangedClass2(currFeature, layer, fieldName, value)

        TOMsMessageLog.logMessage(
            "In field:FormOpen:onAttributeChangedClass 2 - layer: " + str(layer.name()) + " (" + fieldName + "): " + str(value), level=Qgis.Info)


        # self.currRestriction.setAttribute(fieldName, value)
        try:

            currFeature[layer.fields().indexFromName(fieldName)] = value
            #currFeature.setAttribute(layer.fields().indexFromName(fieldName), value)

        except:

            reply = QMessageBox.information(None, "Error",
                                                "onAttributeChangedClass2. Update failed for: " + str(layer.name()) + " (" + fieldName + "): " + str(value),
                                                QMessageBox.Ok)  # rollback all changes


        self.storeLastUsedDetails(layer.name(), fieldName, value)

        return

    def onSaveFieldRestrictionDetails(self, currFeature, currFeatureLayer, dialog):
        TOMsMessageLog.logMessage("In onSaveFieldRestrictionDetails: ", level=Qgis.Info)

        try:
            self.camera1.endCamera()
            self.camera2.endCamera()
            self.camera3.endCamera()
        except:
            None

        attrs1 = currFeature.attributes()
        TOMsMessageLog.logMessage("In onSaveDemandDetails: currRestriction: " + str(attrs1),
                                 level=Qgis.Info)

        TOMsMessageLog.logMessage(
            ("In onSaveDemandDetails. geometry: " + str(currFeature.geometry().asWkt())),
            level=Qgis.Info)

        currFeatureID = currFeature.id()
        TOMsMessageLog.logMessage("In onSaveDemandDetails: currFeatureID: " + str(currFeatureID),
                                 level=Qgis.Info)

        status = currFeatureLayer.updateFeature(currFeature)
        """if currFeatureID > 0:   # Not sure what this value should if the feature has not been created ...

            # TODO: Sort out this for UPDATE
            self.setDefaultRestrictionDetails(currFeature, currFeatureLayer)

            status = currFeatureLayer.updateFeature(currFeature)
            TOMsMessageLog.logMessage("In onSaveDemandDetails: updated Feature: ", level=Qgis.Info)
        else:
            status = currFeatureLayer.addFeature(currFeature)
            TOMsMessageLog.logMessage("In onSaveDemandDetails: added Feature: " + str(status), level=Qgis.Info)"""

        TOMsMessageLog.logMessage("In onSaveDemandDetails: Before commit", level=Qgis.Info)

        """reply = QMessageBox.information(None, "Information",
                                        "Wait a moment ...",
                                        QMessageBox.Ok)"""
        attrs1 = currFeature.attributes()
        TOMsMessageLog.logMessage("In onSaveDemandDetails: currRestriction: " + str(attrs1),
                                 level=Qgis.Info)

        TOMsMessageLog.logMessage(
            ("In onSaveDemandDetails. geometry: " + str(currFeature.geometry().asWkt())),
            level=Qgis.Info)

        """TOMsMessageLog.logMessage("In onSaveDemandDetails: currActiveLayer: " + str(self.iface.activeLayer().name()),
                                 level=Qgis.Info)"""
        TOMsMessageLog.logMessage("In onSaveDemandDetails: currActiveLayer: " + str(currFeatureLayer.name()),
                                 level=Qgis.Info)
        #currFeatureLayer
        #Test
        #status = dialog.attributeForm().save()
        #status = dialog.accept()
        #status = dialog.accept()

        """reply = QMessageBox.information(None, "Information",
                                        "And another ... iseditable: " + str(currFeatureLayer.isEditable()),
                                        QMessageBox.Ok)"""

        #currFeatureLayer.blockSignals(True)

        """if currFeatureID == 0:
            self.iface.mapCanvas().unsetMapTool(self.iface.mapCanvas().mapTool())
            TOMsMessageLog.logMessage("In onSaveDemandDetails: mapTool unset",
                                     level=Qgis.Info)"""

        """try:
            currFeatureLayer.commitChanges()
        except:
            reply = QMessageBox.information(None, "Information", "Problem committing changes" + str(currFeatureLayer.commitErrors()), QMessageBox.Ok)

        #currFeatureLayer.blockSignals(False)

        TOMsMessageLog.logMessage("In onSaveDemandDetails: changes committed", level=Qgis.Info)

        status = dialog.close()"""

        status = dialog.attributeForm().save()
        #currRestrictionLayer.addFeature(currRestriction)  # TH (added for v3)
        currFeatureLayer.updateFeature(currFeature)  # TH (added for v3)

        try:
            currFeatureLayer.commitChanges()
        except:
            reply = QMessageBox.information(None, "Information", "Problem committing changes" + str(currFeatureLayer.commitErrors()), QMessageBox.Ok)

        #currFeatureLayer.blockSignals(False)

        TOMsMessageLog.logMessage("In onSaveDemandDetails: changes committed", level=Qgis.Info)

        status = dialog.close()
        #self.mapTool = None
        #self.iface.mapCanvas().unsetMapTool(self.iface.mapCanvas().mapTool())

    def onRejectFieldRestrictionDetailsFromForm(self, restrictionDialog, currFeatureLayer):
        TOMsMessageLog.logMessage("In onRejectFieldRestrictionDetailsFromForm", level=Qgis.Info)

        try:
            self.camera1.endCamera()
            self.camera2.endCamera()
            self.camera3.endCamera()
        except:
            None

        currFeatureLayer.rollBack()
        restrictionDialog.reject()

        #del self.mapTool

    def photoDetails_field(self, restrictionDialog, currRestrictionLayer, currRestriction):

        # Function to deal with photo fields

        self.demandDialog = restrictionDialog
        self.currDemandLayer = currRestrictionLayer
        self.currFeature = currRestriction

        TOMsMessageLog.logMessage("In photoDetails", level=Qgis.Info)

        FIELD1 = self.demandDialog.findChild(QLabel, "Photo_Widget_01")
        FIELD2 = self.demandDialog.findChild(QLabel, "Photo_Widget_02")
        FIELD3 = self.demandDialog.findChild(QLabel, "Photo_Widget_03")

        photoPath = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('PhotoPath')
        projectFolder = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('project_folder')

        try:
            cameraNr = int(self.params.setParam("cameraNr"))
        except Exception as e:
            TOMsMessageLog.logMessage("In formCamera:init: cameraNr issue: {}".format(e), level=Qgis.Info)
            cameraNr = 0
        TOMsMessageLog.logMessage("In formCamera:init: cameraNr is: {}".format(cameraNr), level=Qgis.Info)

        """ v2.18
        photoPath = QgsExpressionContextUtils.projectScope().variable('PhotoPath')
        projectFolder = QgsExpressionContextUtils.projectScope().variable('project_folder')
        """
        path_absolute = os.path.join(projectFolder, photoPath)

        if path_absolute == None:
            reply = QMessageBox.information(None, "Information", "Please set value for PhotoPath.", QMessageBox.Ok)
            return

        # Check path exists ...
        if os.path.isdir(path_absolute) == False:
            reply = QMessageBox.information(None, "Information", "PhotoPath folder " + str(
                path_absolute) + " does not exist. Please check value.", QMessageBox.Ok)
            return

        layerName = self.currDemandLayer.name()

        # Generate the full path to the file

        # fileName1 = "Photos"
        fileName1 = "Photos_01"
        fileName2 = "Photos_02"
        fileName3 = "Photos_03"

        idx1 = self.currDemandLayer.fields().indexFromName(fileName1)
        idx2 = self.currDemandLayer.fields().indexFromName(fileName2)
        idx3 = self.currDemandLayer.fields().indexFromName(fileName3)

        """  v2.18
        idx1 = self.currDemandLayer.fieldNameIndex(fileName1)
        idx2 = self.currDemandLayer.fieldNameIndex(fileName2)
        idx3 = self.currDemandLayer.fieldNameIndex(fileName3)
        """

        TOMsMessageLog.logMessage("In photoDetails. idx1: " + str(idx1) + "; " + str(idx2) + "; " + str(idx3),
                                 level=Qgis.Info)
        # if currFeatureFeature[idx1]:
        # TOMsMessageLog.logMessage("In photoDetails. photo1: " + str(currFeatureFeature[idx1]), level=Qgis.Info)
        # TOMsMessageLog.logMessage("In photoDetails. photo2: " + str(currFeatureFeature.attribute(idx2)), level=Qgis.Info)
        # TOMsMessageLog.logMessage("In photoDetails. photo3: " + str(currFeatureFeature.attribute(idx3)), level=Qgis.Info)

        if FIELD1:
            TOMsMessageLog.logMessage("In photoDetails. FIELD 1 exisits",
                                     level=Qgis.Info)
            if self.currFeature[idx1]:
                newPhotoFileName1 = os.path.join(path_absolute, self.currFeature[idx1])
                TOMsMessageLog.logMessage("In photoDetails. photo1: {}".format(newPhotoFileName1), level=Qgis.Warning)
            else:
                newPhotoFileName1 = None

            # TOMsMessageLog.logMessage("In photoDetails. Photo1: " + str(newPhotoFileName1), level=Qgis.Info)
            pixmap1 = QPixmap(newPhotoFileName1)
            if pixmap1.isNull():
                pass
                # FIELD1.setText('Picture could not be opened ({path})'.format(path=newPhotoFileName1))
            else:
                FIELD1.setPixmap(pixmap1)
                FIELD1.setScaledContents(True)
                TOMsMessageLog.logMessage("In photoDetails. Photo1: " + str(newPhotoFileName1), level=Qgis.Info)

            START_CAMERA_1 = self.demandDialog.findChild(QPushButton, "startCamera1")
            TAKE_PHOTO_1 = self.demandDialog.findChild(QPushButton, "getPhoto1")
            TAKE_PHOTO_1.setEnabled(False)

            self.camera1 = formCamera(path_absolute, newPhotoFileName1, cameraNr)
            START_CAMERA_1.clicked.connect(
                functools.partial(self.camera1.useCamera, START_CAMERA_1, TAKE_PHOTO_1, FIELD1))
            self.camera1.notifyPhotoTaken.connect(functools.partial(self.savePhotoTaken, idx1))

        if FIELD2:
            TOMsMessageLog.logMessage("In photoDetails. FIELD 2 exisits",
                                     level=Qgis.Info)
            if self.currFeature[idx2]:
                newPhotoFileName2 = os.path.join(path_absolute, self.currFeature[idx2])
                TOMsMessageLog.logMessage("In photoDetails. Photo1: " + str(newPhotoFileName2), level=Qgis.Info)
            else:
                newPhotoFileName2 = None

            # newPhotoFileName2 = os.path.join(path_absolute, str(self.currFeature[idx2]))
            # newPhotoFileName2 = os.path.join(path_absolute, str(self.currFeature.attribute(fileName2)))
            # TOMsMessageLog.logMessage("In photoDetails. Photo2: " + str(newPhotoFileName2), level=Qgis.Info)
            pixmap2 = QPixmap(newPhotoFileName2)
            if pixmap2.isNull():
                pass
                # FIELD1.setText('Picture could not be opened ({path})'.format(path=newPhotoFileName1))
            else:
                FIELD2.setPixmap(pixmap2)
                FIELD2.setScaledContents(True)
                TOMsMessageLog.logMessage("In photoDetails. Photo2: " + str(newPhotoFileName2), level=Qgis.Info)

            START_CAMERA_2 = self.demandDialog.findChild(QPushButton, "startCamera2")
            TAKE_PHOTO_2 = self.demandDialog.findChild(QPushButton, "getPhoto2")
            TAKE_PHOTO_2.setEnabled(False)

            self.camera2 = formCamera(path_absolute, newPhotoFileName2, cameraNr)
            START_CAMERA_2.clicked.connect(
                functools.partial(self.camera2.useCamera, START_CAMERA_2, TAKE_PHOTO_2, FIELD2))
            self.camera2.notifyPhotoTaken.connect(functools.partial(self.savePhotoTaken, idx2))

        if FIELD3:
            TOMsMessageLog.logMessage("In photoDetails. FIELD 3 exisits",
                                     level=Qgis.Info)

            if self.currFeature[idx3]:
                newPhotoFileName3 = os.path.join(path_absolute, self.currFeature[idx3])
                TOMsMessageLog.logMessage("In photoDetails. Photo1: " + str(newPhotoFileName3), level=Qgis.Info)
            else:
                newPhotoFileName3 = None

            # newPhotoFileName3 = os.path.join(path_absolute, str(self.currFeature[idx3]))
            # newPhotoFileName3 = os.path.join(path_absolute,
            #                                 str(self.currFeature.attribute(fileName3)))
            # newPhotoFileName3 = os.path.join(path_absolute, str(layerName + "_Photos_03"))

            # TOMsMessageLog.logMessage("In photoDetails. Photo3: " + str(newPhotoFileName3), level=Qgis.Info)
            pixmap3 = QPixmap(newPhotoFileName3)
            if pixmap3.isNull():
                pass
                # FIELD1.setText('Picture could not be opened ({path})'.format(path=newPhotoFileName1))
            else:
                FIELD3.setPixmap(pixmap3)
                FIELD3.setScaledContents(True)
                TOMsMessageLog.logMessage("In photoDetails. Photo3: " + str(newPhotoFileName3), level=Qgis.Info)

            START_CAMERA_3 = self.demandDialog.findChild(QPushButton, "startCamera3")
            TAKE_PHOTO_3 = self.demandDialog.findChild(QPushButton, "getPhoto3")
            TAKE_PHOTO_3.setEnabled(False)

            self.camera3 = formCamera(path_absolute, newPhotoFileName3, cameraNr)
            START_CAMERA_3.clicked.connect(
                functools.partial(self.camera3.useCamera, START_CAMERA_3, TAKE_PHOTO_3, FIELD3))
            self.camera3.notifyPhotoTaken.connect(functools.partial(self.savePhotoTaken, idx3))

        pass

    def getLookupDescription(self, lookupLayer, code):

        #TOMsMessageLog.logMessage("In getLookupDescription", level=Qgis.Info)

        query = "\"Code\" = " + str(code)
        request = QgsFeatureRequest().setFilterExpression(query)

        #TOMsMessageLog.logMessage("In getLookupDescription. queryStatus: " + str(query), level=Qgis.Info)

        for row in lookupLayer.getFeatures(request):
            #TOMsMessageLog.logMessage("In getLookupDescription: found row " + str(row.attribute("Description")), level=Qgis.Info)
            return row.attribute("Description") # make assumption that only one row

        return None

    @pyqtSlot(str)
    def savePhotoTaken(self, idx, fileName):
        TOMsMessageLog.logMessage("In demandFormUtils::savePhotoTaken ... " + fileName + " idx: " + str(idx),
                                 level=Qgis.Info)
        if len(fileName) > 0:
            simpleFile = os.path.basename(fileName)
            TOMsMessageLog.logMessage("In demandFormUtils::savePhotoTaken. Simple file: " + simpleFile, level=Qgis.Info)

            try:
                self.currFeature[idx] = simpleFile
                TOMsMessageLog.logMessage("In demandFormUtils::savePhotoTaken. attrib value changed", level=Qgis.Info)
            except:
                TOMsMessageLog.logMessage("In demandFormUtils::savePhotoTaken. problem changing attrib value",
                                         level=Qgis.Info)
                reply = QMessageBox.information(None, "Error",
                                                "savePhotoTaken. problem changing attrib value",
                                                QMessageBox.Ok)

