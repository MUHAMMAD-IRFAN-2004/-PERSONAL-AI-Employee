@echo off
echo ========================================
echo Social Poster Debug Mode
echo ========================================
echo.
echo This will run social_poster.py with detailed error information
echo.
pause

python social_poster.py 2>&1 | tee debug_output.log

echo.
echo ========================================
echo Output saved to: debug_output.log
echo ========================================
echo.
pause
