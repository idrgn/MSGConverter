import sys
from struct import pack

for filename in sys.argv[1:]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            new_file = bytearray()
            lines = f.readlines()

            # Get amount of messages and file type
            line_amount = len(lines) - 1
            file_type = int(lines[0].strip())

            # Write to new file
            new_file += pack("II", line_amount, file_type)

            # Initializing values for message processing
            text_array = bytearray()
            base_pointer = line_amount * 4 + 0xC
            accumulated_pointer = 0

            # Iterate over all lines
            for line in lines[1:]:
                current_line = line.strip("\n")
                encoded_line = current_line.encode("utf-16")
                new_file += pack("I", base_pointer + accumulated_pointer)
                accumulated_pointer += len(encoded_line)

                # Remove first 2 bytes and add 0x0000 at the end
                text_array += encoded_line[2:] + b"\x00\x00"

            # Add 0x00000000
            new_file += pack("I", 0x0)

            # Add all the text
            new_file += text_array

            # Save file
            with open(f"{filename}.to_msg", "w+b") as n:
                n.write(new_file)

            print(f"Converted .txt file {filename} to msg")

    except Exception as e:
        print(f"Couldn't convert .txt file {filename} to msg:{e}")
