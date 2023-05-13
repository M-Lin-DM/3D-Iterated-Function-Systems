from typing import Optional
import c4d
from generate_tree import generate_objects
from utils import get_random_base_color

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected


params = dict()
params['generations'] = 5  # # of genertations of the tree to create. # objects increases exponentially over generations
params['scale_factor'] = 0.5  # scale factor controlling object size decay over generations. Lower --> faster decay
params['col_scale_factor'] = 0.8  # decay factor for magnitude of displacement vector in RGB space. Lower --> more homogeneous branches (since faster convergence of colors)
params['min_children'] = 3  # min # branches per parent object
params['max_children'] = 7  # max # branches per parent object
params['dx_size'] = .55  # scale factor affecting how far away children are from their parent object
params['stretch_size'] = 0.4  # factor affecting how much spheres are stretched
params['col_delta_size'] = .22  # size of the initial step in RGB space taken in gen 1
params['rot_delta_size'] = 20  # size of initial rotation taken in gen 1
params['pruning_max_scale'] = 0.7  # Objects with larger scale are not plotted. =max obj scale in gen1 = scale_factor.
params['base_color'] = get_random_base_color()  # e.g. np.array([0.5, 0.5, 0.5])
params['stretch'] = True  # If true, allows ellipsoid. If false, only spheres.



def get_reference_mat(mat_name):
    for i, m in enumerate(doc.GetMaterials()):
        if m.GetName() == mat_name:
            return m


def insert_object(o):
    # INSTANTIATE OBJECT
    if o.obj_type == 'sphere':
        obj = c4d.BaseObject(c4d.Osphere)  # Create new sphere
        obj[c4d.PRIM_SPHERE_SUB] = 60  # controls mesh density on surface of object
        obj[c4d.PRIM_SPHERE_RAD] = o.radius
    elif o.obj_type == 'cube':
        obj = c4d.BaseObject(c4d.Ocube)
        obj[c4d.PRIM_CUBE_LEN] = c4d.Vector(o.length, o.length, o.length)

    # POSITION
    obj.SetRelPos(c4d.Vector(o.px, o.py, o.pz))  # Set position of obj

    # SCALE
    obj.SetRelScale(c4d.Vector(o.sx, o.sy, o.sz))

    # ROTATION
    obj.SetRelRot(c4d.Vector(o.rx, o.ry, o.rz))

    # create material
    mat = c4d.Material()  # must use doc to insert mat
    mat.SetName('mat_')

    # MODIFY MATERIAL -- # remove any of these that work by default
    mat[c4d.MATERIAL_USE_COLOR] = True
    mat[c4d.MATERIAL_USE_LUMINANCE] = False
    mat[c4d.MATERIAL_USE_REFLECTION] = False

    # COLOR
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

    objects_sweep = []
    for sf in [0.5]:
        params['scale_factor'] = sf
        objects_list = generate_objects(params)  # cycle across params to superimpose as layers
        objects_sweep.extend(objects_list)

    print('inserting objects')
    if len(objects_sweep) > 5000:
        raise Exception("Too many objects. C4D may crash. Reduce generations or number of children.")
    
    for obj in objects_sweep:
        if (obj.sx + obj.sy + obj.sz) / 3 <= params['pruning_max_scale']:
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