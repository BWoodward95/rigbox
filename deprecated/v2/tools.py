'''
RigBox Tools

'''

import maya.cmds as cmds
import maya.api.OpenMaya as om

def query_location(name):
    result = cmds.xform(name, q=True, t=True)
        
    return result

def query_rotation(name):
    result = cmds.xform(name, q=True, ws=True, ro=True)
        
    return result
    
def average_location(primaryAxis, lastJoint):
    lastJoint_pos = cmds.xform(lastJoint, q=True, t=True)
    
    if primaryAxis == "X":
        result = lastJoint_pos[0]/2 
        finalResult = (result, 0,0)     
    if primaryAxis == "Y":
        result = lastJoint_pos[1]/2
        finalResult = (0,result,0)        
    if primaryAxis == "Z":
        result = lastJoint_pos[2]/2
        finalResult = (0,0,result)
        
    if primaryAxis == "-X":
        result = lastJoint_pos[0]/2 
        finalResult = ((result*-1), 0,0)     
    if primaryAxis == "-Y":
        result = lastJoint_pos[1]/2
        finalResult = (0,(result*-1),0)        
    if primaryAxis == "-Z":
        result = lastJoint_pos[2]/2
        finalResult = (0,0,(result*-1))            
        
    return finalResult
    
def create_joint_chain(primaryAxis, upAxis, jointList):
    if primaryAxis == "X":
        aim = (1,0,0)            
    if primaryAxis == "Y":
        aim = (0,1,0)
    if primaryAxis == "Z":
        aim = (0,0,1)
    if primaryAxis == "-X":
        aim = (-1,0,0)
    if primaryAxis == "-Y":
        aim = (0,-1,0)
    if primaryAxis == "-Z":
        aim = (0,0,-1)
    
    if upAxis == "X":
        up = (1,0,0)
    if upAxis == "Y":
        up = (0,1,0)
    if upAxis == "Z":
        up = (0,0,1)
    if upAxis == "-X":
        up = (-1,0,0)
    if upAxis == "-Y":
        up = (0,-1,0)
    if upAxis == "-Z":
        up = (0,0,-1)
    
    for i in range(len(jointList)-1):
        aim_joint = cmds.aimConstraint(jointList[i+1], jointList[i], aim=aim, wu=up) # Aim parent at child (X-forward, Z-up)
        cmds.delete(aim_joint) # Delete aim constraint
        cmds.makeIdentity(apply=True, r=True) # Zero joint rotations
        cmds.parent(jointList[i+1], jointList[i]) # Make parent relationship

def create_roll_sys(name, inJoint, outJoint, primaryAxis, factor):    
    sys_node = cmds.createNode("multiplyDivide", n=name)
    
    if primaryAxis == "X":
        cmds.connectAttr(f"{inJoint}.rx", f"{sys_node}.input1X")
        cmds.connectAttr(f"{sys_node}.outputX", f"{outJoint}.rx")

    if primaryAxis == "Y":
        cmds.connectAttr(f"{inJoint}.ry", f"{sys_node}.input1X")
        cmds.connectAttr(f"{sys_node}.outputX", f"{outJoint}.ry")

    if primaryAxis == "Z":
        cmds.connectAttr(f"{inJoint}.rz", f"{sys_node}.input1X")
        cmds.connectAttr(f"{sys_node}.outputX", f"{outJoint}.rz")            
        
    cmds.setAttr(f"{sys_node}.input2X", factor)
    
    return sys_node
    
def create_roll_jnt(name, first, last=None, average=True):
    cmds.select(first)
    roll_jnt = cmds.joint(n=name)
    
    if average:
        roll_jnt_pos = average_location("X", last)
    else:
        roll_jnt_pos = (0,0,0)
                    
    cmds.xform(roll_jnt, t=roll_jnt_pos)
    
    return roll_jnt           

def single_chain_ik(name, start, end, parent=None):
    ik_effector = cmds.ikHandle(n=name, sj=start, ee=end, sol="ikSCsolver")
    
    if parent:
        cmds.parent(ik_effector, parent)
    
    print(ik_effector)    
    return ik_effector
    
def pole_vector(startJoint, midJoint, endJoint, name, distance):
    start = cmds.xform(start, q=True, ws=True, t=True)
    mid = cmds.xform(mid, q=True, ws=True, t=True)
    end = cmds.xform(end, q=True, ws=True, t=True)

    startV = om.MVector(start[0], start[1], start[2])
    midV = om.MVector(mid[0], mid[1], mid[2])
    endV = om.MVector(end[0], end[1], end[2])

    startEnd = endV - startV
    startMid = midV - startV

    dotP = startMid * startEnd

    proj = float(dotP) / float(startEnd.length())

    startEndN = startEnd.normal()

    projV = startEnd * proj

    arrowV = startMid - projV
    arrowV *= 0

    finalV = arrowV + midV

    loc = cmds.spaceLocator()[0]

    cmds.xform(loc, ws=True, t=(finalV.x, finalV.y, finalV.z))
    cmds.rename(loc, f"{name}_poleVector1")    