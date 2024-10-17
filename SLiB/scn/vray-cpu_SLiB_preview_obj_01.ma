//Maya ASCII 2025ff03 scene
//Name: vray-cpu_SLiB_preview_obj_01.ma
//Last modified: Thu, Oct 17, 2024 02:31:08 AM
//Codeset: 1252
requires maya "2025ff03";
requires -nodeType "VRaySettingsNode" -nodeType "VRayLightDomeShape" -nodeType "VRayPlaceEnvTex"
		 -dataType "VRaySunParams" -dataType "vrayFloatVectorData" -dataType "vrayFloatVectorData"
		 -dataType "vrayIntData" "vrayformaya" "6";
requires -nodeType "aiOptions" -nodeType "aiAOVDriver" -nodeType "aiAOVFilter" -nodeType "aiImagerDenoiserOidn"
		 "mtoa" "5.4.2.1";
requires -nodeType "mayaUsdLayerManager" -dataType "pxrUsdStageData" "mayaUsdPlugin" "0.28.0";
requires -nodeType "renderSetup" "renderSetup.py" "1.0";
requires "redshift4maya" "2.0.72";
currentUnit -l centimeter -a degree -t pal;
fileInfo "application" "maya";
fileInfo "product" "Maya 2025";
fileInfo "version" "2025";
fileInfo "cutIdentifier" "202407121012-8ed02f4c99";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 22631)";
fileInfo "vrayBuild" "6.20.03 32743 88ba3e8";
fileInfo "UUID" "EA5E74B5-42CB-AC0A-109F-C2AD3964B8F3";
createNode transform -s -n "persp";
	rename -uid "33A0825E-4D9E-CF70-7808-91ABD8CBD088";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 5.6391372874935497 10.527301142234478 19.320529733671041 ;
	setAttr ".r" -type "double3" 338.12811838464228 2897.3999999924863 0 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "1F4EF882-40E9-BC04-8739-8AB7C8841F1B";
	addAttr -ci true -sn "rsCameraMotionBlur" -ln "rsCameraMotionBlur" -dv 1 -min 0 
		-max 1 -at "bool";
	addAttr -ci true -sn "rsCameraType" -ln "rsCameraType" -min 0 -max 5 -en "Standard:Fisheye=2:Spherical:Cylindrical:Stereo Spherical" 
		-at "enum";
	addAttr -ci true -sn "rsFisheyeScaleX" -ln "rsFisheyeScaleX" -dv 1 -min 0 -max 3.4028234600000001e+38 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeScaleY" -ln "rsFisheyeScaleY" -dv 1 -min 0 -max 3.4028234600000001e+38 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeAngle" -ln "rsFisheyeAngle" -dv 180 -min 1 -max 180 
		-at "double";
	addAttr -ci true -sn "rsCylindricalIsOrtho" -ln "rsCylindricalIsOrtho" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "rsCylindricalFovH" -ln "rsCylindricalFovH" -dv 360 -min 0 
		-max 360 -at "double";
	addAttr -ci true -sn "rsCylindricalFovV" -ln "rsCylindricalFovV" -dv 180 -min 0 
		-max 180 -at "double";
	addAttr -ci true -sn "rsCylindricalOrthoHeight" -ln "rsCylindricalOrthoHeight" -dv 
		100 -min 0 -max 3.4028234600000001e+38 -smn 1 -smx 500 -at "double";
	addAttr -ci true -k true -sn "rsStereoSphericalMode" -ln "rsStereoSphericalMode" 
		-min 0 -max 3 -en "Side By Side:Top Bottom:Left Only:Right Only" -at "enum";
	addAttr -ci true -sn "rsStereoSphericalSeparation" -ln "rsStereoSphericalSeparation" 
		-min 0 -max 3.4028234600000001e+38 -at "double";
	addAttr -ci true -sn "rsStereoSphericalFovH" -ln "rsStereoSphericalFovH" -dv 360 
		-min 0 -max 360 -at "double";
	addAttr -ci true -sn "rsStereoSphericalFovV" -ln "rsStereoSphericalFovV" -dv 180 
		-min 0 -max 180 -at "double";
	addAttr -ci true -sn "rsStereoCubeSeparation" -ln "rsStereoCubeSeparation" -min 
		0 -max 3.4028234600000001e+38 -at "double";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsLensShader" -ln "rsLensShader" -at "message";
	addAttr -s false -ci true -m -sn "rsLensShaderList" -ln "rsLensShaderList" -at "message";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".ff" 2;
	setAttr ".ovr" 1.3;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 21.311045421195715;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0.70873284339904785 19.359516096163716 -0.66257447004318237 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".dr" yes;
createNode transform -s -n "top";
	rename -uid "69650F86-403D-8704-4DF7-D1B9A8F4D566";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 3.6422676521211454 100.1 -0.9991149872871683 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "9BCFD184-4105-4509-2208-798C66CE7379";
	addAttr -ci true -sn "rsCameraMotionBlur" -ln "rsCameraMotionBlur" -dv 1 -min 0 
		-max 1 -at "bool";
	addAttr -ci true -sn "rsCameraType" -ln "rsCameraType" -min 0 -max 5 -en "Standard:Fisheye=2:Spherical:Cylindrical:Stereo Spherical" 
		-at "enum";
	addAttr -ci true -sn "rsFisheyeScaleX" -ln "rsFisheyeScaleX" -dv 1 -min 0 -max 3.4028234600000001e+38 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeScaleY" -ln "rsFisheyeScaleY" -dv 1 -min 0 -max 3.4028234600000001e+38 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeAngle" -ln "rsFisheyeAngle" -dv 180 -min 1 -max 180 
		-at "double";
	addAttr -ci true -sn "rsCylindricalIsOrtho" -ln "rsCylindricalIsOrtho" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "rsCylindricalFovH" -ln "rsCylindricalFovH" -dv 360 -min 0 
		-max 360 -at "double";
	addAttr -ci true -sn "rsCylindricalFovV" -ln "rsCylindricalFovV" -dv 180 -min 0 
		-max 180 -at "double";
	addAttr -ci true -sn "rsCylindricalOrthoHeight" -ln "rsCylindricalOrthoHeight" -dv 
		100 -min 0 -max 3.4028234600000001e+38 -smn 1 -smx 500 -at "double";
	addAttr -ci true -k true -sn "rsStereoSphericalMode" -ln "rsStereoSphericalMode" 
		-min 0 -max 3 -en "Side By Side:Top Bottom:Left Only:Right Only" -at "enum";
	addAttr -ci true -sn "rsStereoSphericalSeparation" -ln "rsStereoSphericalSeparation" 
		-min 0 -max 3.4028234600000001e+38 -at "double";
	addAttr -ci true -sn "rsStereoSphericalFovH" -ln "rsStereoSphericalFovH" -dv 360 
		-min 0 -max 360 -at "double";
	addAttr -ci true -sn "rsStereoSphericalFovV" -ln "rsStereoSphericalFovV" -dv 180 
		-min 0 -max 180 -at "double";
	addAttr -ci true -sn "rsStereoCubeSeparation" -ln "rsStereoCubeSeparation" -min 
		0 -max 3.4028234600000001e+38 -at "double";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsLensShader" -ln "rsLensShader" -at "message";
	addAttr -s false -ci true -m -sn "rsLensShaderList" -ln "rsLensShaderList" -at "message";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 63.347517424429427;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "12186C1B-4E07-8409-D9CB-CB8348A77FA5";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -0.0669164323455953 6.1187719738813513 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "97B6C8B8-4058-3A9A-6938-5782A4CA8687";
	addAttr -ci true -sn "rsCameraMotionBlur" -ln "rsCameraMotionBlur" -dv 1 -min 0 
		-max 1 -at "bool";
	addAttr -ci true -sn "rsCameraType" -ln "rsCameraType" -min 0 -max 5 -en "Standard:Fisheye=2:Spherical:Cylindrical:Stereo Spherical" 
		-at "enum";
	addAttr -ci true -sn "rsFisheyeScaleX" -ln "rsFisheyeScaleX" -dv 1 -min 0 -max 3.4028234600000001e+38 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeScaleY" -ln "rsFisheyeScaleY" -dv 1 -min 0 -max 3.4028234600000001e+38 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeAngle" -ln "rsFisheyeAngle" -dv 180 -min 1 -max 180 
		-at "double";
	addAttr -ci true -sn "rsCylindricalIsOrtho" -ln "rsCylindricalIsOrtho" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "rsCylindricalFovH" -ln "rsCylindricalFovH" -dv 360 -min 0 
		-max 360 -at "double";
	addAttr -ci true -sn "rsCylindricalFovV" -ln "rsCylindricalFovV" -dv 180 -min 0 
		-max 180 -at "double";
	addAttr -ci true -sn "rsCylindricalOrthoHeight" -ln "rsCylindricalOrthoHeight" -dv 
		100 -min 0 -max 3.4028234600000001e+38 -smn 1 -smx 500 -at "double";
	addAttr -ci true -k true -sn "rsStereoSphericalMode" -ln "rsStereoSphericalMode" 
		-min 0 -max 3 -en "Side By Side:Top Bottom:Left Only:Right Only" -at "enum";
	addAttr -ci true -sn "rsStereoSphericalSeparation" -ln "rsStereoSphericalSeparation" 
		-min 0 -max 3.4028234600000001e+38 -at "double";
	addAttr -ci true -sn "rsStereoSphericalFovH" -ln "rsStereoSphericalFovH" -dv 360 
		-min 0 -max 360 -at "double";
	addAttr -ci true -sn "rsStereoSphericalFovV" -ln "rsStereoSphericalFovV" -dv 180 
		-min 0 -max 180 -at "double";
	addAttr -ci true -sn "rsStereoCubeSeparation" -ln "rsStereoCubeSeparation" -min 
		0 -max 3.4028234600000001e+38 -at "double";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsLensShader" -ln "rsLensShader" -at "message";
	addAttr -s false -ci true -m -sn "rsLensShaderList" -ln "rsLensShaderList" -at "message";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 13.596379089637697;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "E489FC4C-445B-FB31-E758-8FAEACD7A189";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 108.49142641928825 0.14913436951257286 -0.64909659135049513 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "E6D30086-42B4-A3CB-D1D4-B38A2591AB65";
	addAttr -ci true -sn "rsCameraMotionBlur" -ln "rsCameraMotionBlur" -dv 1 -min 0 
		-max 1 -at "bool";
	addAttr -ci true -sn "rsCameraType" -ln "rsCameraType" -min 0 -max 5 -en "Standard:Fisheye=2:Spherical:Cylindrical:Stereo Spherical" 
		-at "enum";
	addAttr -ci true -sn "rsFisheyeScaleX" -ln "rsFisheyeScaleX" -dv 1 -min 0 -max 3.4028234600000001e+38 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeScaleY" -ln "rsFisheyeScaleY" -dv 1 -min 0 -max 3.4028234600000001e+38 
		-smn 0.1 -smx 10 -at "double";
	addAttr -ci true -sn "rsFisheyeAngle" -ln "rsFisheyeAngle" -dv 180 -min 1 -max 180 
		-at "double";
	addAttr -ci true -sn "rsCylindricalIsOrtho" -ln "rsCylindricalIsOrtho" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "rsCylindricalFovH" -ln "rsCylindricalFovH" -dv 360 -min 0 
		-max 360 -at "double";
	addAttr -ci true -sn "rsCylindricalFovV" -ln "rsCylindricalFovV" -dv 180 -min 0 
		-max 180 -at "double";
	addAttr -ci true -sn "rsCylindricalOrthoHeight" -ln "rsCylindricalOrthoHeight" -dv 
		100 -min 0 -max 3.4028234600000001e+38 -smn 1 -smx 500 -at "double";
	addAttr -ci true -k true -sn "rsStereoSphericalMode" -ln "rsStereoSphericalMode" 
		-min 0 -max 3 -en "Side By Side:Top Bottom:Left Only:Right Only" -at "enum";
	addAttr -ci true -sn "rsStereoSphericalSeparation" -ln "rsStereoSphericalSeparation" 
		-min 0 -max 3.4028234600000001e+38 -at "double";
	addAttr -ci true -sn "rsStereoSphericalFovH" -ln "rsStereoSphericalFovH" -dv 360 
		-min 0 -max 360 -at "double";
	addAttr -ci true -sn "rsStereoSphericalFovV" -ln "rsStereoSphericalFovV" -dv 180 
		-min 0 -max 180 -at "double";
	addAttr -ci true -sn "rsStereoCubeSeparation" -ln "rsStereoCubeSeparation" -min 
		0 -max 3.4028234600000001e+38 -at "double";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsLensShader" -ln "rsLensShader" -at "message";
	addAttr -s false -ci true -m -sn "rsLensShaderList" -ln "rsLensShaderList" -at "message";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 10.907404981489321;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "VRayLightDome1";
	rename -uid "996246E8-4A34-7B3E-DDA8-F5ADC6DC3149";
createNode VRayLightDomeShape -n "VRayLightDomeShape1" -p "VRayLightDome1";
	rename -uid "A9BD9134-4194-6E30-8FEF-2F98BB63EC74";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr -k off ".v";
	setAttr ".inv" yes;
	setAttr ".afa" no;
	setAttr ".udt" yes;
	setAttr ".dsp" yes;
	setAttr ".subs" 12;
	setAttr ".dadapt" yes;
	setAttr ".aal" -type "attributeAlias" 6 "lightColor" "color" "intensityMult" "intensity" "shadows" "useRayTraceShadows" ;
createNode transform -n "cam_grp";
	rename -uid "06FFFCFC-47EB-B369-9802-BC82B58BDB38";
createNode transform -n "renderCam_Front" -p "cam_grp";
	rename -uid "4D0F4FA9-4191-A38D-6CE8-03AEC48074B2";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" -6.1256326235886385e-16 0.89965297722845217 4.9980720957136233 ;
	setAttr ".s" -type "double3" 0.099961441914272461 0.099961441914272461 0.099961441914272461 ;
	setAttr ".rp" -type "double3" 6.5062448292418292e-17 0 -7.1026876408291501e-16 ;
	setAttr ".sp" -type "double3" 2.2204460492503139e-15 -1.7763568394002505e-15 0 ;
	setAttr ".spt" -type "double3" -1.9984870604744032e-15 1.5987896483795217e-15 0 ;
createNode camera -n "renderCam_FrontShape" -p "renderCam_Front";
	rename -uid "2A8534B6-477A-8ABC-CD94-6DAB13291669";
	setAttr -k off ".v";
	setAttr ".ff" 2;
	setAttr ".ovr" 1.3;
	setAttr ".fl" 50;
	setAttr ".fs" 2;
	setAttr ".fd" 21;
	setAttr ".coi" 80.068987945235975;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0 -1.0347884297370911 -2.9802322387695312e-08 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".dr" yes;
	setAttr ".frs" 3;
createNode transform -n "shaderRoom" -p "cam_grp";
	rename -uid "7AFC2B42-40E3-9836-8B8B-0286210AA9AC";
createNode mesh -n "shaderRoomShape" -p "shaderRoom";
	rename -uid "260A573E-4A73-31B0-E3FC-EC96A8100819";
	addAttr -ci true -sn "vrayOsdSubdivEnable" -ln "vrayOsdSubdivEnable" -dv 1 -at "long";
	addAttr -ci true -sn "vrayOsdSubdivDepth" -ln "vrayOsdSubdivDepth" -dv 4 -min 0 
		-smx 8 -at "long";
	addAttr -ci true -sn "vrayOsdSubdivType" -ln "vrayOsdSubdivType" -at "long";
	addAttr -ci true -sn "vrayOsdPreserveMapBorders" -ln "vrayOsdPreserveMapBorders" 
		-dv 1 -at "long";
	addAttr -ci true -sn "vrayOsdSubdivUVs" -ln "vrayOsdSubdivUVs" -dv 1 -at "long";
	addAttr -ci true -sn "vrayOsdPreserveGeomBorders" -ln "vrayOsdPreserveGeomBorders" 
		-at "long";
	setAttr -k off ".v";
	setAttr ".iog[0].og[0].gcl" -type "componentList" 1 "f[0]";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.49999835959721173 0.50000001303851604 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 18 ".uvst[0].uvsp[0:17]" -type "float2" 0.16746624 0.84183574
		 0.16746624 0.7109372 0.8325305 0.7109372 0.8325305 0.84183574 0.8325305 0.99800003
		 0.16746624 0.99800003 0.16746624 0.62452024 0.16746624 0.56865144 0.8325305 0.56865144
		 0.8325305 0.62452024 0.16746624 0.26693642 0.16746624 0.0020000003 0.8325305 0.0020000003
		 0.8325305 0.26693642 0.8325305 0.46859178 0.16746624 0.46859178 0.16746624 0.52088189
		 0.8325305 0.52088189;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 18 ".pt[0:17]" -type "float3"  31.953491 0 -33.494766 -31.953495 
		0 -33.494766 31.953491 -37.842709 44.469406 -31.953495 -37.842709 44.469406 31.953491 
		-10.334607 34.786201 -31.953495 -10.334607 34.786201 31.953491 -4.1445087e-08 13.954638 
		-31.953495 -4.1445087e-08 13.954638 31.953491 -0.93404496 24.039425 -31.953495 -0.93404496 
		24.039425 31.953491 -22.657532 39.820358 -31.953495 -22.657532 39.820358 31.953491 
		-3.7361789 28.981838 -31.953495 -3.7361789 28.981838 31.953491 0 -6.5524235 -31.953495 
		0 -6.5524235 31.953491 -1.6578035e-07 19.272205 -31.953495 -1.6578035e-07 19.272205;
	setAttr -s 18 ".vt[0:17]"  -36.47502136 0 36.47502899 36.47502518 0 36.47502899
		 -36.47502136 40.81788635 -47.61865234 36.47502518 40.81788635 -47.61865234 -36.47502136 11.14710999 -37.17416382
		 36.47502518 11.14710999 -37.17416382 -36.47502136 4.4703484e-08 -14.70482731 36.47502518 4.4703484e-08 -14.70482731
		 -36.47502136 1.0074791908 -25.58247566 36.47502518 1.0074791908 -25.58247566 -36.47502136 24.43885803 -42.60410309
		 36.47502518 24.43885803 -42.60410309 -36.47502136 4.02991581 -30.91345978 36.47502518 4.02991581 -30.91345978
		 -36.47502136 0 7.41449165 36.47502518 0 7.41449165 -36.47502136 1.7881393e-07 -20.44046021
		 36.47502518 1.7881393e-07 -20.44046021;
	setAttr -s 25 ".ed[0:24]"  0 1 0 2 3 0 2 10 0 10 4 0 3 11 0 11 5 0 4 12 0
		 12 8 0 5 13 0 13 9 0 4 5 1 6 14 0 14 0 0 7 15 0 15 1 0 6 7 1 8 16 0 16 6 0 9 17 0
		 17 7 0 8 9 1 10 11 1 12 13 1 14 15 1 16 17 1;
	setAttr -s 8 -ch 32 ".fc[0:7]" -type "polyFaces" 
		f 4 -6 -22 3 10
		mu 0 4 2 3 0 1
		f 4 -2 2 21 -5
		mu 0 4 4 5 0 3
		f 4 -10 -23 7 20
		mu 0 4 8 9 6 7
		f 4 -11 6 22 -9
		mu 0 4 2 1 6 9
		f 4 0 -15 -24 12
		mu 0 4 11 12 13 10
		f 4 11 23 -14 -16
		mu 0 4 15 10 13 14
		f 4 15 -20 -25 17
		mu 0 4 15 14 17 16
		f 4 -21 16 24 -19
		mu 0 4 8 7 16 17;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".dr" 3;
	setAttr ".dsm" 2;
createNode transform -n "renderCam_Persp_R" -p "cam_grp";
	rename -uid "9BC77469-4BB0-28F1-81B3-B99EABB4375B";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" 2.65 3.5 5.6 ;
	setAttr ".r" -type "double3" -23.5 26 -8.8169216244113859e-16 ;
	setAttr ".s" -type "double3" 0.099961441914272461 0.099961441914272461 0.099961441914272461 ;
	setAttr ".rp" -type "double3" -8.4735422205951716e-06 -2.2558560066509133e-07 1.1789327965855789e-07 ;
	setAttr ".rpt" -type "double3" 6.6531891624398934e-07 5.7232472280956075e-08 3.1789251118175955e-06 ;
	setAttr ".sp" -type "double3" 2.9049299857947242e-15 5.3290705182007514e-15 7.1054273576010019e-15 ;
	setAttr ".spt" -type "double3" -2.6145489957546764e-15 -4.7963689451385655e-15 -6.3951585935180868e-15 ;
createNode camera -n "renderCam_Persp_RShape" -p "renderCam_Persp_R";
	rename -uid "C79AF6B6-4A2D-CAE2-B0AA-A79E1DDC8A78";
	setAttr -k off ".v";
	setAttr ".ff" 2;
	setAttr ".ovr" 1.3;
	setAttr ".fl" 55;
	setAttr ".fs" 2;
	setAttr ".fd" 21;
	setAttr ".coi" 6.0322257587360353;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0 0.89933610652249585 0 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".dr" yes;
	setAttr ".frs" 3;
createNode transform -n "renderCam_Persp_L" -p "cam_grp";
	rename -uid "DA83CBAC-4C9C-1F1D-AFC6-D6A8A6AC07CA";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" -2.65 3.5 5.6 ;
	setAttr ".r" -type "double3" -23.5 -26 -8.8169216244113859e-16 ;
	setAttr ".s" -type "double3" 0.099961441914272461 0.099961441914272461 0.099961441914272461 ;
	setAttr ".rp" -type "double3" -8.4735422205951716e-06 -2.2558560066509133e-07 1.1789327965855789e-07 ;
	setAttr ".rpt" -type "double3" 6.6531891624398934e-07 5.7232472280956075e-08 3.1789251118175955e-06 ;
	setAttr ".sp" -type "double3" 2.9049299857947242e-15 5.3290705182007514e-15 7.1054273576010019e-15 ;
	setAttr ".spt" -type "double3" -2.6145489957546764e-15 -4.7963689451385655e-15 -6.3951585935180868e-15 ;
createNode camera -n "renderCam_Persp_LShape" -p "renderCam_Persp_L";
	rename -uid "0B30FAE5-4F16-E265-B6AC-FF848653E70C";
	setAttr -k off ".v";
	setAttr ".ff" 2;
	setAttr ".ovr" 1.3;
	setAttr ".fl" 55;
	setAttr ".fs" 2;
	setAttr ".fd" 21;
	setAttr ".coi" 6.7272020023012384;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0 0.89933610652249585 0 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".dr" yes;
	setAttr ".frs" 3;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "06680499-40BD-72F8-0BA1-4EAA298B6BDE";
	setAttr -s 3 ".lnk";
	setAttr -s 3 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "141B2ACF-47AA-E0EA-A1AE-B19CE9B473F0";
	setAttr ".cdl" 1;
	setAttr -s 2 ".dli[1]"  1;
createNode displayLayer -n "defaultLayer";
	rename -uid "65A61D00-42B9-1072-82C9-EFAE35820D19";
	setAttr ".ufem" -type "stringArray" 0  ;
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "F39A99BD-4D00-A3DA-A2CB-56A93C7C6A2A";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "4C9E6860-4E0A-0F04-6FF2-3D8D94847E63";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "EB6E70DA-47CB-634E-8759-7CABA2617EFC";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n"
		+ "            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n"
		+ "            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n"
		+ "            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n"
		+ "            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n"
		+ "            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n"
		+ "            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n"
		+ "            -camera \"|persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 1\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n"
		+ "            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n"
		+ "            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 2071\n            -height 1603\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n"
		+ "            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n"
		+ "            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n"
		+ "            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n"
		+ "            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n"
		+ "                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n"
		+ "                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n"
		+ "                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showPlayRangeShades \"on\" \n                -lockPlayRangeShades \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -keyMinScale 1\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -preSelectionHighlight 0\n                -limitToSelectedCurves 0\n                -constrainDrag 0\n                -valueLinesToggle 0\n                -highlightAffectedCurves 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n"
		+ "                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n"
		+ "                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -hierarchyBelow 0\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n"
		+ "                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n"
		+ "                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n"
		+ "                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n"
		+ "                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 1\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 2071\\n    -height 1603\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 1\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 2071\\n    -height 1603\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "A3A59522-40A8-ADF4-D811-DF881B610DE1";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 250 -ast 0 -aet 250 ";
	setAttr ".st" 6;
createNode VRaySettingsNode -s -n "vraySettings";
	rename -uid "4F212CCA-4B78-6D73-5136-E18E1551A52C";
	setAttr ".sver" 1;
	setAttr ".gi" yes;
	setAttr ".pe" 2;
	setAttr ".se" 3;
	setAttr ".cfile" -type "string" "";
	setAttr ".cfile2" -type "string" "";
	setAttr ".casf" -type "string" "";
	setAttr ".casf2" -type "string" "";
	setAttr ".msr" 6;
	setAttr ".aaft" 3;
	setAttr ".dma" 24;
	setAttr ".dac" 1.5;
	setAttr ".ufg" yes;
	setAttr ".fnm" -type "string" "";
	setAttr ".lcfnm" -type "string" "";
	setAttr ".asf" -type "string" "";
	setAttr ".lcasf" -type "string" "";
	setAttr ".urtrshd" yes;
	setAttr ".imcp" 2;
	setAttr ".imaxr" -2;
	setAttr ".icts" 0.4;
	setAttr ".ints" 0.3;
	setAttr ".ifile" -type "string" "";
	setAttr ".ifile2" -type "string" "";
	setAttr ".iasf" -type "string" "";
	setAttr ".iasf2" -type "string" "";
	setAttr ".pmfile" -type "string" "";
	setAttr ".pmfile2" -type "string" "";
	setAttr ".pmasf" -type "string" "";
	setAttr ".pmasf2" -type "string" "";
	setAttr ".dmcstd" yes;
	setAttr ".dmcsat" 0.005;
	setAttr ".cmtp" 6;
	setAttr ".cg" 2.2000000476837158;
	setAttr ".cadap" 0.10000000149011612;
	setAttr ".cadfd" 21;
	setAttr ".mtah" yes;
	setAttr ".srflc" 1;
	setAttr ".seu" yes;
	setAttr ".wi" 512;
	setAttr ".he" 512;
	setAttr ".aspr" 1;
	setAttr ".aspl" no;
	setAttr ".fnprx" -type "string" "tempPreview";
	setAttr ".pngc" 0;
	setAttr ".pngbpp" 16;
	setAttr ".jpegq" 100;
	setAttr ".bkc" -type "string" "";
	setAttr ".vfbSA" -type "Int32Array" 1620 0 6472 1 6460 0 1
		 6452 1700143739 1869181810 825893486 1632379436 1936876921 578501154 1936876886 577662825 573321530 1935764579 574235251
		 1953460082 1881287714 1701867378 1701409906 2067407475 1919252002 1852795251 741423650 1835101730 574235237 1696738338 1818386798
		 1949966949 744846706 1886938402 577007201 1818322490 573334899 1634760805 1650549870 975332716 1702195828 1931619453 1814913653
		 1919252833 1530536563 1818436219 577991521 1751327290 779317089 1886611812 1132028268 1701999215 1869182051 573317742 1886351984
		 1769239141 975336293 1702240891 1869181810 825893486 1634607660 975332717 1936278562 2036427888 1919894304 1952671090 577662825
		 1852121644 1701601889 1920219682 573334901 1634760805 975332462 1702195828 2019893804 1684955504 1701601889 1920219682 573334901
		 1718579824 577072233 573321530 1869641829 1701999987 774912546 1931619376 1600484961 1600284530 1835627120 1986622569 975336293
		 1936482662 1864510565 1601136995 1701603686 572668450 1668227628 1667198825 1919904879 1667330163 809116261 1668227628 1683976041
		 1819308905 1701083489 1701013878 741358114 1768124194 1769365359 1920235365 1718840929 577598063 573321274 1869177711 1986098015
		 1768843621 1701273965 1920219682 573334901 1600349033 1701603686 572668450 1667834412 1919967075 1818846831 1633967973 975331700
		 1819047278 1667834412 1701994339 1852400750 1953391988 741358114 1802265122 1868788848 975337070 1936482662 573341029 761427315
		 1702453612 975336306 1663204187 1936941420 1663187490 1936679272 1717924398 1970238254 1717920626 1701080175 573317746 1886351984
		 1769239141 975336293 1702240891 1869181810 825893486 1634607660 975332717 1970230050 979723122 1111970336 1696738338 1818386798
		 1949966949 744846706 1886938402 577007201 1818322490 573334899 1634760805 1650549870 975332716 1936482662 1646406757 1684956524
		 1685024095 809116261 1886331436 1953063777 825893497 573321262 2003789939 1701998687 2003134838 1920219682 573334901 1600352883
		 1701869940 2100312610 1970479660 1634479458 1936876921 2069576226 1634493218 975336307 1634231074 1915646831 1814980197 1952999273
		 578316653 1919951404 1919250543 1936025972 578501154 1936876918 577662825 573321530 1701667182 1277311522 1952999273 578316621
		 1852121644 1701601889 1634089506 744846188 1886938402 577007201 1818322490 573334899 1634760805 1650549870 975332716 1702195828
		 1931619453 1814913653 1919252833 1530536563 2066513245 1634493218 975336307 1634231074 1915646831 1663985253 1869639023 1702127987
		 1881287714 1701867378 1701409906 2067407475 1919252002 1852795251 741423650 1835101730 574235237 1886220099 1953067887 573317733
		 1650552421 975332716 1936482662 1696738405 1851879544 1715085924 1702063201 2019893804 1684955504 1701601889 1920219682 573334901
		 1852140642 1869438820 975332708 1864510512 1768120688 975337844 741355057 1869116194 1919967095 1701410405 1949966967 2103801202
		 1970479660 1634479458 1936876921 1566259746 746413437 1818436219 577991521 1751327290 779317089 1680762224 1768910437 577922419
		 1919951404 1919250543 1936025972 578501154 1936876918 577662825 573321530 1701667182 1143093794 1768910437 980575603 1634628896
		 1818845558 1701601889 1696738338 1818386798 1715085925 1702063201 2019893804 1684955504 1634089506 744846188 1886938402 1633971809
		 577072226 1970435130 1646406757 1684956524 1685024095 809116261 1886331436 1953063777 825893497 573321262 2003789939 1701998687
		 2003134838 1920219682 573334901 1769235297 975332726 1936482662 1881287781 1702061426 842670708 1953702444 1735288178 975333492
		 741355057 1684107810 577992041 774910266 1747070000 1667449207 1919249509 577074273 1818322490 573334899 1869505892 1919251305
		 1685024095 809116261 1931619453 1814913653 1919252833 1530536563 2066513245 1634493218 975336307 1634231074 1882092399 1752378981
		 1701868129 1818373742 740455029 1869770786 1953654128 577987945 1981971258 1769173605 975335023 1847733297 577072481 1750278714
		 1701868129 1816276846 740455029 1634624802 577072226 1818322490 573334899 1634760805 975332462 1936482662 1696738405 1851879544
		 1818386788 1949966949 744846706 1701601826 1834968174 577070191 573321274 1667330159 578385001 808333626 1752375852 1885304687
		 1769366898 975337317 1702195828 1752375852 1701868129 1818386286 1667199605 1970302319 975332724 1936482662 1931619429 1886544232
		 1633644133 1853189997 825893492 573321262 1918986355 1601070448 1768186226 975336309 741682736 1970037282 1634885490 1937074532
		 774978082 808465203 875573296 892418354 1931619453 1814913653 1919252833 1530536563 2066513245 1634493218 975336307 1634231074
		 1882092399 1701588581 2019980142 1881287714 1701867378 1701409906 2067407475 1919252002 1852795251 741423650 1835101730 574235237
		 1936614732 1717978400 1937007461 1696738338 1818386798 1715085925 1702063201 2019893804 1684955504 1634089506 744846188 1886938402
		 1633971809 577072226 1970435130 1646406757 1684956524 1685024095 809116261 1886331436 1953063777 825893497 573321262 2003789939
		 1701998687 2003134838 1920219682 573334901 1918987367 1852792677 1634089506 744846188 1634494242 1935631730 577075817 774910778
		 1730292784 1701994860 1768257375 578054247 808333626 1818370604 1601007471 1734960503 975336552 808726064 808464432 959787056
		 1730292790 1701994860 1919448159 1869116261 975332460 741355057 1818846754 1601332596 1635020658 1852795252 774912546 1931619376
		 1920300129 1869182049 825893486 573321262 1685217640 1701994871 1667457375 1919249509 1684370529 1920219682 573334901 1684828003
		 1918990175 1715085933 1702063201 1852383788 1634887028 1986622563 1949966949 744846706 1986097954 1818713957 577073761 1818322490
		 573334899 1701536098 1634494303 2002740594 1751607653 1949966964 744846706 1701995298 1600484449 1701209701 1601401955 1970496882
		 1667200108 1852727656 975334501 1702195828 1852121644 1701601889 1634493023 577987940 1970435130 1931619429 1936024681 741751330
		 1634492962 1601398116 1635020658 1852795252 892418594 573321262 1701999731 1650420577 577926508 841887802 808464432 842018864
		 573323321 1600484213 1952543335 577203817 1818322490 573334899 1952543335 1600613993 1936614756 578385001 774911290 1730292784
		 1769234802 1818191726 1952935525 825893480 741355056 1634887458 1735289204 1869576799 893002349 573321262 1952543335 1600613993
		 1886350451 809116261 573321262 1952543335 1600613993 1701999731 1752459118 774978082 1965173808 1868522867 1970037603 1852795251
		 1634089506 744846188 1667460898 1769174380 1935634031 1701670265 1667854964 1920219682 573334901 1818452847 1869181813 1701863278
		 1852138354 842670708 741355056 1667460898 1769174380 1918856815 1952543855 577662825 808333370 1668227628 1937075299 1601073001
		 576942689 808464698 573321262 1600484213 1634886515 577266548 1818322490 573334899 1601332083 1835891059 1769108581 1949966947
		 744846706 1919120162 1952542815 1852990836 741358114 1919120162 1819635039 1818716532 1600483937 1853189987 825893492 1668489772
		 1701076850 1953067886 893002361 741355056 1919120162 1852140639 577270887 774911290 1931619376 1935635043 1701867372 1918989919
		 1668178281 809116261 573321262 1601332083 1952737655 1635147624 1851877746 975332707 741355056 1919120162 1701147487 809116260
		 1668489772 1870290802 975334767 741355058 1919120162 1953460831 1869182049 809116270 573321262 1601332083 1701999731 1752459118
		 774978082 1965173808 1683973491 578057077 1818322490 573334899 1953723748 1952542815 1852990836 741358114 1937073186 1701076852
		 1953067886 893002361 741355056 1937073186 1634885492 1937074532 1918989919 1668178281 809116261 573321262 1953723748 1953065567
		 577922420 808333370 1969496620 2053076083 577597295 808333882 1969496620 1918858355 1952543855 577662825 808333370 1969496620
		 1935635571 1852142196 577270887 808333626 1818698284 1600483937 1600484213 1953718895 1701602145 1634560351 975332711 1936482662
		 1730292837 1701994860 1935830879 1818452340 1835622245 1600481121 1752457584 572668450 1651450412 1767863411 1701273965 1869576799
		 825893485 573321262 1953718895 1634560351 1918854503 1952543855 577662825 808333370 1651450412 1767863411 1701273965 1920234335
		 1952935525 825893480 573321262 1600484213 1953261926 1767862885 1701273965 1634089506 744846188 1634494242 1767859570 1701273965
		 1952542815 574235240 1965173794 1667196275 1836020328 1667855457 1700946271 1952543346 577662825 1818322490 573334899 1869768803
		 1769234797 1650548579 1634890341 1852795252 774912546 808464433 808464432 741946417 1835098914 1600221797 1701869940 741358114
		 1702130466 1601135986 1701080941 2100312610 1970479660 1634479458 1936876921 1566259746 578497661 1935764579 574235251 1868654691
		 1667444339 1768453934 1631741300 1668178284 573317733 1886351984 1769239141 975336293 1702240891 1869181810 825893486 1634607660
		 975332717 1768445730 1109419380 1851878497 740451683 1634624802 577072226 1818322490 573334899 1634760805 975332462 1936482662
		 1696738405 1851879544 1818386788 1949966949 744846706 1701601826 1834968174 577070191 573321274 1667330159 578385001 808333626
		 1752375852 1885304687 1769366898 975337317 1702195828 1702109740 975335533 808465718 573321262 1953393012 774912546 1663183920
		 1919904879 1852404831 1530536564 741355057 741355057 1563438641 1931619453 1814913653 1919252833 1530536563 2066513245 1634493218
		 975336307 1634231074 1663988591 2019896931 1970499440 740451698 1869770786 1953654128 577987945 1981971258 1769173605 975335023
		 1847733297 577072481 2017796666 1970499440 740451698 1634624802 577072226 1818322490 573334899 1634760805 975332462 1936482662
		 1696738405 1851879544 1818386788 1949966949 744846706 1701601826 1834968174 577070191 573321274 1667330159 578385001 808333626
		 1752375852 1885304687 1769366898 975337317 1702195828 2019893804 1970499440 975332722 741355056 1818847266 1952999273 1920295519
		 825893486 573321262 1953394531 1953718642 774912546 573340976 761427315 1702453612 975336306 746413403 1818436219 577991521
		 1751327290 779317089 1663984483 1702261365 573317747 1886351984 1769239141 975336293 1702240891 1869181810 825893486 1634607660
		 975332717 1920287522 577987958 1852121644 1701601889 1634089506 744846188 1886938402 577007201 1818322490 573334899 1634760805
		 1650549870 975332716 1702195828 1818370604 1600417381 1701080941 741358114 1634758434 2037672291 774978082 1931619376 1601662824
		 1986359920 578250089 1970435130 1663183973 1702261365 1634887519 975333488 1702240891 1869181810 825893486 573341053 761427315
		 1702453612 975336306 746413403 1818436219 577991521 1751327290 779317089 1747870563 1632855413 1734954100 740455528 1869770786
		 1953654128 577987945 1981971258 1769173605 975335023 1847733297 577072481 1967661626 539959397 1970561363 1769234802 740453999
		 1634624802 577072226 1818322490 573334899 1634760805 975332462 1936482662 1696738405 1851879544 1818386788 1949966949 744846706
		 1701601826 1834968174 577070191 573321274 1667330159 578385001 808333626 1752375852 1885304687 1769366898 975337317 1702195828
		 1969758764 809116261 573321262 578052467 808333370 1768694316 1853122663 577991525 808333370 1931619453 1814913653 1919252833
		 1530536563 2066513245 1634493218 975336307 1634231074 1663988591 1868770915 1114795884 1851878497 740451683 1869770786 1953654128
		 577987945 1981971258 1769173605 975335023 1847733297 577072481 1866670650 544370540 1634492738 577069934 1852121644 1701601889
		 1634089506 744846188 1886938402 577007201 1818322490 573334899 1634760805 1650549870 975332716 1702195828 1818370604 1600417381
		 1701080941 741358114 1634758434 2037672291 774978082 1931619376 1601662824 1986359920 578250089 1970435130 1931619429 1601662824
		 1970238055 809116272 1818305068 1701994348 809116260 573321262 1600941153 1701147239 809116270 573321262 1600941153 1702194274
		 774912546 1931619376 1868849512 1918858103 975332453 741355056 1634235170 1937207140 1701996383 975335013 741355056 1634235170
		 1937207140 1970037343 809116261 573321262 1600416109 577004914 808333370 1768759852 1919377252 577660261 808333370 1768759852
		 1818386276 975332725 741355056 1734961186 1701994344 809116260 573321262 1751607656 1701996383 975335013 741355056 1734961186
		 1818386280 975332725 2100309552 1970479660 1634479458 1936876921 1566259746 578497661 1935764579 574235251 1868654691 1701981811
		 2019896934 1852990836 740453473 1869770786 1953654128 577987945 1981971258 1769173605 975335023 1847733297 577072481 1631724090
		 1919380323 1684960623 1696738338 1818386798 1715085925 1702063201 2019893804 1684955504 1634089506 744846188 1886938402 1633971809
		 577072226 1970435130 1646406757 1684956524 1685024095 809116261 1886331436 1953063777 825893497 573321262 1600484213 1869377379
		 1715085938 1702063201 1633821228 1919380323 1684960623 1819239263 975336047 858665051 959722802 909128240 808204340 859059758
		 842478385 925972023 774908978 875968311 909520951 859189553 1965173853 1767859571 1701273965 1920219682 573334901 1734438249
		 574235237 1763847202 1701273965 1953064543 741358114 1919903778 1852799593 1600938356 1936090735 975336549 741355056 1919252002
		 1633905012 1718574956 1952805734 774912546 1629629488 1868980083 1919378802 1684960623 1634089506 744846188 1986097954 1852399461
		 1818846815 1949966949 744846706 1819239202 1952412271 1936613746 1836216166 1685024095 809116261 1868767788 1601335148 1667330163
		 1920229221 1718840929 577598063 573321530 1851880052 1919247987 1853187679 1869182051 825893486 1668227628 1767862121 1953853550
		 1819239263 1935635055 1701011824 2100312610 1970479660 1634479458 1936876921 1566259746 578497661 1935764579 574235251 1868654691
		 1667444339 1953852462 1881287714 1701867378 1701409906 2067407475 1919252002 1852795251 741489186 1835101730 574235237 1802465100
		 1411412085 1701601889 1696738338 1818386798 1715085925 1702063201 2019893804 1684955504 1634089506 744846188 1886938402 1633971809
		 577072226 1970435130 1646406757 1684956524 1685024095 809116261 1886331436 1953063777 825893497 573321262 2003789939 1701998687
		 2003134838 1920219682 573334901 1601467756 1701603686 572668450 1768694316 1918985582 1735355442 1634089506 744846188 1852402722
		 846356837 1650946675 1634089506 744846188 1953852450 1819239263 1935635055 1701011824 741358114 1986097954 1852399461 1818846815
		 1715085925 1702063201 1931619453 1814913653 1919252833 1530536563 2103278941 1663204140 1936941420 1663187490 1936679272 1702260526
		 2036427890 1635021614 740454509 1869770786 1953654128 577987945 1981971258 1769173605 975335023 1847733297 577072481 1951605306
		 577793377 1852121644 1701601889 1634089506 744846188 1886938402 577007201 1818322490 573334899 1634760805 1650549870 975332716
		 1702195828 1953702444 1601203553 1769107304 1818320762 577660777 573321530 1835103347 1702256496 1633645682 1852270956 842218018
		 1953702444 1601203553 1869377379 1530536562 741355057 741355057 1563438641 1953702444 1601203553 1953394534 578501154 1936876918
		 577662825 573321530 1852403568 1769168756 975332730 573321265 1768776038 975337836 1931619376 1701607796 741358114 1768257314
		 578054247 573321274 1701011814 1092762146 1818323314 573340962 1835103347 1953718128 1735289202 578501154 1936876918 577662825
		 573321530 1601659250 1769108595 975333230 1378702882 1713404257 1293972079 543258977 1634891301 1919252089 1852795251 1914731552
		 1701080677 1769218162 622880109 1684956530 1769239141 740451693 1852401186 1935633505 1852404340 574235239 1632775510 1868963961
		 1632444530 908091769 1914731552 1701080677 1769218162 538994029 538994736 538996016 1932799537 746421538 1651864354 2036427821
		 577991269 2103270202 573341021 1768383826 1699180143 2067407470 1919252002 1852795251 741423650 1970236706 1717527923 1869376623
		 1852137335 1701601889 1715085924 1702063201 1869423148 1600484213 1819045734 1885304687 1953393007 1668246623 577004907 1818322490
		 573334899 1937076077 1868980069 2003790956 1768910943 2019521646 741358114 1970236706 1717527923 1869376623 1869635447 1601465961
		 809116281 1377971325 1701080677 1701402226 2067407479 1919252002 1852795251 741423650 1634624802 1600482402 1684956530 1918857829
		 1869178725 1715085934 1702063201 1701978668 1919247470 1734701663 1601073001 975319160 808333613 1701978668 1919247470 1734701663
		 1601073001 975319161 808333613 1701978668 1919247470 1734701663 1601073001 975319416 808333613 1701978668 1919247470 1734701663
		 1601073001 975319417 808333613 1769349676 1918859109 975332453 1702195828 1769349676 1734309733 1852138866 1920219682 573334901
		 2003134838 1970037343 1949966949 744846706 1701410338 1869438839 975335278 1936482662 1663183973 1919904879 1634493279 1834971245
		 577070191 741946938 1819239202 1667199599 1886216556 577662815 1970435130 1965173861 1885300083 1818589289 1886609759 1601463141
		 975335023 1936482662 1965173861 1885300083 1919905377 1600220513 2003134838 577662815 1818322490 573334899 1702390128 1852399468
		 1818193766 1701536623 1715085924 1702063201 1768956460 1600939384 1868983913 1919902559 1952671090 1667196005 1919904879 1715085939
		 1702063201 1953702444 1868919397 1685024095 809116261 1092758653 1869182051 975336302 1702240891 1869181810 825893486 1634738732
		 1231385461 1667191376 1801676136 975332453 1936482662 1948396645 1383363429 1918858085 1869177953 825571874 1702109740 1699902579
		 1751342963 1701536613 1715085924 1702063201 1701061164 1399289186 1768186216 1918855022 1869177953 909457954 1701061164 1399289186
		 1768186216 1667196782 1801676136 975332453 1936482662 1931619429 1701995892 1685015919 1634885477 577726820 741881658 1702130466
		 1299146098 1600480367 1667590243 577004907 1818322490 2105369971 ;
	setAttr ".sRGBOn" yes;
	setAttr ".mSceneName" -type "string" "C:/Users/ryan/OneDrive/Documents/maya/plug-ins/SLiB/scn/vray-cpu_SLiB_preview_obj_01.ma";
	setAttr ".rt_productionGpuSamplesLimit" 100;
	setAttr ".rt_engineType" 2;
	setAttr ".rt_gpuTextureFormat" 1;
	setAttr ".rt_vrayProxyObjects" yes;
	setAttr ".rt_particleSystems" yes;
	setAttr ".rt_displacement" yes;
	setAttr ".rt_subdivision" yes;
	setAttr ".rt_hair" yes;
	setAttr ".rt_fur" yes;
	setAttr ".rt_plugin_geometry" yes;
createNode file -n "VRayLightDomeShape1_File01";
	rename -uid "A6A11B8A-4D73-94AC-A8C2-B589C343235F";
	addAttr -ci true -k true -sn "rsFilterEnable" -ln "rsFilterEnable" -dv 2 -min 0 
		-max 2 -en "None:Magnification:Magnification/Minification" -at "enum";
	addAttr -ci true -sn "rsMipBias" -ln "rsMipBias" -min -31 -max 31 -at "double";
	addAttr -ci true -sn "rsBicubicFiltering" -ln "rsBicubicFiltering" -min 0 -max 1 
		-at "bool";
	addAttr -ci true -sn "rsPreferSharpFiltering" -ln "rsPreferSharpFiltering" -dv 1 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "rsAlphaMode" -ln "rsAlphaMode" -min 0 -max 2 -en "None:Coverage:Pre-Multiplied" 
		-at "enum";
	setAttr ".ftn" -type "string" "${SLiB}/scn/Tex/cyclorama_hard_light_1k.hdr";
	setAttr ".ft" 0;
	setAttr ".cs" -type "string" "Raw";
createNode VRayPlaceEnvTex -n "VRayPlaceEnvTex1";
	rename -uid "CBAC484C-4F16-F380-5425-C8907EDBE9BF";
	setAttr ".mt" 2;
	setAttr ".hr" -45;
createNode script -n "IGPUCS";
	rename -uid "5C4B98CE-4519-8F00-CB5B-4F936E5D4064";
	setAttr ".b" -type "string" "try: igpucs_SOuP().scriptJobUpdate()\nexcept: pass";
	setAttr ".st" 7;
	setAttr ".stp" 1;
createNode materialInfo -n "materialInfo114";
	rename -uid "928D045B-48B9-5EB3-7F17-C0B66944C5C0";
createNode shadingEngine -n "floorSG1";
	rename -uid "E0F50013-48D3-AD22-F80C-E4AF4B5A0693";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode lambert -n "floor_MAT";
	rename -uid "4548B7DC-4072-9E82-649A-0B8237A3F697";
	setAttr ".dc" 1;
	setAttr ".c" -type "float3" 0.14901961 0.14901961 0.14901961 ;
createNode nodeGraphEditorBookmarkInfo -n "nodeGraphEditorBookmarkInfo1";
	rename -uid "3202E471-4064-9345-1BE9-349680826A97";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "B94EC19B-4DE3-11BF-AEB2-8E85446E8161";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "B5819364-4EB1-23F3-7278-45BCFABA5E1B";
createNode aiOptions -s -n "defaultArnoldRenderOptions";
	rename -uid "B16D37B6-4516-9C74-9690-83A8528387EF";
	setAttr ".version" -type "string" "5.4.2.1";
createNode aiAOVFilter -s -n "defaultArnoldFilter";
	rename -uid "466848DB-4569-B11A-3A14-C6B66F6ACBAE";
createNode aiAOVDriver -s -n "defaultArnoldDriver";
	rename -uid "34A2D67A-4BAF-A4AC-3F34-AB8CDB51B097";
createNode aiAOVDriver -s -n "defaultArnoldDisplayDriver";
	rename -uid "400360A3-4888-7D32-A353-77BA20D4008C";
	setAttr ".ai_translator" -type "string" "maya";
	setAttr ".output_mode" 0;
createNode aiImagerDenoiserOidn -s -n "defaultArnoldDenoiser";
	rename -uid "E4167372-41A0-4572-CE24-C681C3E2A558";
createNode renderSetup -n "renderSetup";
	rename -uid "62780BD8-4898-59F8-8A71-E39540B14514";
createNode mayaUsdLayerManager -n "mayaUsdLayerManager1";
	rename -uid "4C9BBABD-4C15-5ABB-AD9C-9D872C10CE07";
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".o" 0;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".tmr" 4096;
	setAttr ".dli" 1;
	setAttr ".fprt" yes;
	setAttr ".rtfm" 1;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 3 ".st";
	setAttr -k on ".an";
	setAttr -k on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 6 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
select -ne :defaultRenderingList1;
select -ne :lightList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultTextureList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :standardSurface1;
	setAttr ".b" 0.80000001192092896;
	setAttr ".bc" -type "float3" 1 1 1 ;
	setAttr ".s" 0.20000000298023224;
	setAttr ".sr" 0.5;
select -ne :initialShadingGroup;
	addAttr -s false -ci true -sn "rsSurfaceShader" -ln "rsSurfaceShader" -at "message";
	addAttr -s false -ci true -sn "rsVolumeShader" -ln "rsVolumeShader" -at "message";
	addAttr -s false -ci true -sn "rsShadowShader" -ln "rsShadowShader" -at "message";
	addAttr -s false -ci true -sn "rsPhotonShader" -ln "rsPhotonShader" -at "message";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsBumpmapShader" -ln "rsBumpmapShader" -at "message";
	addAttr -s false -ci true -sn "rsDisplacementShader" -ln "rsDisplacementShader" 
		-at "message";
	addAttr -ci true -sn "rsMaterialId" -ln "rsMaterialId" -min 0 -max 2147483647 -smn 
		0 -smx 100 -at "long";
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	addAttr -s false -ci true -sn "rsSurfaceShader" -ln "rsSurfaceShader" -at "message";
	addAttr -s false -ci true -sn "rsVolumeShader" -ln "rsVolumeShader" -at "message";
	addAttr -s false -ci true -sn "rsShadowShader" -ln "rsShadowShader" -at "message";
	addAttr -s false -ci true -sn "rsPhotonShader" -ln "rsPhotonShader" -at "message";
	addAttr -s false -ci true -sn "rsEnvironmentShader" -ln "rsEnvironmentShader" -at "message";
	addAttr -s false -ci true -sn "rsBumpmapShader" -ln "rsBumpmapShader" -at "message";
	addAttr -s false -ci true -sn "rsDisplacementShader" -ln "rsDisplacementShader" 
		-at "message";
	addAttr -ci true -sn "rsMaterialId" -ln "rsMaterialId" -min 0 -max 2147483647 -smn 
		0 -smx 100 -at "long";
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".macc";
	setAttr -k on ".macd";
	setAttr -k on ".macq";
	setAttr -k on ".mcfr" 25;
	setAttr -cb on ".ifg";
	setAttr -k on ".clip";
	setAttr -k on ".edm";
	setAttr ".edl" no;
	setAttr ".ren" -type "string" "vray";
	setAttr -av -k on ".esr";
	setAttr -k on ".ors";
	setAttr -cb on ".sdf";
	setAttr -av ".outf";
	setAttr -cb on ".imfkey";
	setAttr -k on ".gama";
	setAttr -k on ".an";
	setAttr -cb on ".ar";
	setAttr -k on ".fs";
	setAttr -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -cb on ".me";
	setAttr -cb on ".se";
	setAttr -k on ".be";
	setAttr -cb on ".ep";
	setAttr -k on ".fec";
	setAttr -k on ".ofc";
	setAttr -cb on ".ofe";
	setAttr -cb on ".efe";
	setAttr -cb on ".oft";
	setAttr -cb on ".umfn";
	setAttr -cb on ".ufe";
	setAttr -cb on ".pff";
	setAttr -cb on ".peie";
	setAttr -cb on ".ifp";
	setAttr -k on ".comp";
	setAttr -k on ".cth";
	setAttr -k on ".soll";
	setAttr -cb on ".sosl";
	setAttr -k on ".rd";
	setAttr -k on ".lp";
	setAttr -av -k on ".sp";
	setAttr -k on ".shs";
	setAttr -k on ".lpr";
	setAttr -cb on ".gv";
	setAttr -cb on ".sv";
	setAttr -k on ".mm";
	setAttr -k on ".npu";
	setAttr -k on ".itf";
	setAttr -k on ".shp";
	setAttr -cb on ".isp";
	setAttr -k on ".uf";
	setAttr -k on ".oi";
	setAttr -k on ".rut";
	setAttr -cb on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -k on ".afp";
	setAttr -k on ".pfb";
	setAttr -k on ".pram" -type "string" "python(\"import SLiBPreRenderPY; SLiBPreRenderPY.swapObj()\")";
	setAttr -k on ".poam";
	setAttr -k on ".prlm" -type "string" "";
	setAttr -k on ".polm" -type "string" "";
	setAttr ".prm" -type "string" "";
	setAttr ".pom" -type "string" "";
	setAttr -cb on ".pfrm";
	setAttr -cb on ".pfom";
	setAttr -av ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -k on ".ubc";
	setAttr -k on ".mbc";
	setAttr -cb on ".mbt";
	setAttr -k on ".udbx";
	setAttr -k on ".smc";
	setAttr -k on ".kmv";
	setAttr -cb on ".isl";
	setAttr -cb on ".ism";
	setAttr -cb on ".imb";
	setAttr -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -k on ".tlwd";
	setAttr -k on ".tlht";
	setAttr -k on ".jfc";
	setAttr -cb on ".rsb";
	setAttr -k on ".ope";
	setAttr -k on ".oppf";
	setAttr -cb on ".hbl";
	setAttr ".dss" -type "string" "lambert1";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av ".w" 512;
	setAttr -av ".h" 512;
	setAttr -av ".pa" 1;
	setAttr -av ".al";
	setAttr -av ".dar" 1;
	setAttr -av -k on ".ldar";
	setAttr -cb on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -cb on ".isu";
	setAttr -cb on ".pdu";
select -ne :defaultLightSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".vtn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".vn" -type "string" "ACES 1.0 SDR-video";
	setAttr ".dn" -type "string" "sRGB";
	setAttr ".wsn" -type "string" "ACEScg";
	setAttr ".otn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".potn" -type "string" "ACES 1.0 SDR-video (sRGB)";
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
	setAttr -k off ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr" 25;
connectAttr "VRayLightDomeShape1_File01.oc" "VRayLightDomeShape1.dt";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "floorSG1.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "floorSG1.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "VRayPlaceEnvTex1.ouv" "VRayLightDomeShape1_File01.uv";
connectAttr ":defaultColorMgtGlobals.cme" "VRayLightDomeShape1_File01.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "VRayLightDomeShape1_File01.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "VRayLightDomeShape1_File01.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "VRayLightDomeShape1_File01.ws";
connectAttr "VRayLightDome1.wm" "VRayPlaceEnvTex1.tm";
connectAttr "floorSG1.msg" "materialInfo114.sg";
connectAttr "floor_MAT.msg" "materialInfo114.m";
connectAttr "floor_MAT.oc" "floorSG1.ss";
connectAttr "shaderRoomShape.iog" "floorSG1.dsm" -na;
connectAttr ":defaultArnoldDenoiser.msg" ":defaultArnoldRenderOptions.imagers" -na
		;
connectAttr ":defaultArnoldDisplayDriver.msg" ":defaultArnoldRenderOptions.drivers"
		 -na;
connectAttr ":defaultArnoldFilter.msg" ":defaultArnoldRenderOptions.filt";
connectAttr ":defaultArnoldDriver.msg" ":defaultArnoldRenderOptions.drvr";
connectAttr "floorSG1.pa" ":renderPartition.st" -na;
connectAttr "floor_MAT.msg" ":defaultShaderList1.s" -na;
connectAttr "VRayPlaceEnvTex1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "VRayLightDomeShape1.ltd" ":lightList1.l" -na;
connectAttr "VRayLightDomeShape1_File01.msg" ":defaultTextureList1.tx" -na;
connectAttr "renderCam_FrontShape.msg" ":defaultRenderGlobals.sc";
connectAttr "VRayLightDome1.iog" ":defaultLightSet.dsm" -na;
// End of vray-cpu_SLiB_preview_obj_01.ma
