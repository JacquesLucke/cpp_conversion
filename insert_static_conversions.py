import subprocess
import re
from pprint import pprint
import sys
import json

clang_format_path = """/home/jacques/blender/lib/linux_x86_64_glibc_228/llvm/bin/clang-format"""
compile_commands_path = """/home/jacques/blender/build_release/compile_commands.json"""
source_code_path = """
/home/jacques/blender/blender/source/blender/editors/armature/pose_utils.cc
""".strip()

# Also automatically detected below.
# compile_command = """
# /usr/lib64/ccache/c++ -DNDEBUG -DWITH_ASSERT_ABORT -DWITH_GHOST_WAYLAND_LIBDECOR -DWITH_GREASE_PENCIL_V3 -DWITH_INPUT_NDOF -DWITH_OPENGL -DWITH_POINT_CLOUD -DWITH_PYTHON -DWITH_SIMULATION_DATABLOCK -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE -D_LARGEFILE_SOURCE -D__LITTLE_ENDIAN__ -D__MMX__ -D__SSE2__ -D__SSE__ -I/home/jacques/blender/blender/source/blender/editors/include -I/home/jacques/blender/blender/source/blender/blenfont -I/home/jacques/blender/blender/source/blender/blenkernel -I/home/jacques/blender/blender/source/blender/blenlib -I/home/jacques/blender/blender/source/blender/blentranslation -I/home/jacques/blender/blender/source/blender/bmesh -I/home/jacques/blender/blender/source/blender/depsgraph -I/home/jacques/blender/blender/source/blender/functions -I/home/jacques/blender/blender/source/blender/gpencil_modifiers_legacy -I/home/jacques/blender/blender/source/blender/gpu -I/home/jacques/blender/blender/source/blender/ikplugin -I/home/jacques/blender/blender/source/blender/imbuf -I/home/jacques/blender/blender/source/blender/makesdna -I/home/jacques/blender/blender/source/blender/makesrna -I/home/jacques/blender/blender/source/blender/modifiers -I/home/jacques/blender/blender/source/blender/python -I/home/jacques/blender/blender/source/blender/render -I/home/jacques/blender/blender/source/blender/shader_fx -I/home/jacques/blender/blender/source/blender/windowmanager -I/home/jacques/blender/blender/intern/clog -I/home/jacques/blender/blender/intern/guardedalloc -I/home/jacques/blender/build_release/source/blender/makesdna/intern -I/home/jacques/blender/build_release/source/blender/makesrna -Wuninitialized -Wredundant-decls -Wall -Wno-invalid-offsetof -Wno-sign-compare -Wlogical-op -Winit-self -Wmissing-include-dirs -Wno-div-by-zero -Wtype-limits -Werror=return-type -Wno-char-subscripts -Wno-unknown-pragmas -Wpointer-arith -Wunused-parameter -Wwrite-strings -Wundef -Wformat-signedness -Wrestrict -Wno-suggest-override -Wuninitialized -Wno-stringop-overread -Wno-stringop-overflow -Wundef -Wmissing-declarations -Wimplicit-fallthrough=5 -Wno-stringop-overflow -Wno-stringop-overread -fdiagnostics-color=always -ffold-simple-inlines -msse -pipe -fPIC -funsigned-char -fno-strict-aliasing -ffp-contract=off -msse2 -fmacro-prefix-map="/home/jacques/blender/blender/"="" -fmacro-prefix-map="/home/jacques/blender/build_release/"="" -Wno-maybe-uninitialized -O2 -DNDEBUG -std=c++17   -fopenmp -MD -MT source/blender/editors/object/CMakeFiles/bf_editor_object.dir/object_relations.cc.o -MF source/blender/editors/object/CMakeFiles/bf_editor_object.dir/object_relations.cc.o.d -o source/blender/editors/object/CMakeFiles/bf_editor_object.dir/object_relations.cc.o -c /home/jacques/blender/blender/source/blender/editors/object/object_relations.cc
# """.strip()

compile_commands = json.load(open(compile_commands_path))
for command_entry in compile_commands:
    if source_code_path.endswith(command_entry["file"]):
        compile_command = command_entry["command"]
        break
else:
    print("Can't file compile command")
    sys.exit()

with open(source_code_path) as f:
    source_code = f.read()
source_code = re.subn(r"\bNULL\b", "nullptr", source_code)[0]
source_code = re.subn(r"UNUSED\((\w+)\)", r" /*\g<1>*/", source_code)[0]

source_code_parts = []
for line in source_code.splitlines():
    line = line.strip()
    if len(line) == 0:
        source_code_parts.append("\n")

    source_code_parts.append(line + " ")
    if line.endswith(",") or line.endswith("(") or line.endswith("*"):
        if not (line.startswith("//") or line.startswith("*") or line.startswith("/*") or line.startswith("#")):
            continue
    source_code_parts.append("\n")
source_code = "".join(source_code_parts)

if " ." in source_code:
    print("Warning: file likely contains designated initializers. Search for ' .'")
if "typedef struct" in source_code:
    print("Info: file contains 'typedef struct'. The 'typedef' is likely unnecessary.")

with open(source_code_path, "w") as f:
    f.write(source_code)
with open(source_code_path) as f:
    source_code_lines = f.read().splitlines()

result = subprocess.run(compile_command + " -fno-diagnostics-color", cwd="/home/jacques/blender/build_release", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
errors = result.stderr.decode()
errors = errors.replace("‘", "'").replace("’", "'")
error_lines = errors.splitlines()

handled_lines = set()

def get_code_span(initial_error_line):
    line_number = int(error_lines[initial_error_line+1][:5]) - 1
    column_indicator_line = error_lines[initial_error_line+2][7:]
    if column_indicator_line.strip() == "^":
        begin_column = column_indicator_line.index('^') - 1
        end_column = begin_column + 1
    else:
        begin_column = min(column_indicator_line.index('~'), column_indicator_line.index('^')) - 1
        end_column = column_indicator_line.rindex('~')
    return line_number, begin_column, end_column

for i, error_line in enumerate(error_lines):
    if source_code_path not in error_line:
        continue
    if match := re.search(r"invalid conversion from '(const )?void\*' to '([_a-zA-Z0-9\[\]\*\(\) ]+)'", error_line):
        to_type = match.group(2)
        try:
            line_number, begin_column, end_column = get_code_span(i)
        except:
            continue
        if line_number in handled_lines:
            continue
        old_line = source_code_lines[line_number]
        new_line = f"{old_line[:begin_column]}static_cast<{to_type}>({old_line[begin_column:end_column]}){old_line[end_column:]}"
        source_code_lines[line_number] = new_line
        handled_lines.add(line_number)
    elif match := re.search(r"(invalid conversion from|cannot convert) '(const )?(char|bool|int|short int)' to '(\w+)'", error_line):
        to_type = match.group(4)
        to_type = to_type.replace("short int", "short")
        try:
            line_number, begin_column, end_column = get_code_span(i)
        except:
            continue
        if line_number in handled_lines:
            continue
        old_line = source_code_lines[line_number]
        new_line = f"{old_line[:begin_column]}{to_type}({old_line[begin_column:end_column]}){old_line[end_column:]}"
        source_code_lines[line_number] = new_line
        handled_lines.add(line_number)

with open(source_code_path, "w") as f:
    f.writelines("\n".join(source_code_lines) + "\n")

subprocess.run([clang_format_path, "-i", source_code_path])
