import graphviz

def is_simple_grammar(grammar):
    for nonTerm, rules in grammar.items():
        if len(rules) != 2:
            return False
        for rule in rules:
            if not rule:
                return False
            if not rule[0].islower():
                return False
        if len(set(rules)) != 2:
            return False
        if rules[0][0] == rules[1][0]:
            return False
    return True

def recursive_parse(input_str, grammar, non_terminal, index):
    if index == len(input_str):
        return index

    for rule in grammar[non_terminal]:
        temp_index = index
        stack = []
        for symbol in rule:
            if symbol.isupper():
                temp_index = recursive_parse(input_str, grammar, symbol, temp_index)
                if temp_index == -1:
                    break
            else:
                if temp_index < len(input_str) and input_str[temp_index] == symbol:
                    temp_index += 1
                    stack.append(symbol)
                else:
                    break
        else:
            return temp_index

    return -1

def main():
    print("Recursive Descent Parsing for this Grammar")
    print("Provided Grammar Rules:\n")

    grammar = {}
    for i in range(2):
        nonTerm = input(f"Enter non-terminal {i + 1}: ").strip()
        grammar[nonTerm] = []
        for j in range(2):
            rule = input(f"Enter production {j + 1} for '{nonTerm}': ").strip()
            grammar[nonTerm].append(rule)

    if is_simple_grammar(grammar):
        print("\nThis grammar is classified as SIMPLE.")
    else:
        print("\nThis grammar does NOT fit the SIMPLE grammar criteria.")
        print("Restarting...")
        return main()

    input_str = input("Enter the string to validate: ").strip()
    print(f"Input String as list: {list(input_str)}")

    stack_after_checking = []
    result = recursive_parse(input_str, grammar, list(grammar.keys())[0], 0)

    if result == len(input_str):
        print(f"Stack content: {stack_after_checking}")
        print("Remaining unchecked string: []")
        print("The input string is Accepted.")
    else:
        print(f"Stack content: {stack_after_checking}")
        print(f"Remaining unchecked portion: {list(input_str[result:])}")
        print("The input string is Rejected.")

    while True:
        print("====================================================")
        print("1- Enter a different Grammar")
        print("2- Test a different String")
        print("3- Exit Program")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            return main()
        elif choice == '2':
            input_str = input("Enter a new string to validate: ").strip()
            print(f"Input String as list: {list(input_str)}")

            tree = graphviz.Digraph(format='png')
            tree.attr(dpi='300')

            stack_after_checking = []
            result = recursive_parse(input_str, grammar, list(grammar.keys())[0], 0)

            if result == len(input_str):
                print(f"Stack content: {stack_after_checking}")
                print("Remaining unchecked string: []")
                print("The input string is Accepted.")
                tree.render('parse_tree', view=True)
            else:
                print(f"Remaining unchecked portion: {list(input_str[result:])}")
                print("Remaining unchecked string: []")
                print("The input string is Rejected.")
        elif choice == '3':
            print("Program terminated.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
