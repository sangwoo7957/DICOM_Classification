import pydicom
import matplotlib.pyplot as plt
import numpy as np
import os
from multiprocessing import Pool
import time

def image_path_list(filepath):
    result = []
    for (root, dirs, files) in os.walk(filepath):
        if len(files) > 0:
            root_path = str(root).replace("\\\\", "\\")
            for file_name in files:
                _, file_delimiter = file_name.split(".")
                if file_delimiter == "dcm":
                    result.append(r"" + root_path + "\\" + file_name)
    return result

def image_classify(img_path):
    image_directory = r"D:\user\DICOM_images"
    dataset = pydicom.dcmread(img_path)
    try:
        if dataset.Modality:
            if dataset.BodyPartExamined:
                image_category = str(dataset.Modality) + "-" + str(dataset.BodyPartExamined)
                if not (os.path.isdir(os.path.join(image_directory, image_category))):
                    os.makedirs(os.path.join(image_directory, image_category))
                os.chdir(os.path.join(image_directory, image_category))
                plt.axis("off")
                # plt.imshow(img, cmap=plt.cm.gray)
                plt.imsave(str(dataset.Modality) + "-" + str(dataset.SOPInstanceUID) + ".png", dataset.pixel_array)
                print("SUCCESS")
    except:
        print("No Modality or BodyPartExamined Attribute")

if __name__ == '__main__':
    image_directory = r"D:\user\DICOM_images"
    try:
        if not(os.path.isdir(image_directory)):
            os.makedirs(os.path.join(image_directory))
    except OSError :
        print("File Exception")
    filepath = r"D:\user\DICOM_temp\MR-BRAIN"
    start = time.time()
    image_paths = image_path_list(filepath)
    pool = Pool(processes=5)
    pool.map(image_classify, image_paths)
    pool.close()
    pool.join()
    print(time.time() - start)