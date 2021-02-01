import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='yb-enigma',
    version='1.0.1',
    author='Yurii Bliusiuk',
    author_email='ura.blusuk@gmail.com',
    description='Simple Enigma machine emulator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url='http://github.com/yuriybl/yb-enigma',
    packages=['yb_enigma'],
    entry_points='''
            [console_scripts]
            enigma-cli=yb_enigma.cli:run
      ''',
    zip_safe=False,
)
