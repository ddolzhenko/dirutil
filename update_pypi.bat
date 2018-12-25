rem @echo off
@echo Continue?
@pause
twine upload --repository testpypi dist/*
@pause
twine upload --repository pypi dist/* 
@pause
