@echo #######################SVM########################

python src\testClassifierModel.py svm data\sample\new-2016-10-16-knocking-16k.wav 
python src\testClassifierModel.py svm data\sample\42_das_shvatz_blat_papier.wav
python src\testClassifierModel.py svm data\sample\new43_das_shvatz_blat_papier.wav
python src\testClassifierModel.py svm data\sample\priyantogo_appetita_16k_10.wav
python src\testClassifierModel.py svm data\sample\priyantogo_appetita_16k_09.wav
python src\testClassifierModel.py svm data\sample\unexpected.wav

@echo.
@echo.
@echo.
@echo #######################KNN########################

python src\testClassifierModel.py knn data\sample\new-2016-10-16-knocking-16k.wav 
python src\testClassifierModel.py knn data\sample\42_das_shvatz_blat_papier.wav
python src\testClassifierModel.py knn data\sample\new43_das_shvatz_blat_papier.wav
python src\testClassifierModel.py knn data\sample\priyantogo_appetita_16k_10.wav
python src\testClassifierModel.py knn data\sample\priyantogo_appetita_16k_09.wav
python src\testClassifierModel.py knn data\sample\unexpected.wav

@echo.
@echo.
@echo.
@echo #######################randomforest########################

python src\testClassifierModel.py randomforest data\sample\new-2016-10-16-knocking-16k.wav 
python src\testClassifierModel.py randomforest data\sample\42_das_shvatz_blat_papier.wav
python src\testClassifierModel.py randomforest data\sample\new43_das_shvatz_blat_papier.wav
python src\testClassifierModel.py randomforest data\sample\priyantogo_appetita_16k_10.wav
python src\testClassifierModel.py randomforest data\sample\priyantogo_appetita_16k_09.wav
python src\testClassifierModel.py randomforest data\sample\unexpected.wav

@echo.
@echo.
@echo.
@echo ########################gradientboosting#######################

python src\testClassifierModel.py gradientboosting data\sample\new-2016-10-16-knocking-16k.wav 
python src\testClassifierModel.py gradientboosting data\sample\42_das_shvatz_blat_papier.wav
python src\testClassifierModel.py gradientboosting data\sample\new43_das_shvatz_blat_papier.wav
python src\testClassifierModel.py gradientboosting data\sample\priyantogo_appetita_16k_10.wav
python src\testClassifierModel.py gradientboosting data\sample\priyantogo_appetita_16k_09.wav
python src\testClassifierModel.py gradientboosting data\sample\unexpected.wav

@echo.
@echo.
@echo.
@echo ########################extratrees#######################

python src\testClassifierModel.py extratrees data\sample\new-2016-10-16-knocking-16k.wav 
python src\testClassifierModel.py extratrees data\sample\42_das_shvatz_blat_papier.wav
python src\testClassifierModel.py extratrees data\sample\new43_das_shvatz_blat_papier.wav
python src\testClassifierModel.py extratrees data\sample\priyantogo_appetita_16k_10.wav
python src\testClassifierModel.py extratrees data\sample\priyantogo_appetita_16k_09.wav
python src\testClassifierModel.py extratrees data\sample\unexpected.wav
