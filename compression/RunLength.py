def compress(input_string): 
    count = 1 
    compressed = []

    # Iterate through the input string
    for i in range(1, len(input_string)):
        if input_string[i] == input_string[i - 1]:
            count += 1
        else:
            compressed.append(input_string[i - 1] + str(count)) 
            count = 1

    # Add the last character and its count
    compressed.append(input_string[-1] + str(count)) 
    return ''.join(compressed) 

def decompress(compressed_string):
    decompressed = [] 
    i = 0 

    while i < len(compressed_string):
        char = compressed_string[i] 
        count_str = "" 

        # Extract the count of repetitions
        i += 1
        while i < len(compressed_string) and compressed_string[i].isdigit():
            count_str += compressed_string[i]
            i += 1

        # Append the repeated character to the decompressed string
        decompressed.append(char * int(count_str)) 

    return ''.join(decompressed) 

# Example usage
original_string = "AAAABBBCCDAA"
compressed_string = compress(original_string)
decompressed_string = decompress(compressed_string)

print("Original String:", original_string)
print("Compressed String:", compressed_string)
print("Decompressed String:", decompressed_string)

# Check if the decompressed string matches the original
print("Decompressed matches Original:", decompressed_string == original_string)
