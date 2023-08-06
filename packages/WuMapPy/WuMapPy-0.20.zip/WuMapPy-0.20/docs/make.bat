@ECHO OFF

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set INITIALDIR=%cd%
set BUILDDIR=_build
set DUPLICDIR=..\wumappy\help
set ALLSPHINXOPTS=-d %BUILDDIR%/doctrees %SPHINXOPTS% .
if NOT "%PAPER%" == "" (
	set ALLSPHINXOPTS=-D latex_paper_size=%PAPER% %ALLSPHINXOPTS%
)

if "%1" == "" goto help

if "%1" == "help" (
	:help
	echo.Please use `make ^<target^>` where ^<target^> is one of
	echo.  html       to make standalone HTML files
	echo.  latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter
	goto end
)

if "%1" == "clean" (
	for /d %%i in (%BUILDDIR%\*) do rmdir /q /s %%i
	del /q /s %BUILDDIR%\*
	goto end
)

if "%1" == "html" (
	%SPHINXBUILD% -b html %ALLSPHINXOPTS% %BUILDDIR%/html
	echo.
        xcopy /Y /S %BUILDDIR%\html\* %DUPLICDIR%\html\
	echo.Build finished. The HTML pages are in %BUILDDIR%/html,
        echo.and duplicated in %DUPLICDIR%\html
	goto end
)

if "%1" == "latex" (
	%SPHINXBUILD% -b latex %ALLSPHINXOPTS% %BUILDDIR%/latex
	echo.
	echo.Build finished; the LaTeX files are in %BUILDDIR%/latex.
	goto end
)

if "%1" == "pdf" (
	%SPHINXBUILD% -b latex %ALLSPHINXOPTS% %BUILDDIR%/latex	
	echo.
	echo.Build finished; the LaTeX files are in %BUILDDIR%/latex.
        cd %BUILDDIR%\latex\
	pdflatex.exe WuMapPy.tex
        cd %INITIALDIR%
        xcopy /Y /S %BUILDDIR%\latex\WuMapPy.pdf %DUPLICDIR%\pdf\

	goto end
)

:end
