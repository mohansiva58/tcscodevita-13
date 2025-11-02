import sys
import collections

# Custom precedence: NOT (highest) > OR > AND (lowest)
PRECEDENCE = {
    '|': 2,  # Logical OR
    '&': 1,  # Logical AND
    '!': 3,  # Logical NOT (Unary)
    '(': 0,  # Brackets have lowest stacking precedence, highest evaluation precedence
}

def apply_op(op, b_str, a_str=None):
    """Applies the bitwise operation to the binary string(s)."""
    
    if op == '!':
        # Logical NOT (Unary)
        result_bits = []
        for bit in b_str:
            result_bits.append('1' if bit == '0' else '0')
        return "".join(result_bits)
    
    # Binary operations (OR, AND). Must pad the shorter string to the length of the longer one.
    len_a = len(a_str)
    len_b = len(b_str)
    max_len = max(len_a, len_b)
    
    # Pad both strings with leading zeros to match max_len
    a_padded = a_str.zfill(max_len)
    b_padded = b_str.zfill(max_len)
    
    result_bits = []
    
    for i in range(max_len):
        bit_a = a_padded[i]
        bit_b = b_padded[i]
        
        if op == '|':
            # OR: 1 if either is 1
            result_bits.append('1' if bit_a == '1' or bit_b == '1' else '0')
        elif op == '&':
            # AND: 1 only if both are 1
            result_bits.append('1' if bit_a == '1' and bit_b == '1' else '0')
            
    return "".join(result_bits)


def evaluate(tokens):
    """Evaluates the tokenized expression using the Shunting-Yard approach."""
    
    values = [] # Stack for binary strings (operands)
    ops = []    # Stack for operators and brackets
    
    def process_top_op():
        """Pops an operator and operands from stacks and pushes the result."""
        op = ops.pop()
        
        if op == '!':
            # Unary NOT
            b_str = values.pop()
            values.append(apply_op(op, b_str))
        else:
            # Binary operations (OR, AND)
            b_str = values.pop()
            a_str = values.pop()
            values.append(apply_op(op, b_str, a_str))

    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token.isdigit():
            # Operands are just pushed to the value stack
            values.append(token)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            # Process operators until the matching '(' is found
            while ops[-1] != '(':
                process_top_op()
            ops.pop() # Pop the '('
        else: # Operator: |, &, !
            current_op_precedence = PRECEDENCE[token]
            
            # While the operator stack is not empty, and the top op is not '(',
            # and the precedence of the top op >= precedence of the current op,
            # process the top operator.
            while (ops and ops[-1] != '(' and 
                   PRECEDENCE.get(ops[-1], -1) >= current_op_precedence):
                process_top_op()
            
            ops.append(token)
        
        i += 1

    # After iterating through all tokens, process any remaining operators
    while ops:
        process_top_op()

    # The final result is the single item left on the value stack
    final_binary_string = values[0]
    
    # Convert the final binary string to the numeric value
    # The output format must align with the length of the *original* numbers used.
    # The problem asks to "align the resulting string with the initial numerical format"
    # This is slightly ambiguous, but typically means interpreting the result 
    # as concatenated 9-bit chunks.
    
    # Since the numbers in the result expression (e.g., 51) are formed by groups
    # of 9 bits (3x3 grid), we group the result into 9-bit chunks and convert each
    # chunk back to a digit (0-9), then concatenate the digits.
    
    # Determine the chunk size (9 bits per digit in the final number)
    chunk_size = 9 
    
    # Pad the beginning with zeros if the total length isn't a multiple of 9
    pad_len = (chunk_size - (len(final_binary_string) % chunk_size)) % chunk_size
    padded_result = '0' * pad_len + final_binary_string
    
    result_digits = []
    
    for start in range(0, len(padded_result), chunk_size):
        chunk = padded_result[start : start + chunk_size]
        
        # We need the digit-to-binary map to find the corresponding digit for the chunk.
        # Since the problem asks for the numeric value of the resulting number,
        # we can just use integer conversion of the binary string.
        # However, the output "51" implies digit grouping.
        
        # To get the final numeric value, we treat the sequence of 9-bit chunks 
        # as a sequence of digits in base 10. We just need to ensure the 9-bit 
        # chunk correctly maps back to a single digit string '0'-'9'.
        
        # Since the problem implies the final result *must* be readable as a number 
        # made of 9-bit chunks, we use the original digit map (which we built 
        # during parsing) to convert the chunks back to digits.
        
        # The key is to check which 9-bit pattern in the original DIGIT MAP 
        # (self.pattern_map in the full class structure) matches the chunk.
        
        # Since this evaluation function is outside the main class, we assume 
        # a standard integer conversion is intended if we cannot access the pattern map, 
        # but based on the examples (010110011000001001 -> 51), integer conversion is WRONG.
        # 010110011000001001 in base 10 is 172937, not 51.
        
        # We MUST use the pattern map. Let's return the grouped binary string and do
        # the final conversion in the main solver function where the map exists.
        
        # The explanation of Example 1 shows the result (010110011000001001) is 
        # split into two 9-bit chunks: 010110011 and 000001001.
        # 010110011 is pattern for '5'
        # 000001001 is pattern for '1'
        # Result: "51"
        
        # We return the padded binary string and let the main function map it.
        return padded_result


def solve_the_expression():
    """Main function to read input, parse 7-segment, tokenize, and evaluate."""
    try:
        input_lines = [sys.stdin.readline().rstrip('\n') for _ in range(9)]
    except EOFError:
        return 0 # Handle empty input

    # 1. Parse the 7-segment patterns
    
    # Read patterns for 0-9 (first 3 lines)
    digit_patterns = collections.defaultdict(list)
    for i in range(3):
        # The input contains variable whitespace; split based on 3-char chunks
        line = input_lines[i]
        
        # Find the start columns of each digit (0-9)
        start_cols = []
        in_segment = False
        
        for c in range(len(line)):
            is_segment_char = line[c] not in (' ', '\t')
            if is_segment_char and not in_segment:
                start_cols.append(c)
                in_segment = True
            elif not is_segment_char:
                in_segment = False
        
        # Extract the 10 patterns (3x3 chunks)
        current_col = start_cols[0] # Start of digit 0
        
        for digit in range(10):
            if digit < len(start_cols):
                start = start_cols[digit]
                end = start + 3
            else:
                # Simple fallback: assume 1 space between symbols
                start = current_col + 1
                end = start + 3
            
            pattern_chunk = line[start:end].replace(' ', '0').replace('_', '1').replace('|', '1')
            
            # The input contains pipes and underscores. Map: ' '->0, '|'->1, '_'->1
            mapped_chunk = ''
            for char in line[start:end]:
                if char in ('_', '|'):
                    mapped_chunk += '1'
                elif char in (' ', '\t'):
                    mapped_chunk += '0'
                else:
                    # Should not happen, but treat as unlit
                    mapped_chunk += '0'

            digit_patterns[digit].append(mapped_chunk)
            current_col = end # Update for next iteration

    # Read patterns for OR, AND, NOT, (, ) (next 3 lines)
    op_chars = ['|', '&', '!', '(', ')']
    op_patterns = collections.defaultdict(list)
    
    for i in range(3, 6):
        line = input_lines[i]
        
        start_cols = []
        in_segment = False
        
        for c in range(len(line)):
            is_segment_char = line[c] not in (' ', '\t')
            if is_segment_char and not in_segment:
                start_cols.append(c)
                in_segment = True
            elif not is_segment_char:
                in_segment = False

        current_col = start_cols[0] # Start of op 0
        
        for op_idx in range(5):
            if op_idx < len(start_cols):
                start = start_cols[op_idx]
                end = start + 3
            else:
                start = current_col + 1
                end = start + 3
            
            
            mapped_chunk = ''
            for char in line[start:end]:
                if char in ('_', '|'):
                    mapped_chunk += '1'
                elif char in (' ', '\t'):
                    mapped_chunk += '0'
                else:
                    mapped_chunk += '0'

            op_patterns[op_chars[op_idx]].append(mapped_chunk)
            current_col = end # Update for next iteration

    # Combine 3 rows of 3 columns (9 bits) to form the binary representation for each symbol
    pattern_to_symbol = {}
    symbol_to_binary = {}
    
    for digit in range(10):
        binary = "".join(digit_patterns[digit])
        pattern_to_symbol[binary] = str(digit)
        symbol_to_binary[str(digit)] = binary

    for op in op_chars:
        binary = "".join(op_patterns[op])
        pattern_to_symbol[binary] = op
        symbol_to_binary[op] = binary


    # 2. Tokenize the expression
    
    # Read the expression (last 3 lines)
    expr_lines = input_lines[6:9]
    
    # Concatenate the three lines for easier column processing
    max_len = max(len(l) for l in expr_lines)
    expr_lines_padded = [l.ljust(max_len) for l in expr_lines]
    
    tokens = []
    
    col = 0
    while col < max_len:
        # Extract the 3x3 pattern starting at this column
        pattern_parts = []
        for r in range(3):
            pattern_parts.append(expr_lines_padded[r][col:col+3])
        
        # Convert to the 9-bit binary string
        expr_binary = ""
        for part in pattern_parts:
            mapped_chunk = ''
            for char in part:
                if char in ('_', '|'):
                    mapped_chunk += '1'
                elif char in (' ', '\t'):
                    mapped_chunk += '0'
                else:
                    mapped_chunk += '0'
            expr_binary += mapped_chunk
        
        # Check if the extracted 9-bit pattern corresponds to a known symbol
        if expr_binary in pattern_to_symbol:
            symbol = pattern_to_symbol[expr_binary]
            
            if symbol.isdigit() and tokens and tokens[-1].isdigit():
                # Handle multi-digit numbers by concatenating the binary strings
                # This is the ONLY place where operands are concatenated based on the requirement
                
                # The tokens list stores the *binary string* for numbers, not the digit
                last_binary = tokens.pop()
                current_binary = symbol_to_binary[symbol]
                tokens.append(last_binary + current_binary)
                
            elif symbol.isdigit():
                # Store the binary representation of the single digit
                tokens.append(symbol_to_binary[symbol])
            else:
                # Store the operator/bracket symbol itself
                tokens.append(symbol)
                
            col += 3 # Advance by 3 columns (symbol width)
            
        else:
            # If the pattern is not recognized (e.g., whitespace), skip the column
            col += 1

    # 3. Evaluate the tokenized expression
    
    # The tokens list contains:
    # - Binary strings (operands)
    # - Operator/bracket symbols (|, &, !, (, ))
    final_binary_string_result = evaluate(tokens)
    
    # 4. Final conversion back to a numeric value
    
    # Use the pattern map to convert the final binary string into a sequence of digits
    # The pattern is grouped into 9-bit chunks.
    result_digits = []
    chunk_size = 9
    
    # The evaluation function already ensures the result is padded correctly
    padded_result = final_binary_string_result 
    
    for start in range(0, len(padded_result), chunk_size):
        chunk = padded_result[start : start + chunk_size]
        
        # Search the original digit patterns for a match
        found_digit = '0' # Default to 0 if no match, though problem guarantees valid output
        
        for digit in range(10):
            original_digit_pattern = symbol_to_binary[str(digit)]
            if original_digit_pattern == chunk:
                found_digit = str(digit)
                break
        
        result_digits.append(found_digit)

    # Concatenate the digits and return the final numeric value
    return int("".join(result_digits))


if __name__ == "__main__":
    print(solve_the_expression())
