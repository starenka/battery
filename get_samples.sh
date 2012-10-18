#!/bin/sh

mkdir -p samples/dl
cd samples/dl
wget -r -l4 --no-parent -A.rar http://samples.kb6.de/downloads_en.php
find . -name '*.rar' -exec rar x {} \;
rm -rf samples.kb6.de