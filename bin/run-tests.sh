#!/usr/bin/env bash

set -xe

pipenv run pytest --cov=oc_wrapper tests/
