"""

"""
# standard library dependencies
from unittest.mock import patch
from numbers import Number 

# local dependencies
import geometric_rules_patching_sub1 as submission
import geometric_rules_patching_sol as solution


def test_power(base:Number, power:Number) -> bool:
    """
    """
    return submission.power(base, power) == solution.power(base, power)

def test_area_of_circle(radius:Number) -> bool:
    """
    """
    return submission.area_of_circle(radius) == solution.area_of_circle(radius)

def test_hypothenuse_of_right_triangle(l1:Number, l2:Number, patch_function:bool=False) -> bool:
    """
    """
    if patch_function:
        with patch("geometric_rules_patching_ex.power", side_effect=solution.power) as patched_power:
            submission_result = submission.hypothenuse_of_right_triangle(l1,l2)
            solution_result = solution.hypothenuse_of_right_triangle(l1,l2)
            print(f"{submission_result} == {solution_result}")
            return submission_result == solution_result
    else:
        return submission.hypothenuse_of_right_triangle(l1,l2) == solution.hypothenuse_of_right_triangle(l1,l2)

def main():
    p
    for test_tup in [ (1,1), (1,2), (2,3), (3,4), (4.5,2) ]:
        if not test_power(*test_tup):
            print(f"unexpected behaviour for `power` with input: {test_tup}")
    
    for test_radius in [ 1, 2, 9, 11, 10.5 ]:
        assert test_area_of_circle(test_radius)
    
    for test_tup in [ (1,1), (2,2), (2,1), (1,2), (4,5), (23.2, 0.2) ]:
        for use_patching in [ True, False ]:
            try:
                outcome = test_hypothenuse_of_right_triangle(*test_tup, patch_function=use_patching)
            except Exception as error:
                print(f"unexpected behaviour for `hypothenuse_of_right_triangle` with input: {test_tup}")
                
            else:
                if not outcome:
                    print(f"unexpected behaviour for `hypothenuse_of_right_triangle` with input: {test_tup}")
        
if __name__ == '__main__':
    main()