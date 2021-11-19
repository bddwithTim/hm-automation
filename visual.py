import os
import sys
import time
import argparse
import subprocess
from multiprocessing.pool import ThreadPool

import src.lib.base as base
import src.lib.config as configs
from src.lib.remote import SauceHelper

from PIL import Image
import glob


configs.setup_configs(option='username')
configs.setup_configs(option='access_key')


def crop_top(img_full):
    # Create an Image object from an Image
    imageObject = Image.open(img_full)

    # Crop the iceberg portion
    cropped = imageObject.crop((1,78,1006,750))

    # Display the cropped portion
    path = os.path.dirname(img_full)
    cropped.save(os.path.join(path, os.path.basename(img_full)))


def list_all(all_dirs):
    dirs = []
    for root, directories, files in os.walk(all_dirs):
        for directory in directories:
            dirs.append(os.path.join(root, directory))
        break

    folders = ["baseline", "current"]
    for dir in dirs:
        for folder in folders:
            if os.path.isdir(os.path.join(dir, folder)):
                os.chdir(os.path.join(dir, folder))
                for file in glob.glob("*.png"):
                    crop_top(os.path.join(os.path.join(dir, folder), file))


def remove_excess(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".png"):
                if file.startswith("0000") or file.startswith("0001"):
                    os.remove(os.path.join(root, file))
                if file.endswith("_baseline") or file.endswith("_current"):
                    os.remove(os.path.join(root, file))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(prog="Visual Regression")
    ap.add_argument("reports", help="JSON Report folder/file path")
    ap.add_argument("--baseline", action="store_true", default=False, help="Capture baseline images for comparison")
    args = vars(ap.parse_args())

    path = args['reports']
    user = base.config['username']
    key = base.config['access_key']
    directory = 'C:/Users/rpatali1/GitRepos/AutomationFramework/Automation/imgdiff/'

    if (user is None or user == "") and (key is None or key == ""):
        sys.exit("SauceLabs Username/Access Key required...")
    sauce_helper = SauceHelper(user, key)

    if os.path.isdir(path):
        path = "%s\\reports.json" % args['reports']
    elif os.path.isfile(path):
        pass
    else:
        sys.exit("JSON Report not found...")

    sauce_helper.get_report_nodes(path)

    if args['baseline']:
        sauce_helper.base_flag = True

    if len(sauce_helper.meta) > 0:
        # server.send_message_to_all("Acquiring screen shots list in Saucelabs...")
        result_lists = ThreadPool(10).imap_unordered(sauce_helper.get_screenshot_list, list(sauce_helper.meta))
        for result in result_lists:
            print(result)

        # server.send_message_to_all("Downloading resources...")
        sauce_helper.get_screenshot_items()

        if not sauce_helper.base_flag:
            # server.send_message_to_all("Comparing images...")
            # i = 0

            # crop images
            list_all(directory)

            start = time.time()
            for node in sauce_helper.meta:
                imgdiff_dir = "C:/Users/rpatali1/GitRepos/AutomationFramework/Automation/lib/imgdiff.py"
                # path, base_imgs, current_imgs = imgdiff.baseline(sauce_helper.meta[node]['name'])
                # i += len(base_imgs)
                # imgdiff = subprocess.run("python .\\lib\\imgdiff.py -n \"%s\"" % sauce_helper.meta[node]['name'])
                imgdiff = subprocess.run("python %s -n \"%s\"" % (imgdiff_dir, sauce_helper.meta[node]['name']))
                if imgdiff.stdout is not None:
                    print(imgdiff.stdout.decode('utf-8'))
            end = time.time()
            print(end - start)
            # server.send_message_to_all("Comparison on {} images for {}s".format(i, round(end - start)))
        # remove excess images
        remove_excess(directory)
    else:
        # server.send_message_to_all("No test passing or ran...")
        pass





