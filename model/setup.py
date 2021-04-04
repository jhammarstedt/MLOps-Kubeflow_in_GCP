from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
]

setup(
    name='babyweight',
    version='0.1',
    author = 'V Lakshmanan',
    author_email = 'lak@cloud.google.com',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='Baby Weight prediction in Cloud ML',
    requires=[]
)