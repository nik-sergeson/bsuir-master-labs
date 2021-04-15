from PIL import Image, ImageDraw
from django.shortcuts import redirect, render
from django.views import View
from skimage import img_as_ubyte
from skimage.color import rgb2gray
from skimage.io import imread, imsave
import numpy  as np
from skimage.transform import resize
from sklearn.preprocessing import MultiLabelBinarizer

from svhn_ui.forms import UploadFileForm
from svhn_ui.models import get_bounding_box_detection_model, get_image_detection_model
from svhn_ui.settings import PROJECT_DIR
from os.path import join

BOUNDING_BOX_DETECTION_MODEL = None
DIGITS_DETECTION_MODEL = None


class UploadView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            save_uploaded_file(request.FILES['file'])
            if form.cleaned_data["use_autocrop"]:
                return redirect("process_image_with_autocrop")
            else:
                return redirect("process_image")
        return render(request, self.template_name, {'form': form})


class ProcessImageView(View):
    template_name = "process_image.html"

    def get(self, request, use_autocrop):
        global BOUNDING_BOX_DETECTION_MODEL
        global DIGITS_DETECTION_MODEL
        uploaded_image = rgb2gray(load_uploaded_file())
        if use_autocrop:
            image_processed = resize(uploaded_image, (100, 100)).astype(np.float32)
            if BOUNDING_BOX_DETECTION_MODEL is None:
                BOUNDING_BOX_DETECTION_MODEL = get_bounding_box_detection_model(
                    join(PROJECT_DIR, "weights", "weights-svhn-multiple-numbers-bounding-box-detector.hdf5"))
            box_predicted = BOUNDING_BOX_DETECTION_MODEL.predict(image_processed.reshape(1, 100, 100, 1))[0]
            imsave(join(PROJECT_DIR, "images", "processed", "image_bbox.png"),
                   img_as_ubyte(np.asarray(display_predicted_bbox(image_processed, box_predicted))))
            image_cropped = crop_image(image_processed, box_predicted[0], box_predicted[1],
                                       box_predicted[0] + box_predicted[3], box_predicted[1] + box_predicted[2])
            imsave(join(PROJECT_DIR, "images", "processed", "image_cropped.png"),
                   img_as_ubyte(image_cropped))
            uploaded_image = resize(image_cropped, (54, 54))
        else:
            uploaded_image = resize(uploaded_image, (54, 54)).astype(np.float32)
        if DIGITS_DETECTION_MODEL is None:
            DIGITS_DETECTION_MODEL = get_image_detection_model(
                join(PROJECT_DIR, "weights", "weights-svhn-multiple-numbers.hdf5"))
        y_pred = DIGITS_DETECTION_MODEL.predict(uploaded_image.reshape(1, 54, 54, 1))
        ml_binalizer = MultiLabelBinarizer()
        ml_binalizer.fit([[i] for i in range(10)])
        y_pred = (y_pred >= 0.5).astype('int')
        labels = ml_binalizer.inverse_transform(y_pred)[0]
        return render(request, self.template_name, {"predicted_labels": labels, "use_autocrop": use_autocrop})


def save_uploaded_file(uploaded_file):
    with open(join(PROJECT_DIR, "images", "uploaded_image.png"), 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)


def load_uploaded_file():
    return imread(join(PROJECT_DIR, "images", "uploaded_image.png"))


def crop_image(image, x0, y0, x1, y1):
    image = image * 255
    im = Image.fromarray(image.reshape(image.shape[:2]).astype('uint8'), 'L')
    return np.asarray(im.crop((x0, y0, x1, y1)))


def display_predicted_bbox(image, bbox_pred):
    image = image * 255
    im = Image.fromarray(image.reshape(image.shape[:2]).astype('uint8'), 'L')
    rgbimg = Image.new("RGB", im.size)
    rgbimg.paste(im)
    draw = ImageDraw.Draw(rgbimg)
    draw.rectangle([bbox_pred[0], bbox_pred[1], bbox_pred[0] + bbox_pred[3], bbox_pred[1] + bbox_pred[2]],
                   outline="red")
    rgbimg = rgbimg.resize((150, 150))
    return rgbimg
