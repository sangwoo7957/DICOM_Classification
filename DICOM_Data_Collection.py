import pydicom
from pydicom.multival import MultiValue
import matplotlib.pyplot as plt
import numpy as np
import os
from multiprocessing import Pool
import time

def window_image(img, window_center, window_width, slope, intercept):
    img = (img * slope + intercept)
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    return np.clip(img, img_min, img_max)

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
    image_directory = r"D:\DICOM_tmp"
    dataset = pydicom.dcmread(img_path)
    os.chdir(image_directory)
    try:
        if dataset.Modality:
            if not (os.path.isdir(image_directory + "\\" + str(dataset.Modality))):
                os.makedirs(os.path.join(image_directory + "\\" + str(dataset.Modality)))
                try:
                    if dataset.BodyPartExamined:
                        if dataset.Modality == "MG" and dataset.BodyPartExamined == "BREAST":
                            dataset.WindowWidth = 65535
                            dataset.WindowCenter = 32767
                        if not (os.path.isdir(image_directory + "\\" + str(dataset.Modality) + "\\" + str(dataset.BodyPartExamined))):
                            os.makedirs(os.path.join(image_directory + "\\" + str(dataset.Modality) + "\\" + str(dataset.BodyPartExamined)))
                            try:
                                if type(dataset.WindowCenter) is MultiValue:
                                    dataset.WindowCenter = dataset.WindowCenter[0]
                                if type(dataset.WindowWidth) is MultiValue:
                                    dataset.WindowWidth = dataset.WindowWidth[0]
                                img = window_image(dataset.pixel_array, dataset.WindowCenter, dataset.WindowWidth,
                                                           dataset.RescaleSlope, dataset.RescaleIntercept)
                                os.chdir(image_directory + "\\" + str(dataset.Modality) + "\\" + str(dataset.BodyPartExamined))
                                plt.axis("off")
                                # plt.imshow(img, cmap=plt.cm.gray)
                                plt.imsave(str(dataset.Modality) + "-" + str(dataset.SOPInstanceUID) + ".png", img, cmap=plt.cm.gray)
                            except:
                                print("Exception error")
                        else:
                            try:
                                if type(dataset.WindowCenter) is MultiValue:
                                    dataset.WindowCenter = dataset.WindowCenter[0]
                                if type(dataset.WindowWidth) is MultiValue:
                                    dataset.WindowWidth = dataset.WindowWidth[0]
                                img = window_image(dataset.pixel_array, dataset.WindowCenter, dataset.WindowWidth,
                                                           dataset.RescaleSlope, dataset.RescaleIntercept)
                                os.chdir(image_directory + "\\" + str(dataset.Modality) + "\\" + str(dataset.BodyPartExamined))
                                plt.axis("off")
                                # plt.imshow(img, cmap=plt.cm.gray)
                                plt.imsave(str(dataset.Modality) + "-" + str(dataset.SOPInstanceUID) + ".png", img, cmap=plt.cm.gray)
                            except:
                                print("Exception error")
                except:
                    img = window_image(dataset.pixel_array, dataset.WindowCenter, dataset.WindowWidth,
                                       dataset.RescaleSlope, dataset.RescaleIntercept)
                    os.chdir(image_directory + "\\" + str(dataset.Modality))
                    plt.axis("off")
                    # plt.imshow(img, cmap=plt.cm.gray)
                    plt.imsave(str(dataset.Modality) + "-" + str(dataset.SOPInstanceUID) + ".png", img, cmap=plt.cm.gray)
            else:
                try:
                    if dataset.BodyPartExamined:
                        if dataset.Modality == "MG" and dataset.BodyPartExamined == "BREAST":
                            dataset.WindowWidth = 65535
                            dataset.WindowCenter = 32767
                        if not (os.path.isdir(image_directory + "\\" + str(dataset.Modality) + "\\" + str(
                                dataset.BodyPartExamined))):
                            os.makedirs(os.path.join(image_directory + "\\" + str(dataset.Modality) + "\\" + str(
                                dataset.BodyPartExamined)))
                            try:
                                if type(dataset.WindowCenter) is MultiValue:
                                    dataset.WindowCenter = dataset.WindowCenter[0]
                                if type(dataset.WindowWidth) is MultiValue:
                                    dataset.WindowWidth = dataset.WindowWidth[0]
                                img = window_image(dataset.pixel_array, dataset.WindowCenter, dataset.WindowWidth,
                                                   dataset.RescaleSlope, dataset.RescaleIntercept)
                                os.chdir(image_directory + "\\" + str(dataset.Modality) + "\\" + str(
                                    dataset.BodyPartExamined))
                                plt.axis("off")
                                # plt.imshow(img, cmap=plt.cm.gray)
                                plt.imsave(str(dataset.Modality) + "-" + str(dataset.SOPInstanceUID) + ".png", img, cmap=plt.cm.gray)
                            except:
                                print("Exception error")
                        else:
                            try:
                                if type(dataset.WindowCenter) is MultiValue:
                                    dataset.WindowCenter = dataset.WindowCenter[0]
                                if type(dataset.WindowWidth) is MultiValue:
                                    dataset.WindowWidth = dataset.WindowWidth[0]
                                img = window_image(dataset.pixel_array, dataset.WindowCenter, dataset.WindowWidth,
                                                   dataset.RescaleSlope, dataset.RescaleIntercept)
                                os.chdir(image_directory + "\\" + str(dataset.Modality) + "\\" + str(
                                    dataset.BodyPartExamined))
                                plt.axis("off")
                                # plt.imshow(img, cmap=plt.cm.gray)
                                plt.imsave(str(dataset.Modality) + "-" + str(dataset.SOPInstanceUID) + ".png", img, cmap=plt.cm.gray)
                            except:
                                print("Exception error")
                except:
                    img = window_image(dataset.pixel_array, dataset.WindowCenter, dataset.WindowWidth,
                                       dataset.RescaleSlope, dataset.RescaleIntercept)
                    os.chdir(image_directory + "\\" + str(dataset.Modality))
                    plt.axis("off")
                    # plt.imshow(img, cmap=plt.cm.gray)
                    plt.imsave(str(dataset.Modality) + "-" + str(dataset.SOPInstanceUID) + ".png", img, cmap=plt.cm.gray)
    except:
        print("Exception error")




if __name__ == '__main__':
    image_directory = r"D:\DICOM_tmp"
    try:
        if not(os.path.isdir(image_directory)):
            os.makedirs(os.path.join(image_directory))
    except OSError :
        print("File Exception")
    filepath = r"D:\DICOM_img"
    start = time.time()
    image_paths = image_path_list(filepath)
    pool = Pool(processes=5)
    pool.map(image_classify, image_paths)
    pool.close()
    pool.join()
    print(time.time() - start)