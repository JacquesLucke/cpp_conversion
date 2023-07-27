import os

for dirpath, dirnames, filenames in os.walk("/home/jacques/blender/blender/source/"):
    for name in filenames:
        if name.endswith(".c"):
            print(os.path.join(dirpath, name))
