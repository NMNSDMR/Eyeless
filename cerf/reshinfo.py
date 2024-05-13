from itertools import product

def generate_combinations(letters, length):
    """
    Generate all combinations of the given letters up to the specified length.
    
    Args:
    - letters: A string containing the input letters.
    - length: The maximum length of combinations to generate.
    
    Returns:
    - A generator yielding all combinations.
    """
    for combination_length in range(1, length + 1):
        for combination in product(letters, repeat=combination_length):
            yield ''.join(combination)

def main():
    input_letters = input("Enter the letters: ")
    max_length = int(input("Enter the maximum combination length: "))
    
    combinations = generate_combinations(input_letters, max_length)
    
    for combination in combinations:
        print(combination)

if __name__ == "__main__":
    main()
