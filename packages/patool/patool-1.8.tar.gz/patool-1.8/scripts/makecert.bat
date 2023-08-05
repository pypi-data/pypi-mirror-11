:: run this in a windows sdk command shell
set NAME=%1
makecert.exe -r -pe -n "CN=%NAME% certificate" -b 01/01/2011 -e 01/01/2021 -eku 1.3.6.1.5.5.7.3.3 -sv %NAME%.pvk %NAME%.cer
pvk2pfx.exe -pvk %NAME%.pvk -spc %NAME%.cer -pfx %NAME%.pfx
