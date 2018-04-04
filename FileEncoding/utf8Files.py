"""Function Declaratios.

Modify text file's encoding to utf-8. General for Chinese text files.
Common coding standard:
    GB18030
    GB2312
"""

__author__ = "Liu Kun"
__version__ = 0.1

import os
import queue
import time
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", type=str,
                    help="try to decode files in the given directory")
parser.add_argument("-fp", "--filepath", type=str,
                    help="try to decode files with the given path")

def decode_file_to_unicode(file_path):
    """Return unicode type

    Try to decode text within a file with several coding standard
    """
    try:
        with open(file_path, "rb") as fr:
            content = fr.read().decode("GB18030")
            return content
    except UnicodeError:
        try:
            with open (file_path, "rb") as fr:
                content = fr.read().decode("utf-8")
                return content
        except UnicodeError:
            with open (file_path, "rb") as fr:
                content = fr.read().decode("GB2312")
                return content


def process_file(path):
    try:
        try:
            unicode_content = decode_file_to_unicode(path)
            with open(path, "wb") as fw:
                fw.write(unicode_content.encode("utf-8"))
        except UnicodeError as ue:
            if ignore_bool:
                print("Fail to decode: %s ->ignore"%path)
            else:
                os.remove(path)
                print("Fail to decode: %s ->delete"%path)
    except Exception as E:
        print("Exception happended during processing %s"%path)


def process_files(queue, ignore_bool=True):
    while not queue.empty():
        path = queue.get()
        process_file(path)


def print_progress_bar(queue):
    """Print Progress bar"""
    import sys
    num_total_task = queue.qsize()
    while not queue.empty():
        progress = (num_total_task - queue.qsize())/num_total_task * 100
        sys.stdout.write('\r')
        sys.stdout.write("%.2f%% |[%s]" %(progress,  int(progress)*'>'))
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write('\n')


def try_loading_files(dir_path):
    files = os.listdir(dir_path)
    path_queue = queue.Queue()
    for file in files:
        path_queue.put(os.path.join(dir_path, file))
    t1 = threading.Thread(target=process_files, args=(path_queue,), daemon=True)
    t2 = threading.Thread(target=print_progress_bar, args=(path_queue,), daemon=True)
    threads = [t1, t2]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

if __name__ == '__main__':
    args = parser.parse_args()
    if args.dir:
        try_loading_files(args.dir)
    elif args.filepath:
        process_file(args.filepath)
