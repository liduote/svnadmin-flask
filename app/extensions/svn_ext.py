import subprocess

from config import Config
from app.exception import SvnOperateException

ADMIN_EXCUTOR = 'svnadmin'
CLIENT_EXCUTOR = 'svn'

def create_repository(project):
    cmd = 'su - svn -c "{exec} create {data_dir}/{repo_path}"'\
        .format(exec=ADMIN_EXCUTOR, data_dir=Config.DATA_DIR, repo_path=project.path)
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
        f.write(project.final_auth_content)


def init_repo_dirs(project):
    dirs = ''
    for d in Config.SVN_INIT_DIRS:
        dirs = dirs + ' file://{data_dir}/{repo_path}/{dir}'.\
            format(data_dir=Config.DATA_DIR,
                   repo_path=project.path,
                   dir=d)
    cmd = 'su - svn -c "{exec} mkdir {dirs}"'.format(exec=CLIENT_EXCUTOR, dirs=dirs)
    status, output = subprocess.getstatusoutput(cmd)
    if status != 0:
        raise SvnOperateException(status, output)
