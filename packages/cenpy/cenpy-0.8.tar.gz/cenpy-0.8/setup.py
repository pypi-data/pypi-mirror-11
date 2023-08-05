from setuptools import setup

setup(name='cenpy',
        version='0.8',
      description='Explore and download data from Census APIs',
      url='https://github.com/ljwolf/cenpy',
      author='Levi John Wolf',
      author_email='levi.john.wolf@gmail.com',
      license='3-Clause BSD',
      packages=['cenpy'],
      install_requires=['pandas', 'requests'],
      zip_safe=False)
