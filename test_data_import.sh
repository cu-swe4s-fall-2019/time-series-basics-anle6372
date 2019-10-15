conda install pycodestyle

test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test2 pycodestyle test_data_import.py
assert_no_stdout
assert_no_stderr

run test3 pycodestyle data_import.py
assert_no_stdout
assert_no_stderr