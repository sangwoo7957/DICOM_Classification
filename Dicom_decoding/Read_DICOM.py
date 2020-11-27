import matplotlib.pyplot as plt
import pydicom
from pydicom.data import get_testdata_files

filename = r'C:\Users\JONGHO-PC6\Desktop\DICOM_data\Head-Neck Cetuximab\0522c0001\08-23-1999-NeckHeadNeckPETCT-03251\2.000000-CT 5.0 H30s-55580\1-004.dcm'
dataset = pydicom.dcmread(filename)
text_file = open(str(dataset.SOPInstanceUID) + ".txt", "w")
text_file.write("      Tag      VR Length Value\n")
length_list = []
for key in dataset.keys():
    length_list.append(dataset.get_item(key)[2])

index = 0
# for key in dataset.keys():
#     if type(length_list[index]) == int and length_list[index] > 64:
#         print(dataset.get_item(key).tag, dataset.get_item(key).VR, length_list[index], "Unknown | <Large value not displayed>", sep=" | ")
#         if dataset.get_item(key).VR == "SQ":
#             text_file.write("*" + str(dataset.get_item(key).tag) + " " + str(dataset.get_item(key).VR) + " " + str(length_list[index]) + " " + "Unknown <Large value not displayed>" + "*" + "\n")
#         else:
#             text_file.write(str(dataset.get_item(key).tag) + " | " + str(dataset.get_item(key).VR) + " | " + str(length_list[index]) + " | " + "Unknown | <Large value not displayed>\n")
#     else:
#         print(dataset[key], length_list[index], sep=" | ")
#         if dataset.get_item(key).VR == "SQ":
#             text_file.write(str(dataset[key]) + " " + str(length_list[index]) + "\n")
#         else:
#             text_file.write(str(dataset[key]) + " | " + str(length_list[index]) + "\n")
#     index += 1
# print()

for key in dataset.keys():
    if type(length_list[index]) == int and length_list[index] > 64:
        print(dataset.get_item(key).tag, dataset.get_item(key).VR, length_list[index], "Unknown | <Large value not displayed>", sep=" | ")
        if dataset.get_item(key).VR == "SQ":
            text_file.write(str(dataset.get_item(key).tag) + " " + str(dataset.get_item(key).VR) + " " + str(length_list[index]) + " Unknown | <Large value not displayed>\n")
        else:
            text_file.write(str(dataset.get_item(key).tag) + " | " + str(dataset.get_item(key).VR) + " | " + str(length_list[index]) + " | Unknown | <Large value not displayed>\n")
    else:
        print(dataset.get_item(key).tag, dataset.get_item(key).VR, length_list[index], dataset[key].value, sep="|")
        if dataset.get_item(key).VR == "SQ":
            text_file.write(str(dataset.get_item(key).tag) + " " + str(dataset.get_item(key).VR) + " " + str(length_list[index]) + " " + str(dataset[key].value) + "\n")
        else:
            text_file.write(str(dataset.get_item(key).tag) + " | " + str(dataset.get_item(key).VR) + " | " + str(length_list[index]) + " | " + str(dataset[key].value) + "\n")
    index += 1

if 'PixelData' in dataset:
    rows = int(dataset.Rows)
    cols = int(dataset.Columns)

    print("Image size : {rows:d} x {cols:d}, {size:d} bytes".format(
        rows=rows, cols=cols, size=len(dataset.PixelData)))
    if 'PixelSpacing' in dataset:
        print("Pixel spacing : ", dataset.PixelSpacing)

print("Slice location : ", dataset.get('SliceLocation', "(missing)"))

plt.imshow(dataset.pixel_array, cmap=plt.cm.bone)
plt.savefig(str(dataset.SOPInstanceUID) + ".png")
plt.show()

text_file.close()