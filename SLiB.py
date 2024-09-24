#########################################################################
#
#   SLiB
#
#   Version:    2.0
#   Author:     DGDM
#   Copyright:  2016 DGDM
#
#########################################################################

import sys
import os
import imp
import maya.cmds as cmds
import maya.mel as mel
import importlib

dirPath = os.path.dirname(cmds.pluginInfo('SLiB', q=1, path=1)) + '/SLiB/'
envFile = os.path.dirname(cmds.pluginInfo('SLiB', q=1, path=1)) + '/SLiB.env'

if dirPath and os.path.isdir(dirPath):
    guiPath = dirPath + '/' + 'gui' + '/'
    imgPath = dirPath + '/' + 'img' + '/'
    pytPath = dirPath + '/' + 'pyt' + '/'
    sys.path.append(pytPath)
    
    if os.path.isfile(envFile):
        libPath = open(os.path.dirname(cmds.pluginInfo('SLiB', q=1, path=1)) + '/SLiB.env').readline()
        if libPath:
            mel.eval('putenv "SLiBLib" "' + libPath + '"')
    else:
        if cmds.window('slSetup', ex=1):
            cmds.deleteUI('slSetup')

        libPath = os.path.dirname(cmds.pluginInfo('SLiB', q=1, path=1)) + '/SLiB/lib/'
                
        cmds.window('slSetup', t=' ', sizeable=0)
        cmds.columnLayout('setupWinLayout', w=256, co=['both', 5], adj=1, bgc=[0.18,0.18,0.18], p='slSetup')
        cmds.text(l='BROWSER PRO 2.0 SETUP', w=256, h=50, p='setupWinLayout')
        cmds.text(l='Please set your Library:', w=256, h=50, p='setupWinLayout')
        cmds.button(l='DEFAULT', h=30, bgc=[0,0.75,0.99], c=lambda *args: setup(libPath), p='setupWinLayout')
        cmds.button(l='NEW', h=30, bgc=[0,0.75,0.99], c=lambda *args: setPath(), p='setupWinLayout')
        cmds.button(l='EXISTING', h=30, bgc=[0,0.75,0.99], c=lambda *args: setPath(), p='setupWinLayout')
        cmds.text(l='', w=256, h=20, p='setupWinLayout')
        cmds.showWindow('slSetup')
        cmds.window('slSetup', e=1, w=256, h=210)

    mel.eval('putenv "SLiB"           "' + dirPath + '"')
    mel.eval('putenv "SLiBGui"        "' + guiPath + '"')
    mel.eval('putenv "SLiBImage"      "' + imgPath + '"')
    mel.eval('putenv "SLiBPyt"        "' + pytPath + '"')
    
else:
    cmds.warning('SLiB folder not found!')
    cmds.unloadPlugin('SLiB.py', f=1)
    mel.eval('putenv "SLiB" "' '"')
    sys.exit()

def initializePlugin(obj):
    import SLiBSetupPy
    importlib.reload(SLiBSetupPy)
    SLiBSetupPy.SLiBSetupLoad()
    print('SLiB: >>> Plug-In successfully loaded!')

def uninitializePlugin(obj):
    import SLiBSetupPy
    importlib.reload(SLiBSetupPy)
    SLiBSetupPy.SLiBSetupUnLoad()
    print("SLiB: >>> Plug-In unloaded!")
    
def setPath():
    libPath = cmds.fileDialog2(fm=2)
    if libPath and os.path.isdir(libPath[0]):
        setup(libPath[0] + '/')
    else:
        cmds.warning('SLiB Folder not set?!')
        sys.exit()
        
def setup(libPath):
    try:
        if libPath and os.path.isdir(libPath):
            mel.eval('putenv "SLiBLib"        "' + libPath + '"')
            for e in ['shader', 'objects', 'lights', 'hdri', 'textures', 'maps']:
                if os.path.isdir(os.path.join(libPath, e)) != 1:
                    os.mkdir(os.path.join(libPath, e))
                    
            f = open(os.path.dirname(cmds.pluginInfo('SLiB', q=1, path=1)) + '/SLiB.env', 'w')
            f.write(mel.eval('getenv SLiBLib;'))
            f.close()
    except:
        cmds.warning('SLiB.env not created! Check file write permission on Maya plugin folder.')
        
    if cmds.window('slSetup', ex=1):
        cmds.deleteUI('slSetup')