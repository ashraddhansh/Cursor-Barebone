from functions.get_files_info import get_files_info


case_1 = [
            ("calculator", "."),
 """- main.py: file_size=576 bytes, is_dir=False
 - tests.py: file_size=1343 bytes, is_dir=False
 - pkg: file_size=92 bytes, is_dir=True"""
]

case_2 = [
        ("calculator","pkg"),
 """- calculator.py: file_size=1739 bytes, is_dir=False
 - render.py: file_size=768 bytes, is_dir=False
 - __pycache__: file_size=96 bytes, is_dir=True"""
]

case_3 = [
        ("calculator","/bin"),
        """Error: Cannot list "/bin" as it is outside the permitted working directory"""
]

case_4 = [
        ("calculator", "../"),
        """Error: Cannot list "../" as it is outside the permitted working directory"""
        ]

all_cases = [case_1, case_2, case_3, case_4]
passed = 0
failed = 0
for case in all_cases:
    actual = get_files_info(case[0][0],case[0][1])
    expected = case[1]
    print(f"Actual\n {actual}")
    print(f"Expected\n {expected}")
    if actual == expected:
        passed += 1
    else:
        failed +=1
print(f"total passed: {passed}, total failed: {failed}")
