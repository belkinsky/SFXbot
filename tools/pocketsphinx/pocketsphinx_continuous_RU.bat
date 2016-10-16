set SCRIPT_DIR=%~dp0
set DATA_DIR=%SCRIPT_DIR%\..\..\data
pushd %SCRIPT_DIR%

set PARAMS=-bestpath no -fwdflatsfwin 1 -kws_delay 1 -vad_startspeech 2 -vad_postspeech 5 -vad_prespeech 2 -remove_noise no -debug 1

pocketsphinx_continuous.exe -inmic yes %PARAMS% -hmm cmusphinx-ru-5.2 -lm cmusphinx-ru-5.2\ru.lm -dict cmusphinx-ru-5.2\stupid_ru.dic  2>"%DATA_DIR%\sphinx_log" 1>"%DATA_DIR%\sphinx_speech"