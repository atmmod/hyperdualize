import re
import os

def convert_fortran_variables(file_path):
    """Convert REAL/INT/DOUBLE PRECISION declarations to type(hyperdual) with proper formatting,
       handling both scalar and array initializations (including those with bracketed initializers)
       and preserving original line breaks. Supports both traditional and kind= syntax."""
    
    # Base types: matches real, double precision, int, or integer (case-insensitive)
    base_types = r'(?:real|double\s+precision|int|integer)'
    
    # Updated kind pattern: matches (8) or (kind=8)
    kind_pattern = r'\s*\(\s*(?:kind\s*=\s*)?\d+\s*\)'
    
    # Pattern to match type declarations (non-initialized)
    type_pattern = re.compile(
        r'(?<!\w)'                               # Avoid partial matches
        r'(?P<type>' + base_types + r')'         # Match the base type
        r'(?:' + kind_pattern + r')?'            # Optional kind specifier
        r'(?![\w\(])'                            # Avoid partial matches
        r'(?:\s*,\s*(?P<attributes>[\w\s\(\):,]+))?',  # Optional attributes
        re.IGNORECASE
    )
    
    # Updated pattern to match declarations with initialization.
    # The initializer part now accepts either a bracketed expression ([...]) or a non-bracketed expression.
    init_pattern = re.compile(
        r'(?<!\w)'                                     # Avoid partial matches
        r'(?P<type>' + base_types + r')'               # Base type keyword
        r'(?:' + kind_pattern + r')?'                  # Optional kind specifier
        r'(?:\s*,\s*(?P<attributes>[\w\s\(\):,]+))?'   # Optional attributes
        r'\s*::\s*'
        r'(?P<vars_and_values>'                  # Variables and values group
            r'(?:(?:\w+\s*(?:\([^\)]+\))?\s*=\s*(?:\[[^\]]+\]|[^\n,]+))\s*,\s*)*'  # Possibly multiple declarations
            r'(?:\w+\s*(?:\([^\)]+\))?\s*=\s*(?:\[[^\]]+\]|[^\n,]+))'              # Last declaration
        r')',
        re.IGNORECASE | re.VERBOSE
    )
    
    def process_value(val, val_type):
        """Force conversion to double precision for numeric literals and replace E with d."""
        val = re.sub(r'([eE])', r'd', val)
        if 'd' not in val.lower():
            val = val.strip()
            if '.' not in val:
                val += ".0"
            val += "d0"
        return val

    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    modified_lines = []
    for line in lines:
        # Skip pointer initialization lines (containing "=>")
        if "=>" in line:
            modified_lines.append(line)
            continue

        # Process declarations with initialization
        def replace_init(match):
            type_keyword = match.group('type').lower()
            # Find kind specification (if any)
            kind_match = re.search(kind_pattern, match.group(0), re.IGNORECASE)
            kind = kind_match.group(0) if kind_match else ''
            attributes = match.group('attributes').strip() if match.group('attributes') else ''
            vars_and_values = match.group('vars_and_values')
            
            # Split declarations on commas that separate complete declarations.
            var_decls = re.split(r'\s*,\s*(?=\w+\s*(?:\([^\)]+\))?\s*=)', vars_and_values)
            
            processed_decls = []
            for decl in var_decls:
                if '=' not in decl:
                    continue
                var_part, value = decl.split('=', 1)
                var_part = var_part.strip()
                value = value.strip()
                
                # Extract variable name and any dimensions if present.
                if '(' in var_part:
                    var_name = var_part.split('(')[0].strip()
                    dimensions = '(' + var_part.split('(', 1)[1]
                else:
                    var_name = var_part
                    dimensions = ''
                
                original_type = f"{type_keyword}{kind}"
                # Check if the initializer is an array initializer (starts with [ and ends with ])
                if value.startswith('[') and value.endswith(']'):
                    inner = value[1:-1].strip()
                    # Split array elements on commas
                    elems = [e.strip() for e in re.split(r'\s*,\s*', inner)]
                    converted_elems = []
                    for e in elems:
                        conv = process_value(e, original_type)
                        converted_elems.append(f"hyperdual({conv}, 0.0d0, 0.0d0, 0.0d0)")
                    # Reassemble as a bracketed list (without an outer hyperdual call)
                    hd_value = f"[{', '.join(converted_elems)}]"
                else:
                    processed_val = process_value(value, original_type)
                    hd_value = f"hyperdual({processed_val}, 0.0d0, 0.0d0, 0.0d0)"
                
                attr_str = f", {attributes}" if attributes else ""
                full_decl = f"type(hyperdual){attr_str} :: {var_name}{dimensions} = {hd_value}"
                processed_decls.append(full_decl)
            return "\n".join(processed_decls)
        
        new_line = init_pattern.sub(replace_init, line)
        new_line = type_pattern.sub(lambda m: f"type(hyperdual){', ' + m.group('attributes').strip() if m.group('attributes') else ''}", new_line)
        if not new_line.endswith("\n"):
            new_line += "\n"
        modified_lines.append(new_line)
    
    return ''.join(modified_lines)

def insert_use_hdmod(lines):
    """
    Inserts a "use HDMod" line immediately after the header of any module, program,
    subroutine, or function that does not already contain it.
    """
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check for program unit header (but ignore module procedure)
        if re.match(r'^\s*(module|program|subroutine|function)\b', line, re.IGNORECASE) and not re.search(r'\bmodule\s+procedure\b', line, re.IGNORECASE):
            new_lines.append(line)
            i += 1
            found = False
            insertion_index = len(new_lines)
            while i < len(lines):
                next_line = lines[i]
                if re.match(r'^\s*!', next_line) or re.match(r'^\s*$', next_line) or re.match(r'^\s*use\b', next_line, re.IGNORECASE):
                    if re.match(r'^\s*use\s+HDMod\b', next_line, re.IGNORECASE):
                        found = True
                    new_lines.append(next_line)
                    i += 1
                else:
                    break
            if not found:
                new_lines.insert(insertion_index, "  use HDMod\n")
        else:
            new_lines.append(line)
            i += 1
    return new_lines

def save_modified_code(modified_code, output_file):
    with open(output_file, 'w') as f:
        f.write(modified_code)

if __name__ == "__main__":
    input_file = input("Enter Fortran file name: ").strip()
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        exit(1)
    
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_hd{ext}"
    
    try:
        modified_code = convert_fortran_variables(input_file)
        lines = modified_code.splitlines(keepends=True)
        new_lines = insert_use_hdmod(lines)
        final_code = ''.join(new_lines)
        save_modified_code(final_code, output_file)
        print(f"Converted file saved as: {output_file}")
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        exit(1)