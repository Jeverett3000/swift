import sys

for input_path in sys.argv[1:]:
    with open(input_path, 'r') as yaml_file:
        # Forwarding files are YAML files that start with '---'
        if yaml_file.read(3) != '---':
            print(f"swiftmodule '{input_path}' is not a forwarding module!")
            sys.exit(1)
