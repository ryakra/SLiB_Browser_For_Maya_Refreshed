import maya.cmds as cmds
import maya.mel as mel
import re
import os
import shutil

# --------------------- Utility Functions ---------------------

def open_file_browser(file_mode=1, caption="Select File"):
    """
    Open a file dialog to select a file or directory.
    
    :param file_mode: The mode of file dialog (1 for file, 2 for directory).
    :param caption: The caption of the dialog.
    :return: Selected file path or None if no file is selected.
    """
    file_filter = "V-Ray Material or Scene Files (*.vrmat *.vrscene)" if file_mode == 1 else ""
    file_path = cmds.fileDialog2(fileFilter=file_filter, dialogStyle=2, fileMode=file_mode, okCaption=caption)
    return file_path[0] if file_path else None

def delete_unused_nodes():
    """
    Delete unused nodes in the Hypershade using MEL.
    """
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    print("Deleted unused nodes in Hypershade.")

# --------------------- Shader Replacement Functions ---------------------

def get_vray_vrmat_selectable_values_from_file(vrmat_file):
    """
    Get selectable values from a VRmat file.

    :param vrmat_file: The path to the VRmat file.
    :return: A list of selectable values.
    """
    try:
        selectable_values = cmds.vray("getVRmatList", vrmat_file)
        return selectable_values
    except Exception as e:
        print(f"Failed to retrieve VRmat materials: {e}")
        return []

def get_vray_vrmat_selectable_values_from_shader(shader_node):
    """
    Get selectable values for a VRayVRmatMtl shader node.

    :param shader_node: The name of the VRayVRmatMtl shader node.
    :return: A list of selectable values from the VRmat file.
    """
    if not cmds.objExists(shader_node):
        print(f"Shader node '{shader_node}' does not exist.")
        return []

    if cmds.nodeType(shader_node) != "VRayVRmatMtl":
        print(f"Node '{shader_node}' is not a VRayVRmatMtl shader.")
        return []

    # Get the filename attribute from the shader node
    filename = cmds.getAttr(f"{shader_node}.fileName")
    if not filename:
        print(f"No VRmat file specified for shader '{shader_node}'.")
        return []

    # Use the V-Ray command to get the list of materials
    try:
        selectable_values = cmds.vray("getVRmatList", filename)
        return selectable_values
    except Exception as e:
        print(f"Failed to retrieve selectable values: {e}")
        return []

def get_current_selection(shader_node):
    """
    Get the currently selected value for the VRayVRmatMtl shader node.

    :param shader_node: The name of the VRayVRmatMtl shader node.
    :return: The currently selected value.
    """
    return cmds.getAttr(f"{shader_node}.url")

def set_current_selection(shader_node, selection):
    """
    Set the current selection for the VRayVRmatMtl shader node.

    :param shader_node: The name of the VRayVRmatMtl shader node.
    :param selection: The value to set as the current selection.
    """
    cmds.setAttr(f"{shader_node}.url", selection, type="string")

def replace_shaders_with_vrmat(vrmat_file):
    """
    Replace shaders in the scene with VRayVRmatMtl shaders and set the correct selectable values.

    :param vrmat_file: The path to the VRmat or VRscene file.
    """
    # Determine if the file is VRmat or VRscene
    is_vrmat = vrmat_file.endswith('.vrmat')
    is_vrscene = vrmat_file.endswith('.vrscene')

    if not (is_vrmat or is_vrscene):
        print("Unsupported file type. Please select a .vrmat or .vrscene file.")
        return

    # Get all materials in the scene
    scene_materials = cmds.ls(materials=True)

    # Get selectable values from the VRmat file
    if is_vrmat:
        vrmat_materials = get_vray_vrmat_selectable_values_from_file(vrmat_file)
    else:
        vrmat_materials = [vrmat_file]  # For VRscene, use the file directly

    for scene_mat in scene_materials:
        for vrmat_mat in vrmat_materials:
            # Match the scene material name with the VRmat material name
            if scene_mat in vrmat_mat:
                # Create a new VRayVRmatMtl shader
                vrmat_shader = cmds.shadingNode('VRayVRmatMtl', asShader=True, name=f"{scene_mat}_VRmat")
                cmds.setAttr(f"{vrmat_shader}.fileName", vrmat_file, type="string")

                # Set the correct selectable value
                set_current_selection(vrmat_shader, vrmat_mat)

                # Get the shading group of the scene material
                shading_group = cmds.listConnections(scene_mat, type='shadingEngine')
                if shading_group:
                    # Connect the VRayVRmatMtl shader to the shading group
                    cmds.connectAttr(f"{vrmat_shader}.outColor", f"{shading_group[0]}.surfaceShader", force=True)

                print(f"Replaced '{scene_mat}' with '{vrmat_shader}' and selected '{vrmat_mat}'.")

    # If the file is a .vrscene, extract and handle texture files
    if is_vrscene:
        texture_files = extract_texture_files_from_vrscene(vrmat_file)
        if texture_files:
            print("\nTexture files extracted from VRscene:")
            for texture in texture_files:
                print(f"  {texture}")
            # Optionally, you can implement further handling of textures here

    # Delete unused nodes in Hypershade
    delete_unused_nodes()

# --------------------- Shader Information Functions ---------------------

def get_shading_group_connections(shading_group):
    """
    Get all connections to a specified shading group in Maya.

    :param shading_group: The name of the shading group.
    :return: A dictionary containing incoming and outgoing connections.
    """
    if not cmds.objExists(shading_group):
        print(f"Shading group '{shading_group}' does not exist.")
        return None

    # Get all incoming connections to the shading group
    incoming_connections = cmds.listConnections(shading_group, source=True, destination=False, plugs=True) or []

    # Get all outgoing connections from the shading group
    outgoing_connections = cmds.listConnections(shading_group, source=False, destination=True, plugs=True) or []

    connections = {
        'incoming': incoming_connections,
        'outgoing': outgoing_connections
    }

    return connections

def get_shader_info(shader):
    """
    Get detailed information about a shader and its settings.

    :param shader: The name of the shader.
    :return: A dictionary containing the shader's attributes and their values.
    """
    if not cmds.objExists(shader):
        print(f"Shader '{shader}' does not exist.")
        return None

    # Determine the shader type
    shader_type = cmds.nodeType(shader)

    # Get all keyable attributes of the shader
    attributes = cmds.listAttr(shader, keyable=True) or []
    shader_info = {'type': shader_type}

    for attr in attributes:
        try:
            value = cmds.getAttr(f"{shader}.{attr}")
            shader_info[attr] = value
        except Exception as e:
            # Handle any exceptions (e.g., if the attribute is not readable)
            shader_info[attr] = f"Error: {e}"

    return shader_info

# --------------------- VRScene Texture Handling Functions ---------------------

def extract_texture_files_from_vrscene(vrscene_file):
    """
    Extract texture file paths from a .vrscene file.

    :param vrscene_file: The path to the .vrscene file.
    :return: A list of texture file paths.
    """
    texture_files = []

    try:
        with open(vrscene_file, 'r') as file:
            content = file.read()

            # Regular expression to find file paths in BitmapBuffer nodes
            pattern = r'BitmapBuffer.*?file="(.*?)"'
            matches = re.findall(pattern, content, re.DOTALL)

            texture_files.extend(matches)

    except Exception as e:
        print(f"Failed to read vrscene file: {e}")

    return texture_files

def modify_texture_file_path(vrscene_file, old_path, new_path):
    """
    Modify a texture file path in a .vrscene file.

    :param vrscene_file: The path to the .vrscene file.
    :param old_path: The old texture file path to be replaced.
    :param new_path: The new texture file path.
    """
    try:
        with open(vrscene_file, 'r') as file:
            content = file.read()

        # Replace the old path with the new path
        content = content.replace(f'file="{old_path}"', f'file="{new_path}"')

        # Write the modified content back to the file
        with open(vrscene_file, 'w') as file:
            file.write(content)

        print(f"Replaced '{old_path}' with '{new_path}' in {vrscene_file}.")

    except Exception as e:
        print(f"Failed to modify vrscene file: {e}")

def move_textures_and_update_vrscene(vrscene_file):
    """
    Move textures to a user-specified folder and update the .vrscene file with new relative paths.

    :param vrscene_file: The path to the .vrscene file.
    """
    # Ask user for destination folder
    dest_folder = open_file_browser(file_mode=2, caption="Select Destination Folder")
    if not dest_folder:
        print("No destination folder selected.")
        return

    # Extract texture files from the .vrscene file
    texture_files = extract_texture_files_from_vrscene(vrscene_file)
    if not texture_files:
        print("No texture files found in the vrscene.")
        return

    # Copy the .vrscene file to the destination folder
    vrscene_filename = os.path.basename(vrscene_file)
    new_vrscene_path = os.path.join(dest_folder, vrscene_filename)
    shutil.copy(vrscene_file, new_vrscene_path)

    # Copy textures to the destination folder and update their paths in the .vrscene file
    for texture in texture_files:
        try:
            texture_filename = os.path.basename(texture)
            new_texture_path = os.path.join(dest_folder, texture_filename)
            shutil.copy(texture, new_texture_path)

            # Update the texture path in the .vrscene file
            relative_texture_path = os.path.relpath(new_texture_path, dest_folder)
            modify_texture_file_path(new_vrscene_path, texture, relative_texture_path)

            print(f"Copied and updated texture path: {texture} -> {relative_texture_path}")

        except Exception as e:
            print(f"Failed to copy texture '{texture}': {e}")

# --------------------- VRayVRmat Repathing Functions ---------------------

def get_vrayvrmat_paths():
    """
    Get all unique file paths used by VRayVRmatMtl shaders in the scene.

    :return: A dictionary mapping file paths to shader nodes.
    """
    shaders = cmds.ls(type='VRayVRmatMtl')
    path_to_shaders = {}
    for shader in shaders:
        path = cmds.getAttr(f"{shader}.fileName")
        if path:
            if path not in path_to_shaders:
                path_to_shaders[path] = []
            path_to_shaders[path].append(shader)
    return path_to_shaders

def update_vrayvrmat_paths(old_path, new_path, shaders):
    """
    Update the file path for multiple VRayVRmatMtl shaders.

    :param old_path: The old file path to be replaced.
    :param new_path: The new file path to set.
    :param shaders: The list of shader nodes to update.
    """
    for shader in shaders:
        cmds.setAttr(f"{shader}.fileName", new_path, type="string")
    print(f"Updated path from {old_path} to {new_path} for shaders: {', '.join(shaders)}")
    refresh_vrayvrmat_ui()

def refresh_vrayvrmat_ui():
    """
    Refresh the VRmat Repath Manager UI.
    """
    if cmds.window("VRmatRepathManager", exists=True):
        cmds.deleteUI("VRmatRepathManager")
    repath_vrayvrmat_ui()

def repath_vrayvrmat_ui():
    """
    Create a UI for repathing VRayVRmatMtl shaders by path and shader.
    """
    window_name = "VRmatRepathManager"

    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    cmds.window(window_name, title="VRmat Repath Manager", widthHeight=(400, 300))
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

    # Path-Centric Tab
    child1 = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")
    path_to_shaders = get_vrayvrmat_paths()
    global vrayvrmat_path_list
    vrayvrmat_path_list = cmds.textScrollList(append=list(path_to_shaders.keys()), selectCommand=show_selected_path_shaders, height=150)
    cmds.button(label="Set New Path", command=set_new_vrayvrmat_path)
    global selected_path_field
    selected_path_field = cmds.textFieldGrp(label="Current Path:", editable=False)
    cmds.setParent('..')

    # Shader-Centric Tab
    child2 = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")
    global vrayvrmat_shader_list
    vrayvrmat_shader_list = cmds.textScrollList(append=cmds.ls(type='VRayVRmatMtl'), selectCommand=show_selected_shader_path, height=150)
    cmds.button(label="Set New Shader Path", command=set_new_shader_path)
    global selected_shader_path
    selected_shader_path = cmds.textFieldGrp(label="Current Shader Path:", editable=False)
    cmds.setParent('..')

    cmds.tabLayout(tabs, edit=True, tabLabel=((child1, 'Path-Centric'), (child2, 'Shader-Centric')))
    cmds.showWindow(window_name)

def show_selected_path_shaders():
    """
    Display the current file path of the selected VRayVRmatMtl shader path.
    """
    selected = cmds.textScrollList(vrayvrmat_path_list, query=True, selectItem=True)
    if selected:
        cmds.textFieldGrp(selected_path_field, edit=True, text=selected[0])

def set_new_vrayvrmat_path(*args):
    """
    Set a new file path for the selected VRayVRmatMtl shader path.
    """
    selected = cmds.textScrollList(vrayvrmat_path_list, query=True, selectItem=True)
    if selected:
        new_path = open_file_browser(caption="Select New VRmat File")
        if new_path:
            path_to_shaders = get_vrayvrmat_paths()
            update_vrayvrmat_paths(selected[0], new_path, path_to_shaders[selected[0]])
            cmds.textFieldGrp(selected_path_field, edit=True, text=new_path)

def show_selected_shader_path():
    """
    Display the current file path of the selected VRayVRmatMtl shader.
    """
    selected = cmds.textScrollList(vrayvrmat_shader_list, query=True, selectItem=True)
    if selected:
        current_path = cmds.getAttr(f"{selected[0]}.fileName")
        cmds.textFieldGrp(selected_shader_path, edit=True, text=current_path)

def set_new_shader_path(*args):
    """
    Set a new file path for the selected VRayVRmatMtl shader.
    """
    selected = cmds.textScrollList(vrayvrmat_shader_list, query=True, selectItem=True)
    if selected:
        new_path = open_file_browser(caption="Select New VRmat File")
        if new_path:
            cmds.setAttr(f"{selected[0]}.fileName", new_path, type="string")
            cmds.textFieldGrp(selected_shader_path, edit=True, text=new_path)
            refresh_vrayvrmat_ui()

# --------------------- Maya UI Integration ---------------------

def create_maya_ui():
    """
    Create a simple Maya UI with tabs to execute the main functions.
    """
    window_name = "VRmatShaderManager"

    # If the window already exists, delete it
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    # Create a new window with tabs
    cmds.window(window_name, title="VRmat Shader Manager", widthHeight=(400, 400))
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

    # Tab 1: Shader Replacement and Repathing
    child1 = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")
    cmds.button(label="Replace Shaders with VRmat", command=lambda x: main_replace_shaders())
    cmds.button(label="Move Textures and Update VRscene", command=lambda x: main_move_textures_and_update_vrscene())
    cmds.button(label="Open VRmat Repath Manager", command=lambda x: repath_vrayvrmat_ui())
    cmds.setParent('..')

    # Tab 2: Shader Info
    child2 = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")
    shading_groups = cmds.ls(type='shadingEngine')
    shading_group_menu = cmds.optionMenu(label="Select Shading Group", changeCommand=update_shader_info)
    for sg in shading_groups:
        cmds.menuItem(label=sg)
    global shader_info_list
    shader_info_list = cmds.textScrollList(numberOfRows=8, allowMultiSelection=False, height=150)
    cmds.setParent('..')

    cmds.tabLayout(tabs, edit=True, tabLabel=((child1, 'Shader Replacement & Repathing'), (child2, 'Shader Info')))
    cmds.showWindow(window_name)

def update_shader_info(selected_group):
    """
    Update the shader info display based on the selected shading group.
    
    :param selected_group: The selected shading group.
    """
    shader_info = get_shader_info_from_group(selected_group)
    cmds.textScrollList(shader_info_list, edit=True, removeAll=True)
    if shader_info:
        for key, value in shader_info.items():
            cmds.textScrollList(shader_info_list, edit=True, append=f"{key}: {value}")

def get_shader_info_from_group(shading_group_name):
    """
    Retrieve shader information for the specified shading group.
    
    :param shading_group_name: The name of the shading group.
    :return: A dictionary with shader information.
    """
    connections = get_shading_group_connections(shading_group_name)
    shader = None
    if connections:
        for conn in connections['incoming']:
            if 'outColor' in conn:
                shader = conn.split('.')[0]
                break

    if shader:
        shader_info = get_shader_info(shader)
        return shader_info
    else:
        print(f"No shader connected to '{shading_group_name}'.")
        return {}

# --------------------- Main Functions ---------------------

def main_replace_shaders():
    """
    Main function to replace shaders with VRmat based on user-selected file.
    """
    file_path = open_file_browser()
    if file_path and (file_path.endswith('.vrmat') or file_path.endswith('.vrscene')):
        replace_shaders_with_vrmat(file_path)
    else:
        print("No valid file selected or unsupported file type.")

def main_move_textures_and_update_vrscene():
    """
    Main function to move textures and update paths in a .vrscene file.
    """
    file_path = open_file_browser(caption="Select VRscene File")
    if file_path and file_path.endswith('.vrscene'):
        move_textures_and_update_vrscene(file_path)
    else:
        print("No valid VRscene file selected.")

def show_vrmat_shader_manager():
    """
    Function to show the VRmat Shader Manager UI.
    """
    create_maya_ui()
