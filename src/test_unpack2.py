import re

# Test with exact line from earlier
line = '        "Frame": ("NodeFrame", (0.0, 0.0), False, None, ()),'
print(f'Testing line: {repr(line)}')

match = re.search(r'"([^"]+)":\s*\((.+)\)$', line, re.DOTALL)
if match:
    name = match.group(1)
    tuple_content = match.group(2).strip()
    print(f'Name: {name}')
    print(f'Tuple content: {repr(tuple_content)}')
    
    try:
        value = eval(tuple_content)
        print(f'Parsed tuple: {value}')
        print(f'Length: {len(value)}')
    except Exception as e:
        print(f'Error: {e}')
else:
    print('No match found')
