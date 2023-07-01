import subprocess
import re
from pprint import pprint
import sys

source_code_path = """/home/jacques/blender/blender/source/blender/makesrna/intern/rna_xr.cc"""
compile_command = """
/usr/lib64/ccache/c++ -DHAVE_MALLOC_STATS_H -DNDEBUG -DTBB_SUPPRESS_DEPRECATED_MESSAGES=1 -DWITH_ALEMBIC -DWITH_ASSERT_ABORT -DWITH_AUDASPACE -DWITH_BULLET -DWITH_CINEON -DWITH_COLLADA -DWITH_CYCLES -DWITH_FFMPEG -DWITH_FFTW3 -DWITH_FLUID -DWITH_FREESTYLE -DWITH_GHOST_WAYLAND_LIBDECOR -DWITH_GMP -DWITH_GREASE_PENCIL_V3 -DWITH_INPUT_NDOF -DWITH_INTERNATIONAL -DWITH_OCEANSIM -DWITH_OPENAL -DWITH_OPENEXR -DWITH_OPENGL -DWITH_OPENJPEG -DWITH_OPENSUBDIV -DWITH_OPENVDB -DWITH_OPENVDB_BLOSC -DWITH_PYTHON -DWITH_SDL -DWITH_SIMULATION_DATABLOCK -DWITH_WEBP -DWITH_XR_OPENXR -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE -D_LARGEFILE_SOURCE -D__LITTLE_ENDIAN__ -D__MMX__ -D__SSE2__ -D__SSE__ -I/home/jacques/blender/blender/source/blender/makesrna/intern -I/home/jacques/blender/blender/source/blender/makesrna -I/home/jacques/blender/blender/source/blender/asset_system -I/home/jacques/blender/blender/source/blender/blenfont -I/home/jacques/blender/blender/source/blender/blenkernel -I/home/jacques/blender/blender/source/blender/blenlib -I/home/jacques/blender/blender/source/blender/blenloader -I/home/jacques/blender/blender/source/blender/blentranslation -I/home/jacques/blender/blender/source/blender/bmesh -I/home/jacques/blender/blender/source/blender/depsgraph -I/home/jacques/blender/blender/source/blender/draw -I/home/jacques/blender/blender/source/blender/gpu -I/home/jacques/blender/blender/source/blender/ikplugin -I/home/jacques/blender/blender/source/blender/imbuf -I/home/jacques/blender/blender/source/blender/makesdna -I/home/jacques/blender/blender/source/blender/modifiers -I/home/jacques/blender/blender/source/blender/nodes -I/home/jacques/blender/blender/source/blender/sequencer -I/home/jacques/blender/blender/source/blender/simulation -I/home/jacques/blender/blender/source/blender/windowmanager -I/home/jacques/blender/blender/source/blender/editors/include -I/home/jacques/blender/blender/source/blender/render -I/home/jacques/blender/blender/intern/clog -I/home/jacques/blender/blender/intern/cycles/blender -I/home/jacques/blender/blender/intern/guardedalloc -I/home/jacques/blender/blender/intern/memutil -I/home/jacques/blender/blender/intern/mantaflow/extern -I/home/jacques/blender/build_release/source/blender/makesdna/intern -I/home/jacques/blender/build_release/source/blender/makesrna -I/home/jacques/blender/blender/source/blender/python -I/home/jacques/blender/blender/intern/ffmpeg -I/home/jacques/blender/blender/source/blender/io/alembic -I/home/jacques/blender/blender/intern/rigidbody -I/home/jacques/blender/blender/source/blender/freestyle -I/home/jacques/blender/blender/intern/opensubdiv -I/home/jacques/blender/blender/intern/openvdb -isystem /home/jacques/blender/blender/extern/audaspace/bindings/C -isystem /home/jacques/blender/build_release/extern/audaspace -isystem /home/jacques/blender/lib/linux_x86_64_glibc_228/ffmpeg/include -isystem /home/jacques/blender/lib/linux_x86_64_glibc_228/openvdb/include -isystem /home/jacques/blender/lib/linux_x86_64_glibc_228/boost/include -isystem /home/jacques/blender/lib/linux_x86_64_glibc_228/tbb/include -isystem /home/jacques/blender/lib/linux_x86_64_glibc_228/openexr/include -isystem /home/jacques/blender/lib/linux_x86_64_glibc_228/openexr/include/OpenEXR -isystem /home/jacques/blender/lib/linux_x86_64_glibc_228/imath/include -isystem /home/jacques/blender/lib/linux_x86_64_glibc_228/imath/include/Imath -Wuninitialized -Wredundant-decls -Wall -Wno-invalid-offsetof -Wno-sign-compare -Wlogical-op -Winit-self -Wmissing-include-dirs -Wno-div-by-zero -Wtype-limits -Werror=return-type -Wno-char-subscripts -Wno-unknown-pragmas -Wpointer-arith -Wunused-parameter -Wwrite-strings -Wundef -Wformat-signedness -Wrestrict -Wno-suggest-override -Wuninitialized -Wno-stringop-overread -Wno-stringop-overflow -Wundef -Wmissing-declarations -Wimplicit-fallthrough=5 -Wno-stringop-overflow -Wno-stringop-overread -fdiagnostics-color=always -ffold-simple-inlines -msse -pipe -fPIC -funsigned-char -fno-strict-aliasing -ffp-contract=off -msse2 -fmacro-prefix-map="/home/jacques/blender/blender/"="" -fmacro-prefix-map="/home/jacques/blender/build_release/"="" -Wno-maybe-uninitialized -O2 -DNDEBUG -std=c++17   -fopenmp -Wno-missing-declarations -MD -MT source/blender/makesrna/intern/CMakeFiles/bf_rna.dir/rna_xr_gen.cc.o -MF source/blender/makesrna/intern/CMakeFiles/bf_rna.dir/rna_xr_gen.cc.o.d -o source/blender/makesrna/intern/CMakeFiles/bf_rna.dir/rna_xr_gen.cc.o -c /home/jacques/blender/build_release/source/blender/makesrna/intern/rna_xr_gen.cc
""".strip()

with open(source_code_path) as f:
    source_code = f.read()
source_code = re.subn(r"\bNULL\b", "nullptr", source_code)[0]
source_code = re.subn(r"UNUSED\((\w+)\)", r" /*\g<1>*/", source_code)[0]
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
        begin_column = column_indicator_line.index('~') - 1
        end_column = column_indicator_line.rindex('~')
    return line_number, begin_column, end_column

for i, error_line in enumerate(error_lines):
    if source_code_path not in error_line:
        continue
    if match := re.search(r"invalid conversion from 'void\*' to '([\w\*]+)'", error_line):
        to_type = match.group(1)
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
    # elif match := re.search(r"invalid conversion from 'int' to '(\w+)'", error_line):
    #     to_type = match.group(1)
    #     line_number, begin_column, end_column = get_code_span(i)
    #     old_line = source_code_lines[line_number]
    #     new_line = f"{old_line[:begin_column]}{to_type}({old_line[begin_column:end_column]}){old_line[end_column:]}"
    #     source_code_lines[line_number] = new_line

with open(source_code_path, "w") as f:
    f.writelines("\n".join(source_code_lines))
