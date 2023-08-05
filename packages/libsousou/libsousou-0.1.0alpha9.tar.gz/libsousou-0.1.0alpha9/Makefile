# vim: noexpandtab:syntax=make
CWD	=$(shell pwd)
PYTHON =python3
PYTHON_LIB_DIR =`$(PYTHON) -c "import site;print(site.getsitepackages()[0])"`
PYTHON_MODULE_NAME=libsousou
VCS_COMMIT=git commit
VCS_URI=git@github.com:sousouindustries/libsousou.git
VCS_USER=Sousou Industries
VCS_EMAIL=operations@sousouindustries.com


builddeb:
	dpkg-buildpackage -b -i -I -rfakeroot


clean:
	@find . | grep -E "(__pycache__|\.pyc$\)" | xargs rm -rf
	@rm -rf dist build
	@rm -rf *.egg-info
	@rm -rf ../*.orig.tar.gz
	@rm -rf *.egg-info


commit:
	make clean
	make coverage
	$(VCS_COMMIT)


coverage:
	./run_tests -x


install-development-deps:
	pip3 install coverage nose pylint sphinx sphinxcontrib-napoleon==0.2.11\
		sphinx_rtd_theme==0.1.6 nose-cov

links:
	@make purge
	@ln -s $(CWD)/$(PYTHON_MODULE_NAME) $(PYTHON_LIB_DIR)/$(PYTHON_MODULE_NAME)


publish:
	$(PYTHON) setup.py register
	$(PYTHON) setup.py sdist upload


purge:
	@rm -rf $(PYTHON_LIB_DIR)/$(PYTHON_MODULE_NAME)


reset-repo:
	@rm -rf .git
	@make clean
	@git init
	@git add .
	@git config user.name $(VCS_USER)
	@git config user.email $(VCS_EMAIL)
	@git commit -m "Initial commit"
	@git remote add github $(VCS_URI)
	@git push -u --force github master
