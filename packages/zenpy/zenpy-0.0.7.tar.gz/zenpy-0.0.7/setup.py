from setuptools import setup
import setuptools

setup(
	name='zenpy',
	packages=setuptools.find_packages(),
	version='0.0.7',
	description='Python wrapper for the Zendesk API',
	license='GPLv3',
	author='Face Toe',
	author_email='facetoe@facetoe.com.au',
	url='https://github.com/facetoe/zenpy',
	download_url='https://github.com/facetoe/zenpy/releases/tag/0.0.7',
	install_requires=[
		'requests',
		'python-dateutil'
	],
	keywords=['zendesk', 'api', 'wrapper'],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 2',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
	],
)
