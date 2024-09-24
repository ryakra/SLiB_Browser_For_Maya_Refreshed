#########################################################################
#
#   SLiBUtilities
#
#   Version:    1.0
#   Author:     DGDM
#   Copyright:  2016 DGDM
#
#########################################################################

import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import math
import pymel.core as pm
import pymel.core.datatypes as dt
import Qt


if '2017' in cmds.about(version=1):
    from shiboken2 import wrapInstance
else:
    from shiboken import wrapInstance

from Qt import QtGui, QtCore, QtWidgets
from Qt.QtGui import *
from Qt.QtCore import *
from Qt.QtWidgets import *

SLiB_dir = os.path.dirname(cmds.pluginInfo('SLiB', q=1, path=1)) + '/SLiB/'
SLiB_img = mel.eval('getenv SLiBImage;')

def setRenderer(r, *args):
    cmds.setAttr("defaultRenderGlobals.currentRenderer", r, type="string")
    messager('current Renderer: ' + r, 'green')
    
def gib(x):
    if x == 'library':
        return mel.eval('getenv SLiBRARY;')
        
    if x == 'libraries':
        f = open(SLiB_dir +'set/LIB_Dictionary.txt', 'r')
        libDict = f.read().splitlines()
        return libDict
    
    if x == 'mainCat':
        return cmds.iconTextRadioCollection('mainCatCollection', q=1, sl=1).lower()
        
    if x == 'currLocation':
        try:
            return os.path.normpath(''.join(cmds.treeView('treeView', q=1, si=1)))
        except:
            return None

    if x == 'position':
        return cmds.xform(selection, q=1, t=1)
    
    if x == 'name':
        return cmds.textField('SLiB_TEXTFIELD_Name', q=1, tx=1).replace(' ','_')
        
    if x == 'pickedMat':
        mat = None
        if cmds.swatchDisplayPort('swatchDP', ex=1):
            mat = cmds.swatchDisplayPort('swatchDP', q=1, sn=1)
        return mat
        
    if x == 'mayaVersion':
        return cmds.about(version=1)
        
    if x == 'renderer':
        return cmds.getAttr('defaultRenderGlobals.currentRenderer').lower()
        
    if x == 'thumbsize':
        thumbsize = cmds.textField('SLiB_CBOX_Resolution', q=1, tx=1)
        if thumbsize.isnumeric():
            if int(thumbsize) > int(512):
                thumbsize = 512
                cmds.textField('SLiB_CBOX_Resolution', e=1, tx=512)
        
            return int(thumbsize)
        
        else:
            print 'Please enter numeric value!',
            cmds.textField('SLiB_CBOX_Resolution', e=1, tx=128)
            return int(128)

        
def gibBBox(selection):
    ObjX = abs(cmds.getAttr(selection+'.boundingBoxMaxX')) + abs(cmds.getAttr(selection+'.boundingBoxMinX'))
    ObjY = abs(cmds.getAttr(selection+'.boundingBoxMaxY')) + abs(cmds.getAttr(selection+'.boundingBoxMinY'))
    ObjZ = abs(cmds.getAttr(selection+'.boundingBoxMaxZ')) + abs(cmds.getAttr(selection+'.boundingBoxMinZ'))
    return "%.2f" % ObjX, "%.2f" % ObjY, "%.2f" % ObjZ
    
def gibTexSlot(node):
    if cmds.objectType(node) == 'file':
        return '.fileTextureName'
    if cmds.objectType(node) == 'RedshiftNormalMap' or cmds.objectType(node) == 'RedshiftSprite' or cmds.objectType(node) == 'RedshiftDomeLight' or cmds.objectType(node) == 'RedshiftNormalMap' or cmds.objectType(node) == 'RedshiftLightGobo':
        return '.tex0'
    if cmds.objectType(node) == 'RedshiftBokeh':
        return '.dofBokehImage'

def delete(obj):
    if cmds.objExists(obj):
        cmds.delete(obj)
        
def deleteUI(obj):
    try:
        cmds.deleteUI(obj)
    except:
        pass

def fileType(file):
    fileType = os.path.splitext(file)[1]
    
    if fileType == '.ma':
        fileType = 'mayaAscii'
    
    if fileType == '.mb':
        fileType = 'mayaBinary'
    
    if fileType == '.obj':
        fileType = 'OBJ'
    
    return fileType

def freeze():
    obj = cmds.ls(sl=1)
    if len(obj) != 0:
        cmds.makeIdentity(obj, apply=1, t=1, r=1, s=1, n=0)
        messager('Freezed!', 'blue')
    else:
        messager('Please select an Object!', 'red')

def autoPlacePivot():
    obj = cmds.ls(sl=1)
    if len(obj) != 0:
        cmds.xform(obj, cp=1)
        bbox = cmds.exactWorldBoundingBox()
        bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
        cmds.xform(obj, piv=bottom, ws=1)
        cmds.move( 0, 0, 0, obj, rpr=1 )
        messager('Object moved to Origin and Pivot placed at bottom!', 'blue')
    else:
        messager('Please select an Object!', 'red')

def SNRSpeed():
    newShaderName = cmds.textField('SLiB_TEXTFIELD_Name', q=1 ,text=1)
    if len(newShaderName) == 0:
        messager('Please give a Name', 'red')
        sys.exit()
    else:
        shaderHolder = cmds.ls(sl=1)
        if len(shaderHolder) != 0:
            if cmds.objectType(shaderHolder) == 'transform' or cmds.objectType(shaderHolder) == 'mesh':
                SG = cmds.listConnections(cmds.ls(sl=1, dag=1, s=1), type='shadingEngine')
                MAT = sorted(set(cmds.ls(cmds.listConnections(SG), mat=1)))
                if len(MAT) != 1:
                    for m in MAT:
                        if cmds.nodeType(m) == 'displacementShader':
                            MAT.remove(m)
                        
                cmds.select(MAT)
                
                snrDict=[]
                f = open(mel.eval('getenv SLiB;') +'/set/SNR_Dictionary.txt', 'r')
                for line in f.readlines():
                    snrDict.append([line.rstrip()])
        
                for i in range(0, len(MAT)):
                    cmds.select(cmds.listHistory(SG), noExpand=1)
                    SNW = cmds.ls(sl=1)
                    for e in SNW:
                        nodeTyp = str(cmds.nodeType(e))
                        nodeTyp_oldList = [x[0].split(',')[0] for x in snrDict]
                        nodeTyp_newList = [x[0].split(',')[1] for x in snrDict]
                        
                        if nodeTyp in nodeTyp_oldList:
                           entspricht = nodeTyp_oldList.index(nodeTyp)
                           cmds.rename(e, newShaderName + nodeTyp_newList[entspricht])
    cmds.select(cl=1)
    cmds.select(shaderHolder)
    cmds.textField('SLiB_TEXTFIELD_Name', e=1 ,text='')
    
def SNRenamer():
    if len(cmds.ls(sl=1)) != 0:
        SG = cmds.listConnections(cmds.ls(sl=1), type='shadingEngine')
        if SG == None:
            messager('Please select a Material!', 'red')

        else:
            MAT = cmds.ls(cmds.listConnections(SG), mat=1)
            if len(MAT) > 1:
                for m in MAT:
                    if cmds.nodeType(m) == 'displacementShader':
                        MAT.remove(m)
                    
            cmds.select(MAT)
            snrDict=[]
            f = open(mel.eval('getenv SLiB;') +'/set/SNR_Dictionary.txt', 'r')
            for line in f.readlines():
                snrDict.append([line.rstrip()])

            result = cmds.promptDialog(t='Rename', m='Enter Name:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
            if result == 'OK':
                newName = cmds.promptDialog(q=1, t=1).replace(' ','_')
                for i in range(0, len(MAT)):
                    SG = cmds.listConnections(MAT[i], type='shadingEngine')
                    if SG[0] == "" or SG[0] == 'initialShadingGroup':
                        mel.warning('select a material node first')
                    else:
                        cmds.select(cmds.listHistory(SG[0]), noExpand=1)
                        SNW = cmds.ls(sl=1)
                        for e in SNW:
                            nodeTyp = str(cmds.nodeType(e))
                            nodeTyp_oldList = [x[0].split(',')[0] for x in snrDict]
                            nodeTyp_newList = [x[0].split(',')[1] for x in snrDict]
                            
                            if nodeTyp in nodeTyp_oldList:
                               entspricht = nodeTyp_oldList.index(nodeTyp)
                               cmds.rename(e, newName + nodeTyp_newList[entspricht])
    else:
        messager('Please select a Material!', 'red')

    cmds.select(cl=1)

def selectFromScreen(x):
    activeView = omui.M3dView.active3dView()
    viewObj = []
    
    if x == 'screen':
        om.MGlobal.selectFromScreen(0, 0, activeView.portWidth(), activeView.portHeight(), om.MGlobal.kReplaceList, om.MGlobal.kSurfaceSelectMethod ) #om.MGlobal.kSurfaceSelectMethod
        
        for e in cmds.ls(sl=1):
            cmds.select(e)
            if cmds.filterExpand(sm=12, fp=1) != None:
                viewObj.append(e)
        cmds.select(cl=1)
        
    if x == 'mouse':
        if cmds.iconTextCheckBox('matPicker', q=1, v=1):
            mousePos = cmds.draggerContext('matContext', q=1, ap=1)
            om.MGlobal.selectFromScreen(int(mousePos[0]), int(mousePos[1]), om.MGlobal.kReplaceList, om.MGlobal.kSurfaceSelectMethod)
            try:
                viewObj = cmds.ls(sl=1, l=1)[0]
                cmds.select(cl=1)
            except:
                viewObj = None
        
        if cmds.iconTextCheckBox('ipt', q=1, v=1):
            mousePos = cmds.draggerContext('iptContext', q=1, ap=1)
            om.MGlobal.selectFromScreen(int(mousePos[0]), int(mousePos[1]), om.MGlobal.kReplaceList, om.MGlobal.kSurfaceSelectMethod )
            try:
                viewObj = cmds.listRelatives(cmds.ls(sl=1)[0], f=1)[0].split('|')[1]
                cmds.select(cl=1)
            except:
                viewObj = None
        
    if viewObj:
        return viewObj
    else:
        return None

def intersect(dag, pos, dir):
    print dag
    targetDAGPath = getDAGObject(dag)
    meshObj = om.MFnMesh(targetDAGPath)
    posFP = om.MFloatPoint(pos[0],pos[1],pos[2])
    dirFP = om.MFloatVector(dir[0],dir[1],dir[2])
    
    hitFPoint = om.MFloatPoint()
    hitFace = om.MScriptUtil()
    hitTri = om.MScriptUtil()
    hitFace.createFromInt(0)
    hitTri.createFromInt(0)
    
    hFacePtr = hitFace.asIntPtr()
    hTriPtr = hitTri.asIntPtr()
    
    hit = meshObj.closestIntersection( posFP,
                                dirFP,
                                None,
                                None,
                                True,
                                om.MSpace.kWorld,
                                9999,
                                True,
                                None,
                                hitFPoint,
                                None,
                                hFacePtr,
                                hTriPtr,
                                None,
                                None)
                                
    return hit, hitFPoint, meshObj, hitFace.getInt(hFacePtr), hitTri.getInt(hTriPtr)

def getDagPath(objectName):
    tempList = om.MSelectionList()
    tempList.add(objectName)
    dagpath = om.MDagPath()
    tempList.getDagPath(0, dagpath)
    return dagpath

def getDAGObject(dagstring):
    sList = om.MSelectionList()
    meshDP = om.MDagPath()
    sList.add(dagstring)
    sList.getDagPath(0,meshDP)
    return meshDP;
    
def view_to_world(x,y):
    currentView = omui.M3dView().active3dView()
    resultPt = om.MPoint()
    resultVtr = om.MVector()
    currentView.viewToWorld(int(x), int(y), resultPt, resultVtr)
    return [resultPt.x,resultPt.y,resultPt.z],[resultVtr.x,resultVtr.y,resultVtr.z]

def getEulerRotationQuaternion(upvector, directionvector):
    quat = om.MQuaternion(upvector, directionvector)
    quatAsEuler = om.MEulerRotation()
    quatAsEuler = quat.asEulerRotation()
    return math.degrees(quatAsEuler.x), math.degrees(quatAsEuler.y), math.degrees(quatAsEuler.z)

def getImageSize(img):
    image = om.MImage()
    image.readFromFile(img)
    scriptUtil = om.MScriptUtil()
    width = om.MScriptUtil()
    height = om.MScriptUtil()
    width.createFromInt(0)
    height.createFromInt(0)
    pWidth = width.asUintPtr()
    pHeight = height.asUintPtr() 
    image.getSize( pWidth, pHeight )
    vWidth = width.getUint(pWidth)
    vHeight = height.getUint(pHeight)
    
    return [vWidth,vHeight]

def hypershadeThumbs():
    if cmds.menuItem('slHyperShadeThumbs', q=1, cb=1):
        mel.eval("renderThumbnailUpdate false;")
        print 'Hypershade thumbnail updates turned OFF'
    else:
        mel.eval("renderThumbnailUpdate true;")
        print 'Hypershade thumbnail updates turned ON'

def findSimilar():
    selectedMesh = cmds.ls(sl=1, type='mesh', dag=1, l=1)
    evf = cmds.polyEvaluate(selectedMesh, v=1, e=1, f=1)

    sameMehes = []
    allMeshes = cmds.ls(type='mesh', dag=1, l=1)
    for e in allMeshes:
        if cmds.polyEvaluate(e, v=1, e=1, f=1) == evf:
            sameMehes.append(e)
            
    if sameMehes:
        cmds.select(sameMehes)
        print str(len(sameMehes)) + ' similar meshes found and selected'

def snapshotCam():
    perspPanel = cmds.getPanel(wl='Persp View')
    cmds.setFocus(perspPanel)
    cam = cmds.modelPanel(cmds.getPanel(wf=1), q=1, cam=1)
    if cmds.menuItem('slSnapshotCam', q=1, cb=1):

        global snASR
        global snResW
        global snResW
        global snFit
        global snCamDR
        global snCamGM
        global snCamMO
        global snCamMC
        global snCamOV

        if gib('renderer') == 'vray':
            snASR = cmds.getAttr('vraySettings.aspr')
            snResW = cmds.getAttr('vraySettings.wi')
            snResH = cmds.getAttr('vraySettings.he')
        else:
            snASR = cmds.getAttr('defaultResolution.dar')
            snResW = cmds.getAttr('defaultResolution.w')
            snResH = cmds.getAttr('defaultResolution.h')
        
        snFit = cmds.getAttr(cam + '.ff')
        snCamDR = cmds.getAttr(cam + '.displayResolution')
        snCamGM = cmds.getAttr(cam + '.displayGateMask')
        snCamMO = cmds.getAttr(cam + '.displayGateMaskOpacity')
        snCamMC = list(cmds.getAttr(cam + '.displayGateMaskColor')[0])
        snCamOV = cmds.getAttr(cam + '.overscan')
        
        if gib('renderer') == 'vray':
            cmds.setAttr('vraySettings.wi', 512)
            cmds.setAttr('vraySettings.he', 512)
            cmds.setAttr('vraySettings.aspr', 1)
            mel.eval("vrayUpdateResolution;")
            mel.eval("vrayUpdatePixelAspectRatioControl;")
            mel.eval("vrayUpdateResolution;")
        else:
            cmds.setAttr('defaultResolution.w', 512)
            cmds.setAttr('defaultResolution.h', 512)
            cmds.setAttr('defaultResolution.dar', 1)

        cmds.setAttr(cam + '.ff', 2)
        cmds.setAttr(cam + '.displayResolution', 1)
        cmds.setAttr(cam + '.displayGateMask', 1)
        cmds.setAttr(cam + '.displayGateMaskOpacity', 0.8)
        cmds.setAttr(cam + '.displayGateMaskColor', 0, 0, 0, type='double3')
        cmds.setAttr(cam + '.overscan', 1.25)
        
    else:
        if gib('renderer') == 'vray':
            cmds.setAttr('vraySettings.wi', snResW)
            cmds.setAttr('vraySettings.he', snResW)
            cmds.setAttr('vraySettings.aspr', snASR)
            mel.eval("vrayUpdateResolution;")
            mel.eval("vrayUpdatePixelAspectRatioControl;")
            mel.eval("vrayUpdateResolution;")
        else:
            cmds.setAttr('defaultResolution.w', snResW)
            cmds.setAttr('defaultResolution.h', snResW)
            cmds.setAttr('defaultResolution.dar', snASR)

        cmds.setAttr(cam + '.displayResolution', snCamDR)
        cmds.setAttr(cam + '.displayGateMask', snCamGM)
        cmds.setAttr(cam + '.displayGateMaskOpacity', snCamMO)
        cmds.setAttr(cam + '.displayGateMaskColor', snCamMC[0], snCamMC[1], snCamMC[2], type='double3')
        cmds.setAttr(cam + '.overscan', snCamOV)
        
def fileColorMgt(fileNode):
    try:
        colorMgtGlobals = pm.PyNode('defaultColorMgtGlobals')
        f = pm.ls(fileNode, type='file')
        colorMgtGlobals.cmEnabled >> f.colorManagementEnabled
        colorMgtGlobals.configFileEnabled >> f.colorManagementConfigFileEnabled
        colorMgtGlobals.configFilePath >> f.colorManagementConfigFilePath
        colorMgtGlobals.workingSpaceName >> f.workingSpace
    except:
        pass

def renumber(root):
    i=001
    while cmds.objExists(root[0] + str('{0:03}'.format(i))):
        i = i + 1
    root = cmds.rename(root[0], root[0] + '{0:03}'.format(i))
    return root

def saveSettings():
    SLIBPrefs = []
    if '2017' not in gib('mayaVersion'):
        docked = int(cmds.menuItem('dockMenu', q=1, cb=1))
    else:
        docked = int(1)

    res = str(cmds.textField('SLiB_CBOX_Resolution', q=1, tx=1))
    impRef = int(cmds.menuItem('importREF' , q=1, cb=1))
    expFRZ = int(cmds.checkBox('exportFRZ', q=1, v=1))
    expPIV = int(cmds.checkBox('exportPIV', q=1, v=1))
    expHIS = int(cmds.checkBox('exportHIS', q=1, v=1))
    delConf = int(cmds.menuItem('QuickDelete', q=1, cb=1))
    reuAsst = int(cmds.menuItem('ReUseAsset', q=1, cb=1))
    reuDupl = int(cmds.menuItem('ReUseDuplicate', q=1, rb=1))
    reuInst =  int(cmds.menuItem('ReUseInstance', q=1, rb=1))
    reuShdr =  int(cmds.menuItem('ReUseShader', q=1, cb=1))
    toolbar = int(cmds.menuItem('iconToolbar', q=1, cb=1))

    f = open(os.path.join(mel.eval('getenv SLiB;'), 'set', 'windowPrefs.txt'), 'w')
    for e in [docked, res, impRef, expFRZ, expPIV, expHIS, delConf, reuAsst, reuDupl, reuInst, reuShdr, toolbar]:
        f.write(str(e) + '\n')
    f.close()
    messager('Browser PRO Settings saved!', 'green')

#BROWSER DOCK
def dockUI():
    if cmds.menuItem('dockMenu', q=1, cb=1):
        
        if cmds.dockControl('slBrowserDock', q=1, ex=1):
            cmds.dockControl('slBrowserDock', e=1, fl=0)
        else:
            mainWindow = cmds.paneLayout(p=mel.eval('$temp1=$gMainWindow'))
            cmds.dockControl('slBrowserDock', a='right', l='SLiB Browser Pro v2.0', con=mainWindow, aa=['right', 'left'])
            cmds.control('SLiBBrowserUI', e=1, p=mainWindow)
    else:
        cmds.dockControl('slBrowserDock', e=1, fl=1)

def loadSettings():
    p = [line.rstrip('\n') for line in open(os.path.join(mel.eval('getenv SLiB;'), 'set', 'windowPrefs.txt'))]
    
    if '2017' not in gib('mayaVersion'):
        cmds.menuItem('dockMenu', e=1, cb=int(p[0]))
    cmds.textField('SLiB_CBOX_Resolution', e=1, tx=int(p[1]))
    cmds.menuItem('importREF' , e=1, cb=int(p[2]))
    cmds.checkBox('exportFRZ', e=1, v=int(p[3]))
    cmds.checkBox('exportPIV', e=1, v=int(p[4]))
    cmds.checkBox('exportHIS', e=1, v=int(p[5]))
    cmds.menuItem('QuickDelete', e=1, cb=int(p[6]))
    cmds.menuItem('ReUseAsset', e=1, cb=int(p[7]))
    cmds.menuItem('ReUseDuplicate', e=1, rb=int(p[8]))
    cmds.menuItem('ReUseInstance', e=1, rb=int(p[9]))
    cmds.menuItem('ReUseShader', e=1, cb=int(p[10]))
    cmds.menuItem('iconToolbar', e=1, cb=int(p[11]))
    
    if int(p[11]) == 1:
        cmds.layout('slib_toolbar', e=1, vis=1)

    print 'SLiB >>> Browser PRO Settings found and applied'

    if '2017' not in gib('mayaVersion'):
        if cmds.menuItem('dockMenu', q=1, cb=1):
            dockUI()
            print 'SLiB >>> Browser PRO Window docked\n',
    
    if gib('renderer') not in ['arnold', 'mentalray' , 'redshift', 'vray']:
        cmds.warning('Your currently used Render Engine [ ' + str(gib('renderer')) + ' ] is not fully supported and some functions might not work.')
        
def messager(message, color):
    cmds.textField('SLiB_TEXTFIELD_Message', e=1 , tx=message)
    if color == 'none':
        cmds.textField('SLiB_TEXTFIELD_Message', e=1 , bgc=[0.15,0.15,0.15])  #neutral
    if color == 'green':
        cmds.textField('SLiB_TEXTFIELD_Message', e=1 , bgc=[0,0.9,0])   #success
    if color == 'yellow':
        cmds.textField('SLiB_TEXTFIELD_Message', e=1 , bgc=[1,0.5,0])   #yellow
    if color == 'red':
        cmds.textField('SLiB_TEXTFIELD_Message', e=1 , bgc=[0.9,0,0])   #error
    if color == 'blue':
        cmds.textField('SLiB_TEXTFIELD_Message', e=1 , bgc=[0,0.75,0.99])   #blue

def selectFromMaterial(x):
    shapesInSel = cmds.listRelatives(s=1, f=1)
    if shapesInSel:
        shadingGroups = list(set(cmds.listConnections(shapesInSel, type='shadingEngine')))
        materials = []
        for s in shadingGroups:
            mat = cmds.listConnections(s + '.surfaceShader')
            if mat:
                materials.append(mat[0])
        
        if len(materials) > 1:
            if cmds.window('exportWindow', ex=1):
                cmds.deleteUI('exportWindow')
        
            cmds.window('exportWindow', t=' ', sizeable=1, rtf=1)
            cmds.columnLayout('shaderWinLayout', w=260, h=40, adj=1)
            cmds.text(l='More than one Shader found in Selection. \n Please select the one you want to Export!', w=260, h=50, p='shaderWinLayout')
            cmds.iconTextRadioCollection('itRadCollection')
            for e in shadingGroups:
                if e != 'initialShadingGroup':
                    cmds.iconTextRadioButton(st='textOnly', w=260, h=50, l=e, bgc=[0,0.75,0.99], cc=lambda *args: returnSG(cmds.iconTextRadioButton(cmds.iconTextRadioCollection('itRadCollection', q=1, sl=1), q=1, l=1), x), p='shaderWinLayout')
                    cmds.separator(p='shaderWinLayout')
            cmds.showWindow('exportWindow')
            cmds.window('exportWindow', e=1, h=(len(shadingGroups)*50)+55, w=260)
            
        else:
            returnSG(shadingGroups[0], x)

def returnSG(SG, x):
    if cmds.window('exportWindow', ex=1):
        cmds.deleteUI('exportWindow')
        
    if x == 'SG':
        results = cmds.sets(SG, q=True)
        add_suffix = lambda p:  p + ".f[*]" if not '.f' in p else p
        results = [ add_suffix(r) for r in results] or []
        cmds.select(cmds.filterExpand(*results, sm=34))
        
    if x == 'Mat':
        mat = cmds.listConnections(SG + '.surfaceShader')[0]
        swatchWin(mat)
        
    if x == 'MatCopy':
        cmds.select(SG, ne=1)
        matCopy = pm.duplicate(cmds.ls(sl=1), un=1)
        newSG = cmds.ls(matCopy, type='shadingEngine')
        newMat = cmds.listConnections(newSG[0] + '.surfaceShader')[0]
        swatchWin(newMat)
    
    if x == 'Sel':
        mat = None
        if cmds.swatchDisplayPort('swatchDP', ex=1):
            mat = cmds.swatchDisplayPort('swatchDP', q=1, sn=1)
            results = cmds.sets(SG, q=True)
            add_suffix = lambda p:  p + ".f[*]" if not '.f' in p else p
            results = [ add_suffix(r) for r in results] or []
            cmds.select(cmds.filterExpand(*results, sm=34))
            cmds.hyperShade(a=mat)

def swatchWin(mat):
    view = omui.M3dView()
    omui.M3dView.getM3dViewFromModelPanel('modelPanel4', view)
    viewWidget = wrapInstance(long(view.widget()), QtWidgets.QWidget)
    viewWidget.setObjectName(mat)
    oldWin = viewWidget.findChild(QtWidgets.QWidget, 'swatchWin')
    if oldWin:
        oldWin.deleteLater()
    
    position =  viewWidget.mapToGlobal(viewWidget.pos())
    swatchWin = swatchWidget(mat, viewWidget)
    swatchWin.move(0, viewWidget.geometry().height() / 4)
    swatchWin.show()

class swatchWidget(QtWidgets.QWidget):
    def __init__(self, mat, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        
        for e in ['swatchDP', 'swatchText']:
            if cmds.objExists(e):
                cmds.deleteUI(e)
                
        size = 196

        cmds.swatchDisplayPort('swatchDP', wh=(size, size), rs=size, sn=mat, pc=lambda *args: cmds.select(cmds.swatchDisplayPort('swatchDP', q=1, sn=1)))
        cmds.text('swatchText', l=mat, w=size, h=32, bgc=[0,0,0])
        sdp = wrapInstance(long(omui.MQtUtil.findControl('swatchDP')), QtWidgets.QWidget)
        sdt = wrapInstance(long(omui.MQtUtil.findControl('swatchText')), QtWidgets.QWidget)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0,0,0,0)
        sdp.setFixedSize(size, size)
        sdt.setFixedSize(size, 32)
        main_layout.addWidget(sdp)
        main_layout.addWidget(sdt)
        self.setObjectName('swatchWin')

def helpIPT():
    for w in ['slHelp_MP', 'slHelp_IPT']:
        if cmds.window(w, ex=1):
            cmds.deleteUI(w)

    cmds.window('slHelp_IPT', t='IPT Shortcuts', sizeable=0)
    cmds.rowColumnLayout('helpIPTWinLayout', p='slHelp_IPT')
    cmds.image(w=250, h=320, i=SLiB_img + 'sc_ipt.png', p='helpIPTWinLayout')
    cmds.showWindow('slHelp_IPT')
    cmds.window('slHelp_IPT', e=1, w=250, h=320)

def helpMP():
    for w in ['slHelp_MP', 'slHelp_IPT']:
        if cmds.window(w, ex=1):
            cmds.deleteUI(w)

    cmds.window('slHelp_MP', t='MAT Picker Shortcuts', sizeable=0)
    cmds.rowColumnLayout('helpMPWinLayout', p='slHelp_MP')
    cmds.image(w=250, h=320, i=SLiB_img + 'sc_matpicker.png', p='helpMPWinLayout')
    cmds.showWindow('slHelp_MP')
    cmds.window('slHelp_MP', e=1, w=250, h=320)

def renderPreviewPop():
    if cmds.popupMenu('popupPreview', ex=1):
        cmds.deleteUI('popupPreview')
    
    cmds.popupMenu('popupPreview', parent='SLiB_BUTTON_CreatePreview', ctl=0, button=3)
    cmds.radioMenuItemCollection( 'slPreviewType', p='popupPreview')
    
    if gib('mainCat') == 'shader':
        cmds.menuItem('slPreview_Ball', l='BALL', rb=1)
        cmds.menuItem('slPreview_Cube', l='CUBE', rb=0)
        cmds.menuItem('slPreview_Cloth', l='CLOTH', rb=0)
        cmds.menuItem('slPreview_Holder', l='HOLDER', rb=0)
        #cmds.menuItem('slPreview_Pane', l='PANE', rb=0)
    
    if gib('mainCat') == 'objects':
        cmds.menuItem('slPreview_Front', l='FRONT', rb=1)
        cmds.menuItem('slPreview_PerspR', l='PERSP RIGHT', rb=0)
        cmds.menuItem('slPreview_PerspL', l='PERSP LEFT', rb=0)

def UserManual():
    cmds.showHelp('http://store.cgfront.com/doc/browser/index.html', absolute=1)
