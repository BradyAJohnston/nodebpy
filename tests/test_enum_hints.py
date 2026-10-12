"""A mistyped enum value suggests the closest options."""

import pytest

from nodebpy import geometry as g


@pytest.mark.parametrize(
    ("build", "message"),
    [
        (lambda: g.Math(operation="SUBSTRACT"), "Did you mean 'SUBTRACT'?"),
        (lambda: g.Math(operation="add"), "Did you mean 'ADD'?"),
        (lambda: g.CaptureAttribute(domain="FACES"), "Did you mean 'FACE'?"),
        (lambda: g.IndexSwitch(data_type="FLAOT"), "Did you mean 'FLOAT'"),
    ],
)
def test_enum_typos_suggest_options(build, message):
    with g.tree():
        with pytest.raises(TypeError, match=message):
            build()


def test_menu_socket_typos_suggest_options():
    with pytest.raises(TypeError, match=r"'Mode' menu has no option 'Coutn'.*'Count'"):
        with g.tree():
            g.ResampleCurve(mode="Coutn")


def test_unknown_enum_value_lists_the_options():
    with g.tree():
        with pytest.raises(TypeError, match=r"no option 'XYZZY'\. Options: ADD"):
            g.Math(operation="XYZZY")


def test_optional_enum_typos_suggest_options():
    with g.tree():
        assert g.VoronoiTexture(voronoi_dimensions="2D").voronoi_dimensions == "2D"
        with pytest.raises(TypeError, match="Did you mean '2D'"):
            g.VoronoiTexture(voronoi_dimensions="2d ")


def test_other_type_errors_pass_through():
    from nodebpy.builder._utils import enum_value_error

    error = TypeError("expected a float")
    assert enum_value_error(error, "Math's operation") is error
