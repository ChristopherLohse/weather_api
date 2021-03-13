import os
files = os.listdir(".")
for index, file in enumerate(files):
    if os.path.getsize(file) == 0:
        continue
    if index < training_stop:
        copyfile(file, TRAINING+"/"+file)
    else:
        copyfile(file, TEST+"/"+file)
