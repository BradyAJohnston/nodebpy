# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import ctypes
import platform

import bpy


class bNodeStack(ctypes.Structure):
    vec: ctypes.c_float * 4
    min: ctypes.c_float
    max: ctypes.c_float
    data: ctypes.c_void_p
    hasinput: ctypes.c_short
    hasoutput: ctypes.c_short
    datatype: ctypes.c_short
    sockettype: ctypes.c_short
    is_copy: ctypes.c_short
    external: ctypes.c_short
    _pad: ctypes.c_char * 4


class bNodeSocketRuntimeHandle(ctypes.Structure):
    if platform.system() == "Windows":
        _pad0: ctypes.c_char * 8
    declaration: ctypes.c_void_p
    changed_flag: ctypes.c_uint32
    total_inputs: ctypes.c_short
    _pad1: ctypes.c_char * 2
    location: ctypes.c_float * 2


class bNodeSocket(ctypes.Structure):
    next: ctypes.c_void_p
    prev: ctypes.c_void_p
    prop: ctypes.c_void_p
    identifier: ctypes.c_char * 64
    name: ctypes.c_char * 64
    storage: ctypes.c_void_p
    in_out: ctypes.c_short
    typeinfo: ctypes.c_void_p
    idname: ctypes.c_char * 64
    default_value: ctypes.c_void_p
    _pad: ctypes.c_char * 4
    label: ctypes.c_char * 64
    description: ctypes.c_char * 64
    short_label: ctypes.c_char * 64
    default_attribute_name: ctypes.POINTER(ctypes.c_char)
    to_index: ctypes.c_int
    link: ctypes.c_void_p
    ns: bNodeStack
    runtime: ctypes.POINTER(bNodeSocketRuntimeHandle)


class rctf(ctypes.Structure):
    xmin: ctypes.c_float
    xmax: ctypes.c_float
    ymin: ctypes.c_float
    ymax: ctypes.c_float


class bNodeRuntime(ctypes.Structure):
    declaration: ctypes.c_void_p
    changed_flag: ctypes.c_uint32
    need_exec: ctypes.c_uint8
    original: ctypes.c_void_p
    if bpy.app.version >= (4, 4, 0):
        draw_bounds: rctf
    else:
        totr: rctf
    tmp_flag: ctypes.c_short
    iter_flag: ctypes.c_char
    update: ctypes.c_int
    anim_ofsx: ctypes.c_float
    internal_links: ctypes.c_void_p
    index_in_tree: ctypes.c_int
    forward_compatible_versioning_done: ctypes.c_bool
    is_dangling_reroute: ctypes.c_bool


class bNode(ctypes.Structure):
    next: ctypes.POINTER(bNode)  # type: ignore
    prev: ctypes.POINTER(bNode)  # type: ignore
    inputs: ctypes.c_void_p * 2
    outputs: ctypes.c_void_p * 2
    name: ctypes.c_char * 64
    identifier: ctypes.c_int32
    flag: ctypes.c_int
    idname: ctypes.c_char * 64
    typeinfo: ctypes.c_void_p
    if bpy.app.version >= (4, 4, 0):
        type_legacy: ctypes.c_int16
    else:
        type: ctypes.c_int16
    ui_order: ctypes.c_int16
    custom1: ctypes.c_int16
    custom2: ctypes.c_int16
    custom3: ctypes.c_float
    custom4: ctypes.c_float
    if bpy.app.version >= (4, 3, 0):
        warning_propagation: ctypes.c_int8
        _pad: ctypes.c_char * 7
    id: ctypes.c_void_p
    storage: ctypes.c_void_p
    prop: ctypes.c_void_p
    parent: ctypes.c_void_p
    if bpy.app.version >= (4, 4, 0):
        location: ctypes.c_float * 2
    else:
        locx: ctypes.c_float
        locy: ctypes.c_float
    width: ctypes.c_float
    height: ctypes.c_float
    if bpy.app.version >= (4, 3, 0):
        locx_legacy: ctypes.c_float
        locy_legacy: ctypes.c_float
        offsetx_legacy: ctypes.c_float
        offsety_legacy: ctypes.c_float
    else:
        offsetx: ctypes.c_float
        offsety: ctypes.c_float
    label: ctypes.c_char * 64
    color: ctypes.c_float * 3
    num_panel_states: ctypes.c_int
    panel_states_array: ctypes.c_void_p
    runtime: ctypes.POINTER(bNodeRuntime)


for cls in (
    bNodeStack,
    bNodeSocketRuntimeHandle,
    bNodeSocket,
    rctf,
    bNodeRuntime,
    bNode,
):
    cls._fields_ = [(k, eval(v)) for k, v in cls.__annotations__.items()]
