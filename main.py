import tkinter as tk
from PIL import Image

from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.resnet50 import preprocess_input

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

import pydicom
from pydicom.multival import MultiValue

pth = []
for i in range(1, len(sys.argv)):
    pth.append(sys.argv[i])

if len(pth) > 2:
    path_dir = r" ".join(pth)
else:
    path_dir = r"".join(pth)

# Get all dicom files
# path_dir = r"D:\DICOM_dataset\MR-PROSTATE\Prostate Fused-MRI-Pathology\aaa0044\09-06-2000-PELVISPROSTATE-73728\1.000000-localizer-55037"
real_file_list = []
for root, dirs, files in os.walk(path_dir):
    rootpath = os.path.join(os.path.abspath(path_dir), root)
    for file in files:
        filepath = os.path.join(rootpath, file)
        real_file_list.append(filepath)

# Extract images in dicom files to train
images_train = []
print("Images checking")
for filepath in real_file_list:
    data = pydicom.dcmread(filepath)
    plt.axis("off")
    plt.imsave(os.path.join(os.getcwd(), "images_train", str(data.SOPInstanceUID) + ".png"), data.pixel_array)

    images_train.append(os.path.join(os.getcwd(), "images_train", str(data.SOPInstanceUID) + ".png"))

    img = Image.open(os.path.join(os.getcwd(), "images_train", str(data.SOPInstanceUID) + ".png"))
    img_resize = img.resize((256, 256))
    img_resize.save(os.path.join(os.getcwd(), "images_train", str(data.SOPInstanceUID) + ".png"))

# load the trained model
model = load_model(os.path.join(os.getcwd(), "model", "model.h5"))
LABELS = ['CR-CHEST', 'CT-ABDOMEN', 'CT-BREAST', 'CT-CHEST', 'CT-COLON', 'CT-HEADNECK',
          'CT-KIDNEY', 'CT-LUNG', 'CT-PANCREAS', 'DX-CHEST', 'MG-BREAST', 'MR-ABDOMEN',
          'MR-BRAIN', 'MR-BREAST', 'MR-HEADNECK', 'MR-KIDNEY', 'MR-PELVIS', 'MR-PROSTATE']
labels = dict((k, v) for k, v in enumerate(LABELS))
predicted_labels = []
print("Images training")
for img_train in images_train:
    test_img = img_to_array(load_img(img_train, target_size=(256, 256)))
    test_input = preprocess_input(np.expand_dims(test_img.copy(), axis=0))

    pred = model.predict(test_input)
    predicted_class_indices = int(np.argmax(pred, axis=1))

    predicted_labels.append(labels[predicted_class_indices] + ' %.3f%%' % (pred[0][predicted_class_indices] * 100))
    print(pred)
print(predicted_labels)

# Visualize the images
def window_image(img, window_center, window_width, slope, intercept):
    img = (img * slope + intercept)
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    return np.clip(img, img_min, img_max)

root = tk.Tk()
root.title("DICOM Classification")
root.geometry("700x700")
root.resizable(0, 0)

index = 0
def next_event():
    global index
    global images
    global root
    global click_cnt
    if(index >= click_cnt):
        index = 0

    image = tk.PhotoImage(file=images[index])
    label_img = tk.Label(root, image=image)
    label_img.place(x=100, y=150)

    label_pred = tk.Label(root, text=predicted_labels[index])
    label_pred.grid(row=5, column=2)
    label_pred.configure(font=("Courier", 16, "bold"))

    index += 1

    root.mainloop()

images = []
def click_submit():
    global window_c
    global window_w
    global index
    global images
    global images_train
    global click_cnt
    window_c = int(EntryWidget_c.get())
    window_w = int(EntryWidget_w.get())

    data = pydicom.dcmread(real_file_list[index])
    if click_cnt < len(predicted_labels):
        click_cnt += 1
        try:
            if data.WindowCenter:
                try:
                    if data.RescaleSlope:
                        if type(data.WindowCenter) is MultiValue:
                            img = window_image(data.pixel_array, data.WindowCenter[0], data.WindowWidth[0], data.RescaleSlope,
                                               data.RescaleIntercept)
                            plt.axis("off")
                            plt.imsave(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"), img, cmap=plt.cm.gray)

                            img = Image.open(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))
                            img_resize = img.resize((512, 512), Image.ANTIALIAS)
                            img_resize.save(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))

                            images.append(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))
                        else:
                            img = window_image(data.pixel_array, data.WindowCenter, data.WindowWidth,
                                               data.RescaleSlope,
                                               data.RescaleIntercept)
                            plt.axis("off")
                            plt.imsave(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"), img, cmap=plt.cm.gray)

                            img = Image.open(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))
                            img_resize = img.resize((512, 512), Image.ANTIALIAS)
                            img_resize.save(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))

                            images.append(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))
                            print("Finish")
                except:
                    plt.axis("off")
                    plt.imsave(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"), data.pixel_array, cmap=plt.cm.gray)

                    img = Image.open(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))
                    img_resize = img.resize((512, 512), Image.ANTIALIAS)
                    img_resize.save(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))

                    images.append(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))
                    print("Finish")
        except:
            try:
                if data.RescaleSlope:
                    img = window_image(data.pixel_array, window_c, window_w, data.RescaleSlope,
                                       data.RescaleIntercept)
                    plt.axis("off")
                    plt.imsave(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"), img, cmap=plt.cm.gray)

                    img = Image.open(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))
                    img_resize = img.resize((512, 512), Image.ANTIALIAS)
                    img_resize.save(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))

                    images.append(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))
                    print("Finish")
            except Exception as e:
                plt.axis("off")
                plt.imsave(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"), data.pixel_array,
                           cmap=plt.cm.gray)

                img = Image.open(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))
                img_resize = img.resize((512, 512), Image.ANTIALIAS)
                img_resize.save(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))

                images.append(os.path.join(os.getcwd(), "images", str(data.SOPInstanceUID) + ".png"))
                print("Finish")

window_c = 0
LabelWidget_c = tk.Label(root, text="Window Center")
LabelWidget_c.grid(row=0, column=0)
EntryWidget_c = tk.Entry(root, bd=5)
EntryWidget_c.grid(row=0, column=1)

window_w = 0
LabelWidget_w = tk.Label(root, text="Window Width")
LabelWidget_w.grid(row=1, column=0)
EntryWidget_w = tk.Entry(root, bd=5)
EntryWidget_w.grid(row=1, column=1)

click_cnt = 0
btn_submit = tk.Button(root, text="Submit", command=click_submit)
btn_submit.grid(row=1, column=2, ipadx=20, padx=10, pady=5)

btn_next = tk.Button(root, text="next image", command=next_event, width=20, height=1)
btn_next.grid(row=3, column=0)

root.mainloop()