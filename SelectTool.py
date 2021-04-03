# -*- coding: utf-8 -*-
"""
/***************************************************************************
 movingTrafficSigns
                                 A QGIS plugin
 movingTrafficeSigns
                              -------------------
        begin                : 2019-05-08
        git sha              : $Format:%H$
        copyright            : (C) 2019 by TH
        email                : th@mhtc.co.uk
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

#import resources
# Import the code for the dialog

import os.path

from qgis.PyQt.QtWidgets import (
    QMessageBox,
    QAction,
    QDialogButtonBox,
    QLabel,
    QDockWidget,
    QDialog,
    QLabel,
    QPushButton,
    QApplication,
    QMenu
)

from qgis.PyQt.QtGui import (
    QIcon,
    QPixmap,
    QImage
)


from qgis.PyQt.QtCore import (
    QObject,
    QThread,
    pyqtSignal,
    pyqtSlot,
    Qt,
    QSettings, QTranslator, qVersion, QCoreApplication,
    QDateTime
)

from qgis.core import (
    QgsMessageLog,
    QgsExpressionContextUtils,
    QgsWkbTypes,
    QgsMapLayer, Qgis, QgsRectangle, QgsFeatureRequest, QgsVectorLayer, QgsFeature, QgsProject
)
from qgis.gui import (
    QgsMapToolIdentify
)
#from qgis.core import *
#from qgis.gui import *
from TOMs.core.TOMsMessageLog import TOMsMessageLog
from .demand_VRMs_UtilsClass import VRMsUtilsMixin, vrmParams
from restrictionsWithGNSS.SelectTool import (GeometryInfoMapTool, RemoveRestrictionTool)
#from .formUtils import demandFormUtils

#############################################################################

class demandVRMInfoMapTool(VRMsUtilsMixin, GeometryInfoMapTool):

    notifyFeatureFound = pyqtSignal(QgsVectorLayer, QgsFeature)

    def __init__(self, iface, surveyID, enumerator, dbConn):
        GeometryInfoMapTool.__init__(self, iface)
        self.iface = iface
        VRMsUtilsMixin.__init__(self, iface)

        self.surveyID = surveyID
        self.enumerator = enumerator
        self.dbConn = dbConn
        self.params = vrmParams()
        TOMsMessageLog.logMessage("In demandVRMInfoMapTool ... surveyID: {}; enumerator: {}".format(self.surveyID, self.enumerator), level=Qgis.Warning)

        self.RESTRICTION_TYPES = QgsProject.instance().mapLayersByName("SupplyRestrictionTypesInUse_View")[0]

    def showRestrictionDetails(self, closestLayer, closestFeature):

        self.params.getParams()
        self.surveyID = str(self.params.setParam("CurrentSurvey"))
        self.enumerator = str(self.params.setParam("Enumerator"))

        TOMsMessageLog.logMessage(
            "In demandVRMInfoMapTool.showRestrictionDetails ... surveyID: {}, enumerator: {}".format(self.surveyID, self.enumerator),
            level=Qgis.Info)

        TOMsMessageLog.logMessage(
            "In demandVRMInfoMapTool.showRestrictionDetails ... Layer: {}".format(closestLayer.name()),
            level=Qgis.Info)

        GeometryID = closestFeature[closestLayer.fields().indexFromName("GeometryID")]

        # Now want to swap to use "RestrictionsInSurveys"
        # get relevant feature ...
        restrictionsInSurveysLayer = QgsProject.instance().mapLayersByName("RestrictionsInSurveys")[0]

        filterString = '\"SurveyID\" = {} AND \"GeometryID\" = \'{}\''.format(self.surveyID, GeometryID)

        TOMsMessageLog.logMessage(
            "In demandVRMInfoMapTool.showRestrictionDetails ... filterString: {}".format(filterString),
            level=Qgis.Info)

        request = QgsFeatureRequest().setFilterExpression(filterString)
        restrictionFound = False
        for currRestriction in restrictionsInSurveysLayer.getFeatures(request):
            TOMsMessageLog.logMessage(
                "In demandVRMInfoMapTool.showRestrictionDetails ... restriction found: ",
                level=Qgis.Info)
            restrictionFound = True
            break  # take the first one (assuming only one!)

        if restrictionFound == False:
            reply = QMessageBox.information(None, "Information",
                                            "Restriction not found {} in survey {}".format(GeometryID, self.surveyID),
                                            QMessageBox.Ok)
            return

        # TODO: could improve ... basically check to see if transaction in progress ...
        if restrictionsInSurveysLayer.isEditable() == True:
            if restrictionsInSurveysLayer.commitChanges() == False:
                reply = QMessageBox.information(None, "Information",
                                                "Problem committing changes" + str(restrictionsInSurveysLayer.commitErrors()),
                                                QMessageBox.Ok)
            else:
                TOMsMessageLog.logMessage("In showRestrictionDetails: changes committed", level=Qgis.Info)

        status = restrictionsInSurveysLayer.startEditing()

        try:
            dialog = self.iface.getFeatureForm(restrictionsInSurveysLayer, currRestriction)
        except Exception as e:
            reply = QMessageBox.information(None, "Information",
                                            "Unexcepted error for this restriction {}.{}".format(GeometryID, e),
                                            QMessageBox.Ok)
            return

        self.setupFieldRestrictionDialog(dialog, restrictionsInSurveysLayer, currRestriction)

        dialog.show()

    def getFeatureDetails(self, featureList, layerList):
        TOMsMessageLog.logMessage("In demandVRMInfoMapTool.getFeatureDetails", level=Qgis.Info)

        self.featureList = featureList
        self.layerList = layerList

        # Creates the context menu and returns the selected feature and layer
        TOMsMessageLog.logMessage("In demandVRMInfoMapTool.getFeatureDetails: nrFeatures: " + str(len(featureList)), level=Qgis.Info)

        self.actions = []
        self.menu = QMenu(self.iface.mapCanvas())

        for feature in featureList:

            try:
                GeometryID = feature.attribute('GeometryID')
                RestrictionDescription = self.getLookupDescription(self.RESTRICTION_TYPES, feature.attribute('RestrictionTypeID'))

                title = "{RestrictionDescription} [{GeometryID}]".format(RestrictionDescription=RestrictionDescription,
                                                                         GeometryID=GeometryID)
            except Exception as e:
                reply = QMessageBox.information(None, "Information", "Problem selecting features ...{}".format(e), QMessageBox.Ok)
                return None, None

            action = QAction(title, self.menu)
            self.actions.append(action)

            self.menu.addAction(action)

        TOMsMessageLog.logMessage("In getFeatureDetails: showing menu?", level=Qgis.Info)

        clicked_action = self.menu.exec_(self.iface.mapCanvas().mapToGlobal(self.event.pos()))
        TOMsMessageLog.logMessage(("In getFeatureDetails:clicked_action: " + str(clicked_action)), level=Qgis.Info)

        if clicked_action is not None:

            TOMsMessageLog.logMessage(("In getFeatureDetails:clicked_action: " + str(clicked_action.text())),
                                     level=Qgis.Info)
            idxList = self.getIdxFromGeometryID(clicked_action.text(), featureList)

            TOMsMessageLog.logMessage("In getFeatureDetails: idx = " + str(idxList), level=Qgis.Info)

            if idxList >= 0:
                # TODO: need to be careful here so that we use primary key
                """TOMsMessageLog.logMessage("In getFeatureDetails: feat = " + str(featureList[idxList].attribute('id')),
                                         level=Qgis.Info)"""
                return featureList[idxList], layerList[idxList]

        TOMsMessageLog.logMessage(("In getFeatureDetails. No action found."), level=Qgis.Info)

        return None, None

