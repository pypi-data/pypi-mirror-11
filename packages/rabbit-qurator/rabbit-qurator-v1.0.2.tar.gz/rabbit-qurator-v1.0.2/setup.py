from distutils.core import setup
from pip.req import parse_requirements
import uuid
import subprocess
install_reqs = parse_requirements('requirements.txt', session=str(uuid.uuid4()))
reqs = [str(ir.req) for ir in install_reqs]

version = subprocess.Popen(
    "git describe",
    shell=True,
    stdout=subprocess.PIPE).stdout.read()
version = version.decode('utf-8')
version.strip()

setup(name='rabbit-qurator',
      author='Travis Holton',
      url='https://github.com/heytrav/rpc-qurator',
      author_email='wtholton@gmail.com',
      description='Create RabbitMQ endpoints using decorators.',
      long_description='Create RabbitMQ endpoints for RPC and tasks using decorators based on kombu.',
      version='v1.0.2',
      packages=['qurator',
                'qurator.rpc',
                'qurator.tests'])
