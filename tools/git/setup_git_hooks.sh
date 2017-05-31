#! /bin/bash


HOOK_SRC_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

FLAKE8=`which flake8`
if [ ! $FLAKE8 ]
then
    echo "Couldn't install git hooks: flake8 was not found on the path."
    echo
    echo "Ensure you have flake8 installed and have the following versions:"
    echo '$ flake8 --version'
    echo "2.5.1 (pep8: 1.7.0, pyflakes: 1.0.0, mccabe: 0.4.0) CPython 2.7.13 on Darwin"
    echo
    exit 1
fi

rm -f  $HOME/.config/flake8

rm -f $HOOK_SRC_DIR/../../.git/hooks/pre-commit
ln -fs ../../tools/git/pre_commit.py $HOOK_SRC_DIR/../../.git/hooks/pre-commit
