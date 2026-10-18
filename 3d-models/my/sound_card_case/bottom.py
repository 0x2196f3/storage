import FreeCAD as App
import Part

# -------- Editable dimensions (mm) --------
PCB_W = 29.10
PCB_L = 56.90
HOLE_SPACING_X = 19.00
HOLE_SPACING_Y = 45.00

# Case fit
SIDE_CLEARANCE = 0.50
WALL = 1.60
BOTTOM = 2.00
WALL_HEIGHT = 19.00
CORNER_RADIUS = 2.00

# PCB mounting posts
POST_DIA = 5.50
POST_HEIGHT = 3.50
PILOT_DIA = 1.60        # pilot hole for an M2 self-tapping screw
PILOT_DEPTH = 4.50

# Connector openings
PCB_THICKNESS = 1.60

USB_CUTOUT_W = 9.50
USB_CUTOUT_H = 4.00
USB2_CUTOUT_H = 12.00
USB_CENTER_Z_OFFSET = 3.00
USB2_CENTER_Z_OFFSET = 5.00

# Lid
LID_THICKNESS = 2.00
SKIRT_THICKNESS = 1.60
SKIRT_DEPTH = 3.50
LID_CLEARANCE = 0.20

# -------- Derived dimensions --------
OUT_W = PCB_W + 2.0 * (SIDE_CLEARANCE + WALL)
OUT_L = PCB_L + 2.0 * (SIDE_CLEARANCE + WALL)
IN_W = OUT_W - 2.0 * WALL
IN_L = OUT_L - 2.0 * WALL
BASE_H = BOTTOM + WALL_HEIGHT

# -------- Geometry helper --------
def rounded_box(x, y, z, dx, dy, dz, radius):
    """Create a box with rounded vertical corners."""
    shape = Part.makeBox(dx, dy, dz, App.Vector(x, y, z))
    r = min(radius, dx / 2.0 - 0.01, dy / 2.0 - 0.01)

    if r > 0:
        vertical_edges = []
        for edge in shape.Edges:
            vertices = edge.Vertexes
            if len(vertices) == 2:
                p1 = vertices[0].Point
                p2 = vertices[1].Point
                if abs(p1.x - p2.x) < 1e-7 and abs(p1.y - p2.y) < 1e-7:
                    vertical_edges.append(edge)

        if vertical_edges:
            shape = shape.makeFillet(r, vertical_edges)

    return shape


# -------- Create document --------
doc = App.newDocument("PCB_Case")

# -------- Hollow base tray --------
outer = rounded_box(
    0, 0, 0,
    OUT_W, OUT_L, BASE_H,
    CORNER_RADIUS
)

cavity = rounded_box(
    WALL, WALL, BOTTOM,
    IN_W, IN_L, WALL_HEIGHT + 1.0,
    max(0.5, CORNER_RADIUS - WALL)
)

base_shape = outer.cut(cavity)

# -------- Mounting posts --------
hole_x = [
    OUT_W / 2.0 - HOLE_SPACING_X / 2.0,
    OUT_W / 2.0 + HOLE_SPACING_X / 2.0
]
hole_y = [
    OUT_L / 2.0 - HOLE_SPACING_Y / 2.0,
    OUT_L / 2.0 + HOLE_SPACING_Y / 2.0
]

for x in hole_x:
    for y in hole_y:
        post = Part.makeCylinder(
            POST_DIA / 2.0,
            POST_HEIGHT,
            App.Vector(x, y, BOTTOM)
        )
        base_shape = base_shape.fuse(post)

# Blind pilot holes in the posts for screws inserted through the PCB
post_top = BOTTOM + POST_HEIGHT
pilot_bottom = max(BOTTOM + 0.30, post_top - PILOT_DEPTH)

for x in hole_x:
    for y in hole_y:
        pilot = Part.makeCylinder(
            PILOT_DIA / 2.0,
            post_top - pilot_bottom + 0.05,
            App.Vector(x, y, pilot_bottom)
        )
        base_shape = base_shape.cut(pilot)

# -------- Connector openings through opposite short-end walls --------
board_bottom_z = BOTTOM + POST_HEIGHT
board_mid_z = board_bottom_z + PCB_THICKNESS / 2.0

# USB-C rectangular opening on the -Y end
usb_center_z = board_mid_z + USB_CENTER_Z_OFFSET

usb_cut = Part.makeBox(
    USB_CUTOUT_W,
    WALL + 0.20,
    USB_CUTOUT_H,
    App.Vector(
        OUT_W / 2.0 - USB_CUTOUT_W / 2.0,
        -0.10,
        usb_center_z - USB_CUTOUT_H / 2.0
    )
)
base_shape = base_shape.cut(usb_cut)

# Second USB-C rectangular opening on the opposite, +Y end
usb2_center_z = board_mid_z + USB2_CENTER_Z_OFFSET

usb2_cut = Part.makeBox(
    USB_CUTOUT_W,
    WALL + 0.20,
    USB2_CUTOUT_H,
    App.Vector(
        OUT_W / 2.0 - USB_CUTOUT_W / 2.0,
        OUT_L - WALL - 0.10,
        usb2_center_z - USB_CUTOUT_H / 2.0
    )
)
base_shape = base_shape.cut(usb2_cut)

# -------- Add base to document --------
base_obj = doc.addObject("Part::Feature", "Base")
base_obj.Label = "PCB case base"
base_obj.Shape = base_shape

# -------- Display --------
base_obj.ViewObject.ShapeColor = (0.72, 0.76, 0.82)

doc.recompute()
Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()
