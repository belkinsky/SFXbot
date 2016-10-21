# SFXbot
A hackday project.
An application to create funny atmosphere among friends by playing funny responses and sounds depending on the words spoken nearby with using voice and sound recognition technologies.

The recognition is based on the following tools and libraries:
  - pyAudioAnalisys https://github.com/tyiannak/pyAudioAnalysis
  - Sphinx http://cmusphinx.sourceforge.net/

## Installation
Tested on Windows.
 - [x] Python 3.5
 - [ ] Download and install .whl packages from here (http://www.lfd.uci.edu/~gohlke/pythonlibs/):
	- numpy+mkl
	- scipy
	```
	pip install <package-name>.whl
	```
 - [ ] Install the following packages:
	```
	pip install matplotlib sklearn hmmlearn simplejson eyed3 pygame pyaudio
	```
 - [ ] Download Sphinx dictionary from here (http://vorboss.dl.sourceforge.net/project/cmusphinx/pocketsphinx/5prealpha/pocketsphinx-5prealpha-win32.zip).
	Take `ru.lm`, put in into `tools\pocketsphinx\cmusphinx-ru-5.2`
 - [ ]	Download and install Visual C++ Redistributable for Visual Studio 2012.
	It is required by Sphinx. (http://www.microsoft.com/en-us/download/details.aspx?id=30679#)
		
## Usage
```
train.bat
```

```
run.bat
```

Currently audio analysis doesn't work. Only speech recognition is used.
