#########################################################################
#
#   SLiB Browser Pro
#
#   Version:    2.0
#   Author:     DGDM
#   Copyright:  2016 DGDM
#   Credits:    for mechanize by John J. Lee
#
#########################################################################

import maya.cmds as cmds
import maya.mel as mel
import time
#import datetime
from functools import partial
#import math as math
import os
import shutil
import sys
import platform
import webbrowser
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
from subprocess import check_call
import subprocess
import mechanize
import zipfile
import urllib2
import pymel.core as pm
import Qt
import thread

import SLiBUtilities as SLiB
reload(SLiB)

if '2017' in SLiB.gib('mayaVersion'):
    WorkspaceName = 'WorkspaceBrowser'
    from shiboken2 import wrapInstance
else:
    from shiboken import wrapInstance

from Qt import QtGui, QtCore, QtWidgets
from Qt.QtGui import *
from Qt.QtCore import *
from Qt.QtWidgets import *

SLiB_dir = mel.eval('getenv SLiB;')
SLiB_img = mel.eval('getenv SLiBImage;')
SLiB_gui = mel.eval('getenv SLiBGui;')
SLiB_lib = mel.eval('getenv SLiBLib;')
SLiB_tmp = os.path.normpath(os.path.join(SLiB_dir, 'scn', 'Temp'))

SLiBThumbsScrollLayout = None
copyList = None

mel.eval('putenv "SLiBRARY" "' + SLiB_lib + '"')

#IMPORT
def SLiB_Import(mode):
    if len(cbxList) != 0:
        for item in cbxList:
            SLiB_BrowserImport(mode, item)
    else:
        SLiB.messager('Please select something to import!', 'red')

def SLiB_BrowserImport(mode, item):
    sel = None
    sel = cmds.ls(sl=1, fl=1)

    #if SLiB.gib('renderer') == 'redshift':
    #    cmds.rsRender( r=1, stopIpr=1)

    if mode == 'Texture':
        if SLiB.gib('mainCat') == 'textures':
            if SLiB.gib('renderer') == 'redshift':
                nodeTypes = ['file', 'RedshiftNormalMap', 'RedshiftSprite', 'RedshiftDomeLight', 'RedshiftBokeh']
            else:
                nodeTypes = ['file']
                
            if sel or not sel:
                if sel:
                    selNode = sel[0]
                    
                if len(sel) == 1 and cmds.nodeType(selNode) in nodeTypes:
                    cmds.setAttr(selNode + SLiB.gibTexSlot(selNode), item, type='string')
                    SLiB.messager('Texture replaced!', 'green')
                
                else:
                    fileNode = cmds.shadingNode('file', at=1)
                    cmds.setAttr(fileNode + '.fileTextureName', item, type = 'string')
                    cmds.rename(fileNode, os.path.splitext(os.path.basename(item))[0] + '_file01')
                    SLiB.messager('IMPORT successful!', 'green')
                    cmds.select(cl=1)
                    SLiB.fileColorMgt(fileNode)
        
        #DOME
        if SLiB.gib('mainCat') == 'hdri':
            #FILE NODE
            if not cmds.objExists('SLiB_Dome_file'):
                if SLiB.gib('renderer') in ['vray', 'arnold']:
                    fileNode = cmds.shadingNode('file', at=1)
                    cmds.setAttr(fileNode + '.fileTextureName', item, type = 'string')
                    cmds.rename(fileNode, 'SLiB_Dome_file')
                    SLiB.messager('IMPORT successful!', 'green')
                    SLiB_FileColorMgt(fileNode)
        
            #DOME LIGHT
            if not cmds.objExists('SLiB_Dome'):
                if SLiB.gib('renderer') == 'redshift':
                    SLiB_Dome = cmds.shadingNode('RedshiftDomeLight', al=1)

                if SLiB.gib('renderer') == 'vray':
                    SLiB_Dome = cmds.shadingNode('VRayLightDomeShape', al=1)
                    cmds.setAttr(SLiB_Dome + '.useDomeTex', 1)
                    cmds.connectAttr('SLiB_Dome_file.outColor', SLiB_Dome + '.domeTex')
                
                if SLiB.gib('renderer') == 'arnold':
                    SLiB_Dome = cmds.shadingNode('aiSkyDomeLight', al=1)
                    cmds.connectAttr('SLiB_Dome_file.outColor', SLiB_Dome + '.color')
                    
                if SLiB.gib('renderer') == 'mentalray':
                    SLiB_Dome = cmds.shadingNode('mentalrayIblShape', al=1)
                    
                cmds.rename(SLiB_Dome, 'SLiB_Dome')
                cmds.setAttr('SLiB_Dome.rx', lock=1)
                cmds.setAttr('SLiB_Dome.rz', lock=1)
                cmds.createDisplayLayer(e=1, name='SLiB DomeLight_Lyr')
                cmds.editDisplayLayerMembers('SLiB_DomeLight_Lyr', 'SLiB_Dome')
                cmds.setAttr('SLiB_DomeLight_Lyr.displayType', 2)
                
            if SLiB.gib('renderer') == 'redshift':
                cmds.setAttr('SLiB_Dome.tex0', item, type='string')
            
            if SLiB.gib('renderer') == 'vray':
                cmds.setAttr('SLiB_Dome_file.fileTextureName', item, type = 'string')
                
            if SLiB.gib('renderer') == 'arnold':
                cmds.setAttr('SLiB_Dome_file.fileTextureName', item, type = 'string')
                
            if SLiB.gib('renderer') == 'mentalray':
                cmds.setAttr('SLiB_Dome.texture', item, type = 'string')
            
            cmds.select('SLiB_Dome')
        
    if mode == 'Normal':
        #SHADER
        if SLiB.gib('mainCat') == 'shader':
            SLiB_ShaderImportProc(item, sel)

        #OBJECTS
        if SLiB.gib('mainCat') == 'objects':
            root = SLiB_ObjectImportProc(item)
            return root

    if mode in ['Place', 'Replace']:
        if sel:
            for v in sel:
                root = SLiB_ObjectImportProc(item)
                    
                cp = cmds.xform(v, q=1, t=1, ws=1)
                cr = cmds.xform(v, q=1, ro=1, ws=1)

                cmds.xform(root, t=(cp[0], cp[1], cp[2]), ro=(cr[0], cr[1], cr[2]))
            
            if mode == 'Replace':
                cmds.delete(sel)
            
            if mode == 'Place':
                cmds.select(sel)
                if cmds.ls(sel, hl=1):
                    cmds.selectMode(co=1)

#SHADER
def SLiB_ShaderImportProc(item, sel):
    fileName = os.path.splitext(item)[0]
    shader = open(fileName + '.meta').readline().rstrip()
    reusable = None
    root = None

    for a in cmds.ls(mat=1):
        if shader in a:
            hit = a
            reusable = 1
            
    if cmds.menuItem('ReUseShader', q=1, cb=1) and reusable == 1:
        shader = hit
        
        SLiB.messager(os.path.basename(item) + ' already in scene! Will reuse it.', 'green')

    else:
        if not cmds.menuItem('importREF', q=1, cb=1):
            imported = cmds.file(item, i=1, type=SLiB.fileType(item), uns=0, rnn=1, iv=1)
        else:
            imported = cmds.file(item, r=1, type=SLiB.fileType(item), uns=1, rnn=1, iv=1)
        
        root = cmds.ls(imported, assemblies=1)
        SLiB_AutoRELtoABS(root)

        shader = cmds.rename(shader, shader + '_001')
            
        SLiB.messager(os.path.basename(item) + ' imported!', 'green')

    if sel:
        cmds.select(sel)
        cmds.hyperShade(a=shader)

#OBJECTS
def SLiB_ObjectImportProc(item):
    fileName = os.path.splitext(item)[0]
    asset = open(fileName + '.meta').readline().rstrip()
    reusable = None
    root = None

    matches = []
    for a in cmds.ls(tr=1):
        if asset in a:
            matches.append(a)

    parent = []
    if len(matches) > 1:
        for e in matches:
            parent.append(cmds.listRelatives(e, f=1)[0].split('|')[1])
        hit = list(set(parent))[0]
        reusable = 1
    
    if len(matches) == 1:
        hit = matches[0]
        reusable = 1

    if cmds.menuItem('ReUseAsset', q=1, cb=1) and reusable == 1:
        if cmds.menuItem('ReUseDuplicate', q=1, rb=1):
            duplObject = cmds.duplicate(hit, n=str(asset) + '_Dupl_')
            duplObject = SLiB.renumber(duplObject)
            SLiB.messager(os.path.basename(item) + ' already in scene! Duplicated.', 'green')
            cmds.move(duplObject, rpr=1)
            if cmds.iconTextCheckBox('ipt', q=1, v=1) != 1:
                cmds.select(duplObject)
            
            root = ''.join(duplObject)
            return root
        
        if cmds.menuItem('ReUseInstance', q=1, rb=1):
            instObject = cmds.instance(hit, n=str(asset) + '_Inst_')
            instObject = SLiB.renumber(instObject)
            SLiB.messager(os.path.basename(item) + ' already in scene! Instanced.', 'green')
            cmds.move(instObject, rpr=1)
            if cmds.iconTextCheckBox('ipt', q=1, v=1) != 1:
                cmds.select(instObject)

            root = ''.join(instObject)
            cmds.optionVar(sv=('SLIB_LastIPT', root))
            return root

    else:
        if not cmds.menuItem('importREF', q=1, cb=1):
            imported = cmds.file(item, i=1, type=SLiB.fileType(item), uns=0, rnn=1, iv=1)
        else:
            imported = cmds.file(item, r=1, type=SLiB.fileType(item), uns=1, rnn=1, iv=1)
            
        SLiB.messager(os.path.basename(item) + ' imported!', 'green')

        root = cmds.ls(imported, assemblies=1)
        print root

        if not reusable:
            SLiB_AutoRELtoABS(root)

            if cmds.menuItem('CopyToProjectFolder', q=1, cb=1):
                SLiB_AutoCopyToProject(root)

        if not cmds.menuItem('importREF', q=1, cb=1):
            root = cmds.rename(root[0], root[0] + '_')
            root = [root]
            root = SLiB.renumber(root)
                
        cmds.select(root)
        cmds.optionVar(sv=('SLIB_LastIPT', root[0]))
        return root

def SLiB_ReplaceTexture():
    if SLiB.gib('renderer') == 'redshift':
        nodeTypes = ['file', 'RedshiftNormalMap', 'RedshiftSprite', 'RedshiftDomeLight', 'RedshiftBokeh']
    else:
        nodeTypes = ['file']
    selNode = cmds.ls(sl=1)

def SLiB_absPath(x):
    fileName = x
    if '${SLiBLib}' in fileName:
        fileName = os.path.normpath(fileName.replace('${SLiBLib}', mel.eval('getenv SLiBRARY;')))
    if '${SLiBRARY}' in fileName:
        fileName = os.path.normpath(fileName.replace('${SLiBRARY}', mel.eval('getenv SLiBRARY;')))
    if '${SLiB}' in fileName:
        fileName = os.path.normpath(fileName.replace('${SLiB}', mel.eval('getenv SLiB;')))

    return fileName

def SLiB_relPath(x):
    file = None
    if '|' in x:
        file = os.path.normpath(x.split('|')[0])
    else:
        file = x
   
    if os.path.normpath(mel.eval('getenv SLiBRARY;') + '/shader') in file:
        fileNameNew = os.path.normpath('${SLiBRARY}/shader/' + file.split('shader')[1])
        
    if os.path.normpath(mel.eval('getenv SLiBRARY;') + '/objects') in file:
        fileNameNew = os.path.normpath('${SLiBRARY}/objects/' + file.split('objects')[1])
        
    if os.path.normpath(mel.eval('getenv SLiBRARY;') + '/lights') in file:
        fileNameNew = os.path.normpath('${SLiBRARY}/lights/' + file.split('lights')[1])
        
    if os.path.normpath(mel.eval('getenv SLiBRARY;') + '/textures') in file:
        fileNameNew = os.path.normpath('${SLiBRARY}/textures/' + file.split('textures')[1])
        
    if os.path.normpath(mel.eval('getenv SLiBRARY;') + '/hdri') in file:
        fileNameNew = os.path.normpath('${SLiBRARY}/hdri/' + file.split('hdri')[1])
        
    if os.path.normpath(mel.eval('getenv SLiBRARY;') + '/maps') in file:
        fileNameNew = os.path.normpath('${SLiBRARY}/maps/' + file.split('maps')[1])

    #OLD STUFF
    if os.path.normpath(SLiB_lib + '/shader') in file:
        fileNameNew = os.path.normpath('${SLiBRARY}/shader/' + file.split('shader')[1])
        
    if os.path.normpath(SLiB_lib + '/objects') in file:
        fileNameNew = os.path.normpath('${SLiBRARY}/objects/' + file.split('objects')[1])
        
    if os.path.normpath(SLiB_lib + '/maps') in file:
        fileNameNew = os.path.normpath('${SLiBRARY}/maps/' + file.split('maps')[1])
    
    return fileNameNew

def SLiB_AutoRELtoABS(root):
    cmds.select(root)
    if SLiB_TexList():
        for t in SLiB_TexList():
            fileName = os.path.normpath(cmds.getAttr(t + SLiB.gibTexSlot(t)))
            fileName = SLiB_absPath(fileName)
            cmds.setAttr(t + SLiB.gibTexSlot(t), fileName, type='string')

def SLiB_AutoCopyToProject(root):
    textdestination = os.path.join(cmds.workspace(q=1, rd=1), 'sourceimages')
    cmds.select(root)
    for t in SLiB_TexList():
        fileName = os.path.normpath(cmds.getAttr(t + SLiB.gibTexSlot(t)))
        fileName = SLiB_absPath(fileName)
        
        finalPath = os.path.normpath(os.path.join(textdestination, os.path.basename(fileName)))
        
        if fileName != finalPath:
            if os.path.isfile(fileName):
                shutil.copy(fileName, textdestination)
                cmds.setAttr(t + SLiB.gibTexSlot(t), finalPath, type='string')

#EXPORT
def SLiB_BrowserExport():
    print 'SLiB >> starting EXPORT'
    if len(SLiB.gib('name')) == 0:
        SLiB.messager('Please enter a Name!', 'red')
        sys.exit()
    
    shapesInSel = cmds.listRelatives(s=1) or object
    newShaderName = SLiB.gib('name')
    exportDir = os.path.join(SLiB.gib('currLocation'), newShaderName)
    
    if SLiB.gib('currLocation') != None and SLiB.gib('currLocation') != os.path.normpath(mel.eval('getenv SLiBRARY;') + SLiB.gib('mainCat')):
        if os.path.exists(exportDir):
            answer = cmds.confirmDialog(t='Warning', m='Shader/Asset with this Name already exists! \nDo you want to Update it?', button=['Update','No'], defaultButton='Update', cancelButton='No', dismissString='No' )
            if answer != 'Update':
                sys.exit()

        for ext in ['.ma', '.mb', '.obj']:
            if os.path.isfile(exportDir + '/' + newShaderName + ext):
                os.remove(exportDir + '/' + newShaderName + ext)
        
        global selection
        try:
            selection = cmds.listRelatives(cmds.ls(sl=1)[0], f=1)[0].split('|')[1]
        except:
            if SLiB.gib('mainCat') == 'shader':
                SLiB.messager('Please select the Object that holds the Shader!', 'red')
            else:
                SLiB.messager('Please select the Object or Group you want to export!', 'red')
            sys.exit()

        if SLiB.gib('mainCat') == 'shader': 
            print 'SLiB >> Item = SHADER'
            shadingGroups = list(set(cmds.listConnections(shapesInSel, type='shadingEngine')))
            selMaterials = list(set(cmds.ls(cmds.listConnections(shadingGroups), mat=1)))

            if len(selMaterials) > 1:
                if cmds.window('exportWindow', ex=1):
                    cmds.deleteUI('exportWindow')

                cmds.window('exportWindow', t=' ', sizeable=1, rtf=1)
                cmds.columnLayout('shaderWinLayout', w=260, h=40, adj=1)
                cmds.text(l='More than one Shader found in Selection. \n Please select the one you want to Export!', w=260, h=50, p='shaderWinLayout')
                cmds.iconTextRadioCollection('itRadCollection')
                for e in shadingGroups:
                    if e != 'initialShadingGroup':
                        cmds.iconTextRadioButton(st='textOnly', w=260, h=50, l=e, bgc=[0,0.75,0.99], cc=lambda *args: (SLiB_ExportShader(newShaderName, shapesInSel, cmds.iconTextRadioButton(cmds.iconTextRadioCollection('itRadCollection', q=1, sl=1), q=1, l=1)), cmds.deleteUI('exportWindow')), p='shaderWinLayout')
                        cmds.separator(p='shaderWinLayout')
                cmds.showWindow('exportWindow')
                cmds.window('exportWindow', e=1, h=(len(shadingGroups)*50)+40, w=260)
            
            else:
                SLiB_ExportShader(newShaderName, shapesInSel, shadingGroups[0])

        else:
            print 'SLiB >> Item = OBJECT'
            SLiB_ExportObject(newShaderName, shapesInSel)
    else:
        SLiB.messager('Please select a Category!', 'red')

def SLiB_ExportShader(newShaderName, shapesInSel, shadingGrp):
    type = None
    assetPath = os.path.join(SLiB.gib('currLocation'), newShaderName)
    file = assetPath + '/' + newShaderName

    if os.path.isdir(assetPath) != 1:
        os.mkdir(assetPath)
    
    ### EXPORT WITH TEXTURE(S)
    print 'SLiB >> exporting TEXTURE(S)...'
    if not cmds.optionMenu('exportTEX', q=1, v=1) == 'no Textures':
        SLiB_ExportTex()

    expExt = '.' + cmds.optionMenu('ExportOptions', q=1, v=1).lower()
    if expExt == '.ma':
        type = 'mayaAscii'
        
    if expExt == '.mb':
        type = 'mayaBinary'
    
    cmds.select(shadingGrp, ne=1)
    print shadingGrp
    if expExt == '.obj':
        cmds.confirmDialog(m='No Shader Export as OBJ!')
    else:
        cmds.file(file + expExt, op='v=0', typ=type, es=1)
        
    if os.path.normpath(prevButton.objectName()) != file + '.png':
        image = om.MImage()
        image.readFromFile(os.path.normpath(prevButton.objectName()))
        image.resize( 512, 512 )
        image.writeToFile(file + '.png', 'png')
    
    SLiB_ExportMeta(file, shadingGrp)
    
    SLiB_UpdateView()
    
    SLiB.messager('EXPORT successful!', 'green')

def SLiB_ExportObject(newShaderName, shapesInSel):
    assetPath = SLiB.gib('currLocation') + '/' + newShaderName
    file = os.path.normpath(assetPath + '/' + newShaderName)

    if os.path.isdir(assetPath) != 1:
        os.mkdir(assetPath)
        
    ### DEL HISTORY
    if cmds.checkBox('exportHIS', q=1, v=1):
         cmds.delete(ch=1)
    
    ### AUTO PLACE PIVOT
    if cmds.checkBox('exportPIV', q=1, v=1):
        SLiB.autoPlacePivot()
    
    ### FREEZE
    if cmds.checkBox('exportFRZ', q=1, v=1):
        SLiB.freeze()

    ### EXPORT WITH TEXTURE(S)
    if not cmds.optionMenu('exportTEX', q=1, v=1) == 'no Textures':
        cmds.select(selection)
        SLiB_ExportTex()
    
    expExt = '.' + cmds.optionMenu('ExportOptions', q=1, v=1).lower()
    if expExt == '.ma':
        cmds.file(file + expExt, op='v=0', typ='mayaAscii', es=1)
    if expExt == '.mb':
        cmds.file(file + expExt, op='v=0', typ='mayaBinary', es=1)
    if expExt == '.obj':
        cmds.file(file + expExt, pr=1, typ='OBJexport', es=1, op='groups=0; ptgroups=0; materials=0; smoothing=0; normals=0')

    image = om.MImage()
    image.readFromFile(os.path.normpath(prevButton.objectName()))
    image.resize( 512, 512 )
    image.writeToFile(file + '.png', 'png')

    SLiB_ExportMeta(file, None)

    SLiB_UpdateView()
    
    SLiB.messager('EXPORT successful!', 'green')

def SLiB_ExportTex():
    expTEX = SLiB_TexList()
    if expTEX:
        print 'SLiB >> ' + str(len(expTEX)) + ' Texture(s) found'
        if cmds.optionMenu('exportTEX', q=1, v=1) == 'with custom Texture Folder':
            textdestination =  os.path.normpath(cmds.textField('SLiB_TEXTFIELD_Texpath', q=1, tx=1))
            if len(textdestination) > 1 and os.path.isdir(textdestination):
                pass
            else:
                SLiB.messager('Please specify custom Texture Folder!', 'red')
        else:
            textdestination =  SLiB.gib('currLocation') + '/' + SLiB.gib('name') + '/Tex'
            if not os.path.isdir(textdestination):
                os.mkdir(textdestination)
                print 'SLiB >> TEX folder created'
                
        for t in expTEX:
            fileName = os.path.normpath(cmds.getAttr(t + SLiB.gibTexSlot(t)))
            fileName = SLiB_absPath(fileName)
            
            finalPath = os.path.normpath(os.path.join(textdestination, os.path.basename(fileName)))
            
            if fileName != finalPath:
                if os.path.isfile(fileName):
                    shutil.copy(fileName, textdestination)
                    if cmds.optionMenu('TexPathMode', q=1, v=1) == 'REL':
                        finalPath = SLiB_relPath(finalPath + '|' + t)
                    cmds.setAttr(t + SLiB.gibTexSlot(t), finalPath, type='string')
        
        print 'SLiB >> ' + str(len(expTEX)) + ' Texture(s) copied'

def SLiB_ExportTextures(x):
    if SLiB.gib('currLocation') != None and SLiB.gib('currLocation') != os.path.normpath(mel.eval('getenv SLiBRARY;') + SLiB.gib('mainCat')):
        if x == 'folder':
            path = cmds.fileDialog2(dir=os.sep, fm=4)
            tex = []
            if path:
                inclExt = ['.jpg', '.bmp', '.png', '.gif', '.tif', '.tga', '.iff', '.exr', '.hdr']
                for e in path:
                    if os.path.splitext(e)[1] in inclExt:
                        tex.append(e)
                
        if x == 'scene':
            tex = SLiB_TexList()

        if tex:
            cmds.progressBar('PreviewProgress', e=1, max=(len(tex)))
            for i in tex:
                cmds.progressBar('PreviewProgress', e=1, step=1)
                
                if x == 'folder':
                    fileSource = i
                
                if x == 'scene':
                    fileSource = cmds.getAttr(i + SLiB.gibTexSlot(i))
                    fileSource = SLiB_absPath(fileSource)
                    
                if os.path.isfile(fileSource): 
                    justName = os.path.splitext(os.path.basename(fileSource))[0]
                    ext = os.path.splitext(os.path.basename(fileSource))[1]
                    fileDir = os.path.join(SLiB.gib('currLocation'), justName)
                    fileDest = os.path.join(SLiB.gib('currLocation'), justName, justName + ext)
                    if fileSource != fileDest:
                        if not os.path.isfile(fileDest):
                            os.mkdir(fileDir)
                            os.mkdir(fileDir + '/_THUMBS')
                            shutil.copy(fileSource, fileDest)
                            image = om.MImage()
                            image.readFromFile(fileDest)
                            if SLiB.gib('mainCat') == 'hdri':
                                image.resize( 1024, 512 )
                            else:
                                image.resize( 512, 512 )
                            image.writeToFile(fileDir + '/_THUMBS/' + justName + '.png' , 'png')
                            SLiB_ExportMeta(os.path.join(fileDir, justName) , None)
                            
            cmds.progressBar('PreviewProgress', e=1, pr=0)
            SLiB_UpdateView()
    else:
        SLiB.messager('Please select a Category!', 'red')

def SLiB_Metarize():
    if SLiB.gib('mainCat') != 'paths':
        if cbxList:
            answer = cmds.confirmDialog(t='Warning', m='Please make sure you saved the current scene! \nDo you want to proceed?', ma='center', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            if answer == 'Yes':
                cmds.progressBar('PreviewProgress', e=1, max=len(cbxList))

                for e in cbxList:
                    file = os.path.splitext(e)[0]
                    
                    if SLiB.gib('mainCat') in ['textures', 'hdri']:
                        SLiB_ExportMeta(file, None)
                    else:
                        scene = cmds.file(e, open=1, f=1, iv=1, rnn=1)
                    
                        if SLiB.gib('mainCat') == 'shader':
                            mats = cmds.ls(scene, mat=1)
                            
                            mainMat = []
                            if len(mats) > 1:
                                for m in mats:
                                    if not cmds.nodeType(m) == 'displacementShader':
                                        connections = cmds.listConnections(m, s=0, d=1, type='shadingEngine')
                                        if not connections:
                                            conn = cmds.listConnections(m, s=0, d=1)
                                            if not conn[0] in 'defaultShaderList1':
                                                mainMat.append(conn[0])
                                        if connections:
                                            for c in connections:
                                                if c and not c in ['initialParticleSE', 'initialShadingGroup']:
                                                    mat = cmds.listConnections(c + '.ss')
                                                    mainMat.append(mat[0])
                                
                                mainMat = list(set(mainMat))[0]
                            if len(mats) == 1:
                                mainMat = list(set(mats))[0]
                            
                            shadingGroup = cmds.listConnections(mats, type='shadingEngine')
                            
                            if not shadingGroup:
                                cmds.polyCube(n='ShaderHolder')
                                cmds.select('ShaderHolder')
                                cmds.hyperShade(a=mainMat)
                                SLiB.delete('ShaderHolder')
                                cmds.file(save=1, f=1)
                            
                            SLiB_ExportMeta(file, mainMat)
                        
                        else:
                            global selection
                            selection = cmds.listRelatives(scene, f=1)[0].split('|')[1]
                            cmds.select(selection)
                            SLiB_ExportMeta(file, None)
                            
                    if os.path.isfile(file + '.info'):
                        os.remove(file + '.info')
                    if os.path.isfile(file + '.dim'):
                        os.remove(file + '.dim')
                    
                    SLiB_UpdateInfo(e)
                    
                    cmds.progressBar('PreviewProgress', e=1, step=1)

                cmds.file(f=1, new=1)
                cmds.progressBar('PreviewProgress', e=1, pr=0)
    else:
        SLiB.messager('Not working for paths!', 'yellow')

def SLiB_ExportMeta(file, mainMat):
    tags = cmds.textField('SLiB_TEXTFIELD_Tags', q=1, tx=1)
    locked = cmds.optionMenu('meta_locked', q=1, v=1).upper()
    user = cmds.textField('SLiB_TEXTFIELD_User', q=1, tx=1)
    
    if '15' in SLiB.gib('mayaVersion'):
        version = '2015'
    if '2016' in SLiB.gib('mayaVersion') and not '5' in SLiB.gib('mayaVersion'):
        version = '2016'
    if '2016' in SLiB.gib('mayaVersion') and '5' in SLiB.gib('mayaVersion'):
        version = '2016.5'
    if '17' in SLiB.gib('mayaVersion'):
        version = '2017'
    
    renderer = SLiB.gib('renderer').upper()
    
    if SLiB.gib('mainCat') == 'objects' or SLiB.gib('mainCat') == 'lights':
        size = SLiB.gibBBox(selection)[0] + ' x ' + SLiB.gibBBox(selection)[1]  + ' x ' +  SLiB.gibBBox(selection)[2]
    else:
        size = 'N/A'
        
    proxy = ''

    if SLiB.gib('mainCat') in ['textures', 'hdri']:
        renderer = 'N/A'
        version = 'N/A'
    
    if os.path.isfile(file + '.info'):
        n = open(file + '.info', 'r')
        notes = n.read()
        n.close()
    
    else:
        if os.path.isfile(file + '.meta'):
            notes = []
            lines = [line.rstrip('\n') for line in open(file + '.meta')]
            
            for l in range(15, len(lines)):
                notes.append(lines[l])
            notes = '\n'.join(notes)
        else:
            notes = ''
    
    metaFile = file + '.meta'
    
    f = open(metaFile, 'w')

    #ROOT
    if SLiB.gib('mainCat') == 'shader':
        f.write(mainMat + '\n')
    
    elif SLiB.gib('mainCat') == 'objects' or SLiB.gib('mainCat') == 'lights':
        f.write(cmds.listRelatives(cmds.ls(sl=1)[0], f=1)[0].split('|')[1] + '\n')
    
    else:
        f.write(' ' + '\n')

    #TAGS
    f.write(tags + '\n')
    #LOCKED
    f.write(locked + '\n')
    #USER
    f.write(user + '\n')
    #MAYA VERSION
    f.write(version + '\n')
    #RENDERER
    f.write(renderer + '\n')
    #SIZE
    f.write(size + '\n')
    #PROXY
    f.write(' ' + '\n')
    
    #PLACEHOLDER
    f.write(' ' + '\n')
    #PLACEHOLDER
    f.write(' ' + '\n')
    #PLACEHOLDER
    f.write(' ' + '\n')
    #PLACEHOLDER
    f.write(' ' + '\n')
    #PLACEHOLDER
    f.write(' ' + '\n')
    #PLACEHOLDER
    f.write(' ' + '\n')
    #PLACEHOLDER
    f.write(' ' + '\n')
    #NOTES
    f.write(notes + '\n')
    f.close()
    
    print 'SLiB >> META file written'

def SLiB_UpdateMeta(mode):
    if cbxList:
        for e in cbxList:
            file = os.path.splitext(e)[0]
            metaFile = file + '.meta'
            renderer = None
            locked = 'NO'
    
            if os.path.isfile(metaFile):
                oldLines = [line.rstrip('\n') for line in open(metaFile)]

                if mode == 'tags':
                    tags = cmds.textField('SLiB_TEXTFIELD_Tags', q=1, tx=1)
                else:
                    tags = oldLines[1]
                    
                if mode == 'locked':
                    locked = cmds.optionMenu('meta_locked', q=1, v=1)
                else:
                    locked = oldLines[2]
                    
                if mode == 'user':
                    user = cmds.textField('SLiB_TEXTFIELD_User', q=1, tx=1)
                else:
                    user = oldLines[3]
                
                if mode == 'version':
                    version = cmds.optionMenu('meta_version', q=1, v=1)
                else:
                    version = oldLines[4]
                
                if mode == 'renderer':
                    renderer = cmds.optionMenu('meta_renderer', q=1, v=1).upper()
                else:
                    renderer = oldLines[5]
                
                size = oldLines[6]
                
                if mode == 'proxy':
                    proxy = ''
                    #proxy = cmds.optionMenu('meta_proxy', q=1, v=1).upper()
                else:
                    proxy = oldLines[7]

                notes = []
                lines = [line.rstrip('\n') for line in open(metaFile)]
                
                for l in range(15, len(lines)):
                    notes.append(lines[l])
                notes = '\n'.join(notes)
                
                f = open(metaFile, 'w')
                
                #ROOT
                f.write(oldLines[0] + '\n')
                #TAGS
                f.write(tags + '\n')
                #LOCKED
                f.write(locked + '\n')
                #USER
                f.write(user + '\n')
                #MAYA VERSION
                f.write(version + '\n')
                #RENDERER
                f.write(renderer + '\n')
                #SIZE
                f.write(size + '\n')
                #PROXY
                f.write(' ' + '\n')
                
                #PLACEHOLDER
                f.write(' ' + '\n')
                #PLACEHOLDER
                f.write(' ' + '\n')
                #PLACEHOLDER
                f.write(' ' + '\n')
                #PLACEHOLDER
                f.write(' ' + '\n')
                #PLACEHOLDER
                f.write(' ' + '\n')
                #PLACEHOLDER
                f.write(' ' + '\n')
                #PLACEHOLDER
                f.write(' ' + '\n')
                #NOTES
                f.write(notes + '\n')
                f.close()

                SLiB.messager(str(mode).upper() + ' updated', 'green')
                SLiB_OverlayImage(file + '.png')

def SLiB_ZoomWin(item):
    if cmds.window('SLiB_ZoomButton', ex=1):
        cmds.deleteUI('SLiB_ZoomButton')
        
    mayaMainWindow= wrapInstance(long(omui.MQtUtil.mainWindow()), QWidget) 
    icon = QtGui.QIcon(item)
    button = QtWidgets.QPushButton(parent=mayaMainWindow)
    button.setObjectName('SLiB_ZoomButton')
    button.setFlat(True)
    if SLiB.gib('mainCat') == 'hdri':
        button.setFixedSize(QtCore.QSize(512*2, 512))
    else:
        button.setFixedSize(QtCore.QSize(512, 512))
    button.setIconSize(button.size())
    button.setIcon(icon)
    button.clicked.connect(SLiB_ZoomWinClose)
    button.setWindowFlags(Qt.Window)
    button.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint)
    button.show()
    
def SLiB_ZoomWinClose():
    if cmds.window('SLiB_ZoomButton', ex=1):
        cmds.deleteUI('SLiB_ZoomButton')

#UPDATE INFO
def SLiB_UpdateInfo(file):
    cmds.optionVar(sv=('SLIB_LastIPT', ''))

    fileName = os.path.splitext(file)[0]
    fileExt = os.path.splitext(file)[1]

    if SLiB.gib('mainCat') in ['textures', 'hdri']:
        imageFile = os.path.join(os.path.dirname(fileName), '_THUMBS', os.path.splitext(os.path.basename(fileName))[0] + '.png')
    else:
        imageFile = fileName + '.png'
    
    cmds.text('SLiB_shaderName', e=1, l=os.path.basename(fileName) + ' [ ' + fileExt + ' ]' , al='center')
    
    #META STUFF
    notes = []
    ftime = time.gmtime(os.path.getmtime(file))
    date = str(ftime.tm_year) + '-' + str(ftime.tm_mon) + '-' + str(ftime.tm_mday)  + '   ' + str(ftime.tm_hour)  + ':' + str(ftime.tm_min)  + ':' + str(ftime.tm_sec)
    cmds.textField('SLiB_TEXTFIELD_Date', e=1, tx=date)
    
    if os.path.isfile(fileName + '.meta'):
        lines = [line.rstrip('\n') for line in open(fileName + '.meta')]
        cmds.textField('SLiB_TEXTFIELD_Root', e=1, tx=lines[0])
        cmds.textField('SLiB_TEXTFIELD_Tags', e=1, tx=lines[1])
        cmds.optionMenu('meta_locked', e=1, v=lines[2])
        cmds.textField('SLiB_TEXTFIELD_User', e=1, tx=lines[3])
        cmds.optionMenu('meta_version', e=1, v=lines[4])
        cmds.optionMenu('meta_renderer', e=1, v=lines[5])
        cmds.textField('SLiB_TEXTFIELD_Size', e=1, tx=lines[6])

        for l in range(15, len(lines)):
            notes.append(lines[l])
        cmds.scrollField('SLiB_TEXTFIELD_Info', e=1, tx='\n'.join(notes))
        
        if not len(cmds.scrollField('SLiB_TEXTFIELD_Info', q=1, tx=1)) == 0:
            SLiB.messager('Selection Info updated! [ Notes available ]', 'none')
        else:
            SLiB.messager('Selection Info updated!', 'none')

    if not os.path.isfile(fileName + '.meta'):
        cmds.textField('SLiB_TEXTFIELD_Tags', e=1, tx='')
        cmds.optionMenu('meta_locked', e=1, v='NO')
        cmds.textField('SLiB_TEXTFIELD_User', e=1, tx='')
        cmds.textField('SLiB_TEXTFIELD_Root', e=1, tx='')
        cmds.optionMenu('meta_version', e=1, v='N/A')
        cmds.optionMenu('meta_renderer', e=1, v='N/A')
        cmds.scrollField('SLiB_TEXTFIELD_Info', e=1, tx='')
        cmds.textField('SLiB_TEXTFIELD_Size', e=1, tx='N/A')
        SLiB.messager('Selection Info updated! [ Meta file missing ]', 'yellow')
        
    cmds.optionVar(sv=('SLIB_currItem', cmds.textField('SLiB_TEXTFIELD_Root', q=1, tx=1)))

    if not cmds.iconTextCheckBox('RVLocked', q=1, v=1):
        if os.path.isfile(imageFile):
            SLiB_OverlayImage(imageFile)
        else:
            SLiB_OverlayImage(SLiB_img + 'image_missing.png')


    if cmds.window('SLiB_ZoomButton', ex=1):
        SLiB_ZoomWin(imageFile)

class MoviePlayer(QtWidgets.QWidget): 
    def __init__(self, parent=None): 
        QtWidgets.QWidget.__init__(self, parent)
        
        for childWidget in RenderViewHolder.children():
            childWidget.deleteLater()

        self.movie_screen = QtWidgets.QLabel()
        self.movie_screen.setFixedSize(256, 256)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.movie_screen)
        
        self.setLayout(main_layout) 
        self.setFixedSize(256, 256)
        self.setParent(RenderViewHolder)

        gif = SLiB_img + 'dgdm.gif'
        self.movie = QtGui.QMovie(gif, QByteArray(), self) 
        self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.setScaledSize(QSize(256, 256))
        self.movie.frameChanged.connect(self.theEnd)
        self.movie.start()
        
    def theEnd(self):
        if self.movie.currentFrameNumber() == 100:
            self.movie.stop()
            SLiB_OverlayImage(SLiB_img + 'browser_logo.png')

class PreviewButton(QtWidgets.QPushButton):
    left_clicked = QtCore.Signal(int)
    right_clicked = QtCore.Signal(int)
    
    def __init__(self, imageFile, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, *args, **kwargs)
        
        background = QtGui.QImage(SLiB_img + 'browser_bg01.png')
        overlay = QtGui.QImage(SLiB_img + cmds.optionMenu('meta_renderer', q=1, v=1).lower() + '_overlay.png')
        overlay_scaled = overlay.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lock = QtGui.QImage(SLiB_img + '/' + 'locked_overlay.png')
        lock_scaled = lock.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img = QtGui.QImage(imageFile)
        
        pixmap = QtGui.QPixmap(img)
        scaled = pixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        itemImage = scaled.toImage()
        combined = QtGui.QPixmap(256, 256)

        p = QtGui.QPainter(combined)
        
        p.setRenderHint(QtGui.QPainter.Antialiasing, True)
        p.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        p.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        
        p.drawImage(QtCore.QPoint(0, 0), background)
        p.drawImage(QtCore.QPoint(0, 0), itemImage)
        if cmds.optionMenu('meta_locked', q=1, v=1) == 'YES':
            p.drawImage(QtCore.QPoint(0, 0), lock_scaled)
        p.drawImage(QtCore.QPoint(0, 0), overlay_scaled)
        p.end()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setFixedSize(256, 256)
        icon = QtGui.QIcon(QtGui.QPixmap(combined))
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(256, 256))
        self.setMouseTracking(True)
        self.setFlat(True)
        self.setAutoFillBackground(0)
        self.setParent(RenderViewHolder)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.left_click_count = self.right_click_count = 0
        
        # Context Menu
        self.menu = QtWidgets.QMenu()
        self.menu.addAction('RESET', self.menu_reset)
        self.menu.addSeparator()
        self.menu.addAction('REPLACE', self.menu_replace)
        self.menu.setStyleSheet("selection-background-color: #ffaa00; selection-color: black; background-color: #525252; border: 1px solid black; color: #EBEBEB; padding: 0px 0px 0px 0px;")
        self.customContextMenuRequested.connect(self.context_menu)
        
        self.left_clicked[int].connect(self.left_click)
        self.right_clicked[int].connect(self.right_click)
        
    def left_click(self, nb):
        item = os.path.normpath(prevButton.objectName())
        #modifiers = QtWidgets.QApplication.keyboardModifiers()
        if nb == 1:
            SLiB_ZoomWinClose()
        else:
            SLiB_ZoomWin(item)

    def right_click(self, nb):
        os.path.normpath(prevButton.objectName())
        #modifiers = QtWidgets.QApplication.keyboardModifiers()
        if nb == 1:
            pass
        else:
            pass
        
    def context_menu(self):
        self.menu.popup(QCursor.pos())
        position = self.menu.pos()
        self.menu.move(position.x() + 1, position.y() + 1)
        
    def menu_reset(self):
        icon = QtGui.QIcon(SLiB_img + 'browser_logo.png')
        self.setIcon(icon)
        self.setObjectName(SLiB_img + 'browser_logo.png')
        
    def menu_replace(self):
        SLiB_ReplacePreview()
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.left_click_count += 1
            if not self.timer.isActive():
                self.timer.start()
        
        if event.button() == QtCore.Qt.RightButton:
            self.right_click_count += 1
            if not self.timer.isActive():
                self.timer.start()

    def timeout(self):
        if self.left_click_count >= self.right_click_count:
            self.left_clicked.emit(self.left_click_count)
        else:
            self.right_clicked.emit(self.right_click_count)
        self.left_click_count = self.right_click_count = 0
    
    def enterEvent(self,event):
        pass

    def leaveEvent(self,event):
        pass

class SLiB_OverlayImage(QtWidgets.QWidget):
    def __init__(self, imageFile):
        super(SLiB_OverlayImage, self).__init__()

        for childWidget in RenderViewHolder.children():
            childWidget.deleteLater()
        
        global prevButton
        prevButton = PreviewButton(imageFile)
        prevButton.setObjectName(imageFile)
        prevButton.show()

def SLiB_ReplaceNotes():
    if cbxList:
        notes = cmds.scrollField('SLiB_TEXTFIELD_Info', q=1, tx=1)
        notes = notes.replace(u'\u2018', '').replace(u'\u2019', '').replace(u'\u201c','').replace(u'\u201d', '')
        
        for item in cbxList:
            metaFile = os.path.splitext(item)[0] + '.meta'
            lines = [line.rstrip('\n') for line in open(metaFile)]
            
            f = open(metaFile, 'w')
            f.write(str(lines[0] + '\n'))
            f.write(str(lines[1] + '\n'))
            f.write(str(lines[2] + '\n'))
            f.write(str(lines[3] + '\n'))
            f.write(str(lines[4] + '\n'))
            f.write(str(lines[5] + '\n'))
            f.write(str(lines[6] + '\n'))
            f.write(str('' + '\n'))
            f.write(str('' + '\n'))
            f.write(str('' + '\n'))
            f.write(str('' + '\n'))
            f.write(str('' + '\n'))
            f.write(str('' + '\n'))
            f.write(str('' + '\n'))
            f.write(str('' + '\n'))
            f.write(notes + '\n')
            f.close()
            
        SLiB.messager('Notes updated!', 'green')

def SLiB_ReplacePreview():
    img = os.path.normpath(prevButton.objectName())
    if SLiB.gib('mainCat') in ['textures', 'hdri']:
        SLiB.messager('Not supported!', 'red')
    
    else:
        if cbxList:
            for item in cbxList:
                oldOne = os.path.splitext(item)[0] + '.png'
                image = om.MImage()
                image.readFromFile(img)
                image.resize( 512, 512 )
                image.writeToFile(oldOne, 'png')
                SLiB_UpdateView()
                SLiB.messager('Preview Image replaced!', 'green')

def SLiB_Collect():
    allDirs = []
    #SEARCH
    if cmds.textField('SLiB_TEXTFIELD_Search', q=1, tx=1):
        if cmds.iconTextCheckBox('searchSwitch', q=1, v=1):
            searchLoc = SLiB.gib('currLocation')
            if searchLoc:
            
                matchDirs = []
                #DIRS ONLY
                if not cmds.iconTextCheckBox('tagSwitch', q=1, v=1):
                    fWord = cmds.textField('SLiB_TEXTFIELD_Search', q=1, tx=1)
                    SLiB.messager('Searching...', 'blue')
                        
                    cmds.progressBar('PreviewProgress', e=1, max=1000)
                    for root, dirs, files in os.walk(searchLoc):
                        for name in dirs:
                            cmds.progressBar('PreviewProgress', e=1, step=1)
                            if name != '.mayaSwatches' and name != '_SUB' and name != 'Tex' and name != '.DS_Store' and name != '_THUMBS':
                                allDirs.append(os.path.join(root, name))

                        matchDirs = [k for k in allDirs if fWord.lower() in k.lower()]
                        allDirs = matchDirs
                
                #WITH TAGS
                if cmds.iconTextCheckBox('tagSwitch', q=1, v=1):
                    searchTags = str(cmds.textField('SLiB_TEXTFIELD_Search', q=1, tx=1))
                    SLiB.messager('Searching...', 'blue')
                    
                    cmds.progressBar('PreviewProgress', e=1, max=1000)
                    metaFiles = []
                    for root, dirs, files in os.walk(searchLoc):
                        for file in files:
                            cmds.progressBar('PreviewProgress', e=1, step=1)
                            if file.endswith('.meta'):
                                 metaFiles.append(os.path.join(root, file))
                    cmds.progressBar('PreviewProgress', e=1, pr=0)
                    
                    cmds.progressBar('PreviewProgress', e=1, max=(len(metaFiles)))
                    match = []
                    for e in metaFiles:
                        count = 0
                        cmds.progressBar('PreviewProgress', e=1, step=1)
                        lines = [line.rstrip('\n') for line in open(e)]
                        itemTags = lines[1].split(' ')
                        for i in itemTags:
                            if len(i) > 0:
                                if i in searchTags:
                                   count = count + 1
                                   
                            if count == len(searchTags.split(' ')):
                                match.append(os.path.dirname(e))
                               
                    allDirs = list(set(match + matchDirs))
                cmds.progressBar('PreviewProgress', e=1, pr=0)
                
            else:
                SLiB.messager('Please select a Category or ROOT to search the whole Library!', 'yellow')
                sys.exit()

    #NORMAL
    else:
        dir = SLiB.gib('currLocation')
        if dir != None and dir != os.path.normpath(mel.eval('getenv SLiBRARY;') + SLiB.gib('mainCat')):
            for name in os.listdir(dir):
                if name != '.mayaSwatches' and name != '_SUB' and name != 'Tex' and name != '.DS_Store' and name != '_THUMBS':
                    allDirs.append(os.path.join(dir, name))

    collection = []
    for dir in allDirs:
        for a in os.listdir(dir):
            if SLiB.gib('mainCat') == 'textures':
                if os.path.splitext(a)[1] in ['.jpg', '.bmp', '.png', '.gif', '.tif', '.tga', '.iff', '.exr', '.hdr']:
                    collection.append(os.path.join(dir, a))
            if SLiB.gib('mainCat') == 'hdri':
                if os.path.splitext(a)[1] in ['.hdr', '.exr']:
                    collection.append(os.path.join(dir, a))
            else:
                if os.path.splitext(a)[1] == '.mb' or os.path.splitext(a)[1] == '.ma' or os.path.splitext(a)[1] == '.obj':
                    collection.append(os.path.join(dir, a)) 
    
    if len(collection) > 0:
        return collection
    else:
        return None

def SLiB_UpdateView():
    global SLiBCollection
    global SLiBFolder
    SLiBCollection = []
    SLiBFolder = []
    
    if SLiBThumbsScrollLayout: 
        SLiB_ClearLayout(SLiBThumbsScrollLayout)

    if SLiB.gib('mainCat') == 'paths':
        SLiBThumbsLayout.setStyleSheet("None;")

        SLiBCollection = SLiB_TexList()
        
        if SLiBCollection != None:
            cmds.evalDeferred(lambda: SLiBListTextures())

    else:
        SLiBCollection = SLiB_Collect()
  
        SLiBThumbsLayout.setStyleSheet("background-color: #303030; color: rgb(200,200,200);")

        if SLiB.gib('currLocation') == os.path.normpath(os.path.join(SLiB.gib('library'), SLiB.gib('mainCat'))):
            parentDir = SLiB.gib('currLocation')
            for d in os.listdir(parentDir):
                if os.path.isdir(os.path.join(parentDir, d)) and d != '_SUB':
                    SLiBFolder.append(os.path.join(parentDir, d))
        else:
            parentDir = os.path.join(SLiB.gib('currLocation'), '_SUB')
            for d in os.listdir(parentDir):
                if os.path.isdir(os.path.join(SLiB.gib('currLocation'), '_SUB', d)) and d != '_SUB':
                    SLiBFolder.append(os.path.join(SLiB.gib('currLocation'), '_SUB', d))
            

        SLiBFlowLayout()
        SLiB_SaveCats()

        if cmds.iconTextCheckBox('searchSwitch', q=1, v=1):
            if SLiBCollection:
                SLiB.messager(str(len(SLiBCollection)) + ' Item(s) found!', 'green')
        else:
            if SLiBCollection:
                SLiB.messager(str(len(SLiBCollection)) + ' Item(s) loaded!', 'none')
            if SLiBFolder:
                SLiB.messager(str(len(SLiBFolder)) + ' Folder loaded!', 'none')
            if SLiBCollection and SLiBFolder:
                SLiB.messager(str(len(SLiBFolder)) + ' Folder and ' + str(len(SLiBCollection)) + ' Item(s) loaded!', 'none')

        if not SLiBCollection:
            if cmds.iconTextCheckBox('searchSwitch', q=1, v=1):
                SLiB.messager('Nothing found!', 'yellow')
            else:
                if not SLiBFolder:
                    SLiB.messager('Library or Category is empty!', 'yellow')
                    
class ScrollArea(QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs):
        QtWidgets.QScrollArea.__init__(self, *args, **kwargs)
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setMouseTracking(True)
        
        # Context Menu
        self.menu = QtWidgets.QMenu()
        
        if SLiB.gib('mainCat') == 'paths':
            SLiBThumbsLayout.setStyleSheet("None;")
            self.menu.addAction('Rename Image File', self.sc_renameImage)
            self.menu.addSeparator()
            self.menu.addAction('Copy to Folder...', self.menu_copy)
            self.menu.addSeparator()
            self.menu.addAction('Find Missing...', self.menu_find)
            self.menu.addSeparator()
            self.menu.addAction('Open in File Browser', self.menu_open)
            self.menu.addSeparator()
            self.menu.addAction('Select ALL', self.menu_all)
            self.menu.addAction('Select None', self.menu_none)

            shortcut_rename = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F2), self)
            shortcut_rename.setContext(Qt.WidgetWithChildrenShortcut)
            shortcut_rename.activated.connect(self.sc_renameImage)

        else:
            self.menu.addAction('PASTE', self.menu_paste)
            self.menu.addSeparator()
            self.menu.addAction('New Category', self.menu_add)
            self.menu.addSeparator()
            self.menu.addAction('Open in File Browser', self.menu_open)
            self.menu.addSeparator()
            self.menu.addAction('Select ALL', self.menu_all)
            self.menu.addAction('Select None', self.menu_none)
        
        self.menu.setStyleSheet("selection-background-color: #ffaa00; selection-color: black; background-color: #525252; border: 1px solid black; color: #EBEBEB; padding: 0px 0px 0px 0px;")
        
        self.customContextMenuRequested.connect(self.context_menu)
        
        if not SLiB.gib('mainCat') == 'paths':
            shortcut_rename = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F2), self)
            shortcut_rename.setContext(Qt.WidgetWithChildrenShortcut)
            shortcut_rename.activated.connect(self.sc_rename)
            
            shortcut_copy = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+C'), self)
            shortcut_copy.setContext(Qt.WidgetWithChildrenShortcut)
            shortcut_copy.activated.connect(self.sc_copy)
            
            shortcut_paste = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+V'), self)
            shortcut_paste.setContext(Qt.WidgetWithChildrenShortcut)
            shortcut_paste.activated.connect(self.menu_paste)
            
            shortcut_open = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+O'), self)
            shortcut_open.setContext(Qt.WidgetWithChildrenShortcut)
            shortcut_open.activated.connect(self.menu_open)
            
            shortcut_add = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+N'), self)
            shortcut_add.setContext(Qt.WidgetWithChildrenShortcut)
            shortcut_add.activated.connect(self.menu_add)
            
        shortcut_mark = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+A'), self)
        shortcut_mark.setContext(Qt.WidgetWithChildrenShortcut)
        shortcut_mark.activated.connect(self.sc_mark)

    def sc_mark(self):
        if cbxList:
            SLiB_BrowserMark('none')
        else:
            SLiB_BrowserMark('all')
    
    def sc_renameImage(self):
        SLiB_BrowserRenameImage()

    def sc_rename(self):
        SLiB_BrowserRename()
        
    def sc_copy(self):
        SLiB_BrowserCopy()
        
    def menu_copy(self):
        SLiB_CopyTexturesTo('folder')
    
    def menu_find(self):
        SLiB_FindMissingTextures()
    
    def menu_paste(self):
        SLiB_BrowserPaste()
    
    def menu_open(self):
        if SLiB.gib('mainCat') == 'paths':
            SLiB_OpenInFileBrowser()
        else:
            SLiB_OpenCatInFileBrowser()
    
    def menu_add(self):
        SLiB_CreateDir()
    
    def menu_all(self):
        SLiB_BrowserMark('all')
    
    def menu_none(self):
        SLiB_BrowserMark('none')
        
    def context_menu(self):
        self.menu.popup(QCursor.pos())
        position = self.menu.pos()
        self.menu.move(position.x() + 1, position.y() + 1)
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            pass
            
        if event.button() == QtCore.Qt.MidButton:
            pass
            
        if event.button() == QtCore.Qt.RightButton:
            pass

class BackButton(QtWidgets.QPushButton):
    left_clicked = QtCore.Signal(int)
    right_clicked = QtCore.Signal(int)
    
    def __init__(self, name, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, *args, **kwargs)
        
        thumbsize = SLiB.gib('thumbsize')
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setMouseTracking(True)
        self.setFlat(True)
        
        if SLiB.gib('mainCat') == 'hdri':
            self.setFixedSize(thumbsize*2, thumbsize)
        else:
            self.setFixedSize(thumbsize, thumbsize)
        icon = QtGui.QIcon(SLiB_img + 'browser_back.png')
        self.setIconSize(self.size())
        self.setIcon(icon)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.left_click_count = self.right_click_count = 0
        
        # Context Menu
        self.menu = QtWidgets.QMenu()
        self.menu.addAction('Back to ROOT', self.menu_root)
        self.menu.setStyleSheet("selection-background-color: #ffaa00; selection-color: black; background-color: #525252; border: 1px solid black; color: #EBEBEB; padding: 0px 0px 0px 0px;")
        
        self.customContextMenuRequested.connect(self.context_menu)
        
    def menu_root(self):
        cmds.treeView('treeView', e=1, cs=1)
        cmds.treeView('treeView', e=1, si=(os.path.normpath(os.path.join(mel.eval('getenv SLiBRARY;'), cmds.iconTextRadioCollection('mainCatCollection', q=1, sl=1).lower())), 1))
        SLiB_Expand()
        
    def context_menu(self):
        self.menu.popup(QCursor.pos())
        position = self.menu.pos()
        self.menu.move(position.x() + 1, position.y() + 1)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.left_click_count += 1
            if not self.timer.isActive():
                self.timer.start()
        
        if event.button() == QtCore.Qt.RightButton:
            self.right_click_count += 1
            if not self.timer.isActive():
                self.timer.start()

    def timeout(self):
        if self.left_click_count >= self.right_click_count:
            self.left_clicked.emit(self.left_click_count)
        else:
            self.right_clicked.emit(self.right_click_count)
        self.left_click_count = self.right_click_count = 0

class FolderButton(QtWidgets.QPushButton):
    left_clicked = QtCore.Signal(int)
    right_clicked = QtCore.Signal(int)
    
    def __init__(self, name, folder, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, *args, **kwargs)
        
        thumbsize = SLiB.gib('thumbsize')
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setMouseTracking(True)
        self.setFlat(True)
        
        if SLiB.gib('mainCat') == 'hdri':
            self.setFixedSize(thumbsize*2, thumbsize)
        else:
            self.setFixedSize(thumbsize, thumbsize)
        icon = QtGui.QIcon(SLiB_img + 'browser_folder.png')
        self.setIconSize(self.size())
        self.setIcon(icon)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.left_click_count = self.right_click_count = 0
        
        # Context Menu
        self.menu = QtWidgets.QMenu()
        self.menu.addAction('Move to Folder', partial(self.menu_move, folder, 'move'))
        self.menu.addAction('Copy to Folder', partial(self.menu_move, folder, 'copy'))
        self.menu.addSeparator()
        self.menu.addAction('Open in File Browser', partial(self.menu_open, folder))
        self.menu.addSeparator()
        self.menu.addAction('Remove Category', partial(self.menu_remove, folder))
        self.menu.setStyleSheet("selection-background-color: #ffaa00; selection-color: black; background-color: #525252; border: 1px solid black; color: #EBEBEB; padding: 0px 0px 0px 0px;")
        #self.setMenu(self.menu)
        
        self.customContextMenuRequested.connect(self.context_menu)
    
    def menu_move(self, folder, mode):
        if cbxList:
            for item in cbxList:
                sourceDir = os.path.dirname(item)
                destinationDir = os.path.join(folder, os.path.basename(os.path.dirname(item)))

                if os.path.isdir(destinationDir):
                    SLiB.messager('Item with this Name already exists!', 'red')
                    sys.exit()
                else:
                    shutil.copytree(sourceDir, destinationDir)
                    SLiB_TexPathChangeWarning(destinationDir)
                    
                if mode == 'move':
                    shutil.rmtree(sourceDir)

            if mode == 'move':
                SLiB.messager('Moved [ ' + str(len(cbxList)) + ' ] item(s)', 'green')
            if mode == 'copy':
                SLiB.messager('Copied [ ' + str(len(cbxList)) + ' ] item(s)', 'green')

            cmds.evalDeferred(lambda: SLiB_UpdateView())
            
        else:
            SLiB.messager('Please copy something first!', 'yellow')
    
    def menu_open(self, folder):
        if platform.system() == 'Windows':
            os.startfile(folder)
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', folder])
        else:
            subprocess.Popen(['xdg-open', folder])
        
    def menu_remove(self, folder):
        cmds.treeView('treeView', e=1, cs=1)
        cmds.treeView('treeView', e=1, si=(folder, 1))
        SLiB_RemoveDir()
    
    def context_menu(self):
        self.menu.popup(QCursor.pos())
        position = self.menu.pos()
        self.menu.move(position.x() + 1, position.y() + 1)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.left_click_count += 1
            if not self.timer.isActive():
                self.timer.start()
        
        if event.button() == QtCore.Qt.RightButton:
            self.right_click_count += 1
            if not self.timer.isActive():
                self.timer.start()

    def timeout(self):
        if self.left_click_count >= self.right_click_count:
            self.left_clicked.emit(self.left_click_count)
        else:
            self.right_clicked.emit(self.right_click_count)
        self.left_click_count = self.right_click_count = 0

class ItemButton(QtWidgets.QPushButton):
    left_clicked = QtCore.Signal(int)
    right_clicked = QtCore.Signal(int)
    
    def __init__(self, name, file, fileDir, fileName, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, *args, **kwargs)
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setMouseTracking(True)
        self.setFlat(True)
        
        thumbsize = SLiB.gib('thumbsize')
        
        if SLiB.gib('mainCat') == 'hdri':
            self.setFixedSize(thumbsize*2, thumbsize)
        else:
            self.setFixedSize(thumbsize, thumbsize)
        
        if SLiB.gib('mainCat') in ['textures', 'hdri']:
            try:
                imageFile =  os.path.join(fileDir, '_THUMBS', fileName + '.png')
            except:
                imageFile =  os.path.join(fileDir, fileName + '.png')

        else:
            if os.path.isfile(file + '.png'):
                imageFile = file + '.png'
            else:
                imageFile = os.path.join(SLiB_img, 'image_missing.png')
        
        if cmds.menuItem('slmetathumbs', q=1, cb=1):
            #OVERLAY
            metaFile = os.path.join(fileDir, fileName + '.meta')
            if os.path.isfile(metaFile):
                lines = [line.rstrip('\n') for line in open(metaFile)]
                overlay = QtGui.QImage(os.path.join(SLiB_img, lines[5].lower() + '_overlay.png')) 
            else:
                overlay = QtGui.QImage(os.path.join(SLiB_img, 'blank_overlay.png'))
            
            bg = QtGui.QImage(os.path.join(SLiB_img, 'browser_bg01.png'))
            bg_scaled = bg.scaled(thumbsize, thumbsize, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            overlay_scaled = overlay.scaled(thumbsize, thumbsize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            itemImg = QtGui.QImage(imageFile)
            
            pixmap = QtGui.QPixmap(itemImg)
            if SLiB.gib('mainCat') == 'hdri':
                scaled = pixmap.scaled(thumbsize*2, thumbsize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                itemImage = scaled.toImage()
                combined = QtGui.QPixmap(thumbsize*2, thumbsize)
            else:
                scaled = pixmap.scaled(thumbsize, thumbsize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                itemImage = scaled.toImage()
                combined = QtGui.QPixmap(thumbsize, thumbsize)

            p = QtGui.QPainter(combined)
            
            p.setRenderHint(QtGui.QPainter.Antialiasing, True)
            p.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
            p.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            
            p.drawImage(QtCore.QPoint(0, 0), bg_scaled)
            p.drawImage(QtCore.QPoint(0, 0), itemImage)
            p.drawImage(QtCore.QPoint(0, 0), overlay_scaled)
            p.end()

            pPixmap = QtGui.QPixmap(combined)
            self.icon = QtGui.QIcon(pPixmap)
            
        else:
            self.icon = QtGui.QIcon(imageFile)

        self.orgImage = imageFile
            
        self.setIcon(self.icon)
        if SLiB.gib('mainCat') == 'hdri':
            self.setIconSize(QtCore.QSize(thumbsize*2, thumbsize))
        else:
            self.setIconSize(QtCore.QSize(thumbsize,thumbsize))

        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.left_click_count = self.right_click_count = 0
        
        # Context Menu
        self.menu = QtWidgets.QMenu()
        #TEXTURES / HDRi
        if SLiB.gib('mainCat') in ['textures', 'hdri']:
            self.menu.addAction('IMPORT', self.menu_imp)
            self.menu.addSeparator()
            self.menu.addAction('OPEN in FileBrowser', self.menu_open)
            self.menu.addAction('OPEN in Photoshop', self.menu_openPhotoshop)
            self.menu.addSeparator()
            self.menu.addAction('DUPLICATE', self.menu_duplicate)
            self.menu.addAction('RENAME', self.menu_rename)
            self.menu.addAction('COPY', self.menu_copy)
            self.menu.addSeparator()
            self.menu.addAction('DELETE', self.menu_delete)
        
        #OTHERS
        else:
            self.menu.addAction('IMPORT', self.menu_imp)
            if SLiB.gib('mainCat') == 'objects' or SLiB.gib('mainCat') == 'lights':
                self.menu.addSeparator()
                self.menu.addAction('IMPORT and Place at Selection', self.menu_impPlace)
                self.menu.addAction('IMPORT and Replace Selection', self.menu_impReplace)
            self.menu.addSeparator()
            self.menu.addAction('OPEN in Maya', self.menu_openMaya)
            self.menu.addAction('OPEN in FileBrowser', self.menu_open)
            self.menu.addSeparator()
            self.menu.addAction('DUPLICATE', self.menu_duplicate)
            self.menu.addAction('RENAME', self.menu_rename)
            self.menu.addAction('COPY', self.menu_copy)
            self.menu.addSeparator()
            self.menu.addAction('DELETE', self.menu_delete)

        self.menu.setStyleSheet("selection-background-color: #ffaa00; selection-color: black; background-color: #525252; border: 1px solid black; color: #EBEBEB; padding: 0px 0px 0px 0px;")
        #self.setMenu(self.menu)
        
        self.customContextMenuRequested.connect(self.context_menu)
        
    def enterEvent(self, event):
        thumbsize = SLiB.gib('thumbsize')
        thumbsizeFactor = thumbsize + (thumbsize*5)/10
        
        orgImg = QtGui.QImage(self.orgImage)
        orgImg_scaled = orgImg.scaled(thumbsizeFactor*2, thumbsizeFactor, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        hPixmap = QtGui.QPixmap(orgImg_scaled)
        self.setIcon(QtGui.QIcon(hPixmap))
        
        if SLiB.gib('mainCat') == 'hdri':
            self.setIconSize(QtCore.QSize(thumbsizeFactor*2,thumbsizeFactor))
        else:
            self.setIconSize(QtCore.QSize(thumbsizeFactor,thumbsizeFactor))
            
    def leaveEvent(self,event):
        thumbsize = SLiB.gib('thumbsize')
        self.setIcon(self.icon)
            
        if SLiB.gib('mainCat') == 'hdri':
            self.setIconSize(QtCore.QSize(thumbsize*2,thumbsize))
        else:
            self.setIconSize(QtCore.QSize(thumbsize,thumbsize))
            
    def context_menu(self):
        self.menu.popup(QCursor.pos())
        position = self.menu.pos()
        self.menu.move(position.x() + 1, position.y() + 1)
    
    def menu_imp(self):
        if SLiB.gib('mainCat') in ['textures', 'hdri']:
            SLiB_Import('Texture')
        else:
            SLiB_Import('Normal')
        
    def menu_impPlace(self):
        SLiB_Import('Place')
    
    def menu_impReplace(self):
        SLiB_Import('Replace')
    
    def menu_openMaya(self):
        SLiB_OpenInMaya()
        
    def menu_openPhotoshop(self):
        SLiB_OpenInPhotoshop()
    
    def menu_open(self):
        SLiB_OpenInFileBrowser()
        
    def menu_duplicate(self):
        SLiB_BrowserDuplicate()
    
    def menu_rename(self):
        SLiB_BrowserRename()
    
    def menu_copy(self):
        SLiB_BrowserCopy()
    
    def menu_delete(self):
        SLiB_BrowserDelete()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.left_click_count += 1
            if not self.timer.isActive():
                self.timer.start()
        
        if event.button() == QtCore.Qt.RightButton:
            self.right_click_count += 1
            if not self.timer.isActive():
                self.timer.start()

    def timeout(self):
        if self.left_click_count >= self.right_click_count:
            self.left_clicked.emit(self.left_click_count)
        else:
            self.right_clicked.emit(self.right_click_count)
        self.left_click_count = self.right_click_count = 0

class SLiBFlowLayout(QtWidgets.QWidget):
    def __init__(self):
        super(SLiBFlowLayout, self).__init__()
        
        global cbxList
        cbxList = []

        global flowLayout
        flowLayout = FlowLayout()
        thumbsize = SLiB.gib('thumbsize')

        if SLiB.gib('currLocation') != os.path.normpath(os.path.join(SLiB.gib('library'), SLiB.gib('mainCat'))):
            if cmds.menuItem('slfolderthumbs', q=1, cb=1):
                # Back Widget
                widgetBack = QtWidgets.QWidget()
                if SLiB.gib('mainCat') == 'hdri':
                    widgetBack.setFixedSize(thumbsize*2, thumbsize +20)
                else:
                    widgetBack.setFixedSize(thumbsize, thumbsize +20)
                widgetBack.setStyleSheet("background-color:black;")
                layoutBack = QtWidgets.QVBoxLayout()
                layoutBack.setSpacing(0)
                layoutBack.setContentsMargins(0,0,0,0)
                widgetBack.setLayout(layoutBack)
                
                # Back Thumbnail
                backBtn = BackButton(self)
                backBtn.left_clicked[int].connect(self.left_clickBack)
                backBtn.right_clicked[int].connect(self.right_clickBack)
                layoutBack.addWidget(backBtn)
                
                # Back Label
                labelBack = QtWidgets.QLabel('..')
                if SLiB.gib('mainCat') == 'hdri':
                    labelBack.setFixedSize(thumbsize*2, 20)
                else:
                    labelBack.setFixedSize(thumbsize, 20)
                labelBack.setObjectName('back')
                labelBack.setStyleSheet("font-size: 11px; padding: 2;")
                layoutBack.addWidget(labelBack)
                
                flowLayout.addWidget(widgetBack)
                
        if SLiBFolder and not cmds.iconTextCheckBox('searchSwitch', q=1, v=1) and cmds.menuItem('slfolderthumbs', q=1, cb=1):
            for folder in SLiBFolder:
                folder = os.path.normpath(folder)
                fName = str(os.path.basename(folder))
                
                # Main Folder Widget
                widgetFolder = QtWidgets.QWidget()
                if SLiB.gib('mainCat') == 'hdri':
                    widgetFolder.setFixedSize(thumbsize*2, thumbsize +20)
                else:
                    widgetFolder.setFixedSize(thumbsize, thumbsize +20)
                widgetFolder.setStyleSheet("background-color:black;")
                widgetFolder.setObjectName(folder)
                layoutFolder = QtWidgets.QVBoxLayout()
                layoutFolder.setSpacing(0)
                layoutFolder.setContentsMargins(0,0,0,0)
                widgetFolder.setLayout(layoutFolder)
                
                # Main Folder Thumbnail
                folderBtn = FolderButton(self, folder)
                folderBtn.setObjectName(folder)
                folderBtn.left_clicked[int].connect(self.left_clickFolder)
                folderBtn.right_clicked[int].connect(self.right_clickFolder)
                layoutFolder.addWidget(folderBtn)
                
                # Main Folder Label
                labelFolder = QtWidgets.QLabel(fName)
                if SLiB.gib('mainCat') == 'hdri':
                    labelFolder.setFixedSize(thumbsize*2, 20)
                else:
                    labelFolder.setFixedSize(thumbsize, 20)
                labelFolder.setObjectName(folder)
                labelFolder.setStyleSheet("font-size: 11px; padding: 2;")
                layoutFolder.addWidget(labelFolder)
                
                flowLayout.addWidget(widgetFolder)

        if SLiBCollection:
            cmds.progressBar('PreviewProgress', e=1, max=(len(SLiBCollection)))
            for s in SLiBCollection:
                s = os.path.normpath(s)
                fileDir = os.path.dirname(s)
                fileBase = os.path.basename(s)
                file = os.path.splitext(s)[0]
                fileEx = os.path.splitext(s)[1]
                fileName = os.path.splitext(fileBase)[0]
                fileString = '{0}'.format(file)
                
                # File Widget
                widgetItem = QtWidgets.QWidget()
                if SLiB.gib('mainCat') == 'hdri':
                    widgetItem.setFixedSize(thumbsize*2, thumbsize +20)
                else:
                    widgetItem.setFixedSize(thumbsize, thumbsize +20)
                widgetItem.setStyleSheet("background-color:black;")
                widgetItem.setObjectName(s)
                layoutItem = QtWidgets.QVBoxLayout()
                layoutItem.setSpacing(0)
                layoutItem.setContentsMargins(0,0,0,0)
                widgetItem.setLayout(layoutItem)
                
                # File Thumbnail
                imageBtn = ItemButton(self, file, fileDir, fileName)
                imageBtn.setObjectName(s)
                imageBtn.setToolTip("<font color=white>%s</font>" % fileName)
                imageBtn.left_clicked[int].connect(self.left_click)
                imageBtn.right_clicked[int].connect(self.right_click)
                layoutItem.addWidget(imageBtn)
                
                # File Label
                label = QtWidgets.QLabel(fileName)
                if SLiB.gib('mainCat') == 'hdri':
                    label.setFixedSize(thumbsize*2, 20)
                else:
                    label.setFixedSize(thumbsize, 20)
                label.setObjectName(s)
                label.setStyleSheet("font-size: 11px; padding: 2;")
                layoutItem.addWidget(label)

                # File LabelCbx
                labelCbx = QtWidgets.QCheckBox(fileName)
                if SLiB.gib('mainCat') == 'hdri':
                    labelCbx.setFixedSize(thumbsize*2, 20)
                else:
                    labelCbx.setFixedSize(thumbsize, 20)
                labelCbx.setObjectName(s)
                labelCbx.setStyleSheet("font-size: 11px; padding: 2;")
                layoutItem.addWidget(labelCbx)
                labelCbx.hide()

                flowLayout.addWidget(widgetItem)
                cmds.progressBar('PreviewProgress', e=1, step=1)

        cmds.progressBar('PreviewProgress', e=1, pr=0)
        self.setLayout(flowLayout)
        global scroll
        scroll = ScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self)
        #scroll.left_clicked[int].connect(self.left_clickScroll)
        #scroll.right_clicked[int].connect(self.right_clickScroll)
        SLiBThumbsScrollLayout.addWidget(scroll)
        self.setContentsMargins(5, 5, 5, 5)
        
    #def enterEvent(event, imageFile):
    #    print imageFile
    
    def left_click(self, nb):
        sending_button = self.sender()
        item = os.path.normpath(sending_button.objectName())
        
        modifiers = QtWidgets.QApplication.keyboardModifiers()

        if nb == 1:
            #'Single left click
            buttonWidget = scroll.findChild(QWidget, item)
            checkbox = buttonWidget.findChild(QCheckBox, item)
            label = buttonWidget.findChild(QLabel, item)
            
            if modifiers == QtCore.Qt.ShiftModifier:
                if checkbox.isChecked():
                    checkbox.setChecked(0)
                    label.setStyleSheet("padding: 2;")
                    cbxList.remove(item)
                else:
                    checkbox.setChecked(1)
                    label.setStyleSheet("background-color: #50b0ff; color: black; padding: 2;")
                    cbxList.append(item)
            
            if modifiers == QtCore.Qt.ControlModifier:
                SLiB_ZoomWin(item)
            
            if modifiers == 0:
                SLiB_BrowserMark('none')

                checkbox.setChecked(1)
                label.setStyleSheet("background-color: #50b0ff; color: black; padding: 2;")
                cbxList.append(item)
                
            if cbxList:
                for c in cbxList:
                    print c + '\n'
                    buttonWidget = scroll.findChild(QWidget, c)
                    label = buttonWidget.findChild(QLabel, c)
                    if len(cbxList) > 1:
                            label.setStyleSheet("background-color: #ff9c00; color: black; padding: 2;")
                    
                    if len(cbxList) == 1:
                            label.setStyleSheet("background-color: #50b0ff; color: black; padding: 2;")

            SLiB_UpdateInfo(item)
        
        else:
            if SLiB.gib('mainCat') in ['textures', 'hdri']:
                SLiB_BrowserImport('Texture', item)
            else:
                SLiB_BrowserImport('Normal', item)

    def right_click(self, nb):
        sending_button = self.sender()
        item = os.path.normpath(sending_button.objectName())
        
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        
        if nb == 1:
            buttonWidget = scroll.findChild(QWidget, item)
            checkbox = buttonWidget.findChild(QCheckBox, item)
            label = buttonWidget.findChild(QLabel, item)

            if checkbox.isChecked():
                pass
            else:
                buttonWidget = scroll.findChild(QWidget, item)
                checkbox = buttonWidget.findChild(QCheckBox, item)
                checkbox.setChecked(1)
                cbxList.append(item)
                
            if cbxList:
                for c in cbxList:
                    print c + '\n'
                    buttonWidget = scroll.findChild(QWidget, c)
                    label = buttonWidget.findChild(QLabel, c)
                    if len(cbxList) > 1:
                            label.setStyleSheet("background-color: #ff9c00; color: black; padding: 2;")
                    
                    if len(cbxList) == 1:
                            label.setStyleSheet("background-color: #50b0ff; color: black; padding: 2;")
            
            SLiB_UpdateInfo(item)
            
    def right_clickFolder(self, nb):
        pass
            
    def left_clickFolder(self, nb):
        folder = self.sender()
        item = os.path.normpath(folder.objectName())
        
        if nb == 1:
            cmds.treeView('treeView', e=1, cs=1)
            cmds.treeView('treeView', e=1, si=(item, 1))
            cmds.treeView('treeView', e=1, ei=(item, 1))
            SLiB_UpdateView()
            
    def right_clickBack(self, nb):
        pass
            
    def left_clickBack(self, nb):
        if nb == 1:
            parent = cmds.treeView('treeView', q=1, ip=cmds.treeView('treeView', q=1, si=1)[0])
            cmds.treeView('treeView', e=1, cs=1)
            if not parent:
                cmds.treeView('treeView', e=1, si=(os.path.normpath(os.path.join(mel.eval('getenv SLiBRARY;'), cmds.iconTextRadioCollection('mainCatCollection', q=1, sl=1).lower())), 1))
            else:
                cmds.treeView('treeView', e=1, si=(parent, 1))
            SLiB_UpdateView()
            
        if nb == 2:
            cmds.treeView('treeView', e=1, cs=1)
            cmds.treeView('treeView', e=1, si=(os.path.normpath(os.path.join(mel.eval('getenv SLiBRARY;'), cmds.iconTextRadioCollection('mainCatCollection', q=1, sl=1).lower())), 1))
            SLiB_UpdateView()

class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, spacing=-1):
        super(FlowLayout, self).__init__(parent)
        
        self.setSpacing(spacing)
        self.itemList = []
        self.setObjectName('FlowLayout')

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        size += QtCore.QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            widget = item.widget()
            spaceX = self.spacing() + widget.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            spaceY = self.spacing() + widget.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()

def SLiB_ClearLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                SLiB_ClearLayout(item.layout())

def SLiB_OpenInMaya():
    if cbxList:
        if cmds.optionMenu('meta_locked', q=1, v=1) == 'NO':
            answer = cmds.confirmDialog(t='Warning', m='This will close the current scene! \nDo you want to proceed?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            if answer == 'Yes':
                for item in cbxList:
                    cmds.file(item, open=1, f=1, iv=1)
        else:
            SLiB.messager('Item is locked!', 'red')
    else:
        SLiB.messager('Please select one Item!', 'red')

def SLiB_OpenInFileBrowser():
    if cbxList:
        for item in cbxList:
            path = str(os.path.dirname(item))
            
            if '${SLiB' in path:
                path = SLiB_absPath(path)

            if platform.system() == 'Windows':
                os.startfile(path)
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', path])
            else:
                subprocess.Popen(['xdg-open', path])
    else:
        SLiB.messager('Please select something first!', 'yellow')

def SLiB_OpenInPhotoshop():
    if cbxList:
        if cmds.optionMenu('meta_locked', q=1, v=1) == 'NO':
            for item in cbxList:
                if platform.system() == 'Windows':
                    os.startfile(item)
                elif platform.system() == 'Darwin':
                    check_call(['open', item])
        else:
            SLiB.messager('Item is locked!', 'red')
    else:
        SLiB.messager('Please select something first!', 'red')

def SLiB_OpenCatInFileBrowser():
    if SLiB.gib('currLocation'):
        path = SLiB.gib('currLocation')
        
        if platform.system() == 'Windows':
            os.startfile(path)
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])
    else:
        SLiB.messager('Please select a Category first!', 'yellow')

def SLiB_NameFrom(x):
    if x == 'selection':
        sel = cmds.ls(sl=1)
        if len(sel) == 0:
            SLiB.messager('Please select an Oject!', 'red')
        else:
            cmds.textField('SLiB_TEXTFIELD_Name', e=1, tx=sel[0])
    if x == 'asset':
        if cbxList:
            if len(cbxList) == 1:
                cmds.textField('SLiB_TEXTFIELD_Name', e=1, tx=os.path.splitext(os.path.basename(cbxList[0]))[0])

def SLiB_BrowserDelete():
    if cbxList:
        if cmds.optionMenu('meta_locked', q=1, v=1) == 'NO':
            if cmds.menuItem('QuickDelete', q=1, cb=1):
                answer = cmds.confirmDialog(t='Warning', m='Do you really want to Delete? \nPress YES to proceed.', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            else:
                answer = 'Yes'
            
            if answer == 'Yes':
                for item in cbxList:
                    renameFolder = os.path.dirname(item)
                    renameFile = os.path.splitext(item)[0]
                    newName = cmds.promptDialog(q=1, t=1).replace(' ','_')
                    newDir = os.path.join(SLiB.gib('currLocation'), newName)
                    deleteFolder = os.path.dirname(item)
                    shutil.rmtree(deleteFolder)
            
            if not cmds.iconTextCheckBox('RVLocked', q=1, v=1):
                SLiB_OverlayImage(os.path.join(SLiB_img, 'browser_logo.png'))
            
            cmds.text('SLiB_shaderName', e=1, l='', al='center')
            cmds.evalDeferred(lambda: SLiB_UpdateView())
            SLiB.messager(str(len(cbxList)) + ' Item(s) deleted!', 'green')
        
        else:
            SLiB.messager('Item is locked!', 'red')
        
    else:
        SLiB.messager('Please select something first!', 'yellow')

def SLiB_BrowserRename():
    if cbxList:
        if len(cbxList) == 1:
            if cmds.optionMenu('meta_locked', q=1, v=1) == 'NO':
                for item in cbxList:
                    result = cmds.promptDialog(t='Rename', m='Enter Name:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel', tx=os.path.splitext(os.path.basename(item))[0])
                    
                    if result == 'OK':
                        renameFolder = os.path.dirname(item)
                        renameFile = os.path.splitext(item)[0]
                        newName = cmds.promptDialog(q=1, t=1).replace(' ','_')
                        newDir = str(os.path.join(SLiB.gib('currLocation'), newName))
                        
                        if os.path.isdir(newDir):
                            SLiB.messager('Name already exists!', 'red')
                        
                        else:
                            shutil.move(renameFolder, newDir)
                        
                            allFiles = [os.path.join(newDir,fn) for fn in next(os.walk(newDir))[2]]

                            for e in allFiles:
                                file = os.path.splitext(e)[0]
                                fileExt = os.path.splitext(e)[1]
                                os.rename(e, os.path.join(newDir, newName + fileExt))
                                
                            #TEXTURE THUMBS
                            if SLiB.gib('mainCat') in ['textures', 'hdri']:
                                thumb = newDir + '/_THUMBS/' + next(os.walk(newDir + '/_THUMBS'))[2][0]
                                os.rename(thumb, os.path.join(newDir, '_THUMBS', newName + '.png'))
                            
                            path = newDir

                            SLiB.messager('Renamed!', 'green')
                            cmds.evalDeferred(lambda: SLiB_UpdateView())
                            SLiB_TexPathChangeWarning(path)
            else:
                SLiB.messager('Item is locked!', 'red')
        else:
            SLiB.messager('You can only rename one item at a time!', 'red')
    else:
        SLiB.messager('Please select something first!', 'yellow')
        
def SLiB_BrowserRenameImage():
    if cbxList:
        if len(cbxList) == 1:
            if cmds.optionMenu('meta_locked', q=1, v=1) == 'NO':
                for item in cbxList:
                    i = item
                    if '${SLiB' in item:
                        i = SLiB_absPath(item)
                                                
                    sourcePath = os.path.dirname(i.split('|')[0])
                    sourceFile = os.path.basename(i).split('|')[0]
                    sourceName = os.path.splitext(sourceFile)[0]
                    sourceExt =  os.path.splitext(sourceFile)[1]
                    node = item.split('|')[1]
                    
                    result = cmds.promptDialog(t='Rename Image File', m='Enter Name:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel', tx=sourceName)
                    
                    if result == 'OK':
                        newName = cmds.promptDialog(q=1, t=1).replace(' ','_')
                        finalPath = str(os.path.join(sourcePath, newName + sourceExt))
                        if os.path.isfile(finalPath):
                            SLiB.messager('File already exists!', 'red')
                        
                        else:
                            os.rename(os.path.join(sourcePath, sourceFile), finalPath)
                            if '${SLiB' in item:
                                finalPath = SLiB_relPath(finalPath)
                            
                            cmds.setAttr(node + SLiB.gibTexSlot(node), finalPath, type='string')

                            SLiB.messager('Renamed!', 'green')
                            cmds.evalDeferred(lambda: SLiB_UpdateView())
            else:
                SLiB.messager('Item is locked!', 'red')
        else:
            SLiB.messager('You can only rename one item at a time!', 'red')
    else:
        SLiB.messager('Please select something first!', 'yellow')

def SLiB_BrowserDuplicate():
    if cbxList:
        for item in cbxList:
            doppelFolder = os.path.dirname(item)
            doppelName = os.path.basename(os.path.dirname(item))
            destFolder = os.path.join(SLiB.gib('currLocation'), doppelName + '_Copy')
        
            i=1
            while os.path.exists(destFolder + str(i)):
                i+=1
            ziel = destFolder + str(i)
            shutil.copytree(doppelFolder, ziel)
            allFiles = [os.path.join(ziel,fn) for fn in next(os.walk(ziel))[2]]
            
            #TEXTURES
            if SLiB.gib('mainCat') in ['textures', 'hdri']:
                allFiles.append(ziel + '/_THUMBS/' + next(os.walk(ziel + '/_THUMBS'))[2][0])

            for e in allFiles:
                file = os.path.splitext(e)[0]
                fileExt = os.path.splitext(e)[1]
                os.rename(e, file + '_Copy' + str(i)  + fileExt)
                
            path = destFolder + str(i)
            SLiB_TexPathChangeWarning(path)

            SLiB.messager('Duplicated!', 'green')
            cmds.evalDeferred(lambda: SLiB_UpdateView())
    else:
        SLiB.messager('Please select something first!', 'yellow')

def SLiB_BrowserCopy():
    if cbxList:
        cmds.optionVar(sv=('SLIB_CopyType', SLiB.gib('mainCat')))

        global copyList
        copyList = []

        copyList = cbxList
        SLiB.messager(str(len(copyList)) + ' Item(s) Copied!', 'green')
    else:
        SLiB.messager('Please select something first!', 'yellow')

def SLiB_BrowserPaste():
    if cmds.optionVar(q=('SLIB_CopyType')) == SLiB.gib('mainCat'):
        if copyList:
            if SLiB.gib('currLocation') != None:
                for item in copyList:
                    sourceDir = os.path.dirname(item)
                    destinationDir = os.path.join(SLiB.gib('currLocation'), os.path.basename(os.path.dirname(item)))
                    
                    if sourceDir != destinationDir:
                        if os.path.isdir(destinationDir):
                            SLiB.messager('Item with this Name already exists!', 'red')

                        else:
                            shutil.copytree(sourceDir, destinationDir)
                            SLiB_TexPathChangeWarning(destinationDir)

                    else:
                        SLiB.messager('Cannot COPY and PASTE to the same Location! Use DUPLICATE!', 'red')
                        
                SLiB.messager('Pasted!', 'green')
                cmds.evalDeferred(lambda: SLiB_UpdateView())
            
            else:
                SLiB.messager('Please select a Category!', 'red')
                
        else:
            SLiB.messager('Please copy something first!', 'yellow')
            
    else:
        SLiB.messager('Cannot paste ' + cmds.optionVar(q=('SLIB_CopyType')).upper() + ' in ' + SLiB.gib('mainCat').upper() +'!', 'yellow')

def SLiB_TexPathChangeWarning(path):
    if os.path.isdir(path + '/' + 'Tex'):
        if cmds.menuItem('AutoRepath', q=1, cb=1):
            answer = 'Yes'
        else:
            answer = cmds.confirmDialog(t='Warning', m='You renamed, moved or duplicated a Shader / Asset with Textures.\nDo you want SLiB Browser PRO to automatically repath them?\n( Opens new scene! )', ma='center', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )

        if answer == 'Yes':
            for sceneFile in os.listdir(path):
                if os.path.splitext(sceneFile)[1] in ['.ma', '.mb']:
                    cmds.file(os.path.join(path, sceneFile), o=1, f=1)
                    
                    textdestination = os.path.join(path, 'Tex')

                    for i in SLiB_TexList():
                        orgfile = os.path.normpath(cmds.getAttr(i + SLiB.gibTexSlot(i)))
                        file = SLiB_absPath(orgfile)
                        
                        finalPath = os.path.normpath(os.path.join(textdestination, os.path.basename(file)))
                        
                        if file != finalPath:
                            if os.path.isfile(file):
                                shutil.copy(file, textdestination)
                                
                                print orgfile
                                if '${SLiB' in orgfile:
                                    finalPath = SLiB_relPath(finalPath)
                                
                                cmds.setAttr(i + SLiB.gibTexSlot(i), finalPath, type='string')

                    SLiB.messager('Repathing done!', 'green')

                    cmds.file(rename= path + '/' + sceneFile)
                    cmds.file(s=1)
                    cmds.file(f=1, new=1)

#BROWSER DOCK 2017
def SLiBBrowserWorkspaceControl():
    if cmds.workspaceControl(WorkspaceName, ex=1):
        cmds.deleteUI(WorkspaceName)
        
    global slBrowserUI
    slBrowserUI = cmds.loadUI(f=SLiB_gui + 'SLiBBrowser.ui')
    cmds.workspaceControl(WorkspaceName, l='SLiB Browser Pro v2.0' )
    cmds.control(slBrowserUI, e=1, p=WorkspaceName)
    SLiBBrowserUI()

def SLiB_CustomTexFolder():
    try:
        customTEX = cmds.fileDialog2(dir=os.path.join(mel.eval('getenv SLiBRARY;'), 'maps'), fm=2)[0]
    except:
        customTEX = None
    
    if customTEX != None:
        cmds.optionVar(sv=('customTEXFolder', customTEX))
        cmds.textField('SLiB_TEXTFIELD_Texpath', e=1, tx=os.path.normpath(customTEX))
        
def SLiBQuit():
    print 'SLiB >>> Shutting down Browser Pro...'
    
    if '2017' not in SLiB.gib('mayaVersion'):
        if cmds.dockControl('slBrowserDock', q=1, ex=1):
            cmds.deleteUI('slBrowserDock')
    else:
        if cmds.workspaceControl(WorkspaceName, ex=1):
            cmds.deleteUI(WorkspaceName)
            
    print 'Bye Bye!'
    
#BROWSER UI
def SLiBBrowserUI():
    #WRITE PERMISSION CHECK
    try:
        os.mkdir(SLiB_lib + '/' +  'Writable')
        cmds.sysFile(SLiB_lib + '/' +  'Writable', red=1)
    except:
        cmds.confirmDialog(m='Could not write to specified Library folder: \n' + SLiB_lib + '\nEither change your permissions or run Maya as Administrator')
        sys.exit()
        
    if cmds.dockControl('slBrowserDock', q=1, ex=1):
        cmds.deleteUI('slBrowserDock')

    if '2017' not in SLiB.gib('mayaVersion'):
        if cmds.window('SLiBBrowserUI', q=1, ex=1):
            cmds.deleteUI('SLiBBrowserUI')
            
        global slBrowserUI
        slBrowserUI = cmds.loadUI(f=SLiB_gui + 'SLiBBrowser.ui')
        
    cmds.window('SLiBBrowserUI', e=1, t='Browser Pro 2.0', te=500, le=500)
    
    #Menu Bar
    cmds.menuBarLayout('slMenuBar', h=20, p='slib_menubar_layout')
    
    cmds.menu(l='File', allowOptionBoxes=0, p='slMenuBar')
    cmds.menuItem('Load', l='Load Shader Test Scene...', c=lambda *args: SLiB_LoadTestRoom())
    
    if not '2017' in SLiB.gib('mayaVersion'):
        cmds.menuItem(d=1)
        cmds.menuItem('dockMenu', l='Dock Browser Window', cb=0, c=lambda *args: SLiB.dockUI())
    
    cmds.menuItem(d=1)
    cmds.menuItem('QuickDelete', l='Delete Confirmation ', cb=0, ann=' Deletes selected Item(s) without showing Confirm Dialog ')
    cmds.menuItem(d=1)
    cmds.menuItem('AutoRepath', l='Auto Repath Textures', cb=1, ann=' automatically relinks path of exported, renamed or moved Item(s) to new location [ opens new scene ] ')
    cmds.menuItem(d=1)
    cmds.menuItem('Save', l='Save Settings', c=lambda *args: SLiB.saveSettings())
    
    cmds.menu('Import', l='Import', allowOptionBoxes=1, p='slMenuBar')
    cmds.menuItem('importREF', l='as Reference', cb=0)
    cmds.menuItem(d=1)
    cmds.menuItem('ReUseAsset', l='Reuse Existing Asset', cb=1)

    cmds.radioMenuItemCollection('ReuseAssetOptions')
    cmds.menuItem('ReUseDuplicate', l='  Duplicate', rb=0)
    cmds.menuItem('ReUseInstance', l='  Instance', rb=1)
    cmds.menuItem(d=1)
    cmds.menuItem('ReUseShader', l='Reuse Existing Shader', cb=1)
    cmds.menuItem(d=1)
    #cmds.menuItem('AutoREL', l='Auto REL > ABS', cb=1)
    #cmds.menuItem(d=1)
    cmds.menuItem('CopyToProjectFolder', l='Copy TEX to Project Folder', cb=0, ann='automatically copies Textures of imported Item(s) to current Project Folder')

    cmds.menu('Tools', l='Tools', allowOptionBoxes=0, p='slMenuBar')
    cmds.menuItem('Metarize', l='Metarize', c=lambda *args: SLiB_Metarize(), ann='Create Meta file for Items stored with Browser Pro 1.4 or lower')
    cmds.menuItem(d=1)
    cmds.menuItem('SNR', l='Shading Network Renamer', c=lambda *args: SLiB.SNRenamer() )
    cmds.menuItem('EditDic', l='Edit Dictionary', c=lambda *args: webbrowser.open(SLiB_dir +'set/SNR_Dictionary.txt'))
    cmds.menuItem(d=1)
    cmds.menuItem('slunzipper', l='Load from zip...', c=lambda *args: SLiB_Unzipper())
    cmds.menuItem('slDownloader', l='Load from Store...', c=lambda *args: SLiB_Downloader())
    cmds.menuItem(d=1)
    cmds.menuItem('slConverter', l='vRayMAT to rsMAT (Alpha)', c=lambda *args: SLiB_Converter())
    
    cmds.menu('View', l='View', allowOptionBoxes=1, p='slMenuBar')
    cmds.menuItem('slSnapshotCam', l='Snapshot Framing', c=lambda *args: SLiB.snapshotCam(), cb=0)
    cmds.menuItem(d=1)
    cmds.menuItem('iconToolbar', l='Icon Toolbar', cb=1, c=lambda *args: SLiB_IconToolBar())
    cmds.menuItem(d=1)
    cmds.menuItem('slmetathumbs', l='Thumb Meta Overlay', c=lambda *args: SLiB_UpdateView(), cb=0)
    cmds.menuItem(d=1)
    cmds.menuItem('slfolderthumbs', l='Show Folder Thumbs', c=lambda *args: SLiB_UpdateView(), cb=1)
    cmds.menuItem(d=1)
    cmds.menuItem('slHyperShadeThumbs', l='Disable Thumbs in Hypershade', c=lambda *args: SLiB.hypershadeThumbs(), cb=0)
    
    cmds.menu('menuRenderer', l='Renderer', pmc=lambda *args: SLiB_listRenderers(), p='slMenuBar')

    cmds.menu('Help', l='Help', allowOptionBoxes=1, p='slMenuBar')
    cmds.menuItem('toolShortcut', l='Tool Shortcuts', cb=1)
    cmds.menuItem(d=1)
    cmds.menuItem('manual', l='User Manual', c=lambda *args: SLiB.UserManual())
    cmds.menuItem('about', l='About...', c=lambda *args: SLiB_About())
    
    #SPLITTER
    slSplitter = wrapInstance(long(omui.MQtUtil.findControl('slSplitter')), QtWidgets.QSplitter)
    slSplitter.setSizes([155, 4000])
        
    #MAIN TOOLS LAYOUT
    cmds.layout('slib_toolbar', e=1, vis=0)
    cmds.iconTextButton('importNormal', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_importnormal.png', c=lambda *args: SLiB_Import('Normal'), p='slib_tools_layout', ann=' Import ')
    cmds.iconTextButton('importPlace', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_importplace.png', c=lambda *args: SLiB_Import('Place'), p='slib_tools_layout', ann=' Import and Place Object(s) ')
    cmds.iconTextButton('importReplace', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_importreplace.png', c=lambda *args: SLiB_Import('Replace'), p='slib_tools_layout', ann=' Import and Replace Object(s) ')
    cmds.iconTextButton('openMaya', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_openmaya.png', c=lambda *args: SLiB_OpenInMaya(), p='slib_tools_layout', ann=' Open in Maya ')
    cmds.iconTextButton('openFileBrowser', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_openfilebrowser.png', c=lambda *args: SLiB_OpenInFileBrowser(), p='slib_tools_layout', ann=' Open in File Browser ')
    cmds.iconTextButton('duplicate', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_duplicate.png', c=lambda *args: SLiB_BrowserDuplicate(), p='slib_tools_layout', ann=' Duplicate ')
    cmds.iconTextButton('rename', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_rename.png', c=lambda *args: SLiB_BrowserRename(), p='slib_tools_layout', ann=' Rename ')
    cmds.iconTextButton('copy', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_copy.png', c=lambda *args: SLiB_BrowserCopy(), p='slib_tools_layout', ann=' Copy ')
    cmds.iconTextButton('paste', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_paste.png', c=lambda *args: SLiB_BrowserPaste(), p='slib_tools_layout', ann=' Paste ')
    cmds.iconTextButton('delete', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_del.png', c=lambda *args: SLiB_BrowserDelete(), p='slib_tools_layout', ann=' Delete ')
    #cmds.iconTextButton('STORE', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_cgfront.png', c=lambda *args: SLiB_Downloader(), p='slib_tools_layout', ann=' Load from Store ')
    
    cmds.iconTextButton('importPlace', e=1, en=0)
    cmds.iconTextButton('importReplace', e=1, en=0)

    #SHADER TOOLS LAYOUT
    cmds.layout('shader_tools', e=1, vis=1)
    cmds.iconTextCheckBox('matPicker', mw=0, mh=0, w=32, h=32, onc=lambda *args: SLiB_MatPicker('on'), ofc=lambda *args: SLiB_MatPicker('off'), i=SLiB_img+'slib_matpicker_off.png', si=SLiB_img+'slib_matpicker_on.png', ann=' MAT Picker ', p='shader_tools')
    cmds.iconTextButton('delUnused', mw=0, mh=0, w=32, h=32, c=lambda *args: mel.eval('MLdeleteUnused;'), i=SLiB_img+'slib_delunused.png', ann=' delete unused Nodes ', p='shader_tools')

    #OBJECTS TOOLS LAYOUT
    cmds.layout('objects_tools', e=1, vis=0)
    cmds.iconTextCheckBox('ipt', mw=0, mh=0, w=32, h=32, onc=lambda *args: SLiB_iptOn(), ofc=lambda *args: SLiB_iptOff(), i=SLiB_img+'slib_ipt_off.png', si=SLiB_img+'slib_ipt_on.png', ann=' IPT ON /OFF ', p='objects_tools')
    cmds.popupMenu(parent='ipt', ctl=0, button=3)
    cmds.menuItem('keepRotation', l='Keep Rotation', cb=0)
    cmds.menuItem('keepScale', l='Keep Scale', cb=0)
    cmds.iconTextButton('freezeTrans', mw=0, mh=0, w=32, h=32, c=lambda *args: SLiB.freeze(), i=SLiB_img+'slib_freezetransform.png', ann=' Freeze Transformations ', p='objects_tools')
    cmds.iconTextButton('autoPlacePivot', mw=0, mh=0, w=32, h=32, c=lambda *args: SLiB.autoPlacePivot(), i=SLiB_img+'slib_autoplacepivot.png', ann=' Move Object to Origin and Pivot to Bottom ', p='objects_tools')
    cmds.iconTextButton('findSimilar', mw=0, mh=0, w=32, h=32, c=lambda *args: SLiB.findSimilar(), i=SLiB_img+'slib_similar.png', ann=' Find similar objects ', p='objects_tools')

    #LIGHTS TOOLS LAYOUT
    cmds.layout('lights_tools', e=1, vis=0)
    
    #HDRI TOOLS LAYOUT
    cmds.layout('hdri_tools', e=1, vis=0)
    cmds.iconTextButton(w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_photoshop.png', c=lambda *args: SLiB_OpenInPhotoshop(), p='hdri_tools', ann=' Send HDRI(s) to Photoshop ')
    cmds.iconTextButton(w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_rotdome.png', c=lambda *args: SLiB_DomeRot(), p='hdri_tools', ann=' Rotate SLiB Dome ')
    cmds.iconTextButton(w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_deldome.png', c=lambda *args: SLiB_DelDome(), p='hdri_tools', ann=' Delete SLiB Dome ')

    #TEXTURE TOOLS LAYOUT
    cmds.layout('textures_tools', e=1, vis=0)
    cmds.iconTextButton(w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_importfolder.png', c=lambda *args: SLiB_ExportTextures('folder'), p='textures_tools', ann=' Export Texture(s) from folder ')
    cmds.iconTextButton(w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_photoshop.png', c=lambda *args: SLiB_OpenInPhotoshop(), p='textures_tools', ann=' Send Texture(s) to Photoshop ')

    #PATH TOOLS LAYOUT
    cmds.layout('paths_tools', e=1, vis=0)
    cmds.iconTextButton(l='ABS > REL', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_relative.png', c=lambda *args: SLiB_ABStoREL(), p='paths_tools', ann=' convert ABSOLUTE path to RELATIVE ')
    cmds.iconTextButton(l='REL > ABS', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_absolute.png', c=lambda *args: SLiB_RELtoABS(), p='paths_tools', ann=' convert RELATIVE path to ABSOLUTE ')
    cmds.iconTextButton(l='>> Folder', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_copytofolder.png', c=lambda *args: SLiB_CopyTexturesTo('folder'), p='paths_tools', ann=' copy Texture(s) to Folder ')
    cmds.iconTextButton(l='Find Missing', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_findtextures.png', c=lambda *args: SLiB_FindMissingTextures(), p='paths_tools', ann=' find missing Texture(s) ')
    cmds.iconTextButton(l='Relink', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_relink.png', c=lambda *args: SLiB_RelinkTextures(), p='paths_tools', ann=' Relink to Folder ')

    cmds.iconTextButton('SLiBRefresh', mw=0, mh=0, w=32, h=32, i=SLiB_img + 'slib_refresh.png', c=lambda *args: SLiB_UpdateView(), ann=' Refresh Previews ', p='SLiB_BUTTON_Refresh')
    cmds.textField('SLiB_CBOX_Resolution', e=1, cc=lambda *args: SLiB_UpdateView())
    cmds.popupMenu(parent='SLiB_CBOX_Resolution', ctl=0, button=3)
    cmds.menuItem(l='64', c=lambda *args: (cmds.textField('SLiB_CBOX_Resolution', e=1, tx='64'), SLiB_UpdateView()))
    cmds.menuItem(l='96', c=lambda *args: (cmds.textField('SLiB_CBOX_Resolution', e=1, tx='96'), SLiB_UpdateView()))
    cmds.menuItem(l='128', c=lambda *args: (cmds.textField('SLiB_CBOX_Resolution', e=1, tx='128'), SLiB_UpdateView()))
    cmds.menuItem(l='196', c=lambda *args: (cmds.textField('SLiB_CBOX_Resolution', e=1, tx='196'), SLiB_UpdateView()))
    cmds.menuItem(l='256', c=lambda *args: (cmds.textField('SLiB_CBOX_Resolution', e=1, tx='256'), SLiB_UpdateView()))
    cmds.menuItem(l='384', c=lambda *args: (cmds.textField('SLiB_CBOX_Resolution', e=1, tx='384'), SLiB_UpdateView()))
    cmds.menuItem(l='512', c=lambda *args: (cmds.textField('SLiB_CBOX_Resolution', e=1, tx='512'), SLiB_UpdateView()))
    
    cmds.popupMenu(parent='SLiB_TEXTFIELD_Name', ctl=0, button=3)
    cmds.menuItem(l='Take from Asset', c=lambda *args: SLiB_NameFrom('asset'))
    cmds.menuItem(l='Take from Selected', c=lambda *args: SLiB_NameFrom('selection'))
    cmds.menuItem(l='Cast to Shader Name', c=lambda *args: SLiB.SNRSpeed())
    cmds.menuItem(d=1)
    cmds.menuItem(l='Cast Selected to Shader Name', c=lambda *args: (SLiB_NameFrom('selection'), SLiB.SNRSpeed()))
    
    cmds.popupMenu(parent='SLiB_TEXTFIELD_Info', ctl=0, button=3)
    cmds.menuItem(l='Save Notes', c=lambda *args:  SLiB_ReplaceNotes())
    cmds.menuItem(d=1)
    cmds.menuItem(l='Clear Notes', c=lambda *args: (cmds.scrollField('SLiB_TEXTFIELD_Info', e=1, tx=''), SLiB_ReplaceNotes()))
    
    cmds.iconTextCheckBox('searchSwitch', mw=0, mh=0, w=32, h=32, i=SLiB_img + 'slib_search_off.png', si=SLiB_img + 'slib_search_on.png', onc=lambda *args: SLiB_Search('on'), ofc=lambda *args: SLiB_Search('off'), p='SLiB_BUTTON_Search')
    cmds.textField('SLiB_TEXTFIELD_Search', e=1, cc=lambda *args: SLiB_Search('on'), ec=lambda *args: SLiB_Search('on'), aie=1)
    cmds.popupMenu(parent='SLiB_TEXTFIELD_Search', ctl=0, button=3)
    cmds.menuItem(l='Clear', c=lambda *args: SLiB_Search('off'))
    cmds.iconTextCheckBox('tagSwitch', mw=0, mh=0, w=32, h=32, i=SLiB_img + 'slib_tag_off.png', si=SLiB_img + 'slib_tag_on.png', p='SLiB_BUTTON_Tag', ann=' search using TAGS ')

    cmds.layout('SLiB_export_path', e=1, vis=0)

    cmds.optionMenu('ExportOptions', p='slib_ext_OB')
    cmds.menuItem(l='MB')
    cmds.menuItem(l='MA')
    
    cmds.optionMenu('TexPathMode', p='slib_path_OB')
    cmds.menuItem(l='REL')
    cmds.menuItem(l='ABS')
    
    cmds.checkBox('exportHIS', l='DH', v=1, p='SLiB_export_pre', ann='DELETE HISTORY before export')
    cmds.checkBox('exportFRZ', l='FT', v=1, p='SLiB_export_pre', ann='FREEZE TRANSFORMATIONS before export')
    cmds.checkBox('exportPIV', l='OS', v=1, p='SLiB_export_pre', ann='SNAP PIVOT TO ORIGIN before export')
    
    cmds.optionMenu('sl_OB_library', cc=lambda *args: SLiB_SwitchLib(), p='slib_library_OB')
    SLiB_FillLib()
    
    cmds.optionMenu('exportTEX', cc=lambda *args: SLiB_SwitchTextures(), p='slib_Textures')
    for e in ['no Textures', 'with Textures', 'with custom Texture Folder']:
        cmds.menuItem(l=e)
    cmds.optionMenu('exportTEX', e=1, v='with Textures')
    cmds.iconTextButton(l='exportCUS', w=32, h=20, mh=0, mw=0, i=SLiB_img + 'slib_library.png', c=lambda *args: SLiB_CustomTexFolder(), p='slib_cusFoldeBtn_layout', ann=' Select custom Texture Folder ')

    cmds.optionMenu('meta_version', p='slib_version_OB')
    for e in ['2015', '2016', '2016.5', '2017']:
        cmds.menuItem(l=e.upper())
    
    cmds.menuItem(l='N/A')
    
    #META MAYA
    if '15' in SLiB.gib('mayaVersion'):
        cmds.optionMenu('meta_version', e=1, v='2015')
    if '2016' in SLiB.gib('mayaVersion'):
        if not '5' in SLiB.gib('mayaVersion') and not 'Extension 2' in SLiB.gib('mayaVersion'):
            cmds.optionMenu('meta_version', e=1, v='2016')
        else:
            cmds.optionMenu('meta_version', e=1, v='2016.5')
    if '17' in SLiB.gib('mayaVersion'):
        cmds.optionMenu('meta_version', e=1, v='2017')
    cmds.popupMenu(parent='meta_version', ctl=0, button=3)
    cmds.menuItem(l='update MAYA', c=lambda *args:  SLiB_UpdateMeta('version'))

    #META REND
    cmds.optionMenu('meta_renderer', p='slib_renderer_OB')
    for e in ['arnold', 'mayasoftware', 'mayahardware', 'mayahardware2', 'mentalray' , 'redshift', 'vray', ]:
        cmds.menuItem(l=e.upper())
    cmds.menuItem(l='N/A')
    cmds.optionMenu('meta_renderer', e=1, v=SLiB.gib('renderer').upper())
    cmds.popupMenu(parent='meta_renderer', ctl=0, button=3)
    cmds.menuItem(l='update REND', c=lambda *args:  SLiB_UpdateMeta('renderer'))

    #META LOCK
    cmds.optionMenu('meta_locked', p='slib_locked_OB')
    for e in ['yes', 'no']:
        cmds.menuItem(l=e.upper())
    cmds.optionMenu('meta_locked', e=1, v='NO')
    cmds.popupMenu(parent='meta_locked', ctl=0, button=3)
    cmds.menuItem(l='update LOCK', c=lambda *args:  SLiB_UpdateMeta('locked'))

    #META TAGS
    cmds.textField('SLiB_TEXTFIELD_Tags', e=1, ann=' separate Tags by spaces')
    cmds.popupMenu(parent='SLiB_TEXTFIELD_Tags', ctl=0, button=3)
    cmds.menuItem(l='update TAGS', c=lambda *args:  SLiB_UpdateMeta('tags'))
    
    #META USER
    cmds.popupMenu(parent='SLiB_TEXTFIELD_User', ctl=0, button=3)
    cmds.menuItem(l='update USER', c=lambda *args:  SLiB_UpdateMeta('user'))

    cmds.iconTextRadioCollection( 'mainCatCollection', p='SLiBBrowserUI')
    cmds.iconTextRadioButton('SHADER', l='SHADER', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_type_shader_off.png', si=SLiB_img + 'slib_type_shader_on.png',  p='SLiB_AssetType', onc=lambda *args: SLiB_ChangeType(), ann=' SHADER ')
    cmds.iconTextRadioButton('OBJECTS', l='OBJECTS', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_type_objects_off.png', si=SLiB_img + 'slib_type_objects_on.png', p='SLiB_AssetType', onc=lambda *args: SLiB_ChangeType(), ann=' OBJECTS ')
    cmds.iconTextRadioButton('LIGHTS', l='LIGHTS', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_type_lights_off.png', si=SLiB_img + 'slib_type_lights_on.png', p='SLiB_AssetType', onc=lambda *args: SLiB_ChangeType(), ann=' LIGHTS ')
    cmds.iconTextRadioButton('HDRI', l='HDRI', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_type_hdri_off.png', si=SLiB_img + 'slib_type_hdri_on.png', p='SLiB_AssetType', onc=lambda *args: SLiB_ChangeType(), ann=' HDRI ')
    cmds.iconTextRadioButton('TEXTURES', l='TEXTURES', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_type_textures_off.png', si=SLiB_img + 'slib_type_textures_on.png', p='SLiB_AssetType', onc=lambda *args: SLiB_ChangeType(), ann=' TEXTURES ')
    cmds.iconTextRadioButton('PATHS', l='PATHS', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_type_paths_off.png', si=SLiB_img + 'slib_type_paths_on.png', p='SLiB_AssetType', onc=lambda *args: SLiB_ChangeType(), ann=' PATHS ')
    cmds.iconTextRadioButton('SHADER', e=1, sl=1)
    
    cmds.iconTextButton('LIBRARY', w=32, h=20, mh=0, mw=0, i=SLiB_img + 'slib_library.png', c=lambda *args: SLiB_AddLib(), p='lib_layout', ann=' add new Library ')
    cmds.popupMenu('popupLib', parent='LIBRARY', ctl=0, button=3)
    cmds.menuItem(l='Remove Library', c=lambda *args: SLiB_RemoveLib())
    cmds.menuItem(d=1)
    cmds.menuItem(l='Edit Libraries', c=lambda *args: SLiB_EditLibraries())

    cmds.iconTextButton('SLiB_BUTTON_CreatePreview', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_createpreview.png', c=lambda *args: SLiB_CreatePreview(), p='SLiB_RenderButtonLayout01', ann=' Generate Preview Image ')
    SLiB.renderPreviewPop()
    
    cmds.iconTextButton('SLiB_BUTTON_Render', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_render.png', c=lambda *args: (SLiB_OverlayImage(SLiB_img + 'browser_rendering.png'), SLiB_Render()), dcc=lambda *args: SLiB_ToggleSnapshotCam(), p='SLiB_RenderButtonLayout02', ann=' Render Preview Image ')
    cmds.iconTextButton('slPlayblast', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_playblast.png', c=lambda *args: SLiB_PlayBlast(), dcc=lambda *args: SLiB_ToggleSnapshotCam(), p='SLiB_RenderButtonLayout03', ann=' Snapshot ')
    
    cmds.iconTextButton('slfromRV', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_renderview.png', c=lambda *args: SLiB_LoadFromRV(), p='SLiB_RenderButtonLayout04', ann=' Grab Preview Image from RenderView ')
    cmds.iconTextButton('slfromFile', w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_fileload.png', c=lambda *args: SLiB_LoadFromFile(), p='SLiB_RenderButtonLayout05', ann=' Load Preview Image from Disk ')
    cmds.iconTextCheckBox('RVLocked', w=32, h=32, mh=0, mw=0, v=0, i=SLiB_img + 'slib_unlocked.png', si=SLiB_img + 'slib_locked.png', p='SLiB_RenderLockLayout', ann=' Lock Preview Image ')

    global SLiBThumbsLayout
    SLiBThumbsLayout = wrapInstance(long(omui.MQtUtil.findLayout('SLiB_thumbsframe')), QtWidgets.QWidget)
    global SLiBThumbsScrollLayout
    SLiBThumbsScrollLayout = SLiBThumbsLayout.children()[0]
    global RenderViewHolder
    RenderViewHolder = wrapInstance(long(omui.MQtUtil.findLayout('PrevLayout')), QtWidgets.QWidget)
    
    if '2017' not in SLiB.gib('mayaVersion'):
        cmds.showWindow('SLiBBrowserUI')

    SLiB_SwitchExportButton()

    SLiB_BuildTree()
    SLiB_LoadCats()
    player = MoviePlayer() 
    player.show()
    
    try:
        cmds.evalDeferred(lambda: SLiB.loadSettings())
    except:
        cmds.warning('Failed on loading Browser PRO Settings! Please try to save them again.')
    
    cmds.scriptJob(e=['quitApplication', SLiBQuit])
    
    SLiB.messager('Browser PRO v2.0 loaded', 'green')

    print 'SLiB >>> Browser PRO v2.0 loaded'

def SLiB_listRenderers():
    cmds.menu('menuRenderer', e=1, dai=1)
    cmds.radioMenuItemCollection('Renderer', p='menuRenderer')
    for r in cmds.renderer(q=1, ava=1):
        cmds.menuItem(r, l=r, c=partial(SLiB.setRenderer, r), rb=0, p='menuRenderer')
    cmds.menuItem(cmds.getAttr('defaultRenderGlobals.currentRenderer'), e=1, rb=1)

def SLiB_ToggleSnapshotCam():
    if cmds.menuItem('slSnapshotCam', q=1, cb=1):
        cmds.menuItem('slSnapshotCam', e=1, cb=0)
    else:
        cmds.menuItem('slSnapshotCam', e=1, cb=1)
    SLiB.snapshotCam()

def SLiB_IconToolBar():
    if cmds.menuItem('iconToolbar', q=1, cb=1):
        if SLiB.gib('mainCat') != 'paths':
            cmds.layout('slib_toolbar', e=1, vis=1)
    else:
        cmds.layout('slib_toolbar', e=1, vis=0)

def SLiB_BuildTree():
    cmds.setFocus('SLiB_TEXTFIELD_Name')
    if cmds.formLayout('treeLayout', ex=1):
        cmds.deleteUI('treeLayout')
        
    if SLiB.gib('mainCat') != 'paths': 
        treeLayout = cmds.formLayout('treeLayout', p='CatLayout')
        treeControl = cmds.treeView('treeView', p='treeLayout', arp=0, enk=1, irc=lambda *args: SLiB_RefreshTree())

        cmds.formLayout(treeLayout, e=True, attachForm=[(treeControl,'top', 2), (treeControl,'left', 2), (treeControl,'bottom', 2), (treeControl,'right', 2)])
        
        libPath = os.path.normpath(os.path.join(mel.eval('getenv SLiBRARY;'), cmds.iconTextRadioCollection('mainCatCollection', q=1, sl=1).lower()))
        library = os.path.basename(mel.eval('getenv SLiBRARY'))
        
        cmds.treeView('treeView', e=1, addItem=(libPath, ''))
        cmds.treeView('treeView', e=1, dl=(libPath, 'ROOT'))
        cmds.popupMenu(p='treeView', ctl=False, button=3)
        cmds.menuItem(l='Refresh', c=lambda *args: SLiB_RefreshTree())
        cmds.menuItem(d=1)
        cmds.menuItem(l='New Category', c=lambda *args: SLiB_CreateDir())
        cmds.menuItem(l='Open in File Browser', c=lambda *args: SLiB_OpenCatInFileBrowser())
        cmds.menuItem(d=1)
        cmds.menuItem(l='Remove Category', c=lambda *args: SLiB_RemoveDir())
        
        for r in next(os.walk(libPath))[1]:
            if r == '.DS_Store':
                pass
            else:
                r = os.path.normpath(libPath + '/' + r)

                cmds.treeView('treeView', e=1, addItem=(r, ''), scc=lambda *args: SLiB_Expand())
                cmds.treeView('treeView', e=1, dl=(r, os.path.basename(r)))
                cmds.treeView('treeView', e=1, ei=(r, 0))
                
                if not os.path.isdir(os.path.join(r, '_SUB')):
                    cmds.sysFile(os.path.join(r, '_SUB'), makeDir=1 )

                if '_SUB' in next(os.walk(r))[1]:
                    parent = os.path.join(str(r), '_SUB')
                    SLiB_populateTreeView('treeView', parent, r)

def SLiB_populateTreeView(treeControl, parent, parentname):
    children = next(os.walk(parent))[1]
    for child in children:
        if child == '.DS_Store':
            pass
        else:
            child = os.path.normpath(os.path.join(parent, child))
            cmds.treeView('treeView', e=1, addItem=(child, parentname), scc=lambda *args: SLiB_Expand())
            cmds.treeView('treeView', e=1, bgc=[0,0,0], lbc=[child,0,0,0], dl=(child, os.path.basename(child)))
            
            if not os.path.isdir(os.path.join(child, '_SUB')):
                cmds.sysFile(os.path.join(child, '_SUB'), makeDir=1 )

            for c in os.listdir(child):
                if '_SUB' in c:
                    childParent = os.path.join(child, '_SUB')
                    SLiB_populateTreeView(treeControl, childParent, child)

def SLiB_Expand():
    try:
        cat = cmds.treeView('treeView', q=1, si=1)[0]
        if cmds.treeView('treeView', q=1, iie=cat):
            cmds.treeView('treeView', e=1, ei=(cat, 0))
        else:
            cmds.treeView('treeView', e=1, ei=(cat, 1))
        SLiB_UpdateView()
    except:
        pass

def SLiB_ChangeType():
    for l in ['shader_tools', 'objects_tools','lights_tools', 'hdri_tools','textures_tools', 'paths_tools']:
        cmds.layout(l, e=1, vis=0)
        cmds.layout('slib_toolbar', e=1, vis=0)
        cmds.iconTextButton('importPlace', e=1, en=1)
        cmds.iconTextButton('importReplace', e=1, en=1)
        cmds.iconTextButton('openMaya', e=1, en=1)
        
        if cmds.menuItem('iconToolbar', q=1, cb=1): 
            cmds.layout('slib_toolbar', e=1, vis=1)
            
    if SLiB.gib('mainCat') in ['shader', 'objects']:
        cmds.iconTextButton('SLiB_BUTTON_CreatePreview', e=1, c=lambda *args: SLiB_CreatePreview())
    else:
        cmds.iconTextButton('SLiB_BUTTON_CreatePreview', e=1, c=lambda *args: SLiB.messager('Only working for Shader or Objects', 'yellow'))
        
    SLiB.renderPreviewPop()
    
    if cmds.optionMenu('ExportOptions', ex=1): #script job attached
        cmds.deleteUI('ExportOptions')
    
    cmds.optionMenu('ExportOptions', p='slib_ext_OB')
    cmds.menuItem(l='MB')
    cmds.menuItem(l='MA')
    if SLiB.gib('mainCat') == 'objects':
        cmds.menuItem(l='OBJ')
    
    cmds.layout(SLiB.gib('mainCat') + '_tools', e=1, vis=1)
    
    if SLiB.gib('mainCat') in ['shader', 'textures', 'hdri']:
        cmds.iconTextButton('importPlace', e=1, en=0)
        cmds.iconTextButton('importReplace', e=1, en=0)
        
    if SLiB.gib('mainCat') in ['textures', 'hdri']:
        cmds.iconTextButton('importNormal', e=1, c=lambda *args: SLiB_Import('Texture'))
        cmds.iconTextButton('openMaya', e=1, en=0)
    else:
        cmds.iconTextButton('importNormal', e=1, c=lambda *args: SLiB_Import('Normal'))
        
    if SLiBThumbsScrollLayout: 
        SLiB_ClearLayout(SLiBThumbsScrollLayout)

    SLiB.messager('', 'none')
    
    SLiB_BuildTree()
    
    if cmds.optionVar(q=('latest_' + SLiB.gib('mainCat') + '_Cat')):
        SLiB_LoadCats()
        
    if SLiB.gib('mainCat') == 'paths':
        cmds.layout('slib_toolbar', e=1, vis=0)
         
        pathsJob = cmds.scriptJob(e=["SelectionChanged", SLiB_UpdateView], p='ExportOptions')
        
        SLiB_UpdateView()
        
    SLiB_SwitchExportButton()

def SLiB_RefreshTree():
    cmds.evalDeferred(lambda: SLiB_BuildTree())

def SLiB_Search(x):
    if x == 'on':
        if len(cmds.textField('SLiB_TEXTFIELD_Search', q=1, tx=1)) != 0:
            cmds.iconTextCheckBox('searchSwitch', e=1, v=1)
    if x == 'off':
        cmds.textField('SLiB_TEXTFIELD_Search', e=1, tx='')
        cmds.iconTextCheckBox('searchSwitch', e=1, v=0)
    
    SLiB_UpdateView()

def SLiB_SaveCats():
    if cmds.treeView('treeView', q=1, ch=1) != None:
        cmds.optionVar(sv=('latest_' + SLiB.gib('mainCat') + '_Cat', SLiB.gib('currLocation'))) 

def SLiB_LoadCats():
    if SLiB.gib('mainCat') != 'paths':
        cmds.treeView('treeView', e=1, cs=1)
        try:
            def expandParent(itemParent):
                cmds.treeView('treeView', e=1, ei=(itemParent, 1))
                while cmds.treeView('treeView', q=1, ip=itemParent):
                    itemParent = cmds.treeView('treeView', q=1, ip=itemParent)
                    expandParent(itemParent)
            
            treeItem = os.path.normpath(cmds.optionVar(q=('latest_' + SLiB.gib('mainCat') + '_Cat')))
            cmds.treeView('treeView', e=1, ei=(treeItem, 1))
            itemParent = cmds.treeView('treeView', q=1, ip=treeItem)
            if itemParent:
                expandParent(itemParent)
                
            itemParent = cmds.treeView('treeView', e=1, si=(treeItem, 1))
            SLiB_UpdateView()

        except:
            pass

def SLiB_CreateDir():
    parent = cmds.treeView('treeView', q=1, si=1)
    if parent:
        parent = parent[0]
        result = cmds.promptDialog(t='Create New Category', m='Enter Name:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
        if result == 'OK':
                newDirName = cmds.promptDialog(q=1, t=1).replace(' ','_')
                
                if SLiB.gib('currLocation') == os.path.normpath(mel.eval('getenv SLiBRARY;') + SLiB.gib('mainCat')):
                    newDir = os.path.normpath(mel.eval('getenv SLiBRARY;') + SLiB.gib('mainCat') + '/' + newDirName)
                else:
                    newDir = os.path.normpath(SLiB.gib('currLocation') + '/_SUB/' + newDirName)
                
                if os.path.isdir(newDir) == 1:
                    SLiB.messager('Category already exists!', 'red')
                    sys.exit()
                
                else:
                    cmds.sysFile(newDir, makeDir=1 )
                    cmds.sysFile(os.path.join(newDir, '_SUB'), makeDir=1 )
                    cmds.evalDeferred(lambda: SLiB_BuildTree())
                    cmds.evalDeferred(lambda: cmds.treeView('treeView', e=1, cs=1))
                    cmds.evalDeferred(lambda: cmds.treeView('treeView', e=1, si=(parent, 1)))
                    cmds.evalDeferred(lambda: cmds.treeView('treeView', e=1, shi=parent))
                    #cmds.evalDeferred(lambda: cmds.treeView('treeView', e=1, cs=1))
                    #cmds.evalDeferred(lambda: cmds.treeView('treeView', e=1, si=(newDir, 1)))
                    #cmds.evalDeferred(lambda: cmds.treeView('treeView', e=1, shi=newDir))
                    cmds.evalDeferred(lambda: SLiB_UpdateView())
                    cmds.evalDeferred(lambda: SLiB.messager('Cat < ' + str(newDirName) + ' > created.', 'green'))
                    cmds.evalDeferred(lambda: cmds.treeView('treeView', e=1, ei=(parent, 1)))
    else:
        SLiB.messager('Please select ROOT to add a new Category or an existing Category to add a Sub-Category!', 'yellow')

def SLiB_RemoveDir():
    if SLiB.gib('currLocation'):
        if SLiB.gib('currLocation') == os.path.normpath(mel.eval('getenv SLiBRARY;') + SLiB.gib('mainCat')):
            SLiB.messager('ROOT is not deletable!', 'red')
        else:
            deleteDir = SLiB.gib('currLocation')
            parentDir = os.path.normpath(cmds.treeView('treeView', q=1, ip=deleteDir))

            subs = []
            for root, dirs, files in os.walk(deleteDir, topdown=0):
                for name in dirs:
                    if name != '_SUB':
                        subs.append(name)

            if len(subs) > 0:
                answer = cmds.confirmDialog(t='Warning', m='Category contains Files and/or Subcategories! \nDo you wish to proceed?', button=['Delete','No'], defaultButton='Delete', cancelButton='No', dismissString='No' )
                if answer != 'Delete':
                    sys.exit()
            
            shutil.rmtree(deleteDir, ignore_errors=1)
            if parentDir != '.':
                cmds.treeView('treeView', e=1, cs=1)
                cmds.treeView('treeView', e=1, si=(parentDir, 1))
                cmds.treeView('treeView', e=1, shi=parentDir)
            
            SLiB_OverlayImage(SLiB_img + 'browser_logo.png')
            
            parent = cmds.treeView('treeView', q=1, ip=deleteDir)
            cmds.evalDeferred(lambda: SLiB_RemoveDirPost(parent))
            
            cmds.evalDeferred(lambda: SLiB.messager('Cat < ' + os.path.basename(deleteDir) + ' > removed.', 'green'))
            cmds.evalDeferred(lambda: SLiB_UpdateView())

    else:
        SLiB.messager('Please select the Category you want to remove!', 'yellow')
        sys.exit()
        
def SLiB_RemoveDirPost(parent):
    SLiB_BuildTree()
    if parent:
        root = parent
    else:
        root = os.path.normpath(os.path.join(SLiB.gib('library'), SLiB.gib('mainCat')))
    cmds.treeView('treeView', e=1, cs=1)
    cmds.treeView('treeView', e=1, si=(root, 1))
    cmds.treeView('treeView', e=1, ei=(root, 1))
    SLiB_UpdateView()

def SLiB_CreatePreview():
    errorList = []
    if cbxList:
        for e in cbxList:
            meta = os.path.splitext(e)[0] + '.meta'
            if os.path.isfile(meta):
                lines = [line.rstrip('\n') for line in open(meta)]
                renderer = lines[5].lower()
                if not renderer in ['arnold', 'mentalray', 'redshift', 'vray']:
                    SLiB.messager('Render Engine not supported for [ ' + os.path.basename(e) + ' ]', 'yellow')
                    print 'Render Engine not supported for [ ' + os.path.basename(e) + ' ]'
                    cbxList.remove(e)
                    errorList.append(e)

            else:
                SLiB.messager('Meta data not found for [ ' + os.path.basename(e) + ' ] - please Metarize item.', 'yellow')
                print 'Meta data not found for [ ' + os.path.basename(e) + ' ] - please Metarize item.'
                cbxList.remove(e)
                errorList.append(e)
    
    if cbxList:
        previewCat = SLiB.gib('currLocation')
        mode = None
        cam = None
        
        if SLiB.gib('mainCat') == 'shader':
            type = 'mat'
            
            if cmds.menuItem('slPreview_Ball', q=1, rb=1):
                mode = str(1)
            if cmds.menuItem('slPreview_Cube', q=1, rb=1):
                mode = str(2)
            if cmds.menuItem('slPreview_Cloth', q=1, rb=1):
                mode = str(3)
            if cmds.menuItem('slPreview_Holder', q=1, rb=1):
                mode = str(4)
                
            cam = 'renderCam'

        if SLiB.gib('mainCat') == 'objects':
            type = 'obj'
            mode = str(1)
        
            if cmds.menuItem('slPreview_Front', q=1, rb=1):
                cam = 'renderCam_Front'
            if cmds.menuItem('slPreview_PerspR', q=1, rb=1):
                cam = 'renderCam_Persp_R'
            if cmds.menuItem('slPreview_PerspL', q=1, rb=1):
                cam = 'renderCam_Persp_L'

        try:
            cmds.iconTextButton('SLiB_BUTTON_CreatePreview', e=1, w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_rendering.png', c=lambda *args: SLiB.messager('Already rendering...', 'red'))
            if errorList:
                SLiB.messager('Generating Preview Image(s)... (some errors occured - check Script Editor!)', 'yellow')
            else:
                SLiB.messager('Generating Preview Image(s)... ', 'green')
            thread.start_new_thread(SLiB_CreatePreviewRender, (previewCat, mode, cam, type))
        except:
            cmds.iconTextButton('SLiB_BUTTON_CreatePreview', e=1, w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_createpreview.png', c=lambda *args: SLiB_CreatePreview())
    
    else:
        if errorList:
            SLiB.messager('Some errors occured - check Script Editor!', 'red')
            cmds.iconTextButton('SLiB_BUTTON_CreatePreview', e=1, w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_createpreview.png', c=lambda *args: SLiB_CreatePreview())
        else:
            SLiB.messager('Please select Item(s) first!', 'red')

def SLiB_CreatePreviewRender(previewCat, mode, cam, type):
    batchList = cbxList
    
    SLiBDir = mel.eval('getenv SLiB;')
    SLiBTempStore = os.path.join(SLiBDir, 'scn', 'Temp')
    
    for item in batchList:
        selItem = os.path.basename(os.path.splitext(item)[0])
        selExt = os.path.splitext(item)[1]
        imageFile =  os.path.join(SLiBDir, 'scn', 'Temp')
        selShaderPreview = os.path.splitext(item)[0] + '.png'
        cmds.evalDeferred(lambda: SLiB_UpdateBatch(item, selItem, batchList))

        meta = os.path.splitext(item)[0] + '.meta'
        lines = [line.rstrip('\n') for line in open(meta)]
        renderer = lines[5].lower()

        for f in ['/temp_preview_mat.ma', '/temp_preview_mat.mb', '/temp_preview_obj.ma', '/temp_preview_obj.mb']:
            if os.path.isfile(SLiBTempStore + f):
                os.remove(SLiBTempStore + f) 
            
        tempFile = SLiBTempStore + '/temp_preview_' + type
        sceneFile =  SLiBDir + '/scn/' + renderer + '_SLiB_preview_' + type + '_0' + mode + '.ma'

        shutil.copy(item, tempFile + selExt)

        ## WINDOWS
        if platform.system()  == 'win32' or platform.system()  == 'Windows':
            RenderComLoc = mel.eval('getenv "MAYA_LOCATION"') + '/bin'

            if renderer == 'mentalray':
                command = '"' + RenderComLoc + "/render" + '"' + " -r mr -v 5 -cam " + '"' + cam + '"' + " -rd " + '"' + imageFile + '"' + ' ' + '"' + sceneFile + '"'
            else:            
                command = '"' + RenderComLoc + "/render" + '"' + " -r " + renderer +  " -cam " + cam + " -rd " + '"' + imageFile + '"' + ' ' + '"' + sceneFile + '"'

            #batchName = (SLiBLib + '/scn/RenderPreviews.bat')
            #batchFile = open(batchName,"w")
            #batchFile.write(command)
            #batchFile.close()

            subprocess.call(command)

        ## MAC
        elif platform.system()  == 'darwin' or platform.system()  == 'Darwin':
            RenderComLoc = mel.eval('getenv "MAYA_LOCATION"') + '/bin'

            if renderer == 'mentalray':
                command = str(RenderComLoc + "/Render -r mr -v 5 -cam " + '"' + cam + '"' + " -rd " + imageFile  + ' ' + sceneFile)
            else:            
                command = str(RenderComLoc + "/Render -r " + renderer +  " -cam " + cam +  " -rd " + imageFile  + ' ' + sceneFile)

            batchName = (SLiBDir + '/scn/RenderPreviews.sh')
            batchFile = open(batchName, "w")
            batchFile.write("#!/bin/bash")
            batchFile.write("\n")
            batchFile.write(str(command))
            batchFile.close()
            os.system("chmod 755 "+ batchName)
            subprocess.call(batchName)

        '''
        ## LINUX
        elif platform.system()  == "linux" or platform.system()  == "linux2":
            RenderComLoc = mel.eval('getenv "MAYA_LOCATION"') + '/bin'
            if SLiB.getRenderEngine() == 'mentalray':
                command = RenderComLoc + "/Render -r mr -v 5 -rd " + imageFile  + ' ' + sceneFile
            else:            
                command = RenderComLoc + "/Render -r " + SLiB.getRenderEngine() + " -rd " + imageFile  + ' ' + sceneFile
        '''
        SLiB_SwapImage(selShaderPreview, renderer)
            
    cmds.evalDeferred(lambda: SLiB_ThreadEnd(previewCat))

def SLiB_UpdateBatch(item, selItem, batchList):
    i = batchList.index(item) + 1
    print (' currently rendering: ' +  str(i) + ' / ' + str(len(batchList)) + ' [ ' +  selItem + ' ] '),

def SLiB_ThreadEnd(previewCat):
    if SLiB.gib('currLocation') == previewCat:
        cmds.evalDeferred(lambda: SLiB_UpdateView())
    cmds.iconTextButton('SLiB_BUTTON_CreatePreview', e=1, w=32, h=32, mh=0, mw=0, i=SLiB_img + 'slib_createpreview.png', c=lambda *args: SLiB_CreatePreview(), ann=' Generate Preview Image ')
    SLiB.messager('Preview Image Generation finished!', 'green')

def SLiB_SwapImage(selShaderPreview, renderer):
    if renderer == 'arnold':
        if os.path.isfile(SLiB_tmp + '/tempPreview.tif'):
            image = om.MImage()
            image.readFromFile(SLiB_tmp + '/tempPreview.tif')
            image.writeToFile(SLiB_tmp + '/tempPreview.png', 'png')
    
    if os.path.isfile(SLiB_tmp + '/tempPreview.png'):
        shutil.copy(SLiB_tmp + '/tempPreview.png', selShaderPreview)

def SLiB_Render():
    SLiB_StopRender()

    perspPanel = cmds.getPanel(wl='Persp View')
    cmds.setFocus(perspPanel)
    cmds.select(cl=1)
    renderCam = cmds.modelPanel(cmds.getPanel(wf=1), q=1, cam=1)
    imageName = os.path.normpath(SLiB_tmp + '/tempPreview.png')
    if os.path.isfile(imageName):
        os.remove(imageName)
    
    if SLiB.gib('renderer') == 'redshift':
        cmds.setAttr('redshiftOptions.postRenderMel', 'python("import SLiBBrowserPy; SLiBBrowserPy.SLiB_LoadDelayed()")', type='string')
        cmds.setAttr('redshiftOptions.renderTwoPassesForDenoising', 1)
        cmds.setAttr('defaultRenderGlobals.imageFormat', 32)
        cmds.setAttr('defaultResolution.width', 512)
        cmds.setAttr('defaultResolution.height', 512)
        aspRatio = float(cmds.getAttr('defaultResolution.width'))/float(cmds.getAttr('defaultResolution.height'))
        cmds.setAttr('defaultResolution.deviceAspectRatio', aspRatio)
        
        cmds.rsRender(r=1, cam=renderCam)
        
    if SLiB.gib('renderer') == 'vray':
        mel.eval("vrend -ipr false;")
        cmds.setAttr('vraySettings.wi',512)
        cmds.setAttr('vraySettings.he', 512)
        aspRatio = float(cmds.getAttr('vraySettings.wi'))/float(cmds.getAttr('vraySettings.he'))
        cmds.setAttr('vraySettings.aspr', aspRatio)
        cmds.setAttr('vraySettings.vfbOn', 0)
        cmds.setAttr('vraySettings.samplerType', 1)
        cmds.setAttr ('vraySettings.sRGBOn', 1)
        
        mel.eval("vrend -cam "+renderCam+";")

    if SLiB.gib('renderer') == 'arnold':
        cmds.setAttr('defaultArnoldDriver.ai_translator', 'tif', type='string')
        cmds.setAttr('defaultResolution.width', 512)
        cmds.setAttr('defaultResolution.height', 512)
        aspRatio = float(cmds.getAttr('defaultResolution.width'))/float(cmds.getAttr('defaultResolution.height'))
        cmds.setAttr('defaultResolution.deviceAspectRatio', aspRatio)
        imageName = os.path.normpath(SLiB_tmp + '/icontemp.tif')

        cmds.arnoldRender(cam=renderCam)

    if SLiB.gib('renderer') == 'mentalray':
        cmds.setAttr('defaultRenderGlobals.imageFormat', 3)
        cmds.setAttr('defaultResolution.width', 512)
        cmds.setAttr('defaultResolution.height', 512)
        aspRatio = float(cmds.getAttr('defaultResolution.width'))/float(cmds.getAttr('defaultResolution.height'))
        cmds.setAttr('defaultResolution.deviceAspectRatio', aspRatio)
        imageName = os.path.normpath(SLiB_tmp + '/icontemp.tif')
        
        cmds.Mayatomr(pv=1, cam=renderCam)

    if SLiB.gib('renderer') in ['vray', 'arnold', 'mentalray']:
        cmds.renderWindowEditor('renderView', e=1, wi=imageName)
        
    if SLiB.gib('renderer') in ['arnold', 'mentalray']:
        if os.path.isfile(imageName):
            image = om.MImage()
            image.readFromFile(imageName)
            image.writeToFile(os.path.normpath(SLiB_tmp + '/tempPreview.png', 'png'))
            os.remove(imageName)
            imageName = os.path.normpath(SLiB_tmp + '/tempPreview.png')

    SLiB_OverlayImage(imageName)

def SLiB_PlayBlast():
    oldAA = cmds.getAttr('hardwareRenderingGlobals.lineAAEnable')
    oldMS = cmds.getAttr('hardwareRenderingGlobals.multiSampleEnable')
    oldMSC = cmds.getAttr('hardwareRenderingGlobals.multiSampleCount')

    cmds.setAttr('hardwareRenderingGlobals.lineAAEnable', 1)
    cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
    cmds.setAttr('hardwareRenderingGlobals.multiSampleCount', 16)
    
    if cmds.objExists('SLiB_Dome'):
        cmds.setAttr('SLiB_DomeLight_Lyr.visibility', 0)

    object = cmds.ls(sl=1)
    imageName = os.path.normpath(SLiB_tmp + '/snapshot')
    perspPanel = cmds.getPanel(wl='Persp View')
    cmds.setFocus(perspPanel)
    cmds.select(cl=1)
    camera1 = cmds.modelPanel(cmds.getPanel(wf=1), q=1, cam=1)

    if cmds.menuItem('slSnapshotCam', q=1, cb=1):
        cmds.camera(camera1, e=1, displayResolution=0, overscan=1.0)
        playBlast = cmds.playblast(forceOverwrite = 1, framePadding=0, viewer=0, showOrnaments=0, frame=cmds.currentTime(q=1), widthHeight=[512,512], percent=100, format='iff', compression='png', filename=imageName)
        SLiB.snapshotCam()
    else:
        playBlast = cmds.playblast(forceOverwrite = 1, framePadding=0, viewer=0, showOrnaments=0, frame=cmds.currentTime(q=1), widthHeight=[512,512], percent=100, format='iff', compression='png', filename=imageName)
    
    playBlast = playBlast.replace('####', '0')

    SLiB_OverlayImage(playBlast)
    
    cmds.evalDeferred(lambda:cmds.setAttr('hardwareRenderingGlobals.lineAAEnable', oldAA))
    cmds.evalDeferred(lambda:cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', oldMS))
    cmds.evalDeferred(lambda:cmds.setAttr('hardwareRenderingGlobals.multiSampleCount', oldMSC))
    
    if object != None:
        cmds.select(object)
        
    if cmds.objExists('SLiB_Dome'):
        cmds.setAttr('SLiB_DomeLight_Lyr.visibility', 1)

def SLiB_LoadDelayed():
    imageName = os.path.normpath(SLiB_tmp + '/tempPreview.png')
    cmds.setAttr('defaultRenderGlobals.imageFormat', 32)
    pm.renderWindowEditor('renderView', e=1, wi=imageName, com=1)

    SLiB_OverlayImage(imageName)
    
    cmds.setAttr('redshiftOptions.postRenderMel', ' ', type='string')
    cmds.setAttr('redshiftOptions.renderTwoPassesForDenoising', 1)

def SLiB_LoadFromRV():
    imageName = os.path.normpath(SLiB_tmp + '/tempPreview.png')
    renderGlobals = cmds.getAttr('defaultRenderGlobals.imageFormat')
    cmds.setAttr('defaultRenderGlobals.imageFormat', 32)
    
    if SLiB.gib('renderer') == 'redshift':
        pm.renderWindowEditor('renderView', e=1, wi=imageName, com=1)
    else:
        cmds.renderWindowEditor('renderView', e=1, wi=imageName)
    
    cmds.setAttr('defaultRenderGlobals.imageFormat', renderGlobals)

    SLiB_OverlayImage(imageName)

def SLiB_LoadFromFile():
    imageName = cmds.fileDialog(m=0)
    if len(imageName) == 0:
        sys.exit()
    else:
        SLiB_OverlayImage(imageName)

def SLiB_StopRender():
    try:
        if SLiB.gib('renderer') == 'arnold':
            cmds.arnoldIpr(mode='stop')
        if SLiB.gib('renderer') == 'vray':
            mel.eval("vrayProgressEnd;")
            mel.eval("vrend -ipr false;")
        if SLiB.gib('renderer') == 'redshift':
            cmds.rsRender(r=1, stopIpr=1)
    except:
        pass

def SLiB_SwitchExportButton():
    expType = cmds.iconTextRadioCollection('mainCatCollection', q=1, sl=1)
    cmds.button('SLiB_BUTTON_Export', e=1, en=1, l='EXPORT ' + str(expType), c=lambda *args: SLiB_BrowserExport())
    
    if cmds.iconTextRadioButton('TEXTURES', q=1, sl=1):
        cmds.button('SLiB_BUTTON_Export', e=1, en=1, l='EXPORT TEXTURES', c=lambda *args: SLiB_ExportTextures('scene'), ann=' Exports all TEX files in current scene')
        
    if cmds.iconTextRadioButton('PATHS', q=1, sl=1):
        cmds.button('SLiB_BUTTON_Export', e=1, en=0, l='NO EXPORT')
        
    if cmds.iconTextRadioButton('HDRI', q=1, sl=1):
        cmds.button('SLiB_BUTTON_Export', e=1, l='EXPORT FROM FOLDER', c=lambda *args: SLiB_ExportTextures('folder'), ann=' Export HDRI(s) from folder ')

def SLiB_iptOn():
    if cmds.iconTextCheckBox('matPicker', q=1, v=1):
        SLiB_MatPicker('off')

    if cmds.menuItem('toolShortcut', q=1, cb=1):
        SLiB.helpIPT()

    SLiB.messager('IPT started!', 'green')
    placerMAT = cmds.shadingNode('lambert', asShader=1, skipSelect=1)
    placerSG = cmds.sets(n='placerSG', r=1, nss=1, em=1)
    cmds.connectAttr(placerMAT + '.outColor', placerSG + '.surfaceShader')
    cmds.rename(placerMAT, 'placerMAT')
    cmds.setAttr('placerMAT.color', 1, 0.55, 0, type='double3')
    cmds.setAttr('placerMAT.ambientColor', 0.5, 0.25, 0.25, type='double3')
    cmds.setAttr('placerMAT.transparency', 0.4, 0.4, 0.4, type='double3')

    Context = 'iptContext'
    if cmds.draggerContext(Context, q=1, ex=1):
        cmds.deleteUI(Context)
        
    worldUp = om.MVector(0,1,0)
    x,y,z = None,None,None
    
    def onPress():
        ctxBtn = cmds.draggerContext(Context, q=1, button=1)
        ctxMod = cmds.draggerContext(Context, q=1, modifier=1)
    
        targetList = SLiB.selectFromScreen('screen')
        global targetShapes
        targetShapes = []
        if targetList:
            for t in targetList:
                transform = cmds.ls(t, l=1)[0].split("|")[1]
                
                if cmds.optionVar(q=('SLIB_LastIPT')) != '':
                    if transform == cmds.optionVar(q=('SLIB_LastIPT')):
                        pass
                    else:
                        shape = ''.join(cmds.listRelatives(t, s=1, f=1))
                        if cmds.objExists(shape):
                            if cmds.nodeType(shape) == 'mesh':
                                targetShapes.append(shape)
                else:
                    shape = ''.join(cmds.listRelatives(t, s=1, f=1))
                    if cmds.objExists(shape):
                        if cmds.nodeType(shape) == 'mesh':
                            targetShapes.append(shape)
        else:
            sys.exit()

        initPos = cmds.draggerContext(Context, q=1, ap=1)
        
        if targetShapes:
            pos = om.MPoint()
            dir = om.MVector()
            hitpoint = om.MFloatPoint()
            omui.M3dView().active3dView().viewToWorld(int(initPos[0]), int(initPos[1]), pos, dir)
            pos2 = om.MFloatPoint(pos.x, pos.y, pos.z)
            for mesh in targetShapes:
                selectionList = om.MSelectionList()
                selectionList.add(mesh)
                dagPath = om.MDagPath()
                selectionList.getDagPath(0, dagPath)
                fnMesh = om.MFnMesh(dagPath)
                intersection = fnMesh.closestIntersection(om.MFloatPoint(pos2), om.MFloatVector(dir), None, None, False, om.MSpace.kWorld, 99999, False, None, hitpoint, None, None, None, None, None)
                if intersection:
                    x = hitpoint.x
                    y = hitpoint.y
                    z = hitpoint.z
                    
                    #LMB
                    if ctxBtn == int(1):
                        if ctxMod == 'none':
                            # FROM BROWSER
                            if cbxList:
                                if len(cbxList) > 1:
                                    SLiB.messager('Please select only one Asset!', 'red')
                                    sys.exit()
                                    
                                else:
                                    SLiB.delete('Placer')
                                    cmds.polyCube(n='Placer', h=10, w=10, d=10)
                                
                                    if os.path.isfile(os.path.splitext(cbxList[0])[0] + '.meta'):
                                        dim = cmds.textField('SLiB_TEXTFIELD_Size', q=1, tx=1).split('x')
                                        cmds.polyCube('Placer', e=1, d=float(dim[2]), h=float(dim[1]), w=float(dim[0]))
                                        distance = float(dim[1])/2
                                        cmds.move(0, distance*-1, 0, 'Placer.scalePivot','Placer.rotatePivot', a=1)
                                        cmds.move(0, distance, 0, 'Placer', a=1)
                                        cmds.makeIdentity('Placer', apply=1, t=1, r=1, s=1, n=0)

                                    cmds.hyperShade('Placer', a='placerMAT')
                                    cmds.setAttr('Placer.translateX', x)
                                    cmds.setAttr('Placer.translateY', y)
                                    cmds.setAttr('Placer.translateZ', z)
                                    
                            # FROM SCENE
                            if not cbxList:
                                selObj = cmds.optionVar(q=('SLIB_UserIPT'))
                                
                                if selObj:
                                    if cmds.menuItem('ReUseDuplicate', q=1, rb=1):
                                        duplObject = cmds.duplicate(selObj, n=str(selObj) + '_Dupl_')
                                        selection = SLiB.renumber(duplObject)
                                        cmds.optionVar(sv=('SLIB_CopyIPT', selection))
                                        
                                    if cmds.menuItem('ReUseInstance', q=1, rb=1):
                                        instObject = cmds.instance(selObj, n=str(selObj) + '_Inst_')
                                        selection = SLiB.renumber(instObject)
                                        cmds.optionVar(sv=('SLIB_CopyIPT', selection))
                                        
                                    cmds.setAttr(selection + '.translateX', x)
                                    cmds.setAttr(selection + '.translateY', y)
                                    cmds.setAttr(selection + '.translateZ', z)
                                    
                    #MMB
                    if ctxBtn == int(2):
                        lastImported = cmds.optionVar(q=('SLIB_LastIPT'))
                        if not cmds.optionVar(q=('SLIB_LastIPT')) == '':
                            cmds.select(lastImported)
                                
                            if ctxMod == 'none':
                                cmds.setAttr(lastImported + '.translateX', x)
                                cmds.setAttr(lastImported + '.translateY', y)
                                cmds.setAttr(lastImported + '.translateZ', z)
                                
                            if ctxMod == 'shift':
                                global initSclX
                                global initSclY
                                global initSclZ
                                initSclX = cmds.getAttr(lastImported + '.scaleX')
                                initSclY = cmds.getAttr(lastImported + '.scaleY')
                                initSclZ = cmds.getAttr(lastImported + '.scaleZ')
                            
                            if ctxMod == 'ctrl':
                                global initRotY
                                initRotY = cmds.getAttr(lastImported + '.rotateY')
            
            
            if ctxBtn == int(1):
                if ctxMod == 'shift':
                    selection = SLiB.selectFromScreen('mouse')
                    cmds.optionVar(sv=('SLIB_LastIPT', selection))
                    cmds.optionVar(sv=('SLIB_UserIPT', selection))
                    cmds.select(selection)
                    
                if ctxMod == 'ctrl':
                    selection = SLiB.selectFromScreen('mouse')
                    if selection:
                        cmds.select(selection)
                        SLiB.delete(selection)
                        cmds.optionVar(sv=('SLIB_LastIPT', ''))

            cmds.refresh()
                
    def onDrag():
        ctxBtn = cmds.draggerContext(Context, q=1, button=1)
        ctxMod = cmds.draggerContext(Context, q=1, modifier=1)
        
        currentPos = cmds.draggerContext(Context, q=1, dp=1)
        
        if targetShapes:
            pos = om.MPoint()
            dir = om.MVector()
            hitpoint = om.MFloatPoint()
            omui.M3dView().active3dView().viewToWorld(int(currentPos[0]), int(currentPos[1]), pos, dir)
            pos2 = om.MFloatPoint(pos.x, pos.y, pos.z)
            for mesh in targetShapes:
                selectionList = om.MSelectionList()
                selectionList.add(mesh)
                dagPath = om.MDagPath()
                selectionList.getDagPath(0, dagPath)
                fnMesh = om.MFnMesh(dagPath)
                intersection = fnMesh.closestIntersection(om.MFloatPoint(pos2), om.MFloatVector(dir), None, None, False, om.MSpace.kWorld, 99999, False, None, hitpoint, None, None, None, None, None)
                if intersection:
                    x = hitpoint.x
                    y = hitpoint.y
                    z = hitpoint.z
                    
                    mHit = om.MPoint(hitpoint)
                    normal = om.MVector()
                    fnMesh.getClosestNormal(mHit, normal, om.MSpace.kWorld, None)

                    rx, ry, rz = SLiB.getEulerRotationQuaternion(worldUp, normal)
                    
                    #LMB
                    if ctxBtn == int(1):
                        if ctxMod == 'shift':
                            pass
                            
                        if ctxMod == 'none':
                            if cbxList:
                                cmds.setAttr('Placer.translateX', x)
                                cmds.setAttr('Placer.translateY', y)
                                cmds.setAttr('Placer.translateZ', z)

                                cmds.setAttr('Placer.rotateX', rx)
                                cmds.setAttr('Placer.rotateY', ry)
                                cmds.setAttr('Placer.rotateZ', rz)
                                
                            if not cbxList:
                                selObj = cmds.optionVar(q=('SLIB_CopyIPT'))
                                
                                if selObj:
                                    cmds.setAttr(selObj + '.translateX', x)
                                    cmds.setAttr(selObj + '.translateY', y)
                                    cmds.setAttr(selObj + '.translateZ', z)

                                    cmds.setAttr(selObj + '.rotateX', rx)
                                    cmds.setAttr(selObj + '.rotateY', ry)
                                    cmds.setAttr(selObj + '.rotateZ', rz)
                    
                    #MMB
                    if ctxBtn == int(2):
                        lastImported = cmds.optionVar(q=('SLIB_LastIPT'))
                        if not cmds.optionVar(q=('SLIB_LastIPT')) == '':
                            if ctxMod == 'none':
                                cmds.setAttr(lastImported + '.translateX', x)
                                cmds.setAttr(lastImported + '.translateY', y)
                                cmds.setAttr(lastImported + '.translateZ', z)
                                
                                if not cmds.menuItem('keepRotation', q=1, cb=1):
                                    cmds.setAttr(lastImported + '.rotateX', rx)
                                    cmds.setAttr(lastImported + '.rotateY', ry)
                                    cmds.setAttr(lastImported + '.rotateZ', rz)
                                
                                cmds.select(lastImported)
            
                #MMB
                if ctxBtn == int(2):
                    lastImported = cmds.optionVar(q=('SLIB_LastIPT'))
                    if not cmds.optionVar(q=('SLIB_LastIPT')) == '':
                
                        start = cmds.draggerContext(Context, q=1, ap=1)[0]
                        end = currentPos[0]
                        
                        if ctxMod == 'ctrl':
                            rotValue =  initRotY + (end - start) / 2
                            cmds.setAttr(lastImported + '.rotateY', rotValue)
                            
                            SLiB.messager(str(format(rotValue, '.1f')), 'blue')
                            
                        if ctxMod == 'shift':
                            sclValueX =  initSclX + (end - start) / 40
                            sclValueY =  initSclY + (end - start) / 40
                            sclValueZ =  initSclZ + (end - start) / 40
                            
                            cmds.setAttr(lastImported + '.scaleX', sclValueX)
                            cmds.setAttr(lastImported + '.scaleY', sclValueY)
                            cmds.setAttr(lastImported + '.scaleZ', sclValueZ)
                            
                            SLiB.messager(str(format(sclValueX, '.1f')), 'blue')
                            
            cmds.refresh()

    def onRelease():
        ctxBtn = cmds.draggerContext(Context, q=1, button=1)
        ctxMod = cmds.draggerContext(Context, q=1, modifier=1)
        
        impObject = ''
        lastImported = cmds.optionVar(q=('SLIB_LastIPT'))
        
        try:
            #LMB
            if ctxBtn == int(1):
                        
                if ctxMod == 'none':
                    if cbxList:
                        impObject = SLiB_BrowserImport('Normal', cbxList[0])
                        
                        if impObject:
                            global initRotY
                            global initSclX
                            global initSclY
                            global initSclZ

                            initRotY = cmds.getAttr(impObject + '.rotateY')
                            initSclX = cmds.getAttr(impObject + '.scaleX')
                            initSclY = cmds.getAttr(impObject + '.scaleY')
                            initSclZ = cmds.getAttr(impObject + '.scaleZ')

                            posX = cmds.getAttr('Placer.translateX')
                            posY = cmds.getAttr('Placer.translateY')
                            posZ = cmds.getAttr('Placer.translateZ')
                   
                            if not cmds.menuItem('keepRotation', q=1, cb=1):
                                rotX = cmds.getAttr('Placer.rotateX')
                                rotY = cmds.getAttr('Placer.rotateY')
                                rotZ = cmds.getAttr('Placer.rotateZ')
                            else:
                                rotX = cmds.getAttr(lastImported + '.rotateX')
                                rotY = cmds.getAttr(lastImported + '.rotateY')
                                rotZ = cmds.getAttr(lastImported + '.rotateZ')
                            
                            if not cmds.menuItem('keepScale', q=1, cb=1):
                                scalX = cmds.getAttr('Placer.scaleX')
                                scalY = cmds.getAttr('Placer.scaleY')
                                scalZ = cmds.getAttr('Placer.scaleZ')
                            else:
                                scalX = cmds.getAttr(lastImported + '.scaleX')
                                scalY = cmds.getAttr(lastImported + '.scaleY')
                                scalZ = cmds.getAttr(lastImported + '.scaleZ')
                            
                            cmds.setAttr(impObject + '.translateX', posX)
                            cmds.setAttr(impObject + '.translateY', posY)
                            cmds.setAttr(impObject + '.translateZ', posZ)

                            cmds.setAttr(impObject + '.rotateX', rotX)
                            cmds.setAttr(impObject + '.rotateY', rotY)
                            cmds.setAttr(impObject + '.rotateZ', rotZ)
                            
                            cmds.setAttr(impObject + '.scaleX', scalX)
                            cmds.setAttr(impObject + '.scaleY', scalY)
                            cmds.setAttr(impObject + '.scaleZ', scalZ)
                                
                            SLiB.delete('Placer')
                            
                            cmds.optionVar(sv=('SLIB_LastIPT', impObject))
                            cmds.select(impObject)
            #MMB
            if ctxBtn == int(2):
                if not cmds.optionVar(q=('SLIB_LastIPT')) == '':
                    cmds.select(lastImported)

        except:
            SLiB.delete('Placer')
            SLiB.delete(impObject)
            SLiB_iptOff()
            SLiB.messager('Error!  Try again or restart IPT', 'red')
        
    cmds.draggerContext(Context, pc=onPress, dc=onDrag, rc=onRelease, n=Context, cur='crossHair', i1= SLiB_img + 'slib_ipt_on.png')
    cmds.setToolTo(Context)
    SLiB.messager('IPT running...', 'blue')

def SLiB_iptOff():
    for v in ['SLIB_CopyIPT', 'SLIB_UserIPT', 'SLIB_LastIPT']:
        if cmds.optionVar(ex=v):
            cmds.optionVar(rm=v)

    cmds.iconTextCheckBox('ipt', e=1, v=0)
    cmds.setToolTo('selectSuperContext')
    
    if cmds.window('slHelp_IPT', ex=1):
        cmds.deleteUI('slHelp_IPT')

    #if cmds.draggerContext('iptContext', ex=1):
    #    cmds.deleteUI('iptContext')

    SLiB.delete('Placer')
    SLiB.delete('placerMAT')
    SLiB.delete('placerSG')

    SLiB.messager('IPT stopped!', 'none')

def SLiB_LoadTestRoom():
    if SLiB.gib('renderer') in ['arnold', 'mentalray', 'redshift', 'vray']:
        answer = cmds.confirmDialog(t='Warning', m='Please make sure you saved the current scene! \nDo you want to proceed?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if answer == 'Yes':
            needSave = cmds.file(q=1, modified=1)
            if SLiB.gib('mainCat') == 'shader':
                testroomfile = SLiB_dir + '/scn/' + SLiB.gib('renderer') + '_SLiB_shaderTestRoom.ma'
            else:
                SLiB.messager('Only Shader supported!', 'yellow')
                sys.exit()
            
            cmds.file( f=1, new=1 )
            cmds.file( testroomfile, o=1 )
            savename = cmds.workspace(q = 1, fullName = 1) + '/' + SLiB.gib('renderer') + '_' + cmds.date().replace (" ", "_").replace ("/", "").replace (":", "") + '.ma'
            cmds.file( rename=savename )
            cmds.file( save=1, type='mayaAscii' )
            SLiB.messager('ShaderBall Scene for ' + str(SLiB.gib('renderer')) + ' loaded!', 'green')
    else:
        SLiB.messager('Renderer: ' + str(SLiB.gib('renderer')) + ' not supported.!', 'red')

def SLiB_BrowserMark(m):
    if SLiB.gib('mainCat') == 'paths':
        path = SLiBThumbsLayout.children()[1].children()[0].children()[0]
        if cbxAll != None:
            for s in cbxAll:
                checkbox = path.findChild(QCheckBox, s)

                if m == 'none':
                    checkbox.setChecked(0)
                    cbxList.remove(s)
                    SLiB.messager('', 'none')
                    SLiB.messager('All items deselected!', 'none')
                
                if m == 'all':
                    checkbox.setChecked(1)
                    cbxList.append(s)
                    SLiB.messager(str(len(cbxAll)) + ' Item(s) selected!', 'none')
    else:
        for s in SLiBCollection:
            s = os.path.normpath(s)
            buttonWidget = scroll.findChild(QWidget, s)
            checkbox = buttonWidget.findChild(QCheckBox, s)
            label = buttonWidget.findChild(QLabel, s)
            
            if m == 'none':
                if checkbox.isChecked():
                    checkbox.setChecked(0)
                    cbxList.remove(s)
                    checkbox.setStyleSheet("padding: 2;")
                    label.setStyleSheet("padding: 2;")
                    SLiB.messager('All items deselected!', 'none')
            
            if m == 'all':
                if checkbox.isChecked() == False:
                    checkbox.setChecked(1)
                    cbxList.append(s)
                    checkbox.setStyleSheet("background-color: #50b0ff; color: black; padding: 2;")
                    label.setStyleSheet("background-color: #50b0ff; color: black; padding: 2;")
                    SLiB.messager(str(len(SLiBCollection)) + ' Item(s) selected!', 'none')

def SLiB_TexList():
    if cmds.ls(sl=1):
        shapes = cmds.ls(cmds.listRelatives(ad=1), type='shape')
        if shapes:
            shadingGroups = cmds.listConnections(shapes, type='shadingEngine')
            if shadingGroups:
                selMaterials = sorted(set(cmds.listConnections(shadingGroups, s=1)))
                history = cmds.listHistory(selMaterials, af=1)
            else:
                history = None
                
            nodeList = []
            if SLiB.gib('renderer') == 'redshift':
                nodeTypes = ['file', 'RedshiftNormalMap', 'RedshiftSprite', 'RedshiftDomeLight', 'RedshiftBokeh']
            else:
                nodeTypes = ['file']
            
            for t in nodeTypes:
                nodeList.append(cmds.ls(history, type=t))
                nodeList.append(cmds.ls(shapes, type=t))
             
            return sorted(set(sum(nodeList, [])))
    else:
        if SLiB.gib('renderer') == 'redshift':
            return sorted(set(cmds.ls(type='file') + cmds.ls(type='RedshiftNormalMap') + cmds.ls(type='RedshiftSprite') + cmds.ls(type='RedshiftDomeLight') + cmds.ls(type='RedshiftBokeh')))
        else:
            return sorted(set(cmds.ls(type='file')))

class SLiBListTextures(QtWidgets.QFormLayout):
    def __init__(self):
        super(SLiBListTextures, self).__init__()

        global cbxList
        cbxList = []
        
        global cbxAll
        cbxAll = []
        
        global cbxMissing
        cbxMissing= []
        
        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setLayout(self)

        scroll = ScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scrollWidget)
        
        fWord = cmds.textField('SLiB_TEXTFIELD_Search', q=1, tx=1)

        if SLiBCollection:
            cmds.progressBar('PreviewProgress', e=1, max=(len(SLiBCollection)))
            for i in SLiBCollection:
                '''
                if cmds.iconTextCheckBox('searchSwitch', q=1, v=1):
                    fileName = os.path.normpath(cmds.getAttr(i + SLiB.gibTexSlot(i)))
                    if fWord in fileName:
                            pass'''

                fileName = os.path.normpath(cmds.getAttr(i + SLiB.gibTexSlot(i)))
                
                if fileName:
                    texCbx = QtWidgets.QCheckBox(fileName)
                    if os.path.isfile(SLiB_absPath(fileName)):
                        texCbx.setStyleSheet("color: #c5c5c5; padding: 2;")
                    else:
                        texCbx.setStyleSheet("color: red; padding: 2;")
                        cbxMissing.append(fileName + '|' + i)
                    
                    texCbx.setObjectName(fileName + '|' + i)
                    texCbx.setFixedHeight(20)
                    texCbx.clicked.connect(self.clicked)

                    self.addWidget(texCbx)
                    
                    cbxAll.append(fileName + '|' + i)
                    cmds.progressBar('PreviewProgress', e=1, step=1)
                    
             
            SLiBThumbsScrollLayout.addWidget(scroll)
            cmds.progressBar('PreviewProgress', e=1, pr=0)
            
            if cbxMissing:
                SLiB.messager(str(len(cbxMissing)) + ' Texture File(s) missing!', 'red')

    def clicked(self):
        cbx = self.sender()
        item = os.path.normpath(cbx.objectName())
        file = os.path.normpath(cbx.objectName().split('|')[0])
        imageName = os.path.normpath(SLiB_absPath(file))
        print item
        
        if QtWidgets.qApp.mouseButtons() & QtCore.Qt.RightButton:
            pass
        
        if cbx.isChecked():
            cbxList.append(item)
            if os.path.isfile(imageName):
                SLiB_OverlayImage(imageName)
            else:
                SLiB_OverlayImage(SLiB_img + 'image_missing.png')
        
        else:
            cbxList.remove(item)
            SLiB_OverlayImage(SLiB_img + 'browser_logo.png')

def SLiB_ABStoREL():
    if cbxList:
        for i in cbxList:
            file = os.path.normpath(i.split('|')[0])
            node = i.split('|')[1]
           
            if os.path.normpath(mel.eval('getenv SLiBRARY;') + '/shader') in file:
                fileNameNew = os.path.normpath('${SLiBRARY}/shader/' + file.split('shader')[1])
                cmds.setAttr(node + SLiB.gibTexSlot(node), fileNameNew, type='string')
                
            if os.path.normpath(mel.eval('getenv SLiBRARY;') + '/objects') in file:
                fileNameNew = os.path.normpath('${SLiBRARY}/objects/' + file.split('objects')[1])
                cmds.setAttr(node + SLiB.gibTexSlot(node), fileNameNew, type='string')
                
            if os.path.normpath(mel.eval('getenv SLiBRARY;') + '/lights') in file:
                fileNameNew = os.path.normpath('${SLiBRARY}/lights/' + file.split('lights')[1])
                cmds.setAttr(node + SLiB.gibTexSlot(node), fileNameNew, type='string')
                
            if os.path.normpath(mel.eval('getenv SLiBRARY;') + '/textures') in file:
                fileNameNew = os.path.normpath('${SLiBRARY}/textures/' + file.split('textures')[1])
                cmds.setAttr(node + SLiB.gibTexSlot(node), fileNameNew, type='string')
                
            if os.path.normpath(mel.eval('getenv SLiBRARY;') + '/hdri') in file:
                fileNameNew = os.path.normpath('${SLiBRARY}/hdri/' + file.split('hdri')[1])
                cmds.setAttr(node + SLiB.gibTexSlot(node), fileNameNew, type='string')
                
            if os.path.normpath(mel.eval('getenv SLiBRARY;') + '/maps') in file:
                fileNameNew = os.path.normpath('${SLiBRARY}/maps/' + file.split('maps')[1])
                cmds.setAttr(node + SLiB.gibTexSlot(node), fileNameNew, type='string')

            # OLD STUFF
            if os.path.normpath(SLiB_lib + '/shader') in file:
                fileNameNew = os.path.normpath('${SLiBRARY}/shader/' + file.split('shader')[1])
                cmds.setAttr(node + SLiB.gibTexSlot(node), fileNameNew, type='string')
                
            if os.path.normpath(SLiB_lib + '/objects') in file:
                fileNameNew = os.path.normpath('${SLiBRARY}/objects/' + file.split('objects')[1])
                cmds.setAttr(node + SLiB.gibTexSlot(node), fileNameNew, type='string')
                
            if os.path.normpath(SLiB_lib + '/maps') in file:
                fileNameNew = os.path.normpath('${SLiBRARY}/maps/' + file.split('maps')[1])
                cmds.setAttr(node + SLiB.gibTexSlot(node), fileNameNew, type='string')
                
        SLiB_UpdateView()
        SLiB.messager(str(len(cbxList)) + ' path(s) converted to RELATIVE!', 'green')
        
    else:
        SLiB.messager('Nothing selected to work with :(', 'yellow')

def SLiB_RELtoABS():
    if cbxList:
        for i in cbxList:
            file = os.path.normpath(i.split('|')[0])
            node = i.split('|')[1]
            
            fileNameNew = SLiB_absPath(file)
            cmds.setAttr(node + SLiB.gibTexSlot(node), fileNameNew, type='string')

        SLiB_UpdateView()
        SLiB.messager(str(len(cbxList)) + ' path(s) converted to ABSOLUTE!', 'green')
        
    else:
        SLiB.messager('Nothing selected to work with :(', 'yellow')

def SLiB_CopyTexturesTo(x):
    if cbxList:
        if x == 'project':
            textdestination = os.path.join(cmds.workspace(q=1, rd=1), 'sourceimages')
        
        if x == 'folder':
            try:
                textdestination = cmds.fileDialog2(dir=mel.eval('getenv SLiBRARY;') + '/maps', fm=3)[0]
            except:
                textdestination = None
        
        if textdestination != None:
            cmds.progressBar('PreviewProgress', e=1, max=(len(cbxList)))
            for i in cbxList:
                file = os.path.normpath(i.split('|')[0])
                node = i.split('|')[1]

                file = SLiB_absPath(file)
                
                finalPath = os.path.normpath(os.path.join(textdestination, os.path.basename(file)))
                
                if file != finalPath:
                    if os.path.isfile(file):
                        shutil.copy(file, textdestination)
                        cmds.setAttr(node + SLiB.gibTexSlot(node), finalPath, type='string')
                        
                cmds.progressBar('PreviewProgress', e=1, step=1)
            cmds.progressBar('PreviewProgress', e=1, pr=0)

            cmds.evalDeferred(lambda: SLiB_UpdateView())
            SLiB.messager(str(len(cbxList)) + ' texture(s) copied and relinked to to:' + textdestination + '!', 'green')
    
    else:
        SLiB.messager('Nothing selected to work with :(', 'yellow')

def SLiB_FindMissingTextures():
    if cbxMissing:
        fixed = []
        try:
            searchLoc = cmds.fileDialog2(dir=mel.eval('getenv SLiBRARY;') + '/maps', fm=3)[0]
        except:
            searchLoc = None
        
        if searchLoc != None:
            for i in cbxMissing:
                file = os.path.normpath(i.split('|')[0])
                node = i.split('|')[1]
                
                file = SLiB_absPath(file)

                name = os.path.basename(file)
                
                for root,dirs,files in os.walk(searchLoc):
                    if name in files:
                        newpath = os.path.join(root,name)
                        if not '_THUMBS' in newpath:
                            cmds.setAttr(node + SLiB.gibTexSlot(node), newpath, type='string')
                            print '>>> missing Texture found!\n',
                            fixed.append(name)

            SLiB_UpdateView()
            if len(fixed) == len(cbxMissing):
                SLiB.messager('Texture(s) found!', 'green')
            else:
                SLiB.messager(str(len(fixed)) + ' Texture(s) found! ' + str(len(cbxMissing) - len(fixed)) + ' still missing.', 'yellow')
            
    else:
        SLiB.messager('There is nothing to find!', 'yellow')

def SLiB_RelinkTextures():
    if cbxList:
        fixed = []
        try:
            searchLoc = cmds.fileDialog2(dir=mel.eval('getenv SLiBRARY;') + '/maps', fm=3)[0]
        except:
            searchLoc = None
        
        if searchLoc != None:
            for i in cbxList:
                file = os.path.normpath(i.split('|')[0])
                node = i.split('|')[1]
                
                file = SLiB_absPath(file)

                name = os.path.basename(file)
                
                for root,dirs,files in os.walk(searchLoc):
                    if name in files:
                        newpath = os.path.join(root,name)
                        cmds.setAttr(node + SLiB.gibTexSlot(node), newpath, type='string')
                        fixed.append(name)

            SLiB_UpdateView()
            if len(fixed) == len(cbxList):
                SLiB.messager('Texture(s) relinked!', 'green')
            else:
                SLiB.messager(str(len(fixed)) + ' Texture(s) relinked! ' + str(len(cbxList) - len(fixed)) + ' missing.', 'yellow')

def SLiB_AddLib():
    try:
        newLibPath = cmds.fileDialog2(dir=os.sep, fm=3)[0] + '/'
    except:
        newLibPath = None

    if newLibPath != None:
        mel.eval('putenv "SLiBRARY" "' + newLibPath + '"')
        for e in ['shader', 'objects', 'lights', 'hdri', 'textures', 'maps']:
            if os.path.isdir(os.path.join(newLibPath, e)) != 1:
                os.mkdir(os.path.join(newLibPath, e))
                
        libDict = SLiB.gib('libraries')
        libDict.append(newLibPath)
        libDict = sorted(set(libDict))
        
        f = open(SLiB_dir +'set/LIB_Dictionary.txt', 'w')
        for e in libDict:
            f.write(e + '\n')
        f.close()
        
        mel.eval('putenv "SLiBRARY" "' + newLibPath + '"')
        
        SLiB_FillLib()
        cmds.optionMenu('sl_OB_library', e=1, v=newLibPath)
        SLiB_SwitchLib()
        SLiB.messager('Library: ' + newLibPath + ' added!', 'green')

def SLiB_FillLib():
    if cmds.optionMenu('sl_OB_library', ex=1):
        cmds.deleteUI('sl_OB_library')
        
    cmds.optionMenu('sl_OB_library', cc=lambda *args: SLiB_SwitchLib(), p='slib_library_OB')
    cmds.menuItem(l='MAIN', p='sl_OB_library')
    for l in SLiB.gib('libraries'):
        cmds.menuItem(l=l, p='sl_OB_library')

def SLiB_SwitchLib():
    if cmds.optionMenu('sl_OB_library', q=1, v=1) == 'MAIN':
        mel.eval('putenv "SLiBRARY" "' + SLiB_lib + '"')
    else:
        path = cmds.optionMenu('sl_OB_library', q=1, v=1) + '/'
        mel.eval('putenv "SLiBRARY" "' + path + '"')
    
    SLiB_RefreshTree()
    SLiB_ClearLayout(SLiBThumbsScrollLayout)

def SLiB_RemoveLib():
    delLib = cmds.optionMenu('sl_OB_library', q=1, v=1)
    if delLib != 'MAIN':
        libDict = SLiB.gib('libraries')
        libDict.remove(delLib)
        libDict = sorted(set(libDict))
        
        f = open(SLiB_dir +'set/LIB_Dictionary.txt', 'w')
        for e in libDict:
            f.write(e + '\n')
        f.close()
        
        mel.eval('putenv "SLiBRARY" "' + SLiB_lib + '"')
        SLiB_RefreshTree()
        SLiB_FillLib()
        SLiB_ClearLayout(SLiBThumbsScrollLayout)
        cmds.optionMenu('sl_OB_library', e=1, v='MAIN')
        SLiB.messager('Library [ ' + delLib + ' ] removed!', 'green')
        
    else:
        SLiB.messager('You cannot delete the MAIN library!', 'red')

def SLiB_EditLibraries():
    webbrowser.open(SLiB_dir +'set/LIB_Dictionary.txt')

def SLiB_SwitchTextures():
    if cmds.optionMenu('exportTEX', q=1, v=1) == 'no Textures':
        cmds.optionMenu('TexPathMode', e=1, en=0)
        cmds.layout('SLiB_export_path', e=1, vis=0)
        cmds.textField('SLiB_TEXTFIELD_Texpath', e=1, tx='')
    
    if cmds.optionMenu('exportTEX', q=1, v=1) == 'with Textures':
        cmds.optionMenu('TexPathMode', e=1, en=1)
        cmds.layout('SLiB_export_path', e=1, vis=0)
        cmds.textField('SLiB_TEXTFIELD_Texpath', e=1, tx='')
    
    if cmds.optionMenu('exportTEX', q=1, v=1) == 'with custom Texture Folder':
        cmds.optionMenu('TexPathMode', e=1, en=1)
        cmds.layout('SLiB_export_path', e=1, vis=1)

def SLiB_Downloader():
    if cmds.window('SLiB_Downloader', q=1, ex=1):
        cmds.deleteUI('SLiB_Downloader')
        
    cmds.window('SLiB_Downloader', t='SLiB Downloader', s=0)
    cmds.columnLayout('sldWinLayout', p='SLiB_Downloader')
    cmds.image('cgfLogo', i=SLiB_img + 'cgf_logo.png', p='sldWinLayout')
    cmds.text(l='', h=20, p='sldWinLayout')
    
    cmds.rowColumnLayout('sldUserLayout', w=300, h=30, nc=3, cw=[(1,50),(2,230),(3,20)], cal=[(1,'center')], p='sldWinLayout')
    cmds.text(l='USER', p='sldUserLayout')
    cmds.textField('slUser', w=230 ,p='sldUserLayout')

    cmds.rowColumnLayout('sldPassLayout', w=300, h=30, nc=3, cw=[(1,50),(2,230),(3,20)], cal=[(1,'center')], p='sldWinLayout')
    cmds.text(l='PASS', p='sldPassLayout')
    cmds.textField('slPass', w=230 ,p='sldPassLayout')
    
    cmds.rowColumnLayout('sldLinkLayout', w=300, h=30, nc=3, cw=[(1,50),(2,230),(3,20)], cal=[(1,'center')], p='sldWinLayout')
    cmds.text(l='LINK', p='sldLinkLayout')
    cmds.textField('slLink', w=230 ,p='sldLinkLayout')
        
    cmds.showWindow('SLiB_Downloader')
    cmds.progressBar('slDownloadBar', w=300, h=12, p='sldWinLayout')
    cmds.button('SLiB_BUTTON_Download', w=300, h=32, l='INSTALL', bgc=[0,0.75,0.99], c=lambda *args: SLiB_Login(), p='sldWinLayout')
    cmds.window('SLiB_Downloader', e=1, w=300, h=200)
    
def SLiB_Login():
    for e in ['shader', 'objects', 'lights', 'hdri', 'textures']:
        if not os.path.isdir(os.path.normpath(os.path.join(SLiB_lib, e, 'Download'))):
            os.mkdir(os.path.normpath(os.path.join(SLiB_lib, e, 'Download')))
            os.mkdir(os.path.normpath(os.path.join(SLiB_lib, e, 'Download', '_SUB')))
            
    if SLiB.gib('mainCat') in ['shader', 'objects', 'lights', 'hdri', 'textures']:
        slLink = str(cmds.textField('slLink', q=1, tx=1))
        slUser = str(cmds.textField('slUser', q=1, tx=1))
        slPass = str(cmds.textField('slPass', q=1, tx=1))
        slURL = 'http://www.store.cgfront.com/login?back=my-account'
        
        if slUser and slPass and slLink:
            browser = mechanize.Browser()
            browser.set_handle_robots(False)
            cookies = mechanize.CookieJar()
            browser.set_cookiejar(cookies)
            browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
            browser.set_handle_refresh(False)
            browser.open(slURL)
            
            for n in range(0,4):
                browser.select_form(nr=n)
                try:
                    browser.form['email'] = slUser
                    browser.form['passwd'] = slPass
                    browser.submit()
                except mechanize._form.ControlNotFoundError:
                    continue
                break 
        
            response = browser.open(slLink)
            SLiB_Download(response, report=SLiB_DownloadProgress)
        
        else:
            SLiB.messager('Please fill all fields!', 'red')
    else:
        SLiB.messager('Cannot install in PATHS!', 'red')

def SLiB_DownloadProgress(bytes_so_far, chunk_size, total_size):
    prozent = (float(bytes_so_far) / total_size) * 100
    cmds.progressBar('slDownloadBar', e=1, pr=int(prozent))

def SLiB_Download(response, chunk_size=8192, report=None):
    cmds.progressBar('slDownloadBar', e=1, pr=0)
    try:
        file_name = (response.info().getheader('Content-Disposition')).split('"')[1]
    except:
        SLiB.messager('Please check Username, Password and Link!', 'red')
        sys.exit()
    total_size = int(response.info().getheader('Content-Length').strip())
    total_size = int(total_size)
    cmds.progressBar('slDownloadBar', e=1, max=100)
    bytes_so_far = 0
    data = []
    targetFile = os.path.normpath(os.path.join(SLiB_lib, SLiB.gib('mainCat'), 'Download', file_name))
    f = open(targetFile, "w")
    cmds.button('SLiB_BUTTON_Download', e=1, l='loading: ' + file_name)

    while 1:
        chunk = response.read(chunk_size)
        f.write(chunk)
        bytes_so_far += len(chunk)

        if not chunk:
            break

        data += chunk
        if report:
            report(bytes_so_far, chunk_size, total_size)

    f.close()
    
    cmds.button('SLiB_BUTTON_Download', e=1, l='INSTALL')
    
    if os.path.isfile(targetFile):
        if str(os.path.getsize(targetFile)) == str(total_size):
            zip_ref = zipfile.ZipFile(targetFile, 'r')
            zip_ref.extractall(mel.eval('getenv SLiBRARY;'))
            zip_ref.close()
            
            cmds.evalDeferred(lambda: os.remove(targetFile))
            cmds.evalDeferred(lambda: SLiB_UpdateView())

def SLiB_Unzipper():
    z = cmds.fileDialog2(fm=1, ff='*.zip')
    if z:
        z = z[0]
        if os.path.isfile(z):
            SLiB.messager('Extracting archive...', 'blue')
            thread.start_new_thread(SLiB_unzip, (z,))

def SLiB_unzip(z):
    zip_ref = zipfile.ZipFile(z, 'r')
    members = zip_ref.infolist()

    for i, member in enumerate(members):
        zip_ref.extract(member, mel.eval('getenv SLiBRARY;'))

    cmds.evalDeferred(lambda: SLiB_RefreshTree())
    cmds.evalDeferred(lambda: SLiB_UpdateView())
    cmds.evalDeferred(lambda: SLiB.messager('Archive successfully extracted!', 'green'))
 
def SLiB_About():
    if cmds.window('slAbout', ex=1):
        cmds.deleteUI('slAbout')

    cmds.window('slAbout', t=' ', sizeable=0)
    cmds.columnLayout('aboutWinLayout', w=256, adj=1, bgc=[0.18,0.18,0.18], p='slAbout')
    cmds.text(l='BROWSER PRO 2.0', w=256, h=50, p='aboutWinLayout')
    cmds.text(l='by', w=256, p='aboutWinLayout')
    cmds.image(w=250, h=100, i=SLiB_img + 'dgdm.png', p='aboutWinLayout')
    cmds.text(l='', w=256, h=20, p='aboutWinLayout')
    cmds.text(l='And very special thanks to\n Kornelis van der Bij\n for helping with UI, Functionality,\n Design and Help Documentation', w=256, h=50, p='aboutWinLayout')
    cmds.text(l='', w=256, h=20, p='aboutWinLayout')
    cmds.text(l='www.store.cgfront.com', w=256, h=50, p='aboutWinLayout', hl=1)

    cmds.showWindow('slAbout')
    cmds.window('slAbout', e=1, w=256, h=320)

#MAT Picker
def SLiB_MatPicker(x):
    if cmds.iconTextCheckBox('ipt', q=1, v=1):
        SLiB_iptOff()

    if cmds.menuItem('toolShortcut', q=1, cb=1):
        SLiB.helpMP()
        
    if x == 'on':
        SLiB.messager('MAT Picker started!', 'green')
        Context = 'matContext'
        if cmds.draggerContext(Context, q=1, ex=1):
            cmds.deleteUI(Context)

        worldUp = om.MVector(0,1,0)
        
        def onPress():
            ctxBtn = cmds.draggerContext(Context, q=1, button=1)
            ctxMod = cmds.draggerContext(Context, q=1, modifier=1)
        
            targetList = SLiB.selectFromScreen('screen')
            global targetShapes
            targetShapes = []
            
            if targetList:
                for t in targetList:
                    shape = ''.join(cmds.listRelatives(t, s=1, f=1))
                    if shape:
                        targetShapes.append(shape)
                    
                initPos = cmds.draggerContext(Context, q=1, ap=1)
                worldPos, worldDir = SLiB.view_to_world(initPos[0],initPos[1])
                closestObj = None
                hit = None
                
                if targetShapes:
                    for obj in targetShapes:
                        state, hit, fnMesh, facePtr, triPtr = SLiB.intersect(obj, worldPos, worldDir)
                        
                        if state is True:
                            closestObj = [state, hit, fnMesh, facePtr, triPtr]
                
                    if closestObj is not None:
                        state, hit, fnMesh, facePtr, triPtr = closestObj

                        if hit:
                            #LMB
                            if ctxBtn == int(1):
                                sourceObj = SLiB.selectFromScreen('mouse')
                                cmds.select(sourceObj)

                                if ctxMod == 'none' or ctxMod == 'shift':
                                    SLiB.selectFromMaterial('Mat')
                                    SLiB.messager('Material successful picked', 'green')

                                if ctxMod == 'ctrl':
                                    SLiB.selectFromMaterial('MatCopy')
                                    SLiB.messager('picked Material duplicated', 'green')

                                if ctxMod == 'shift':
                                    SLiB.selectFromMaterial('SG')

                            #MMB
                            if ctxBtn == int(2):
                                mat = SLiB.gib('pickedMat')
                                targetObj = SLiB.selectFromScreen('mouse')
                                cmds.select(targetObj)
                                
                                if mat:
                                    if ctxMod == 'none':
                                        targetShape = cmds.listRelatives(targetObj, ad=1, s=1, f=1)[0]
                                        cmds.select(targetShape)
                                        cmds.hyperShade(a=mat)
                                        SLiB.messager('[ ' + mat + ' ] assigned to [ ' + targetShape + ' ]' , 'green')
                                        
                                    if ctxMod == 'shift':
                                        SLiB.findSimilar()
                                        cmds.hyperShade(a=mat)
                                        SLiB.messager('[ ' + mat + ' ] assigned to similar object(s)', 'green')

                                    if ctxMod == 'ctrl':
                                        SLiB.selectFromMaterial('Sel')
                                        SLiB.messager('[ ' + mat + ' ] assigned to object(s) with same Material', 'green')

                    cmds.refresh()
                    
                else:
                    sys.exit()

        cmds.draggerContext(Context, pc=onPress, n=Context, cur='hand', i1= SLiB_img + 'slib_matpicker_on.png')
        cmds.setToolTo(Context)
        SLiB.messager('MAT Picker running...', 'blue')
    
    if x == 'off':
        if cmds.window('slHelp_MP', ex=1):
            cmds.deleteUI('slHelp_MP')
            
        view = omui.M3dView()
        omui.M3dView.getM3dViewFromModelPanel('modelPanel4', view)
        viewWidget = wrapInstance(long(view.widget()), QtWidgets.QWidget)
        oldWin = viewWidget.findChild(QtWidgets.QWidget, 'swatchWin')
        if oldWin:
            oldWin.deleteLater()
            
        cmds.iconTextCheckBox('matPicker', e=1, v=0)
        cmds.setToolTo('selectSuperContext')

        if cmds.draggerContext('matContext', ex=1):
            cmds.deleteUI('matContext')
        
        SLiB.messager('MAT Picker stopped!', 'none')

def SLiB_Converter():
    import SLiBConvert
    reload(SLiBConvert)

def SLiB_UserLiB(x):
    if x == 'save':
        path = cmds.optionMenu('sl_OB_library', q=1, v=1)
        if path and os.path.isdir(path):
            f = open(os.path.dirname(cmds.pluginInfo('SLiB', q=1, path=1)) + '/SLiB.env', 'w')
            f.write(path)
            f.close()
    
    if x == 'load':
        path = open(os.path.dirname(cmds.pluginInfo('SLiB', q=1, path=1)) + '/SLiB.env').readline()
        if path and os.path.isdir(path):
            mel.eval('putenv "SLiBRARY" "' + path + '"')
            SLiB_FillLib()
            cmds.optionMenu('sl_OB_library', e=1, v=path)
            SLiB_SwitchLib()

def SLiB_DomeRot():
    if cmds.objExists('SLiB_Dome'):
        cmds.select('SLiB_Dome')
        cmds.setToolTo('Rotate')
        
        if SLiB.gib('renderer') == 'vray':
            envTex = cmds.listConnections('SLiB_Dome', type='VRayPlaceEnvTex')
            if envTex:
                cmds.setAttr(envTex[0] + '.useTransform', 1)
                cmds.rename(envTex[0], 'SLiB_VRayPlaceEnvTex')

def SLiB_DelDome():
    for e in ['SLiB_Dome', 'SLiB_VRayPlaceEnvTex', 'SLiB_DomeLight_Lyr']:
        SLiB.delete(e)