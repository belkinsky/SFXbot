set SCRIPT_DIR=%~dp0
pushd %SCRIPT_DIR%

cat %SCRIPT_DIR%\ru.dic | grep -w ���� -w ������ -w ������������ -w ��� -w ��� -w ����� -w ��������� -w �������� -w ������ -w ���� -w ���������� -w ������ -w ���� -w ����� -w ���� -w ���� -w ���� -w ���� -w ����� -w ����� -w ��� >%SCRIPT_DIR%\stupid_ru.dic