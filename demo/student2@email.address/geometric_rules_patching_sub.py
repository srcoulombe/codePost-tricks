"""

"""

# standard library dependencies
from math import pi
from numbers import Number 

def power(number:Number, power:Number) -> Number:
    """
    Wrapper around x**y.
    ----------
    Arguments:
        number: the base (x in the expression x^y).
        power:  the exponent (y in the expression x^y).
    ----------
    Returns:
        `number` raised to the `power`th power.
    ----------
    Doctest:
    >>> from math import pow
    >>> assert pow(2,3) == power(2,3) == 2**3

    """
    return number**power

def area_of_circle(radius:Number) -> Number:
    """
    Correctly computes the area of a circle of radius `radius`.
    ----------
    Arguments:
        radius: number specifying the radius of the circle.
    ----------
    Returns:
        the area of the circle of radius `radius`.
    ----------
    Raises:
        ValueError if radius <= 0
    ----------
    Doctest:
    """
    try:
        assert radius > 0
    except AssertionError as invalid_radius:
        raise ValueError("`area_of_circle`'parameter is a number > 0") from invalid_radius
    
    return pi * power(radius, 2)
    
def hypothenuse_of_right_triangle(sidelength1:Number, sidelength2:Number) -> Number:
    """
    Computes the length of the hypothenuse of the right triangle
    with a sidelength of length `sidelength`.
    ----------
    Arguments:
        sidelength1, sidelength2:   numbers specifying the lengths of the two orthogonal
                                    sides of the right triangle.
    ----------
    Returns:
        the length of the triangle's hypothenuse, as given by Pythagoras's theorem.
    ----------
    Raises:
        ValueError if a sidelength <= 0
    ----------
    Doctest:
    """ 
    try:
        assert sidelength1 > 0 and sidelength2 > 0
    except AssertionError as invalid_sidelength:
        raise ValueError("`hypothenuse_of_right_triangle`'s parameters are 2 numbers > 0") from invalid_sidelength
    
    return power(
        power(sidelength1, 2) + power(sidelength2, 2),
        0.5
    )
