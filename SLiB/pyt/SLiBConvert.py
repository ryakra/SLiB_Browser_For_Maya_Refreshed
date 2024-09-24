#########################################################################
#
#   SLiBConvert
#
#   Version:    0.1
#   Author:     DGDM
#   Copyright:  2016 DGDM
#
#########################################################################

import maya.cmds as cmds

def checkBlend(e):
    for b in blendMat:
        if e in cmds.ls(cmds.listConnections(b), mat=1):
            return False
        else:
            return True
            
def dispatch(node):
    if cmds.nodeType(node) == 'VRayBlendMtl':
        return 'RedshiftMaterialBlender'
    if cmds.nodeType(node) == 'VRayMtl':
        return 'RedshiftMaterial'
    if cmds.nodeType(node) == 'VRayCarPaintMtl':
        return 'RedshiftCarPaint'
    if cmds.nodeType(node) == 'VRayFastSSS2':
        return 'RedshiftSubSurfaceScatter'
    if cmds.nodeType(node) == 'VRaySkinMtl':
        return 'RedshiftSkin'
    if cmds.nodeType(node) == 'VRayFresnel':
        return 'RedshiftFresnel'
    if cmds.nodeType(node) == 'VRayDirt':
        return 'RedshiftAmbientOcclusion'
    if cmds.nodeType(node) == 'displacementShader':
        return 'RedshiftDisplacement'
    if cmds.nodeType(node) == 'bump2d':
        return 'RedshiftBumpMap'    
        
def assignMaterial(sourceMAT, destMAT):
    sourceSG = cmds.listConnections(sourceMAT, type='shadingEngine')[0]
    destSG = cmds.sets(n=destMAT + 'SG', r=1, nss=1, em=1)
    cmds.connectAttr(destMAT + '.outColor', destSG + '.surfaceShader')
    
    #CHECK DISPLACEMENT
    displacement = cmds.listConnections(sourceSG + '.displacementShader')
    if displacement:
        dTex = cmds.listConnections(displacement[0] + '.d', type='file')[0]
        displacementRS = cmds.shadingNode('RedshiftDisplacement', au=1, n=displacement[0]+'_RS')
        cmds.connectAttr(dTex + '.outColor', displacementRS + '.texMap')
        cmds.connectAttr(displacementRS + '.out',  destSG + '.rsDisplacementShader')
    
    componentsWithMaterial = cmds.sets(sourceSG, q=1)
    cmds.select(componentsWithMaterial)
    cmds.hyperShade(a=destMAT)

def checkAttribs(sourceMAT, destMAT):
    mtlAttrList = None
    if cmds.nodeType(sourceMAT) == 'VRayMtl':
        mtlAttrList = \
        [("diffuse_color", "color"),\
        ("diffuse_weight", "diffuseColorAmount"),\
        ("opacity_color","opacityMap"),\
        ("diffuse_roughness","roughnessAmount"),\
        ("refl_color","reflectionColor"),\
        ("refl_weight","reflectionColorAmount"),\
        ("refl_roughness","reflectionGlossiness"),\
        ("refl_ior","fresnelIOR"),\
        ("refl_depth","reflectionsMaxDepth"),\
        ("refr_ior","refractionIOR"),\
        ("refr_color","refractionColor"),\
        ("refr_weight","refractionColorAmount"),\
        ("refr_roughness","refractionGlossiness"),\
        ("refl_aniso","anisotropy"),\
        ("refl_aniso_rotation","anisotropyRotation"),\
        ("emission_color","illumColor"),\
        ("bump_input","bm")]
        
    if cmds.nodeType(sourceMAT) == 'VRayCarPaintMtl':
        mtlAttrList = \
        [("base_color", "color"),\
        ("spec_weight", "base_reflection"),\
        ("spec_gloss","base_glossiness"),\
        ("flake_color","flake_color"),\
        ("flake_gloss","flake_glossiness"),\
        ("flake_density","flake_density"),\
        ("flake_scale","flake_scale"),\
        ("clearcoat_color","coat_color"),\
        ("clearcoat_weight","coat_strength"),\
        ("clearcoat_gloss","coat_glossiness")]
        
    if cmds.nodeType(sourceMAT) == 'VRayFastSSS2':
        mtlAttrList = \
        [("ior", "ior"),\
        ("scale", "scale"),\
        ("scatter_radius","scatterRadiusMult"),\
        ("sub_surface_color","subsurfaceColor"),\
        ("scatter_color","scatterRadiusColor"),\
        ("diffuse_amount","diffuseAmount"),\
        ("reflectivity","reflectionAmount"),\
        ("refl_color","reflection"),\
        ("refl_gloss","glossiness")]
        
    if cmds.nodeType(sourceMAT) == 'VRaySkinMtl':
        mtlAttrList = \
        [("radius_scale", "scale"),\
        ("diffuse_amount","diffuseAmount"),\
        ("shallow_color","shallowColor"),\
        ("shallow_weight","shallowAmount"),\
        ("shallow_radius","shallowRadius"),\
        ("mid_color","mediumColor"),\
        ("mid_weight","mediumAmount"),\
        ("mid_radius","mediumRadius"),\
        ("deep_color","deepColor"),\
        ("deep_weight","deepAmount"),\
        ("deep_radius","deepRadius"),\
        ("refl_color0","primaryReflectonColor"),\
        ("refl_weight0","primaryReflectionAmount"),\
        ("refl_gloss0","primaryReflectionGlossiness"),\
        ("refl_color1","secondaryReflectonColor"),\
        ("refl_weight1","secondaryReflectionAmount"),\
        ("refl_gloss1","secondaryReflectionGlossiness")]
    
    for a in mtlAttrList:
        print('...checking Attribute >>> ' + a[1])
        if cmds.objExists(sourceMAT + '.' + a[1]):
            if a[1] == 'fresnelIOR':
                if cmds.getAttr(sourceMAT + '.lockFresnelIORToRefractionIOR'):
                    a = ("refl_ior","refractionIOR")
            
            isConnection = cmds.connectionInfo(sourceMAT + "." + a[1], isDestination=1)
            if isConnection:
                whatConnection = cmds.connectionInfo(sourceMAT + "." + a[1], sourceFromDestination=1)
                
                #BUMP OR NORMAL MAP
                if a[1] == 'bm':
                    print('Bump Slot -  Connection found')
                    if cmds.nodeType(whatConnection.split('.')[0]) == 'file':
                        connNode = whatConnection.split('.')[0]
                        if cmds.getAttr(sourceMAT + '.bumpMapType') == 0:
                            rsBump = cmds.shadingNode('RedshiftBumpMap', au=1, n=destMAT + '_Bump')
                            cmds.connectAttr(connNode + '.outColor', rsBump + '.input')
                            cmds.connectAttr(rsBump + '.out', destMAT + '.bump_input')
                        else:
                            rsNormal = cmds.shadingNode('RedshiftNormalMap', au=1, n=destMAT + '_Normal')
                            normalTex = cmds.getAttr(connNode + '.fileTextureName')
                            cmds.setAttr(rsNormal + '.tex0', normalTex, type='string')
                            cmds.connectAttr(rsNormal + '.outDisplacementVector', destMAT + '.bump_input')
                  
                else:
                    outAttr = whatConnection
                    inAttr = (destMAT + "." + a[0])
                    cmds.connectAttr(outAttr, inAttr)
                    
            else:
                outAttr = cmds.getAttr(sourceMAT + "." + a[1])
                if a[1] in ['reflectionGlossiness', 'refractionGlossiness', 'base_glossiness', 'flake_glossiness', 'coat_glossiness', 'glossiness', 'primaryReflectionGlossiness', 'secondaryReflectionGlossiness']:
                    outAttr = abs(outAttr-1)

                inAttr = (destMAT + "." + a[0])
                try:
                    cmds.setAttr(inAttr, outAttr)
                except:
                    newOutAttr = str((outAttr)[0]).replace('(','').replace(')','').split(',')
                    cmds.setAttr(inAttr, float(newOutAttr[0]), float(newOutAttr[1]), float(newOutAttr[2]), type="double3")


def collectMats():
    global blendMat, normMat, carMat, sssMat, skinMat, domeLight
    blendMat, normMat, carMat, sssMat, skinMat, domeLight = [], [], [], [], [], []

    for e in cmds.ls(mat=1):
        if cmds.nodeType(e) == 'VRayBlendMtl':
            blendMat.append(e)

    for e in cmds.ls(mat=1):  
        if cmds.nodeType(e) == 'VRayMtl':
            if blendMat:
                if checkBlend(e):
                    normMat.append(e)
            else:
                normMat.append(e)
        if cmds.nodeType(e) == 'VRayCarPaintMtl':
            if blendMat:
                if checkBlend(e):
                    carMat.append(e)
            else:
                carMat.append(e)
        if cmds.nodeType(e) == 'VRayFastSSS2':
            if blendMat:
                if checkBlend(e):
                    sssMat.append(e)
            else:
                sssMat.append(e)
        if cmds.nodeType(e) == 'VRaySkinMtl':
            if blendMat:
                if checkBlend(e):
                    skinMat.append(e)
            else:
                skinMat.append(e)
                
    print(str(len(blendMat)) + ' VRayBlendMtl')
    print(str(len(normMat)) + ' VRayMtl')
    print(str(len(carMat)) + ' VRayCarPaintMtl')
    print(str(len(sssMat)) + ' VRayFastSSS2')
    print(str(len(skinMat)) + ' VRaySkinMtl')
            


def SLiB_Convert():
    collectMats()
    if blendMat:
        cmds.progressBar('ConvertProgress', e=1, max=(len(blendMat)))
        cmds.textScrollList('ConvertScrollList', e=1, si=str(len(blendMat)) + ' VRayBlendMtl')
        for e in blendMat:
            cmds.progressBar('ConvertProgress', e=1, step=1)
            print('converting Material >>> ' + e + ' [ ' + cmds.nodeType(e) + ' ]')
            blendMat_RS = cmds.shadingNode('RedshiftMaterialBlender', asShader=1, n=e + '_to_RS')
            baseMaterial = cmds.listConnections(e + '.bm')
            baseMaterialAdditive = cmds.getAttr(e + '.am')
            if baseMaterial:
                print('converting BaseMaterial of ' + e)
                baseMaterial = baseMaterial[0]
                baseMaterial_RS = cmds.shadingNode(dispatch(baseMaterial), asShader=1, n=baseMaterial + '_to_RS')
                checkAttribs(baseMaterial, baseMaterial_RS)
                cmds.connectAttr(baseMaterial_RS + '.outColor', blendMat_RS + '.baseColor', f=1)
           
            for r in range(0,5):
                coatMaterial = cmds.listConnections(e + '.cm' + str(r))
                blendAmount = cmds.listConnections(e + '.blend_amount_' + str(r))
                if coatMaterial:
                    print('converting CoatMaterial of ' + e + ' [ ' + str(r) + ' ]')
                    coatMaterial = coatMaterial[0]
                    coatMaterial_RS = cmds.shadingNode(dispatch(coatMaterial), asShader=1, n=coatMaterial + '_to_RS')
                    checkAttribs(coatMaterial, coatMaterial_RS)
                    cmds.connectAttr(coatMaterial_RS + '.outColor', blendMat_RS + '.layerColor' + str(r+1), f=1)
                if blendAmount:
                    print('converting BlendAmount of ' + e + ' [ ' + str(r) + ' ]')
                    blendAmount = blendAmount[0]
                    if cmds.nodeType(blendAmount) == 'file':
                        cmds.connectAttr(blendAmount + '.outColor', blendMat_RS + '.blendColor' + str(r+1), f=1)
                else:
                    blendAmount = cmds.getAttr(e + '.blend_amount_' + str(r))
                    blendAmount = str((blendAmount)[0]).replace('(','').replace(')','').split(',')
                    cmds.setAttr(blendMat_RS + '.blendColor' + str(r+1), float(blendAmount[0]), float(blendAmount[1]), float(blendAmount[2]), type="double3")
                    if cmds.getAttr(e + '.additive_mode'):
                        cmds.setAttr(blendMat_RS + '.additiveMode' + str(r+1), 1)
                                    
            assignMaterial(e, blendMat_RS)
            print(e + ' successfully converted!')
            cmds.progressBar('ConvertProgress', e=1, pr=0)
        
    if normMat or carMat or sssMat or skinMat:
        cmds.progressBar('ConvertProgress', e=1, max=(len(normMat + carMat + sssMat + skinMat)))
        for e in normMat + carMat + sssMat + skinMat:
            if e in normMat:
                cmds.textScrollList('ConvertScrollList', e=1, si=str(len(normMat)) + ' VRayMtl')
            if e in carMat:
                cmds.textScrollList('ConvertScrollList', e=1, si=str(len(carMat)) + ' VRayCarPaintMtl')
            if e in sssMat:
                cmds.textScrollList('ConvertScrollList', e=1, si=str(len(sssMat)) + ' VRayFastSSS2')
            if e in skinMat:
                cmds.textScrollList('ConvertScrollList', e=1, si=str(len(skinMat)) + ' VRaySkinMtl')

            cmds.progressBar('ConvertProgress', e=1, step=1)
            print('converting Material >>> ' + e + ' [ ' + cmds.nodeType(e) + ' ]')
            convMaterial = cmds.shadingNode(dispatch(e), asShader=1, n=e + '_to_RS')
            checkAttribs(e, convMaterial)
            
            assignMaterial(e, convMaterial)
            print(e + ' successfully converted!')
            cmds.select(cl=1)
        cmds.progressBar('ConvertProgress', e=1, pr=0)
        
def SLiB_ConvertUI():
    if cmds.window('SLiB_ConvertUI', ex=1):
        cmds.deleteUI('SLiB_ConvertUI')
        
    if cmds.objExists('ConvertScrollList'):
        cmds.deleteUI('ConvertScrollList')

    cmds.window('SLiB_ConvertUI', t=' ', sizeable=0)
    cmds.columnLayout('ConvertUILayout', w=256, adj=1, bgc=[0.18,0.18,0.18], p='SLiB_ConvertUI')
    cmds.textScrollList('ConvertScrollList', h=100, numberOfRows=8, p='ConvertUILayout')
    collectMats()
    cmds.textScrollList('ConvertScrollList', e=1, append=[str(len(blendMat)) + ' VRayBlendMtl'])
    cmds.textScrollList('ConvertScrollList', e=1, append=[str(len(normMat)) + ' VRayMtl'])
    cmds.textScrollList('ConvertScrollList', e=1, append=[str(len(carMat)) + ' VRayCarPaintMtl'])
    cmds.textScrollList('ConvertScrollList', e=1, append=[str(len(sssMat)) + ' VRayFastSSS2'])
    cmds.textScrollList('ConvertScrollList', e=1, append=[str(len(skinMat)) + ' VRaySkinMtl'])
    
    cmds.progressBar('ConvertProgress', h=10, p='ConvertUILayout')
    cmds.button('ConvertButton', l='convert', h=30, bgc=[0,0.75,0.99], c=lambda *args: SLiB_Convert(), p='ConvertUILayout')


    cmds.showWindow('SLiB_ConvertUI')
    cmds.window('SLiB_ConvertUI', e=1, w=256, h=140)
SLiB_ConvertUI()