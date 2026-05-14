# SPDX-License-Identifier: GPL-2.0-or-later

import ctypes
import platform
from typing import Any

import bpy


class bNodeStack(ctypes.Structure):
    pass


bNodeStack._fields_ = [
    ("vec", ctypes.c_float * 4),
    ("min", ctypes.c_float),
    ("max", ctypes.c_float),
    ("data", ctypes.c_void_p),
    ("hasinput", ctypes.c_short),
    ("hasoutput", ctypes.c_short),
    ("datatype", ctypes.c_short),
    ("sockettype", ctypes.c_short),
    ("is_copy", ctypes.c_short),
    ("external", ctypes.c_short),
    ("_pad", ctypes.c_char * 4),
]


class bNodeSocketRuntimeHandle(ctypes.Structure):
    pass


_bNodeSocketRuntimeHandle_fields: list[tuple[str, Any]] = []
if platform.system() == "Windows":
    _bNodeSocketRuntimeHandle_fields.append(("_pad0", ctypes.c_char * 8))
_bNodeSocketRuntimeHandle_fields += [
    ("declaration", ctypes.c_void_p),
    ("changed_flag", ctypes.c_uint32),
    ("total_inputs", ctypes.c_short),
    ("_pad1", ctypes.c_char * 2),
    ("location", ctypes.c_float * 2),
]
bNodeSocketRuntimeHandle._fields_ = _bNodeSocketRuntimeHandle_fields


class bNodeSocket(ctypes.Structure):
    pass


bNodeSocket._fields_ = [
    ("next", ctypes.c_void_p),
    ("prev", ctypes.c_void_p),
    ("prop", ctypes.c_void_p),
    ("identifier", ctypes.c_char * 64),
    ("name", ctypes.c_char * 64),
    ("storage", ctypes.c_void_p),
    ("in_out", ctypes.c_short),
    ("typeinfo", ctypes.c_void_p),
    ("idname", ctypes.c_char * 64),
    ("default_value", ctypes.c_void_p),
    ("_pad", ctypes.c_char * 4),
    ("label", ctypes.c_char * 64),
    ("description", ctypes.c_char * 64),
    ("short_label", ctypes.c_char * 64),
    ("default_attribute_name", ctypes.POINTER(ctypes.c_char)),
    ("to_index", ctypes.c_int),
    ("link", ctypes.c_void_p),
    ("ns", bNodeStack),
    ("runtime", ctypes.POINTER(bNodeSocketRuntimeHandle)),
]


class rctf(ctypes.Structure):
    pass


rctf._fields_ = [
    ("xmin", ctypes.c_float),
    ("xmax", ctypes.c_float),
    ("ymin", ctypes.c_float),
    ("ymax", ctypes.c_float),
]


class bNodeRuntime(ctypes.Structure):
    pass


_bNodeRuntime_fields: list[tuple[str, Any]] = [
    ("declaration", ctypes.c_void_p),
    ("changed_flag", ctypes.c_uint32),
    ("need_exec", ctypes.c_uint8),
    ("original", ctypes.c_void_p),
]
if bpy.app.version >= (4, 4, 0):
    _bNodeRuntime_fields.append(("draw_bounds", rctf))
else:
    _bNodeRuntime_fields.append(("totr", rctf))
_bNodeRuntime_fields += [
    ("tmp_flag", ctypes.c_short),
    ("iter_flag", ctypes.c_char),
    ("update", ctypes.c_int),
    ("anim_ofsx", ctypes.c_float),
    ("internal_links", ctypes.c_void_p),
    ("index_in_tree", ctypes.c_int),
    ("forward_compatible_versioning_done", ctypes.c_bool),
    ("is_dangling_reroute", ctypes.c_bool),
]
bNodeRuntime._fields_ = _bNodeRuntime_fields


class bNode(ctypes.Structure):
    pass


_bNode_fields: list[tuple[str, Any]] = [
    ("next", ctypes.POINTER(bNode)),
    ("prev", ctypes.POINTER(bNode)),
    ("inputs", ctypes.c_void_p * 2),
    ("outputs", ctypes.c_void_p * 2),
    ("name", ctypes.c_char * 64),
    ("identifier", ctypes.c_int32),
    ("flag", ctypes.c_int),
    ("idname", ctypes.c_char * 64),
    ("typeinfo", ctypes.c_void_p),
]
if bpy.app.version >= (4, 4, 0):
    _bNode_fields.append(("type_legacy", ctypes.c_int16))
else:
    _bNode_fields.append(("type", ctypes.c_int16))
_bNode_fields += [
    ("ui_order", ctypes.c_int16),
    ("custom1", ctypes.c_int16),
    ("custom2", ctypes.c_int16),
    ("custom3", ctypes.c_float),
    ("custom4", ctypes.c_float),
]
if bpy.app.version >= (4, 3, 0):
    _bNode_fields += [
        ("warning_propagation", ctypes.c_int8),
        ("_pad", ctypes.c_char * 7),
    ]
_bNode_fields += [
    ("id", ctypes.c_void_p),
    ("storage", ctypes.c_void_p),
    ("prop", ctypes.c_void_p),
    ("parent", ctypes.c_void_p),
]
if bpy.app.version >= (4, 4, 0):
    _bNode_fields.append(("location", ctypes.c_float * 2))
else:
    _bNode_fields += [
        ("locx", ctypes.c_float),
        ("locy", ctypes.c_float),
    ]
_bNode_fields += [
    ("width", ctypes.c_float),
    ("height", ctypes.c_float),
]
if bpy.app.version >= (4, 3, 0):
    _bNode_fields += [
        ("locx_legacy", ctypes.c_float),
        ("locy_legacy", ctypes.c_float),
        ("offsetx_legacy", ctypes.c_float),
        ("offsety_legacy", ctypes.c_float),
    ]
else:
    _bNode_fields += [
        ("offsetx", ctypes.c_float),
        ("offsety", ctypes.c_float),
    ]
_bNode_fields += [
    ("label", ctypes.c_char * 64),
    ("color", ctypes.c_float * 3),
    ("num_panel_states", ctypes.c_int),
    ("panel_states_array", ctypes.c_void_p),
    ("runtime", ctypes.POINTER(bNodeRuntime)),
]
bNode._fields_ = _bNode_fields
