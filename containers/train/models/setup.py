
from setuptools import setup
 
REQUIRED_PACKAGES = []
 
setup(
   name="Test_model",
   version="0.1",
   scripts=["model_prediction.py"],
   install_requires=install_requires=['torch @ https://download.pytorch.org/whl/cpu/torch-1.8.1-cp37-cp37m-linux_x86_64.whl']
)
