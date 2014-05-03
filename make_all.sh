#!/bin/bash
set -x
rm external/* -rf && \
cd external && \
git clone https://github.com/eliben/pycparser.git && \
cd -
