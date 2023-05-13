from typing import Optional
import c4d
import numpy as np
from generate_tree import Functions, generate_objects

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected


param = dict()
# # spatial distrib properties
param['N_generations'] = 5  # 
# param['y_spread'] = 400  # spread in y axis for stacked 2D plot

def get_reference_mat(mat_name):
    for i, m in enumerate(doc.GetMaterials()):
        # print(m.GetName())
        if m.GetName() == mat_name:
            return m


def insert_object(o):
    # INSTANTIATE OBJECT
    if o.obj_type == 'sphere':
        obj = c4d.BaseObject(c4d.Osphere)  # Create new sphere
        obj[c4d.PRIM_SPHERE_SUB] = o.segments
        obj[c4d.PRIM_SPHERE_RAD] = o.radius
    elif o.obj_type == 'cube':
        print(o)
        return
        obj = c4d.BaseObject(c4d.Ocube)
        obj[c4d.PRIM_CUBE_LEN] = o.length

    # POSITION
    obj.SetRelPos(c4d.Vector(o.px, o.py, o.pz))  # Set position of obj

    # SCALE
    obj.SetRelScale(c4d.Vector(o.sx, o.sy, o.sz))

    # ROTATION
    obj.SetRelRot(c4d.Vector(o.rx, o.ry, o.rz))

    # create material
    mat = c4d.Material()  # cant create a material this way. must use doc to insert
    mat.SetName('mat_')

    # MODIFY MATERIAL -- # remove any of these that are work by default
    mat[c4d.MATERIAL_USE_COLOR] = True
    mat[c4d.MATERIAL_USE_LUMINANCE] = False
    mat[c4d.MATERIAL_USE_REFLECTION] = False

    # color
    mat[c4d.MATERIAL_COLOR_COLOR] = c4d.Vector(o.R, o.G, o.B)

    doc.InsertMaterial(mat, None)

    # create tag
    texture_tag = c4d.TextureTag()
    texture_tag.SetMaterial(mat)  # attach a certain material to this tag

    obj.InsertTag(texture_tag)  # attach tag containing material to object
    doc.InsertObject(obj)  # Insert object in document


def remove_spheres(doc):
    # Get a list of all objects in the document
    objects = doc.GetObjects()
    for obj in objects:
        if obj.GetType() == c4d.Osphere:
            obj.Remove()  # Delete object


def main() -> None:
    doc = c4d.documents.GetActiveDocument()
    render_data = doc.GetActiveRenderData()
    # adjust save path in render data
    render_data[
        c4d.RDATA_PATH] = f'C:/Users/MrLin/OneDrive/Documents/Experiments/3D Iterated Function Systems/Renders/img.png'

    # make bitmap
    bmp = c4d.bitmaps.BaseBitmap()
    bmp.Init(int(render_data[c4d.RDATA_XRES]), int(render_data[c4d.RDATA_YRES]), depth=24)

    funcs = Functions()
    function_list = [funcs.f0, funcs.f1, funcs.f2, funcs.f3, funcs.f4, funcs.f5]  # this could be mutated each gen or each object its applied to

    objects_list = generate_objects(generations=param['N_generations'], f_list=function_list)

    #print(objects_list)

    print('inserting objects')
    for obj in objects_list:
        insert_object(obj)

    c4d.EventAdd()

    print('Rendering')
    # if c4d.documents.RenderDocument(doc, render_data.GetData(), bmp, c4d.RENDERFLAGS_EXTERNAL) != c4d.RENDERRESULT_OK:
    #     raise RuntimeError("Failed to render the temporary document.")

    print('removing objects')
    # clear out all spheres
    # remove_spheres(doc)
    # c4d.EventAdd()


if __name__ == '__main__':
    main()