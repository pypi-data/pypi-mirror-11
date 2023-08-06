VERSION := ${shell python -c "import BitArray2D;print BitArray2D.__version__"}

default:
	@echo
	@echo "  *** Welcome to BitArray2D ${VERSION} ***"
	@echo
	@echo "  docs   -  Build documentation (html)"
	@echo "  help   -  Open the documentation"
	@echo
	@echo "  clean  -  Remove temporary files"
	@echo "  test   -  Run the unittests"
	@echo "  check  -  Look for rough spots"
	@echo "  sdist  -  Build a source distribution tar ball"

docs:
	pydoc -w BitArray2D

help:
	open BitArray2D.html

clean:
	rm -f *.pyc *~

real-clean: clean
	rm -f MANIFEST  *.html bitarray2d-py.info
	rm -rf build dist

# Run the unittest
test:
	@echo
	@echo Testing...
	@echo
	./TestBitArray2D/Test.py 

sdist: test
	@echo
	@echo Building a source distribution...
	@echo
	./setup.py sdist --formats=gztar,bztar

# Look for rough spots
check:
	@grep -n FIX *.py *.in PKG-INFO Makefile | grep -v grep
	@echo
	pychecker BitArray2D

##############################
# Mac OSX Fink.sf.net package file
#
bitarray2d-py.info: bitarray2d-py.info.in Makefile sdist
	perl -p -e "s/\@VERSION\@/${VERSION}/g" $< > fink.tmp
	MD5=`md5 dist/BitArray2D-${VERSION}.tar.bz2| awk '{print $$4}'` \
	      && perl -p -e "s/\@MD5\@/$$MD5/g" fink.tmp > $@
	rm -f fink.tmp

FINK_TREE := 10.4-transitional
install-fink: bitarray2d-py.info
	sudo cp bitarray2d-py.info /sw/fink/${FINK_TREE}/local/main/finkinfo/libs/
	sudo cp dist/BitArray2D-${VERSION}.tar.bz2 /sw/src/
