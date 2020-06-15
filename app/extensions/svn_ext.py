import subprocess

from config import Config
from app.exception import SvnOperateException

EXCUTOR = 'svnadmin'


def create_repository(project):
    cmd = 'su - svn -c "{exec} create {data_dir}/{repo_path}"'\
        .format(exec=EXCUTOR, data_dir=Config.DATA_DIR, repo_path=project.path)
    status, output = subprocess.getstatusoutput(cmd)
    if status != 0:
        raise SvnOperateException(status, output)


def delete_repository(project):
    cmd = 'rm -rf {data_dir}/{repo_path}'\
        .format(data_dir=Config.DATA_DIR, repo_path=project.path)
    status, output = subprocess.getstatusoutput(cmd)
    if status != 0:
        raise SvnOperateException(status, output)


def save_authz(project):
    file = '{}/{}/conf/authz'.format(Config.DATA_DIR, project.path)
    with open(file=file, mode='w') as f:
        f.write(project.setting_auth_content)

