import sys
import subprocess
import json
import yaml


if __name__ == '__main__':

    version = subprocess.check_output(['python', '-V'],
                                      universal_newlines=True).split('\n')[0]

    venv = sys.base_prefix

    exec_py = sys.executable

    pip_loc = subprocess.run('which pip', shell=True, stdout=subprocess.PIPE)
    pip_loc = pip_loc.stdout.rstrip().decode('utf-8')

    pythonpath = sys.path

    raw_packages = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE)
    raw_packages = raw_packages.stdout.decode('utf-8').split()

    packages = {}
    for i in raw_packages:
        pack = i.split("==")
        packages[pack[0]] = pack[1]

    site_packages = next(p for p in sys.path if 'site-packages' in p)

    result_dict = {
        'Version of python': version,
        'Virtual environment': venv,
        'Python executable location': exec_py,
        'Pip location': pip_loc,
        'PYTHONPATH': pythonpath,
        'Installed packages (name, version)': packages,
        'Site-packages location': site_packages
    }

    with open('result.json', 'w') as result:
        json.dump(result_dict, result, indent=4)

    with open('result.yaml', 'w') as result:
        yaml.dump(result_dict, result, default_flow_style=False)
