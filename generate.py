import csv
import logging
import pathlib
import subprocess
import os
import argparse


def build_args():
    parser = argparse.ArgumentParser()
    parser.set_defaults(slice_types=['usages', 'reachables'])
    parser.add_argument(
        '--repo-csv',
        type=pathlib.Path,
        default='sources.csv',
        help='Path to sources.csv',
        dest='repo_csv'
    )
    parser.add_argument(
        '--clone-dir',
        type=pathlib.Path,
        default='/home/runner/work/src_repos',
        help='Path to src_repos',
        dest='clone_dir'
    )
    parser.add_argument(
        '-o',
        '--output-dir',
        type=pathlib.Path,
        default='/home/runner/work/atom-samples/atom-samples',
        help='Path to output',
        dest='output_dir'
    )
    lang_parser_group = parser.add_mutually_exclusive_group()
    lang_parser_group.set_defaults(langs=['java', 'python', 'javascript'])
    lang_parser_group.add_argument(
        '-i',
        '--include-langs',
        choices=['java', 'python', 'javascript'],
        default=['java', 'python', 'javascript'],
        help='Languages to generate samples for',
        dest='langs',
        nargs='*',
    )
    lang_parser_group.add_argument(
        '-e',
        '--exclude-langs',
        choices=['java', 'python', 'javascript'],
        dest='elangs',
        nargs='*'
    )
    parser.add_argument(
        '-s',
        '--slice-type',
        choices=['usages', 'reachables'],
        help='Slice type to generate',
        dest='slice_types',
        const=['usages', 'reachables'],
        nargs='?'
    )
    parser.add_argument(
        '--skip-clone',
        action='store_false',
        dest='clone',
        default=True,
        help='Skip cloning the repositories (must be used with the --repo-dir argument)'
    )
    parser.add_argument(
        '--debug-cmds',
        action='store_true',
        dest='debug_cmds',
    )
    parser.add_argument(
        '--skip-build',
        action='store_true',
        dest='skip_build',
        default=False,
        help='Skip building the samples and just run atom. Should be used with --skip-clone'
    )
    return parser.parse_args()


def generate(repo_data, clone_dir, output_dir, slice_types, clone, debug_cmds, skip_build):
    if not skip_build:
        run_pre_builds(repo_data, output_dir, debug_cmds)

    commands = f'\n{subprocess.list2cmdline(["sdk", "use", "java", "20.0.2-tem"])}' if skip_build else ''

    for repo in repo_data:
        project = repo['project']
        lang = repo['language']
        loc = os.getcwd()
        repo_dir = os.path.join(clone_dir, lang, project)
        if clone:
            clone_repo(repo['link'], clone_dir, repo_dir)

        commands += f"\n{subprocess.list2cmdline(['cd', repo_dir])}"

        if not skip_build and len(repo['pre_build_cmd']) > 0:
            cmds = repo['pre_build_cmd'].split(';')
            cmds = [cmd.lstrip().rstrip() for cmd in cmds]
            for cmd in cmds:
                new_cmd = list(cmd.split(' '))
                commands += f"\n{subprocess.list2cmdline(new_cmd)}"

        if not skip_build and len(repo['build_cmd']) > 0:
            cmds = repo['build_cmd'].split(';')
            cmds = [cmd.lstrip().rstrip() for cmd in cmds]
            for cmd in cmds:
                new_cmd = list(cmd.split(' '))
                commands += f"\n{subprocess.list2cmdline(new_cmd)}"

        commands += f"\n{subprocess.list2cmdline(['cd', loc])}"

        if not skip_build and lang == 'java':
            commands += f'\n{subprocess.list2cmdline(["sdk", "env", "clear"])}'

        for stype in slice_types:
            slice_file = os.path.join(output_dir, lang, f"{project}-{stype}.json")
            atom_file = os.path.join(repo_dir, f"{project}.atom")
            cmd = ['atom', stype, '-l', lang, '-o', atom_file, '-s', slice_file, repo_dir]
            commands += f"\n{subprocess.list2cmdline(cmd)}"

        commands += '\n\n'

    sh_path = os.path.join(output_dir, 'atom_commands.sh')
    use_script(sh_path, commands, debug_cmds)

def read_csv(csv_file, langs):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        repo_data = list(reader)
    
    if len(langs) != 3:
        return [repo for repo in repo_data if repo['language'] in langs]
    
    return repo_data


def clone_repo(url, clone_dir, repo_dir):
    os.chdir(clone_dir)
    if os.path.exists(repo_dir):
        logging.warning(f'{repo_dir} already exists, skipping clone.')
        return
    clone_cmd = f'git clone {url} {repo_dir}'
    subprocess.run(clone_cmd, shell=True, encoding='utf-8', check=False)
    

def run_pre_builds(repo_data, output_dir, debug_cmds):
    install_sdkman = ["curl", "-s", "'https://get.sdkman.io'", "|", "bash"]
    cp = subprocess.run(install_sdkman, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        env=os.environ.copy(), encoding='utf-8', check=False, )
    print(cp.stdout)
    cmds = []
    [
        cmds.extend(row['pre_build_cmd'].split(';'))
        for row in repo_data
        if row['pre_build_cmd']
    ]
    cmds = [cmd.lstrip().rstrip() for cmd in cmds]
    cmds = set(cmds)

    commands = [c.replace('use', 'install') for c in cmds]
    commands = '\n'.join(commands)
    sh_path = os.path.join(output_dir, 'sdkman_installs.sh')
    use_script(sh_path, commands, debug_cmds)


def use_script(file_path, commands, debug_cmds):
    with open(file_path, 'w', encoding='utf-8') as f:
        sdkman_path = os.path.join('home', 'runner', '.sdkman', 'bin', 'sdkman-init.sh')
        f.write(f'#!/usr/bin/bash\nsource "{sdkman_path}"\n\n')
        f.write(commands)
    if debug_cmds:
        print(commands)
    # else:
    #     cmd = ['sudo', 'chmod', '+x', file_path]
    #     cp = subprocess.run(cmd, shell=True,
    #         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    #         env=os.environ.copy(), encoding='utf-8', check=False, )
    #
    #     print(cp.stdout)


def check_dirs(clone, clone_dir, output_dir):
    if clone and not os.path.exists(clone_dir):
        os.makedirs(clone_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def main():
    args = build_args()
    langs = set(args.langs)
    if args.elangs:
        langs = langs - set(args.elangs)
    # if not args.debug_cmds or not os.getenv('CI'):
    check_dirs(args.clone, args.clone_dir, args.output_dir)
    repo_data = read_csv(args.repo_csv, langs)
    generate(repo_data, args.clone_dir, args.output_dir, args.slice_types, args.clone, args.debug_cmds, args.skip_build)


if __name__ == '__main__':
    main()