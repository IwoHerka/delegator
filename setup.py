import setuptools
import delegator

setuptools.setup(
    name             = 'dele-gator',
    version          = delegator.__version__,
    license          = 'MIT',
    requires         = ['python (>= 3.5)'],
    provides         = ['delegator'],
    description      = 'delegator is a micro-package for defining delegated methods and attributes.',
    url              = 'http://github.com/IwoHerka/delegator',
    packages         = setuptools.find_packages(),
    maintainer       = 'Iwo Herka',
    maintainer_email = 'hi@iwoherka.eu',
    author           = 'Iwo Herka',
    author_email     = 'hi@iwoherka.eu',

    classifiers  = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
