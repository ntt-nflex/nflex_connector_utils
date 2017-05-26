#!/bin/bash

while true
do
    fswatch -o .. | make html
done
