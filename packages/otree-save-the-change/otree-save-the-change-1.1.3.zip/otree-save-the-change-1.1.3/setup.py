# -*- coding: utf-8 -*-

import otree_save_the_change


try:
	from setuptools import setup

except ImportError:
	from distutils.core import setup

install_requires = []
for line in open('requirements.txt', 'rU').readlines():
	if line and line not in '\n' and not line.startswith(('#', '-')):
		install_requires.append(line.replace('\n', ''))

setup(
	name="otree-save-the-change",
	version=otree_save_the_change.__version__,
	description="Automatically save only changed model data.",
	long_description="\n\n".join([open('README.rst', 'rU').read(), open('HISTORY.rst', 'rU').read()]),
	author=otree_save_the_change.__author__,
	author_email=otree_save_the_change.__contact__,
	url=otree_save_the_change.__homepage__,
	license=open('LICENSE', 'rU').read(),
	packages=['otree_save_the_change'],
	package_dir={'otree_save_the_change': 'otree_save_the_change'},
	package_data={'': ['README.rst', 'HISTORY.rst', 'LICENSE']},
	include_package_data=True,
	install_requires=install_requires,
	zip_safe=False,
	classifiers=(
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.1',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
	),
	test_suite='tests.test.run_tests',
)
