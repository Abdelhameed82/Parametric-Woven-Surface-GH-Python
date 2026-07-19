import Grasshopper as ghc
import ghpythonlib.components as gh


# ============================================================
# 1. GENERATE BASE CURVES
# ============================================================

def generate_base_curves(start_x,end_x,base_y,height,spacing,count):
    
    """
Creates a diagonal base curve and duplicates it along the X-axis.

Parameters:
    start_x : X-coordinate of the starting point.
    end_x   : X-coordinate used to define the ending point.
    base_y  : Y-coordinate shared by both endpoints.
    height  : Z-coordinate of the ending point.
    spacing : Distance between duplicated curves.
    count   : Number of curves in the linear array.
    """
    
    start_point = gh.ConstructPoint(start_x, base_y, 0)
    
    end_point = gh.ConstructPoint(-end_x, base_y, height)
    
    base_curve = gh.Line(start_point,end_point)
    
    base_curves = gh.LinearArray(base_curve, gh.UnitX(spacing), count)[0]
    
    return base_curves


# ============================================================
# 2. CREATE WAVY SEGMENTS
# ============================================================

def create_wavy_segments(base_curve, subdiv_count, alternate_direction, amplitude):
    
    """
    Divide a base curve and alternately displace its points
    along the Y-axis to create a wavy pattern.

    Parameters:
        base_curve          : Input curve to be subdivided.
        subdiv_count        : Number of curve divisions.
        alternate_direction : Defines the initial displacement pattern.
        amplitude           : Distance of point displacement.
    """
    
    if subdiv_count < 3:
        raise ValueError("subdiv_count must be at least 3")
    
    # Divide the curve into points
    points = gh.DivideCurve(base_curve, subdiv_count, False)[0]
    
    deformed_points = []
    
    # Alternately displace the curve points
    for i, point in enumerate(points):
        
        if alternate_direction:
            move_condition = i % 2 == 0
        else:
            move_condition = i % 2 != 0
        
        if move_condition:
            
            deformed_point = gh.Move(point,gh.UnitY(-amplitude))[0]
            
            deformed_points.append(deformed_point)
        
        else:
            deformed_points.append(point)
    
    # Connect consecutive points into line segments
    segment_lines = []
    
    for point_a, point_b in zip(deformed_points,deformed_points[1:]):
        
        segment_lines.append(gh.Line(point_a,point_b))
    
    return segment_lines


# ============================================================
# 3. GENERATE SEGMENTED CURVE NETWORK
# ============================================================

def generate_curve_network(base_curves,subdiv_count,alternate_direction,amplitude):
    
    """
Generates a network of alternating wavy curves.

Neighboring base curves use opposite displacement patterns,
creating an alternating woven or interlocking effect.
    """
    
    curve_network = []
    
    for j, crv in enumerate(base_curves):
        
        current_direction = alternate_direction
        
        # Reverse the pattern on neighboring curves
        if j % 2 != 0:
            current_direction = not alternate_direction
        
        curve_segments = create_wavy_segments(crv,subdiv_count,current_direction,amplitude)
        
        curve_network.append(curve_segments)
    
    return curve_network


# ============================================================
# 4. GENERATE BASE CURVES
# ============================================================

base_curves = generate_base_curves(start_x,end_x,base_y,height,spacing,count)


# ============================================================
# 5. GENERATE CURVE NETWORK
# ============================================================

curve_network = generate_curve_network(base_curves,subdiv_count,alternate_direction,amplitude)

# ============================================================
# 6. GENERATE RULED SURFACE PANELS
# ============================================================

panels = ghc.DataTree[object]()

for k in range(len(curve_network) - 1):
    
    for sub_ind, (a,b) in enumerate(zip(curve_network[k], curve_network[k + 1])):
        
        path = ghc.Kernel.Data.GH_Path(k, sub_ind)
        panel = gh.RuledSurface(a,b)
        panels.Add(panel,path)

