import sys
from struct import unpack


def read_byte_array(fdata: bytes, position: int, size: int) -> bytes:
    if position + size > len(fdata):
        size = len(fdata) - position
    return fdata[position : position + size]


def read_ushort(fdata: bytes, position: int) -> int:
    return unpack("H", read_byte_array(fdata, position, 2))[0]


def read_int(fdata: bytes, position: int) -> int:
    return unpack("i", read_byte_array(fdata, position, 4))[0]


def read_str16(fdata: bytes, position: int) -> str:
    string_bytes = bytearray()
    size = 0x0
    while read_ushort(fdata, position + size) != 0x0000:
        size += 2
    string_bytes = read_byte_array(fdata, position, size)
    string = unpack(f"{len(string_bytes)}s", string_bytes)[0]
    decoded_string = string.decode("utf-16")
    return decoded_string


for filename in sys.argv[1:]:
    try:
        with open(filename, "rb") as f:
            data = f.read()

            # Read file amount and file type
            file_amount = read_int(data, 0x0)
            file_type = read_int(data, 0x4)

            # First message is file type
            messages = [f"{str(file_type)}\n"]

            # Iterate over all files
            for file_index in range(file_amount):
                current_dict_index = file_index * 4 + 0x8
                current_message_position = read_int(data, current_dict_index)
                current_message = read_str16(data, current_message_position)
                # print(f" - Message {file_index}: {current_message}")
                messages.append(f"{current_message}\n")

            # Remove last line jump
            messages[-1] = messages[-1][:-1]

            # Save file
            with open(f"{filename}.to_str", "w", encoding="utf-8") as n:
                n.writelines(messages)

            print(f"Converted .msg file {filename} to text")

    except Exception as e:
        print(f"Couldn't convert .msg file {filename} to text:{e}")
