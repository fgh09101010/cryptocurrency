import subprocess

python_path = "d:/env/Scripts/python.exe"  # 虛擬環境的 Python 路徑

subprocess.run([python_path, "d:/新增資料夾/cryptocurrency/api/coindata/4.py"], check=True)
subprocess.run([python_path, "d:/新增資料夾/cryptocurrency/api/coindata/901.py"], check=True)
subprocess.run([python_path, "d:/新增資料夾/cryptocurrency/api/coindata/1801.py"], check=True)

print("所有腳本執行完畢！")
