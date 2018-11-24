#!/bin/bash

python -m pytest
if [[ $? != 0 ]];
then
	exit $?;
fi

echo "Running mypy..."
mypy ./mmillion/rules.py
