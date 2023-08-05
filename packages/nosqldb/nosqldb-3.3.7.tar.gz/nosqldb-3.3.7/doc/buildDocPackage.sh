#!/bin/bash

# Make sure our environment makes sense

echo "Testing current location."
if [ ! -f source/index.rst ]
then
    echo "Could not find the index.rst file."
    echo "Make sure you run this script from the kv.python/doc directory."
    exit -1
fi
export clone_dir=`pwd`
echo " "

echo "Testing for ondb.thrift file"
if [ ! $ONDB_THRIFT ]
then
    echo "The ONDB_THRIFT environment variable is not set."
    echo "This environment variable must point to a valid odb.thrift file."
    exit -1
fi
if [ ! -f $ONDB_THRIFT ]
then
    echo "Could not find thrift file at:"
    echo $ONDB_THRIFT
    echo "Is the ONDB.THRIFT environment variable set?"
    exit -1
fi
echo " "

echo "Try to find a thrift compiler. Note that this script doesn't check for the right version."
command -v thrift >/dev/null 2>&1 || { echo >&2 "thrift not found"; exit -1; }

echo " "

echo "Testing for docs_books environment."
if [ ! $DOCS_PDF_BUILDER ]
then
    echo "DOCS_PDF_BUILDER environment variable is not set."
    exit -1
fi

if [ ! -f $DOCS_PDF_BUILDER ]
then
    echo "fop file not found here:"
    echo $DOCS_PDF_BUILDER
    exit -1
fi

if [ ! $DOCS_PARSER ]
then
    echo "DOCS_PARSER environment variable is not set."
    exit -1
fi

if [ ! -f $DOCS_PARSER ]
then
    echo "xsltproc not found here:"
    echo $DOCS_PARSER
    exit -1
fi

if [ ! $DOCS_REPOSITORY ]
then
    echo "DOCS_REPOSITORY environment variable is not set."
    exit -1
fi

if [ ! -d $DOCS_REPOSITORY ]
then
    echo "docs_books clone not found here:"
    echo $DOCS_REPOSITORY
    exit -1
fi

echo "docs_books environment looks okay."
echo " "

# There's a utility script in the docs_books clone
# that we use to help make this package.
driver_util="$DOCS_REPOSITORY/tools/misc_doc_scripts/nosql_driver_util.py"

# get the package name
echo "Get the package name."
pname=`$driver_util -t driver-python -p`

echo "Creating the doc build directory."
rm -rf $pname
mkdir $pname
mkdir $pname/api-reference
export DOCS_TARGET_REPOSITORY="$clone_dir/$pname"
echo $DOCS_TARGET_REPOSITORY

echo " "
echo "Make sure thrift stubs are up-to-date"
echo "(API Reference will not build without this.)"
cd ..
python makethrift.py $ONDB_THRIFT
echo " "

echo "Get the license file."
cp LICENSE.txt $DOCS_TARGET_REPOSITORY

echo "Build the API reference ...."
cd doc
make clean
make html

echo " "
echo "Move the files into place."
cp -r build/html/* $DOCS_TARGET_REPOSITORY/api-reference

echo "Building the Quick Start"
$DOCS_REPOSITORY/tools/buildBooks/buildBooks.py -a -t kvstore_python -h
$DOCS_REPOSITORY/tools/buildBooks/buildBooks.py -a -t kvstore_python -p

echo "Making the doc landing page."

$driver_util -i $clone_dir/index.html \
    -o $clone_dir/$pname -t driver-python



echo "making archive"
archivename="$pname.tar"
echo $archivename
tar cvf $archivename $pname
gzip -f $archivename
archivename="$archivename.gz"
echo " "
echo " "
echo "Archive $archivename created in $clone_dir"

