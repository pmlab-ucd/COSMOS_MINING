import os.path

def handle_md(md_file):
    print(md_file)
    with open(md_file, 'r') as text_file:
        for line in text_file:
            sub_lines = line.split('|')

            # if not (('T' or 't' or 'F' or 'f' or 'D' or 'd') in sub_lines[len(sub_lines) - 2]):
            #   continue

            if line.startswith('#') or line.startswith('| Index ') or line.startswith('| --'):
                continue
            png_path = sub_lines[len(sub_lines) - 4].split('(')[1]
            png_path = png_path.split(')')[0]

            if ('D' or 'd') in sub_lines[len(sub_lines) - 2]:
                print(line)
                md_targets.append(line)
            else:
                continue


def parse_labelled(gnd_dir, instances):
    for root, dirs, files in os.walk(gnd_dir):
        for file_name in files:
            if file_name.endswith('.md'):
                # try:
                handle_md(os.path.join(root, file_name))


if __name__ == '__main__':
    instances = []
    md_targets = []
    gnd_based_dir = 'output/gnd/'
    perm_type = 'RECORD_AUDIO'
    instance_dir = gnd_based_dir + '/' + perm_type + '/'
    md_file_path = gnd_based_dir + perm_type + '.md'
    parse_labelled(instance_dir, instances)
    if os.path.exists(md_file_path):
        os.remove(md_file_path)
    text_file = open(md_file_path, 'a')
    text_file.write('### {}\n'.format(perm_type))

    text_file.write("| Index | Entry Point & APIs | Screen shot | Resource id | Label |\n")
    text_file.write('| ------------- | ------------- | ------------- |-------------|-------------|\n')
    for md_target in md_targets:
        text_file.write(md_target)
    print(len(md_targets))
