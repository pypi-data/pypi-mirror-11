try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

exec(open('gtts/version.py').read())

setup(
    name='gTTS',
    version=__version__,
    author='Pierre Nicolas Durette',
    author_email='pndurette@gmail.com',
    url='https://github.com/pndurette/gTTS',
    packages=['gtts'],
    scripts=['bin/gtts-cli', 'bin/gtts-cli.py'],
    license='MIT',
    description='Create an mp3 file from spoken text via the Google TTS (Text-to-Speech) API',
    long_description=open('README.txt').read(),
    install_requires=[
        "requests"
    ],
    classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Software Development :: Libraries',
          'Topic :: Multimedia :: Sound/Audio :: Speech'
    ],
)
