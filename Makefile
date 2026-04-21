# Minimal Sphinx Makefile for the dmsAIR documentation site.
#
# Usage:
#   make html            # build docs locally in _build/html
#   make clean           # wipe _build
#   make livehtml        # auto-rebuild on file change (requires sphinx-autobuild)
#   make install-deps    # pip install -r requirements.txt

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR      = .
BUILDDIR       = _build

.PHONY: help html clean livehtml install-deps

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean:
	rm -rf "$(BUILDDIR)"

livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)

install-deps:
	pip install -r requirements.txt
