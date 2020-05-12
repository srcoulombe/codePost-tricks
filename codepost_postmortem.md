# CodePost Post-Mortem: COMP 202 Winter 2020

## On handling exceptions
We aimed to handle exceptions in the submissions to return insightful feedback on where the code crashed and why (including the arguments which made it crash) instead of simply letting it crash.


### Things we did
When no exceptions were expected, we could use the catch-all ```except Exception``` pattern to catch any exception. We would then use the ```traceback``` library to provide context in the error message returned by the codePost test. 

In cases when the submissions were expected to raise specific exceptions, we needed to pay special attention to the order of ```except``` blocks. This often resulted in having multiple ```try/except .../else``` blocks, and we simply used ```pass``` in the ```except``` block corresponding to the expected exception.


```python
import traceback

try:
    student_answer = student_function(...)
 
# expected exception type 
# e.g. we anticipate students might not account for division-by-zero, so we could use
# except ZeroDivisionError as zde:
#     ...
except exception_type_1 as et1:
    # we tried making error messages as helpful as possible
    message = "\n".join([
        "Test failed.",
        f"Unexpected {type(et1)} when calling {student_function} with the following arguments:",
        arguments,
        et1, 
        ''.join(traceback.format_exception_only(type(et1), et1))
    ])
    return TestOutput(passed=False, logs=message)

# include this "catch all else" except block to provide more feedback on which case made
# the code crash
except Exception as any_other_unexpected_exception:
    # we tried making error messages as helpful as possible
    message = "\n".join([
        "Test failed.",
        f"Unexpected {type(any_other_unexpected_exception)} when calling {student_function} with the following arguments:",
        arguments,
        et1, 
        ''.join(traceback.format_exception_only(type(any_other_unexpected_exception), any_other_unexpected_exception))
    ])
    return TestOutput(passed=False, logs=message)

# carry on with the rest of the test
# Note: "else:" is optional; removing it could keep the code flatter
else:
    ...
```

### Things we could have done

1. Add an extra ```assert isinstance(student_answer, expected_return_type)``` statement in the ```try``` block and always include an ```except AssertionError as return_type_mismatch``` block.
    
    **Challenge #1:** This becomes tricky when dealing with collections of heterogeneous types and nested collections.
    
    **Solution #1:** Use a nested type checker

## On handling mutable arguments
Students sometimes modified mutable arguments in their functions; this made it harder to provide feedback when their code failed the test cases, as we couldn't simply tell them the (modified) mutable arguments which made their code crash.

### Things we did
Made separate copies of all mutable variables prior to calling the relevant function.


```python
mutable_arg_1 = ...
mutable_arg_2 = ...
...

mutable_arg_1_copy = ...
mutable_arg_2_copy = ...
...

student_answer = student_function(mutable_arg_1, mutable_arg_2, ...)
...

try:
    student_answer = student_function(...)
 
except exception_type_1 as et1:
    message = "\n".join([
        "Test failed.",
        f"Unexpected {type(et1)} when calling {student_function} with the following arguments:",
        mutable_arg_1_copy, # use copied mutable variable
        mutable_arg_2_copy, # use copied mutable variable
        et1, 
        ''.join(traceback.format_exception_only(type(et1), et1))
    ])
    return TestOutput(passed=False, logs=message)

```

### Things we could have done

#### When students should not modify mutable arguments
1. Use tuples instead of lists and frozensets instead of sets.

2. Python doesn't have a "FrozenDict" type (AFAIK, see [PEP 416](https://www.python.org/dev/peps/pep-0416/)), but the built-in ```types.MappingProxyType``` class might be useful:

    **Pros:** same methods as a normal dictionary, but forbids item assignment (raises ```TypeError: 'mappingproxy' object does not support item assignment```)
    
    **Cons:** would need to account for the ```TypeError: 'mappingproxy' object does not support item assignment``` exception in autograding code

## On parsing STDOUT
Functions would often need to print specific things to STDOUT. CodePost has a GUI interface to setup simple tests that check whether some string was printed or not (no coding required). However, these tests didn't return very informative messages upon failure. Furthermore, some print messages were fairly "personalisable", and Python's ```re``` library allowed for more detailed regex parsing than what we could do with Bash unit tests. For those reasons, some of the tests that checked and parsed STDOUT were Bash unit tests and others were Python unit tests.

## Things we did (with Python unit tests)
We used ```contextlib``` and ```io``` standard library modules to capture what was printed to STDOUT. The ```re``` module was used for regex parsing.


```python
# need to parse print statements, so 
# capture stdout into a string
captured_stdout = io.StringIO()
with redirect_stdout(captured_stdout):
    try:
         result = function(...)
    except Exception as error:
        error_message = ...
        return TestOutput(passed=False, logs=error_message)

# no longer in the redirect_stdout context,
# get what was printed as a single string
# (line breaks are represented using standard '\n' character)
string_stdout = captured_stdout.getvalue()

... 
```

### Things we could have done (with Python unit tests)
Nothing comes to mind, although enforcing students to have less "personalized" print statements could make the regex portion of unit tests less complicated.

## On forbidden things in submissions
This became relevant when checking that students weren't using functions or modules that could solve questions (e.g. ```reversed``` or ```sort``` when reversing a list, or using a specific random seed in a function).

### Things we did
We used the ```inspect``` module in the standard library to read the submission's source code as a string and use ```re``` for regex parsing purposes. 


```python
from submission import funct
source_code = inspect.getsource(funct)
# regex stuff
```

### Things we could have done
We could alternatively treat the submission as a normal text file and read it using ```open```, but this was more verbose than tha ```inspect``` solution.
The ```ast``` module was also used a few times.

## On patching functions and dependencies
Patching was often needed. Python's ```unittest``` module has library called ```patch``` that makes this fairly straightforward. Common use cases were:

1. When questions asked for user input from the CLI
2. When function ```foo``` used function ```bar```, and ```bar``` had a mistake that we didn't want to penalize again when testing ```foo```

### Things we did
We would patch a function/class/method with a hardcoded variable or the correct version of the dependency.

#### example 1: using input() once, and patching the builtin input() function to return a single predetermined value


```python
from unittest.mock import patch

test_case_arg = "Hello world!"
with patch('builtins.input', side_effect=test_case_arg) as mocked_input:
    # call the function that depends on input() as you would normally do it
    result = submission.add_greeting_to_input(" My name is Samy!")
    assert result == "Hello world! My name is Samy!"
```

#### example 2: using input() twice, and patching the builtin input() function to iterate over a pre-determined sequence instead of prompting for user input (the sequence must be of the same length as the number of calls to input())


```python
from unittest.mock import patch

user_input_sequence = ["First string input from STDIN", "Second string input from STDIN"]
with patch('builtins.input', side_effect=iter(user_input_sequence)) as mocked_input:
    # call the function that depends on input() as you would normally do
    # 
    submission_get_fair_quantity = submission.this_function_calls_input(...)
```

#### example 3: patching a dependency with the corresponding object in the solution code


```python
# foo.py 
# def divide(x, y): 
#     return x / y # doesn't account for division by zero

# bar.py 
# from foo import divide
# def calculate_velocity(distance, time): 
#     return divide(distance, time)

# testing bar.calculate_velocity, which depends on foo.divide
try:
    initial_answer = calculate_velocity(test_distance, test_time)
except ...
else:
    if initial_answer != expected answer:
        with patch('foo.divide', wraps=solution_foo.divide):
            # calculate_velocity's call to foo.divide is now replaced at runtime
            # by a call to solution_foo.divide
            try:
                patched_answer = calculate_velocity(test_distance, test_time)
            except ...
            else: ...
```

#### example 4: patching multiple dependencies with the corresponding objects in the solution code


```python
# foo.py 
# def divide(x, y): 
#     return x / y # doesn't account for division by zero

# bah.py
# def unit_of_measure():
#     return km / hr # km and hr are undefined

# bar.py 
# from foo import divide
# from bah import unit_of_measure
# def calculate_velocity(distance, time): 
#     return str( divide(distance, time) ) + str( unit_of_measure() )



# testing bar.calculate_velocity, which depends on foo.divide
try:
    initial_answer = calculate_velocity(test_distance, test_time)
except ...
else:
    if initial_answer != expected answer:
        with patch('foo.divide', wraps=solution_foo.divide):
            with patch('bah.unit_of_measure', wraps=solution_bah.unit_of_measure):
                # calculate_velocity's call to foo.divide is now replaced at runtime
                # by a call to solution_foo.divide
                try:
                    patched_answer = calculate_velocity(test_distance, test_time)
                except ...
                else: ...
```

### Things we could have done
We could have used the ```@patch``` decorator approach instead of using ```patch``` as a context manager; this might flatten the tester code and make it more legible.

Nothing else comes to mind, but other approaches (whether they involve a safer use of the unittest.mock library or an external module) would be welcome!

## On randomness in test cases
### Things we did
Made the random seed a parameter in our tests, which made sure that students were tested on the same pseudo-randomly-generated arguments.
### Things we could have done
Test cases were themselves created deterministically (sometimes with the input of other TAs and mentors) to assess different aspects of the students' code. We could also have opted to use a 'monkey testing' approach to test the students' code on random inputs.

**Pros:** 
- This could help TAs find more nuanced edge cases
- Testing on more edge cases could make the distinction between great code and good code more evident
- Libraries exist to do this fairly simply (see below)

**Cons:**
- This kind of testing might be overkill for an introduction-to-coding course, especially if the instructor(s) want to keep students as enthusiastic as possible
- Might require TAs to spend some time learning extra libraries
- No guarantee of complete coverage of edge cases

**Available Resources:** 
- [Hypothesis](https://hypothesis.readthedocs.io/en/latest/)

## On testing multiple aspects of same function
Sometimes we wanted to test both the function's print statements and their returned values. In such cases, we would write a  codePost unit test for each of those two things individually. 
