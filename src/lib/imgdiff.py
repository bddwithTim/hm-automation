# import the necessary packages
import sys
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import os
from multiprocessing import Process


src_dir = "imgdiff"
base_dir = "baseline"
current_dir = "current"


# source: https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/
def imgdiff(image_a, image_b, image_out):
    image_name = image_a.split("\\")[-1]
    image_name, ext_name = image_name.split(".")
    # load the two input images
    imageA = cv2.imread(image_a)
    imageB = cv2.imread(image_b)
    imageAx = imageA.copy()
    imageBx = imageB.copy()

    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    print("SSIM: {}".format(score))
    if int(score) == 1:
        return

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    diff = (diff * 225).astype("uint8")
    thresh = cv2.threshold(diff, 0, 225,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    rgbA = (0, 255, 0)
    rgbB = (255, 0, 255)
    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), rgbA, -1)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), rgbB, -1)

    alpha = 0.6
    cv2.addWeighted(imageA, alpha, imageAx, 1 - alpha, 0, imageAx)
    cv2.addWeighted(imageB, alpha, imageBx, 1 - alpha, 0, imageBx)

    # show the output images
    cv2.imwrite("%s\\%s_baseline.%s" % (image_out, image_name, ext_name), imageAx)
    cv2.imwrite("%s\\%s_current.%s" % (image_out, image_name, ext_name), imageBx)
    # cv2.imwrite(".\\s\\diff.png", diff)
    # cv2.imwrite(".\\s\\thresh.png", thresh)
    cv2.waitKey(0)


def baseline(test_name):
    """
    Get baseline image list
    :param test_name: test name
    :return: list of file names
    """
    if test_name is None:
        return None
    _base = []
    _current = []
    named_path = "%s\\%s\\%s" % (os.getcwd().split("imgdiff")[0], src_dir, test_name)

    if os.path.isdir(named_path):
        _base = os.listdir(os.path.join(named_path, base_dir))
        _current = os.listdir(os.path.join(named_path, current_dir))

    return named_path, _base, _current


if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--name", required=True, help="Folder name")
    args = vars(ap.parse_args())
    name = args['name']
    path, base_imgs, current_imgs = baseline(name)

    # print(name)
    if len(base_imgs) < 1 or len(current_imgs) < 1:
        sys.exit("There is no base/current images for test folder \"%s\"" % name)

    jobs = []
    for img in base_imgs:
        baseline = os.path.join(os.path.join(path, base_dir), img)
        current = os.path.join(os.path.join(path, current_dir), img)
        p = Process(target=imgdiff, args=(baseline, current, path))
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()
