# check running programs
echo "--- node -----------------------"
ps aux | grep node | grep -v grep
echo
echo "--- julius ---------------------"
ps aux | grep julius | grep -v grep
echo
echo "--- python ---------------------"
ps aux | grep python | grep -v grep

