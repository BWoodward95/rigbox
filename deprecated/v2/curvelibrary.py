'''
Curve Library v1.0

To-Do:
    Curved Arrows
    4-Point Arrow
    Gear 
    Semi-Circle
'''

import maya.cmds as cmds

COLORS = {
    "red": (1, 0, 0),
    "orange": (1, 0.25, 0),
    "yellow": (1, 0.75, 0),
    "green": (0, 1, 0),
    "cyan": (0, 1, 1),
    "blue": (0, 0, 1),
    "indigo": (0.1, 0, 1),
    "violet": (0.25, 0, 1),
    "pink": (1, 0, 1),
    "white": (1, 1, 1),
    "grey": (0.5, 0.5, 0.5),
    "black": (0, 0, 0),
}
    

def create_curve(points, name, color):
    curve = cmds.curve(d=1, p=points)
    RigBoxCurveLibrary.change_colors(curve, color)
    RigBoxCurveLibrary.finalize_curve(curve, name)


def change_colors(curve, color):
    cmds.setAttr(f"{curve}.overrideEnabled", 1)
    cmds.setAttr(f"{curve}.overrideRGBColors", 1)
    
    rgb = ("R", "G", "B")
    color_values = RigBoxCurveLibrary.COLORS.get(color, (1, 1, 1))

    for channel, value in zip(rgb, color_values):
        cmds.setAttr(f"{curve}.overrideColor{channel}", value)


def finalize_curve(curve, name):
    cmds.closeCurve(curve, rpo=True)
    cmds.rename(curve, name)

def single_arrow(self, name, color, length=2):
    points = [(0,0,-1), (length,0,-1), (length,0,-2), (length+2,0,0), (length,0,2), (length,0,1), (0,0,1)]
    self.create_curve(points, name, color)

def double_arrow(self, name, color, length=2):
    points = [(length,0,-1), (length,0,-2), (length+2,0,0), (length,0,2), (length,0,1), (-length,0,1), (-length,0,1), (-length,0,2), (-length-44,0,0), (-length,0,-2), (-length,0,-1)]
    self.create_curve(points, name, color)
    
def square(self, name, color):
    points = [(2,0,2), (2,0,-2), (-2,0,-2), (-2,0,2)]
    self.create_curve(points, name, color)

def cube(self, name, color):
    points = [(1,-1,1), (-1,-1,1), (-1,-1,-1), (1,-1,-1), (1,-1,1), (1,1,1), (-1,1,1), (-1,-1,1), (-1,1,1), (-1,-1,1), (-1,1,1), (-1,1,-1), (-1,-1,-1), (-1,1,-1), (1,1,-1), (1,-1,-1), (1,1,-1), (1,1,1)]
    self.create_curve(points, name, color)

def circle(self, name, color):
    curve = cmds.circle(name=name, nr=(0, 1, 0))
    self.change_colors(curve[0], color)
