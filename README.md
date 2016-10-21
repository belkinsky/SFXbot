# SFXbot
A hackday project.
An application to create funny atmosphere among friends by playing funny responses and sounds depending on the words spoken nearby with using voice and sound recognition technologies.

The recognition is based on the following tools and libraries:
  pyAudioAnalisys https://github.com/tyiannak/pyAudioAnalysis
  Sphinx http://cmusphinx.sourceforge.net/

Installation
	
	Download and install whl:
		numpy+mkl
		scipy
	from http://www.lfd.uci.edu/~gohlke/pythonlibs/

	
	Do:
		pip install matplotlib sklearn hmmlearn simplejson eyed3 pygame pyaudio

	Download:
		http://vorboss.dl.sourceforge.net/project/cmusphinx/pocketsphinx/5prealpha/pocketsphinx-5prealpha-win32.zip or the latest version
		Take ru.lm, put in into tools\pocketsphinx\cmusphinx-ru-5.2
	
	Install:
		Visual C++ Redistributable for Visual Studio 2012 Update 4 http://www.microsoft.com/en-us/download/details.aspx?id=30679#