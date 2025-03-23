# PythonをJavaに準えてサクッとざっくり把握したい
Javaはわかるという方が10分程度で把握できるくらいの内容です。

## 参考
- [Python 公式ドキュメント](https://www.python.org/)
- [BeginnersGuide](https://wiki.python.org/moin/BeginnersGuide/Programmers)
- [Python チュートリアル](https://docs.python.org/ja/3/tutorial/index.html)

## JVM
インタプリタ

## アクセス修飾子
厳密なアクセス修飾子はなし。
変数名に_(protected)や__(private)を付与して表現する慣習がある。
変数へのアクセスを制限できるわけではない。

## 文末 ;(セミコロン)
改行

## コメント //
```py
# コメントです
```

## ブロックコメント /* ... */
なし

## Javadoc コメント /** ... */
ダブルクォーテーションまたはシングルクォーテーション3個で囲んで記述するdocstringがある。  
記述場所はクラスや関数の前ではなく、後。
```py
def add(a, b):
    """
    aとbを加算した結果を返却します
    複数行で記述できます
    """
    return a + b
```

## public static void main

```py
if __name__ == "__main__":
    # ここに処理を記述
    print('Hello World')
```

## コードブロック {} (波括弧、ブレース)
:(コロン) + 改行 + インデント(半角スペース4個推奨)によりコードブロックを開始し、  
インデントの終了によりコードブロックの終了を表す。

```py
def my_function():
    print("This is my function")

def my_function2():
    print("This is my function")
```

## 型
基本的な型名で異なるのは以下。
| Java | Python |
|---|---|
|String|str|
|boolean|bool|

また、文字列はシングルクォート、ダブルクォートどちらでも定義できる。
```py
str = '文字列です'
str_2 = "文字列2です"
```

boolはTrue,Falseと頭が大文字になる。
```py
bool = True
bool_2 = False
```

## 変数定義
Javaが静的型付け言語で変数の型を宣言するのに対し、
動的型付け言語のため変数の型は宣言しない。
```py
my_number = 10
print(my_number)
```
また、変数名はスネークケース推奨。

## if
```py
if x > 0:
    print("xは正の数です")
elif x < 0:
    print("xは負の数です")
else:
    print("xは0です")
```

## &&, ||, !
and, or, not
```py
if a == b and b == c:
    # 処理

if a == 1 or b == 2:
    # 処理

if not (c == 3):
    # 処理
```

## for
- 構文
```py
for 要素 in イテラブルオブジェクト:
    繰り返す処理
```
- 例
```py
numbers = [1, 3, 4, 5, 6, 9]
for number in numbers:
    print(number)
```

## メソッド
Classに属する関数で、selfを第一引数にとる。
```py
def メソッド名(self, 引数リスト):
    # メソッドの処理
    return 戻り値
```

クラスに属さない独立した関数もある。
```py
def 関数名(引数リスト):
    # 関数の処理
    return 戻り値
```

### 戻り値
戻り値の宣言は不要。returnするだけ。
```py
def add(a, b):
    return a + b
```
明示的に宣言することもできる。
```py
def add(a, b) -> int:
    return a + b
```

### 引数の型
引数も戻り値同様に宣言は不要。明示的に宣言もできる。
```py
def add(a: int, b: int) -> int:
    return a + b
```

### void
戻り値のないメソッドはretrun不要。
```py
def test():
    print('test')
```

## Exception 構文
catchではなく、except,else。
```py
try:
    # 例外が発生する可能性のあるコード
except 例外タイプ1:
    # 例外タイプ1が発生した場合の処理
except 例外タイプ2:
    # 例外タイプ2が発生した場合の処理
else:
    # 例外が発生しなかった場合の処理
finally:
    # 例外の有無に関わらず実行される処理
```
## 以下はまたの機会に。
## List
## Map
## Package
## Import
## Class
## Extends
## オーバーライド
## Interface
## オーバーロード