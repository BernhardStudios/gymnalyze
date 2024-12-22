from setuptools import setup, find_packages

setup(
    name='gymnalyze',
    version='0.1.0',
    author='Bernardo Martínez Celda',
    author_email='bernhard.studios@gmail.com',
    description='A package for analyzing training videos and assessing poses to improve movements using MediaPipe.',
    packages=find_packages(),
    install_requires=[  # todo: review and update
        'mediapipe',
        'opencv-python'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)