"""
Utilities
"""
import json
import os
from subprocess import STDOUT, check_output
import logging
import threading
import re

ISO_TIME_FORMAT = '%m%d-%H-%M-%S'

class Dict2obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Dict2obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Dict2obj(b) if isinstance(b, dict) else b)


class Utilities:
    @staticmethod
    def save_json(data, file_path):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)

    @staticmethod
    def load_json(file_path):
        if not os.path.exists(file_path):
            print(file_path + ' does not exist.')
            return None
        with open(file_path) as data_file:
            data = json.load(data_file)
            return data

    logger = None
    ISOTIMEFORMAT = '%m%d-%H-%M-%S'

    @staticmethod
    def run_cmd(cmd):
        Utilities.logger.debug('Run cmd: ' + cmd)

        seconds = 60
        result = True
        for i in range(1, 3):
            try:
                result = True
                output = check_output(cmd, stderr=STDOUT, timeout=seconds)
                for line in output.split('\n'):
                    if 'Failure' in line or 'Error' in line:
                        result = False
                    tmp = line.replace(' ', '')
                    tmp = tmp.replace('\n', '')
                    if tmp != '':
                        Utilities.logger.debug(line)
                break
            except Exception as exc:
                Utilities.logger.warn(exc)
                result = False
                if i == 2:
                    # close_emulator(emu_proc)
                    # emu_proc = open_emu(emu_loc, emu_name)
                    raise Exception(cmd)

        return result

    @staticmethod
    def set_file_log(logger, file_path):
        print(os.path.dirname(file_path))
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        file_handler = logging.FileHandler(file_path, mode='w')
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        return file_handler

    @staticmethod
    def str2words(str):
        #print 'English Detected!'
        str = re.sub('(http|com|net|org|/|\?|=|_|:|&|\.)', ' ', str)  # if English only
        words = str.lower().split()
        #words = [w for w in words if not w in stopwords.words("english")]
        #print words

        # print '/'.join(words) #  do not use print if you want to return
        return ' '.join(words)


def set_logger(tag, level='DEBUG'):
    log = logging.getLogger(tag)
    console_handler = logging.StreamHandler()

    if level == 'DEBUG':
        log.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
    elif level == 'INFO':
        log.setLevel(logging.INFO)
        console_handler.setLevel(logging.INFO)
    elif level == 'WARN':
        log.setLevel(logging.WARN)
        console_handler.setLevel(logging.WARN)
    else:
        log.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    log.addHandler(console_handler)
    return log



