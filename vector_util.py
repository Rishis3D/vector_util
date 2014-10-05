import pymel.core as pm

def viz_vec_3(end, start=(0,0,0), name='curve', color_index=16):
                   
    pos = ([end[0], end[1], end[2]], [start[0], start[1], start[2]])        
    crv = pm.curve(degree=1, p=pos, name=name)   
    
    # 6:blue, 16:white, 17:yellow
    if(color_index):
        pm.setAttr('{0}.overrideEnabled'.format(crv.getShape()), 1)
        pm.setAttr('{0}.overrideColor'.format(crv.getShape()), color_index)
        
    return [crv, crv.getShape()]
    
     
def ortho_vectors_from_aim_and_up(aim_vec, up_vec, invert_aim=False, invert_up=False):
    
    if aim_vec == up_vec:
        pm.warning('The joint aim axis can not be equal to the joint up axis!')
        return
            
    # create a pymel vector and normalize
    aim_vec = pm.datatypes.Vector(aim_vec[0], aim_vec[1], aim_vec[2])
    up_vec = pm.datatypes.Vector(up_vec[0], up_vec[1], up_vec[2])
      
    # normalize the input vectors
    vec_aim_n = aim_vec.normal()
    vec_up_n = up_vec.normal()
    
    # invert the vectors 
    if invert_aim:
        vec_aim_n *= -1
            
    if invert_up:
        vec_up_n *= -1
        
    # get the cross product 
    vec_cross = vec_up_n.cross(vec_aim_n)
    
    # make sure that the up vector is orthogonal
    vec_up_orto_n = vec_aim_n.cross(vec_cross)
    
    return {'aim':vec_aim_n , 'up':vec_up_orto_n, 'cross':vec_cross}
        
def remap_aim_and_up(aim_vec, up_vec, pos=(0,0,0), aim_axis=0, up_axis=2, invert_aim=False, invert_up=False):
    
    ortho_axis = ortho_vectors_from_aim_and_up(aim_vec=aim_vec, up_vec=up_vec, aim_axis=aim_axis, up_axis=up_axis, invert_aim=invert_aim, invert_up=invert_up)
    
    
   
d = [n for n in pm.ls(type='transform') if isinstance(n.getShape(), pm.nodetypes.NurbsCurve)]
pm.delete(d)

aim_vec = (.5,0,-.5)
up_vec=(2,2,2)        

vecs = ortho_vectors_from_aim_and_up(aim_vec=aim_vec, up_vec=up_vec, invert_aim=False, invert_up=False)

viz_vec_3(end=aim_vec, name='aim_first', color_index=17)
viz_vec_3(end=up_vec, name='up_first', color_index=17)

viz_vec_3(end=vecs.get('aim'), name='aim', color_index=16)
viz_vec_3(end=vecs.get('up'), name='up', color_index=6)
viz_vec_3(end=vecs.get('cross'), name='cross', color_index=11)

#d = matrix_from_aim_and_position(aim_vec=aim_vec, up_vec=up_vec)




