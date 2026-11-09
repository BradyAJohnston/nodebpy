# Check the unpacking logic
line = '        "Frame": ("NodeFrame", (0.0, 0.0), False, None, ()),'

# Extract the tuple content
import re
match = re.search(r'"([^"]+)":\s*\((.+)\)$', line, re.DOTALL)
if match:
    name = match.group(1)
    tuple_content = match.group(2).strip()
    print(f'Name: {name}')
    print(f'Tuple content: {repr(tuple_content)}')
    
    # Try to parse it as Python literal
    try:
        value = eval(tuple_content)
        print(f'Parsed tuple: {value}')
        print(f'Length: {len(value)}')
        if len(value) == 5:
            _, bl_idname, loc, hide_status, parent = value
            print(f'  bl_idname: {bl_idname}')
            print(f'  loc: {loc}')
            print(f'  hide_status: {hide_status}')
            print(f'  parent: {parent}')
    except Exception as e:
        print(f'Error: {e}')
