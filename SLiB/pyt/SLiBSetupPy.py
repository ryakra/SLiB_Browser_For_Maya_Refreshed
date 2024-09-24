#########################################################################
#
#   SLiB Setup
#
#   Version:    1.1
#   Author:     DGDM
#   Copyright:  2017 DGDM
#
#########################################################################


import maya.cmds as cmds
import maya.mel as mel
import os

SLiBImage = mel.eval('getenv SLiBImage;')
pytPath = os.path.dirname(cmds.pluginInfo('SLiB', q=1, path=1)) + '/SLiB/pyt/'
MAYA_VERSION = cmds.about(version=1)

def SLiBSetupSM():
    gMainWindow = mel.eval('$temp1=$gMainWindow')
    if cmds.menu('SLiBMenu', q=1, ex=1):
        cmds.deleteUI('SLiBMenu', menu=1)
    if cmds.shelfLayout("SLiB", ex=1):
        cmds.deleteUI("SLiB")
        
    SLiBMenu = cmds.menu('SLiBMenu', p=gMainWindow, to=1, l='SLiB')
    mel.eval('$scriptsShelf = `shelfLayout -cellWidth 33 -cellHeight 33 -p $gShelfTopLevel SLiB`;')

    #BROWSER
    if os.path.isfile(pytPath +  'SLiBBrowserPy.py'):
        if MAYA_VERSION != '2017':
            cmds.menuItem(parent = 'SLiBMenu', l='SLiB Browser ...', c='import SLiBBrowserPy; reload(SLiBBrowserPy); SLiBBrowserPy.SLiBBrowserUI()') #MENU ENTRY
            cmds.shelfButton('browser', i=SLiBImage + 'shelf_browser.png', c='import SLiBBrowserPy; reload(SLiBBrowserPy); SLiBBrowserPy.SLiBBrowserUI()', p='SLiB') #SHELF BUTTON
        else:
            cmds.menuItem(parent = 'SLiBMenu', l='SLiB Browser ...', c='import SLiBBrowserPy; reload(SLiBBrowserPy); SLiBBrowserPy.SLiBBrowserWorkspaceControl()') #MENU ENTRY
            cmds.shelfButton('browser', i=SLiBImage + 'shelf_browser.png', c='import SLiBBrowserPy; reload(SLiBBrowserPy); SLiBBrowserPy.SLiBBrowserWorkspaceControl()', p='SLiB') #SHELF BUTTON
        
        cmds.menuItem(parent = 'SLiBMenu', d=1)
    
    #FLOORGEN
    if os.path.isfile(pytPath +  'SLiBFloorGenPY.py'):
        cmds.menuItem(parent = 'SLiBMenu', l='SLiB FloorGen ...', c='import SLiBFloorGenPY; reload(SLiBFloorGenPY)') #MENU ENTRY
        cmds.shelfButton('floorgen', i=SLiBImage + 'shelf_floorgen.png', c='import SLiBFloorGenPY; reload(SLiBFloorGenPY)', p='SLiB') #SHELF BUTTON
        
        cmds.menuItem(parent = 'SLiBMenu', d=1) 
    
    #LEUCHTKRAFT
    if os.path.isfile(pytPath +  'SLiBLeuchtkraftPY.py'):
        if MAYA_VERSION != '2017':
            cmds.menuItem(parent = 'SLiBMenu', l='SLiB Leuchtkraft ...', c='import SLiBLeuchtkraftPY; reload(SLiBLeuchtkraftPY); SLiBLeuchtkraftPY.SLiBLeuchtkraftUI()') #MENU ENTRY
            cmds.shelfButton('leuchtkraft', i=SLiBImage + 'shelf_leuchtkraft.png', c='import SLiBLeuchtkraftPY; reload(SLiBLeuchtkraftPY); SLiBLeuchtkraftPY.SLiBLeuchtkraftUI()', p='SLiB') #SHELF BUTTON
        else:
            cmds.menuItem(parent = 'SLiBMenu', l='SLiB Leuchtkraft ...', c='import SLiBLeuchtkraftPY; reload(SLiBLeuchtkraftPY); SLiBLeuchtkraftPY.SLiBLeuchtkraftWorkspaceControl()') #MENU ENTRY
            cmds.shelfButton('leuchtkraft', i=SLiBImage + 'shelf_leuchtkraft.png', c='import SLiBLeuchtkraftPY; reload(SLiBLeuchtkraftPY); SLiBLeuchtkraftPY.SLiBLeuchtkraftWorkspaceControl()', p='SLiB') #SHELF BUTTON
        
        cmds.menuItem(parent = 'SLiBMenu', d=1) 
    
    #PARTIKEL
    if os.path.isfile(pytPath +  'SLiBPartikelPY.py'):
        cmds.menuItem(parent = 'SLiBMenu', l='SLiB Partikel ...', c='import SLiBPartikelPY; reload(SLiBPartikelPY); SLiBPartikelPY.partikel()') #MENU ENTRY
        cmds.shelfButton('partikel', i=SLiBImage + 'shelf_partikel.png', c='import SLiBPartikelPY; reload(SLiBPartikelPY); SLiBPartikelPY.partikel()', p='SLiB') #SHELF BUTTON
        
        cmds.menuItem(parent = 'SLiBMenu', d=1)
    
    #MATCH
    if os.path.isfile(pytPath +  'SLiBMatchPY.py'):
        cmds.menuItem(parent = 'SLiBMenu', l='SLiB Match ...', c='import SLiBMatchPY; reload(SLiBMatchPY); SLiBMatchPY.match_UI()') #MENU ENTRY
        cmds.shelfButton('match', i=SLiBImage + 'shelf_match.png', c='import SLiBMatchPY; reload(SLiBMatchPY); SLiBMatchPY.match_UI()', p='SLiB') #SHELF BUTTON
        
        cmds.menuItem(parent = 'SLiBMenu', d=1) 
    
    #VPR
    if os.path.isfile(pytPath +  'SLiB_VPR.py'):
        if MAYA_VERSION != '2017':
            cmds.menuItem(parent = 'SLiBMenu', l='SLiB VPR ...', c='import SLiB_VPR; reload(SLiB_VPR); SLiB_VPR.VPRStart()') #MENU ENTRY
            cmds.shelfButton('vpr', i=SLiBImage + 'shelf_vpr.png', c='import SLiB_VPR; reload(SLiB_VPR); SLiB_VPR.VPRStart()', p='SLiB') #SHELF BUTTON
        else:
            cmds.menuItem(parent = 'SLiBMenu', l='SLiB VPR ...', c='import SLiB_VPR; reload(SLiB_VPR); SLiB_VPR.vprWorkspaceControl()') #MENU ENTRY
            cmds.shelfButton('vpr', i=SLiBImage + 'shelf_vpr.png', c='import SLiB_VPR; reload(SLiB_VPR); SLiB_VPR.vprWorkspaceControl()', p='SLiB') #SHELF BUTTON
        
        cmds.menuItem(parent = 'SLiBMenu', d=1) 
        
        #WEB
        cmds.menuItem(parent = 'SLiBMenu', l='Homepage', c='import maya;maya.cmds.showHelp("http://store.cgfront.com", absolute=1)') #MENU ENTRY

def SLiBSetupLoad():
    SLiBSetupSM()
    print 'SLiB: >>> Menu Entry and Shelf created!'

def SLiBSetupUnLoad():
    if cmds.menu('SLiBMenu', q=1, ex=1):
        cmds.deleteUI('SLiBMenu', menu=1)
    if cmds.shelfLayout("SLiB", ex=1):
        cmds.deleteUI("SLiB")
    print 'SLiB: >>> Menu Entry and Shelf removed!'