# how to use this package from your laptop

まずtokenを環境変数に書き込む．環境変数の保持はあくまで一時的？
ちなみに，今回のtokenは2025.12.09まで有効．
```
PS C:\Users\uikur\Documents\ikz\research\experiments\202506_NLcoeff> $env:GITHUB_TOKEN="github_pat_xxxyyyzzz"
```
次にpip install でアクセス．
```
PS C:\Users\uikur\Documents\ikz\research\experiments\202506_NLcoeff> pip install "git+https://${GITHUB_TOKEN}@github.com/ui-kurodai/202508_crystal_database.git@main"
```
```
Collecting git+https://****@github.com/ui-kurodai/202508_crystal_database.git@main
  Cloning https://****@github.com/ui-kurodai/202508_crystal_database.git (to revision main) to c:\users\uikur\appdata\local\temp\pip-req-build-b_x6mek2
  Running command git clone --filter=blob:none --quiet 'https://****@github.com/ui-kurodai/202508_crystal_database.git' 'C:\Users\uikur\AppData\Local\Temp\pip-req-build-b_x6mek2'
  Resolved https://****@github.com/ui-kurodai/202508_crystal_database.git to commit e  Building wheel for crystaldatabase (pyproject.toml) ... done
  Created wheel for crystaldatabase: filename=crystaldatabase-0.1-py3-none-any.whl size=3494 sha256=c0e4906d3a1c084bebc0d1a18768a1799446d6a1a8d7590727459bdc59823f62      
  Stored in directory: C:\Users\uikur\AppData\Local\Temp\pip-ephem-wheel-cache-5cpenxwq\wheels\63\cb\cb\1f768e67f8b9d75e1f63c0aa0bfdbfe80c020f361c5958ac16
Successfully built crystaldatabase
Installing collected packages: crystaldatabase
Successfully installed crystaldatabase-0.1

[notice] A new release of pip is available: 24.3.1 -> 25.2
[notice] To update, run: python.exe -m pip install --upgrade pip
PS C:\Users\uikur\Documents\ikz\research\experiments\202506_NLcoeff>
```