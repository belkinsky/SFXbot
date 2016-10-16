set SCRIPT_DIR=%~dp0
pushd %SCRIPT_DIR%

cat %SCRIPT_DIR%\ru.dic | grep -w клей -w привет -w здравствуйте -w кто -w там -w удачи -w приятного -w аппетита -w добрый -w день -w здравствуй -w доброе -w утро -w вечер -w день -w алло -w окей -w гугл -w гугол -w гугль -w три >%SCRIPT_DIR%\stupid_ru.dic