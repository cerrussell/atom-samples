import csv
import logging
import subprocess
import os
import argparse


def build_args():
    parser = argparse.ArgumentParser()
    parser.set_defaults(langs=['java', 'python', 'javascript'], elangs=[])
    parser.add_argument(
        '--repo-csv',
        type=str,
        default='sources.csv',
        help='Path to sources.csv',
        dest='repo_csv'
    )
    parser.add_argument(
        '--clone-dir',
        type=str,
        default='/home/runner/work/src_repos',
        help='Path to src_repos',
        dest='clone_dir'
    )
    parser.add_argument(
        '-o',
        '--output-dir',
        type=str,
        default='/home/runner/work/atom-samples/atom-samples',
        help='Path to output',
        dest='output_dir'
    )
    subparsers = parser.add_subparsers()
    lang_parser = subparsers.add_parser(
        'filter',
        help='Filter languages to include or exclude')
    lang_parser_group = lang_parser.add_mutually_exclusive_group()
    lang_parser_group.set_defaults(langs=['java', 'python', 'javascript'])
    lang_parser_group.add_argument(
        '-i',
        '--include',
        choices=['java', 'python', 'javascript'],
        help='Languages to generate samples for',
        dest='langs',
        nargs='*',

    )
    lang_parser_group.add_argument(
        '-e',
        '--exclude',
        choices=['java', 'python', 'javascript'],
        dest='elangs',
        nargs='*'
    )
    parser.add_argument(
        '-s',
        '--slice_types',
        choices=['usages', 'reachables'],
        default=['usages', 'reachables'],
        help='Slice types to generate, default is both usages and reachables',
        dest='slice_types',
        nargs='*'
    )
    parser.add_argument(
        '--skip-clone',
        action='store_false',
        dest='clone',
        default=True,
        help='Skip cloning the repositories (must be used with the --repo-dir argument)'
    )
    return parser.parse_args()


def generate(repo_data, clone_dir, output_dir, slice_types, clone):
    run_pre_builds(repo_data)

    for repo in repo_data:
        project = repo['project']
        lang = repo['language']
        loc = os.getcwd()
        repo_dir = os.path.join(clone_dir, lang, project)
        if clone:
            clone_repo(repo['link'], clone_dir, repo_dir)

        if len(repo['build_cmd']) > 0:
            cmds = repo['build_cmd'].split(';')
            os.chdir(repo_dir)
            for cmd in cmds:
                subprocess.run(cmd, shell=True, encoding='utf-8', check=False)

        for stype in slice_types:
            fname = f'{output_dir}/{lang}/{project}-{stype}.json'
            print(
                f'Generating {stype} slice for {project} at {output_dir}/'
                f'{lang}/{fname}',
            )
            cmd = f'atom {stype} -l {lang} -o {project}.atom -s {fname} .'
            subprocess.run(cmd, shell=True, encoding='utf-8', check=False)
        os.chdir(loc)


def sdkman_installs(cmd):
    new_cmd = 'bash ' + cmd.replace('use', 'install')
    cp = subprocess.run(new_cmd, stdout=subprocess.PIPE, shell=True,
        stderr=subprocess.STDOUT, env=os.environ.copy(), encoding='utf-8',
        check=False, )


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
    

def run_pre_builds(repo_data):
    cmds = []
    [
        cmds.extend(row['pre_build_cmd'].split(';'))
        for row in repo_data
        if row['pre_build_cmd']
    ]
    cmds = set(cmds)

    commands = [c.lstrip().replace('use', 'install') for c in cmds]
    with open('sdkman_installs.sh', 'w', encoding='utf-8') as f:
        f.write('#!/usr/bin/env bash\n')
        f.write('source "/${SDKMAN_DIR}/bin/sdkman-init.sh"\n')
        f.write('\n'.join(commands))

    cp = subprocess.run(
        'sdkman_installs.sh',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ.copy(),
        encoding='utf-8', check=False, )

def check_dirs(clone_dir, output_dir, clone):
    if clone and not os.path.exists(clone_dir):
        os.makedirs(clone_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def main():
    args = build_args()
    langs = set(args.langs)
    if args.elangs:
        langs = langs - set(args.elangs)
    check_dirs(args.clone_dir, args.output_dir, args.clone)
    repo_data = read_csv(args.repo_csv, langs)
    generate(repo_data, args.clone_dir, args.output_dir, args.slice_types, args.clone)


if __name__ == '__main__':
    main()