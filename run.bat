set SCRIPT_DIR=%~dp0
pushd %SCRIPT_DIR%

start %SCRIPT_DIR%\tools\pocketsphinx\pocketsphinx_continuous_RU.bat 
	
python src\voiceRecorder.py svm
::python src\voiceRecorder.py knn
::python src\voiceRecorder.py randomforest
::python src\voiceRecorder.py gradientboosting
::python src\voiceRecorder.py extratrees
