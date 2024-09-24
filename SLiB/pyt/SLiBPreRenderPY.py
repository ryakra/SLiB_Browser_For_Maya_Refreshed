#########################################################################
#
#   SLiBPreRenderPY
#
#   Version:    2.0
#   Author:     DGDM
#   Copyright:  2016 DGDM
#
#########################################################################

import maya.cmds as cmds
import maya.mel as mel
import os

SLiB_dir = mel.eval('getenv SLiB;')

#SHADER
def swapMat():
    beforeSG = set(cmds.ls(type='shadingEngine'))
    if os.path.isfile(SLiB_dir + '/scn/Temp/temp_preview_mat.ma'):
        tempMat = SLiB_dir + '/scn/Temp/temp_preview_mat.ma'
    else:
        tempMat = SLiB_dir + '/scn/Temp/temp_preview_mat.mb'
    imported = cmds.file(tempMat, i=1, uns=0, rnn=1, iv=1)
    afterSG  = set(cmds.ls(type='shadingEngine'))
    SG = ', '.join(afterSG.difference(beforeSG))
    
    replaceMat = 'replace_me_MAT'
    
    results = cmds.sets('replace_meSG', q=True) or [] 
    add_suffix = lambda p:  p + ".f[*]" if not '.f' in p else p
    results = [ add_suffix(r) for r in results]
    matFaces = cmds.filterExpand(*results, sm=34) or []

    for e in matFaces:
        cmds.sets(e, e=1, forceElement=SG)

#OBJECTS

def swapObj():
    if os.path.isfile(SLiB_dir + '/scn/Temp/temp_preview_obj.ma'):
        tempObj = SLiB_dir + '/scn/Temp/temp_preview_obj.ma'
    else:
        tempObj = SLiB_dir + '/scn/Temp/temp_preview_obj.mb'
    
    imp = cmds.file(tempObj, i=1, uns=0, rnn=1, iv=1)
    selection = cmds.ls(imp, assemblies=1)
    
    bbox = cmds.exactWorldBoundingBox(selection)

    ObjX = abs(bbox[0]) + abs(bbox[3])
    ObjY = abs(bbox[1]) + abs(bbox[4])
    ObjZ = abs(bbox[2]) + abs(bbox[5])

    longestSide = sorted([ObjX, ObjY, ObjZ], key=float)[2]

    cmds.setAttr('cam_grp.sx', longestSide / 1.75)
    cmds.setAttr('cam_grp.sy', longestSide / 1.75)
    cmds.setAttr('cam_grp.sz', longestSide / 1.75)
    
    for c in ['renderCam_Front', 'renderCam_Persp_R', 'renderCam_Persp_L']:
        cmds.viewPlace(c, la=[0, ObjY/2, 0])

