![Python Logo](https://i.ibb.co/dPhyzbZ/Python-background.png)

<br>

# Basic Error and Exception Handling in Python

Errors and exceptions are an integral part of programming, often arising from various sources like invalid user input, unavailable resources, or coding errors. Without proper handling, these issues can cause your programs to crash or behave unpredictably. By implementing effective error and exception handling, you can ensure that your programs respond to unexpected situations gracefully, maintaining stability and providing informative feedback to users.

In Python, exception handling is primarily done using the try, except, else, and finally blocks. This article will delve into fundamental techniques for managing errors and exceptions in Python, equipping you with the tools to create programs that handle errors intelligently, recover from them when possible, and manage potential failures.

<br>

## What Exactly Are Exceptions?

Exceptions are events that disrupt the normal flow of a program's execution. When an exception occurs, Python creates an object representing the error and halts the program. Exceptions must derive from the BaseException class. Python has many built-in exceptions, and it is also possible to create custom exceptions using subclasses of Exception, not BaseException. This approach avoids potential conflicts and maintains compatibility across Python versions. Built-in exceptions often include an associated value, providing details about the error.

<br>

![Python Builtin Exceptions](https://i.ibb.co/Ns5bhtW/python-builtin-exceptions-screengrab.png)

[\*source: Python Docs](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)

<br>

Don't be overwhelmed, you can use this visual as a cheat sheet and after a while you will know these exceptions thoroughly.

Now, let's take a look at some basic exception handling methods. The examples as stripped down as possible to illustrate the concepts.

<br>


## Catching All Exceptions (Don't do this)

You can catch all exceptions using a generic except block, but this should be used cautiously to avoid masking unexpected errors: 

```python

    try:
        risky_operation()
    except Exception as e:
        print(f"An error occurred: {e}")

```

This practice is considered bad practice because it can hide bugs making debugging difficult. Instead, catch specific exceptions to handle expected error conditions appropriately and ensure other errors are noticed and fixed. Avoid doing this and save yourself a ton of headaches down the road.

<br>


## Utilizing else and finally Clauses

The try - except - else - finally structure is a powerful tool for error handling. The try block contains the code that might raise an exception. If an exception occurs, it is caught by the except blocks. The else clause runs if no exceptions occur, and the finally clause runs regardless of whether an exception occurs, making it useful for cleanup tasks like closing files or releasing resources.

```python

    try:
        value = int(input("Enter a number: "))
        result = 10 / value
    except ValueError:
        print("Error: Invalid input. Please enter a valid number.")
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
    else:
        print(f"Result: {result}")
    finally:
        print("Execution complete.")

```

<br>


## Utilizing try-except Blocks:

A try-except block allows you to catch and handle exceptions effectively. By specifying different except blocks for different exceptions, you can tailor the program's response based on the specific error that occurred. This flexibility allows you to implement the necessary logic to handle various error conditions appropriately.

```python

    try:
        # Code that might raise an exception
        risky_operation()
    except ExceptionType:
        # Code that runs if the exception occurs
        handle_exception()

```

As you can probably tell, this gives you great flexability in creating as complex of tools that you need.

<br>


## Handling Division by Zero:

Dividing by zero raises Python's built-in ZeroDivisionError. You can catch and handle this by printing an error message or prompting the user for a valid number. This approach ensures the program does not crash and can recover from the error gracefully.

```python

    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")

```

<br>


## Handling Multiple Exceptions

You can handle multiple exceptions by specifying multiple except blocks. For example, handling both ValueError (if the input is not a number) and ZeroDivisionError (if the input is zero):

```python

    try:
        value = int(input("Enter a number: "))
        result = 10 / value
    except ValueError:
        print("Error: Invalid input. Please enter a valid number.")
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")

```

<br>


## Creating Custom Exceptions

Custom exceptions can be created by subclassing the built-in Exception class. This allows you to define errors specific to your application and helps you debug more efficiently.

```python

    class CustomError(Exception):
        pass

    try:
        raise CustomError("This is a custom error message.")
    except CustomError as e:
        print(f"Caught custom exception: {e}")

```

<br>


## Logging Exceptions

Logging exceptions is crucial for debugging and maintaining code. Python's built-in logging module simplifies setting up and using logging in your applications and provides a record of errors, making it easier to diagnose and fix issues.

```python

    import logging

    logging.basicConfig(level=logging.ERROR)

    try:
        value = int(input("Enter a number: "))
        result = 10 / value
    except Exception as e:
        logging.error("An error occurred: %s", e)

```

<br>


## Best Practices for Exception Handling:

To recap, here are some best practices for handling exceptions and errors in Python:

    
    - Catch Specific Exceptions: Catch specific exceptions to make your code more readable and 
      maintainable. Avoid catching all exceptions generically.
    
    - Avoid Silent Failures: Avoid using bare except clauses that catch all exceptions without 
      handling them properly.
    
    - Utilize try-except Blocks: Catch exceptions specifically and allow your program to react 
      according to which exception was raised.
    
    - Use else-finally Clauses: Use the else clause for code that should run if no exceptions 
      occur, and the finally clause for cleanup tasks such as closing files or network connections.
    
    - Create Custom Exceptions: Custom exceptions help you know exactly what is happening in your 
      program and what to do about it.
    
    - Log Exceptions: Logging exceptions can help you diagnose issues in your code and ensure that 
      the code is running as expected.

<br>


## EXAMPLE:

Here's a basic example of exception handling in Python:

```python
import logging
from typing import Union


class NegativeResultError(Exception):
    """Custom exception for negative results."""
    pass


class Divider:
    ''' ---------------------------------------------------------------------------------
     ::class::  Divider - class that divides two integers and returns the result.
     ::param::  num1 - str/int - required - the first number to operate on
     ::param::  num2 - str/int - required - the second number to operate on
     ::return:: result - result from dividing num1 and num2.
     ::errors:: TypeError, ValueError, ZeroDivisionError, NegativeResultError, Exception
     -------------------------------------------------------------------------------- '''
    def __init__(self, num1: Union[str, int], num2: Union[str, int]):
        self.num1 = self.validate_input(num1)
        self.num2 = self.validate_input(num2)

    def validate_input(self, value: Union[str, int]) -> int:
        ''' --------------------------------------------------------------
         ::method:: validate_input - Validates that input is a valid integer.
         ::param::  value - required - input to be validated.
         ::return:: int - validated integer.
         ::errors:: TypeError or ValueError.
        -------------------------------------------------------------- '''
        if value is None:
            raise TypeError("Input value is required.")
        try:
            return int(value)
        except ValueError:
            raise ValueError("Invalid input. Conversion to integer failed.")

    def divide(self) -> float:
        ''' --------------------------------------------------------------
         ::method:: divide - Divides two parameters and returns the result.
         ::param::  uses self.num1 and self.num2. Call init with params 
                    before calling this method.
         ::return:: result - result from dividing num1 and num2.
         ::errors:: ZeroDivisionError, NegativeResultError or Exception
         -------------------------------------------------------------- '''
        try:
            result = self.num1 / self.num2
            if result < 0:
                raise NegativeResultError("Results are negative.")

            logging.info(f'Success! The result is: {result}')
            return result

        except ZeroDivisionError:
            # built-in exception
            logging.error('python:divide:error: Invalid parameters. Cannot divide by zero.')
            raise
        except NegativeResultError as e:
            # Our custom exception
            logging.error(f'python:divide:error: {str(e)}')
            raise
        except Exception:
            logging.error('python:divide:error: An unknown error has occurred. Please try again.')
            raise

# Example usage:
# divider = Divider("10", "2")
# result = divider.divide()
# print(f"The result of division is: {result}")

```

**take note of the syntax used like: `python def __init__(self, num1: Union[str, int], num2: Union[str, int])`, this is another best practice that I will be covering soon called type hinting.

<br>


## Conclusion

This article demonstrates how to handle various types of exceptions in Python, including invalid input, division by zero, and custom exceptions. It also shows how to use logging for error reporting and ensure cleanup with a finally block. By following these best practices, you can write robust and maintainable Python code. 

The files and code for this article are available at [GitHub](https://github.com/ShellDisciple/linkedin_articles). 

Have fun!

<br>
<br>
