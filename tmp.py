import fileinput
import os


def parse_labelled(gnd_dir, instances):
    for root, dirs, files in os.walk(gnd_dir):
        for file_name in files:
            if file_name.endswith('.md'):
                # try:

                file = os.path.join(root, file_name)
                with fileinput.FileInput(file, inplace=True) as file:
                    for line in file:
                        print(line.replace('D:\\', 'F:\\'), end='')


if __name__ == '__main__':
    instances = {}
    gnd_based_dir = 'output/gnd/'
    perm_type = 'Camera' #SEND_SMS'
    instance_dir = gnd_based_dir + '/' + perm_type
    parse_labelled(instance_dir, instances)
