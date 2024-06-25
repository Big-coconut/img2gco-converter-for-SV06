import re
from tkinter.filedialog import askopenfilename, asksaveasfilename


def remove_semicolon_lines(text):
    lines = text.split("\n")
    filtered_lines = [line for line in lines if not line.startswith(";")]
    return "\n".join(filtered_lines)


def remove_Z0(text):
    # Replace ' Z0' with an empty string
    text = text.replace(" Z0", "")
    # Replace any remaining 'Z0' with an empty string
    text = text.replace("Z0", "")
    return text


def replace_Y(text):
    # Replace 'Y-' with 'Y'
    text = text.replace("Y-", "Y")
    return text


def replace_G(text):
    # Add a G1 before movement lines
    text = text.replace("\nX", "\nG1 X")
    return text


def replace_M(text):
    # Convert S0 to M107
    text = text.replace("M106 S0", "M107")
    return text


def replace_end(text):
    # Add a semmicolon at the end of each line
    text = text.replace("\n", ";\n")
    return text


def replace_X(text):
    # Find all lines starting with 'X' and ending with 'S[x]'
    lines = text.split("\n")
    for i in range(len(lines)):
        match = re.match(r"X(.*)S(\d+)", lines[i])
        if match:
            # Replace the line with 'M106 S[x]\nX...'
            lines[i] = f"M106 S{match.group(2)}\nX{match.group(1)}"
    return "\n".join(lines)


def convert(gcode):
    gcode = remove_semicolon_lines(gcode)
    gcode = remove_Z0(gcode)
    gcode = replace_Y(gcode)
    gcode = replace_X(gcode)
    gcode = replace_G(gcode)
    gcode = replace_M(gcode)
    return replace_end(gcode) + ";"


x = askopenfilename()
print(x)
data = open(x, "r")
converted = convert(data.read())
data.close()
path = asksaveasfilename()
print(path)
writeFile = open(path, "w")
writeFile.write(converted)
writeFile.close()
