import matplotlib.pyplot as plt
import pydicom
import numpy as np


filename = r'D:\DICOM_data\VICTRE\1778001589\01-06-2018-DBT Reconstructed Volume-11940\DBT slices-88879\20-01.dcm'
dataset = pydicom.dcmread(filename)

def window_image(img, window_center, window_width, slope, intercept):
    img = (img * slope + intercept)
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    return np.clip(img, img_min, img_max)

print(dataset)
if dataset.Modality == "MG" and dataset.BodyPartExamined == "BREAST":
    dataset.WindowWidth = 65535
    dataset.WindowCenter = 32767
dataset.WindowWidth = 80
dataset.WindowCenter = 35
img = window_image(dataset.pixel_array, dataset.WindowCenter, dataset.WindowWidth,
                   dataset.RescaleSlope, dataset.RescaleIntercept)

plt.axis("off")
plt.imshow(img, cmap=plt.cm.gray)
plt.imsave(str(dataset.SOPInstanceUID) + ".png", img, cmap=plt.cm.gray)
plt.show()

try:
    if dataset.RescaleSlope:
        print("yes")
except:
    print("no")

plt.axis("off")
plt.imshow(dataset.pixel_array)
plt.imsave(str(dataset.SOPInstanceUID) + ".png", dataset.pixel_array)
plt.show()