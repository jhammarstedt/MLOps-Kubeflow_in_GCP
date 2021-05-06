
from setuptools import setup
 
#REQUIRED_PACKAGES = []
 
setup(
   name="Test_model",
   version="0.1",
   scripts=["model_prediction.py","network.py"],
   include_package_data=True,
   install_requires=['torch @ https://download.pytorch.org/whl/cpu/torch-0.4.1-cp35-cp35m-linux_x86_64.whl']

)
