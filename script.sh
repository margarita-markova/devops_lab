#!/bin/bash

for i in {2..3}; do
	if pyenv versions | grep ${i}.7.1; then
		echo "${i}.7 version already installed"
	else
		pyenv install ${i}.7.1
	fi
	pyenv virtualenv ${i}.7.1 venv${i}71
	pyenv activate venv${i}71
	python -c "print('It works!')"
done

