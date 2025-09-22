import sys

def display_welcome():
    print("=" * 50)
    print("          COMMAND-LINE CALCULATOR")
    print("=" * 50)
    print("Operations available:")
    print("  + : Addition")
    print("  - : Subtraction")
    print("  * : Multiplication")
    print("  / : Division")
    print("  % : Modulo (remainder)")
    print("  ^ : Power")
    print("  q : Quit the calculator")
    print("-" * 50)

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def get_operation():
    valid_operations = ['+', '-', '*', '/', '%', '^', 'q']
    
    while True:
        op = input("Enter operation (+, -, *, /, %, ^, q to quit): ").strip()
        if op in valid_operations:
            return op
        else:
            print("Invalid operation! Please choose from: +, -, *, /, %, ^")

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed!"
    return a / b

def modulo(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed!"
    return a % b

def power(a, b):
    return a ** b

def perform_calculation(a, b, operation):
    operations = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide,
        '%': modulo,
        '^': power
    }
    
    if operation in operations:
        return operations[operation](a, b)
    else:
        return "Invalid operation"

def format_result(result):
    if isinstance(result, float):
        if result.is_integer():
            return int(result)
        else:
            return round(result, 4)
    return result

def main():
    display_welcome()
    
    current_result = get_number("Enter first number: ")
    print(f"Current value: {format_result(current_result)}")
    
    while True:
        operation = get_operation()
        
        if operation == 'q':
            print("\nThank you for using the calculator. Goodbye!")
            break
        
        next_number = get_number("Enter next number: ")
        
        result = perform_calculation(current_result, next_number, operation)
        
        if isinstance(result, str): 
            print(f"Result: {result}")
        else:
            print(f"{format_result(current_result)} {operation} {format_result(next_number)} = {format_result(result)}")
            current_result = result
        
        print("-" * 30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCalculator terminated by user. Goodbye!")
        sys.exit(0)