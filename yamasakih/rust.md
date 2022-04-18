Rust が街にやってきた

## 1. イントロダクション
## 1.1 目的
`Rust` のことを知り将来触れる機会があった時に「そういえばこんな話聞いていたな」と参考になれば嬉しいなと思います。  
もちろん明日から `Rustacean` になってもらえたらなお嬉しいです。

### 今日の目標
- `Rust` がどんな言語なのか学ぶ
- インストールから `cargo` コマンドの使い方まで学ぶ
- Python, R と比較しながらどういう実装をすればよいのか学ぶ
- Rust ユニークな特性の一つである型推論を学ぶ

### 1.2. Rust ってどんな言語？
- コンパイラ型
- 謎用語たくさん(あくまで冗談です)
- Stack Overflow アンケートの Rustを好きな理由
  - パフォーマンス、制御、メモリ安全性、並行性に強みを持つこと
  - 興味深い機能を提供すること
  - 開発プロセスがオープンであること

<blockquote class="twitter-tweet" lang="en">
 <a href="https://twitter.com/reibitto/status/1432844799359389705?s=20"></a>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script></blockquote>

:bulb: **キーポイント** :bulb:  
Rust は Python, R と比べて長所があればもちろん短所もあります。
プログラミング言語に優劣はなく「いつ、どこで、どのように使うか」が重要です。

## 2. インストールから Hello world! そして Hello cargo! まで

### 2.1. インストール
```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

で `rustup` がインストールができます。

- `rustup`：`Rust` ツールチェーンインストールやバージョン管理を行う。`rustc`, `cargo` をまとめてインストールしてくれるすごいやつ
  - `rustc` : `Rust` のコンパイラ
  - `cargo` :  `Rust` の*ビルドツール

*ビルド：コンパイルとその周辺処理を合わせてビルドといいます。周辺処理というのは、プログラムの部品となるクレート(ライブラリ)を必要に応じて揃えたり、プログラムが正常に動作するかテストしたりすることです。

:bulb: **キーポイント** :bulb:  
まとめると `rustup` をインストールすればOK！

### 2.2. 計算環境
これ以降は以下の環境で実装を行っていきます。

```sh:rust-tutorial
rust-tutorial
┝ .devcontainer
│ └ devcontainer.json
└ Dockerfile
```

```Dockerfile:rust-tutorial
FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc-multilib \
    curl \
    software-properties-common \
    zsh \
    git

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
ENV PATH $PATH:$HOME/.cargo/bin
```

```json:devcontainer.json
{
    "name": "${localWorkspaceFolderBasename}",
    "build": {
        "dockerfile": "../Dockerfile"
    },
    "settings": {
        "terminal.integrated.defaultProfile.linux": "zsh",
        "terminal.integrated.profiles.linux": {
            "zsh": {
                "path": "/usr/bin/zsh",
                "args": [
                    "-l"
                ]
            }
        },
    },
    "extensions": [
        "matklad.rust-analyzer",
        "vadimcn.vscode-lldb",
    ],
}
```

### 2.3. Hello world!
`hello.rs` という名前でファイルを開き以下のように編集しましょう。

```Rust
fn main() {
    println!("{}", "Hello, world!");
}
```

main 関数は「エントリーポイント」と呼ばれ、 Rust の実行可能ファイルを実行した際に最初に実行される関数です。

続けて `rustc` でコンパイルし実行可能ファイルを作成してみましょう。

```sh
rustc hello.rs
```

最後に実行可能ファイルを実行してみます。

```sh
> ./hello
Hello, world!
```

これで Rust の一連の流れができました！

### 2.4. Hello cargo!
`rustc` を直接実行しコンパイルをしてもよいですが実際のコーディングでは `cargo` コマンドを利用することが多いです。  
`cargo` は様々なサブコマンドを持ち非常に多機能です。

cargo サブコマンド一覧

| サブコマンド | 説明                      |
| ------------ | ------------------------- |
| new          | *プロジェクトの雛形を作る |
| build        | プロジェクトのビルド      |
| run          | プログラムの実行          |
| check        | プログラムの文法チェック  |
| test         | プログラムのテスト        |
| doc          | ドキュメントの生成        |
| publish      | ライブラリを公開          |

*プロジェクト：ライブラリやソフトウェアを指します

`cargo new` を実行してプロジェクトを作成してみましょう。

```sh
cargo new hello_cargo
cd hello_cargo
```

プロジェクトの中には `src/main.rs` というファイルがありこれがコードを実装するメインの場所になります。

```Rust
fn main() {
    println!("{}", "Hello, world!");
}
```

`cargo run` を使うと `rustc` によるコンパイルから実行可能ファイルの起動までまとめて行ってくれます。

```sh
cargo run
```

実行可能ファイルは `target/debug/hello_cargo` という名前で作成されています。
直接実行したい場合は以下のようにします。

```sh
./target/debug/hello_cargo
```

:bulb: **キーポイント** :bulb:  
実務などでコーディングをする時に利用するのは `cargo` です。
`cargo` が `rustc` を呼び出すので直接 `rustc` を実行することはないです。

## 3. Python/R から Rust への準備体操

### 3.1. FizzBuzz を実装してみる
**問題**  
1 から 100 までの数を順に 1 行ずつ出力するプログラムを書いてください。ただし、3 の倍数のときは数の代わりに `Fizz` と、 5 の倍数の時には `Buzz` と表示してください。そして 3 と 5 の倍数の時は `FizzBuzz` と表示してください。

---

<details><summary>Pythonコード例</summary>

```py
for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```
</details>

---

<details><summary>Rコード例</summary>

```r
for (i in 1:100) {
    if ((i %% 3 == 0) && (i %% 5 == 0)) {
        print("FizzBuzz")
    } else if (i %% 3 == 0) {
        print("Fizz")
    } else if (i %% 5 == 0) {
        print("Buzz")
    } else {
        print(i)
    }
}
```
</details>

---

<details><summary>Rustコード例</summary>

```Rust
fn main() {
    for i in 1..101 {
        if i % 3 == 0 && i % 5 == 0 {
            println!("FizzBuzz");
        } else if i % 3 == 0 {
            println!("Fizz");
        } else if i % 5 == 0 {
            println!("Buzz");
        } else {
            println!("{}", i);
        }
    }
}
```
</details>

---

3.2. 型推論
`Rust` は以下のように変数の型を指定する必要はありますが **型推論** という機能があり可能な限り自動で型を判断してくれます。
簡単なコードの場合 Python や R とほぼ同じ感覚でコーディングができます。

```RUST
fn main() {
    let x: i32 = 1024;  // let は変数を宣言する時につける
    let y = 2048;
    println!("{}", x + y);
}
```

:bulb: **キーポイント** :bulb:  
- `println!` という*マクロで標準出力を行えます
- `Rust` は変数の型を指定する必要はありますが **型推論** がよしなにしてくれるため、簡単なコードの場合 Python や R とほぼ同じ感覚でコーディングができます。

*マクロ：非常に長くなる関数などをまとめて省略したもの。 `C++` などにも存在する機能

## 4. Rust は難しい？
### 4.1. 学習が難しいポイント
Rust はいくつか学習が難しいポイントがありそこで挫折してしまうことがあり、そこから習得が難しいというイメージがついていることがあります。

今日は時間の関係上、難しいポイントを解説することはできませんが、どこか難しいかをまとめておくので自身で学習する時にそこで躓いたからと言って「自分に向いてない」と投げ出さずゆっくり進めてもらったらいいなと思います。

- 所有権システム (値渡し、参照渡しをすでに完全理解してたら難しくないかも)
- 構造体・メソッド (JAVAやC++でいうインターフェイスみたいなものです)
- トレイト・ジェネリクス (頭にたくさん？が浮かびます)

### 4.2. ガードレールが多い
Rust はいくつかの機能によって、他の言語ではウヤムヤにできたことを無視せずにコーディングする必要があるためなれないうちはコンパイラーが何度もエラーを出します。これによりイライラしたり難しいと感じたりするのではないかと思います。

これはよくないことのように見えますが安全のためのガードレールにぶつかっている状態であるといえ、コーディング中は見つからなかったが実務で実行したらバグが見つかったというケースが減らすことにつながります。

例) Python でリストの末尾からデータを取り出す

```python
> a = [1, 2, 3]
> a.pop()
3
> b = []
> b.pop()
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
<ipython-input-4-81e119d9eb25> in <module>
----> 1 b.pop()

IndexError: pop from empty list
```

例) Rust でリストに相当する Vector の末尾からデータを取り出す

```Rust
fn main() {
    let mut a = vec![1, 2, 3]; // 可変可能な変数の宣言は let mut とする
    let a_element = a.pop();
    match a_element {
        Some(i) => println!("a = {}", i), // 要素がある場合
        None => println!("There is no element in a"), // 要素がない場合
    }

    let mut b: Vec<i32> = vec![]; // 要素が入ってない場合型推論できないので Vec<i32> と型を指定する
    let b_element = b.pop();
    match b_element {
        Some(i) => println!("b = {}", i),  // 要素がある場合
        None => println!("There is no element in b"), // 要素がない場合
    }

    let mut c = vec![1, 2, 3];
    let c_element = c.pop().unwrap_or(-1); // 要素がない場合 -1 を代入したい
    println!("c = {}", c_element);
}
```

実行結果

```sh
55b98994726f# cargo run 
   Compiling hello_cargo v0.1.0 (/workspaces/mishima.syk.18/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 6.85s
     Running `target/debug/hello_cargo`
a = 3
There is no element in b
c = 3
```

## 5. 様々な分野でのRust

### 5.1. ケモインフォマティクス
化学構造を取り扱うライブラリである RDKit も *FFI にて Rust から利用できるようにした [rdkitcffi](https://github.com/chrissly31415/rdkitcffi) と呼ばれるクレートがあります。

*FFI: Rust から他の言語のコードを利用する機能。逆に他の言語から Rust を利用することも可能。

cf. [Use RDKit from Rust](https://iwatobipen.wordpress.com/2022/01/29/use-rdkit-from-rust-rdkit-rdkitcffi-rust/)

### 5.2. バイオインフォマティクス
[ゲノコン2021 - DNA配列解析チャレンジ](https://atcoder.jp/contests/genocon2021?lang=ja) にて優勝したテリーさんは Rust を使ってコードの実装をしていました。
アルゴリズムとしては焼きなまし法(Simulated annealing)を採用しており、高速に計算できるコンパイラ型のメリットが活かされたのかもしれないです。

cf.
- [テリーさんの提出コード](https://atcoder.jp/contests/genocon2021/submissions/26010960)
- [ゲノコン2021で優勝しました！](https://www.terry-u16.net/entry/genocon2021)

### 5.3. 機械学習
LightGBMなどの機械学習に関するクレート(ライブラリ)が増えつつある。

cf. https://vaaaaaanquish.hatenablog.com/entry/2021/01/23/233113

## 6. まとめ (目標達成チェック)
- `Rust` がどんな言語なのか説明できるようになりました :ballot_box_with_check: 
- インストールから `cargo` コマンドの使い方まで学び以下のコマンドを説明できるようになりました
    - `cargo new` :ballot_box_with_check: 
    - `cargo run`  :ballot_box_with_check: 
- Python, R と比較しながらどういう実装をすればよいのか学び、以下の実装ができるようになりました
    - for 文 :ballot_box_with_check: 
    - if 文 :ballot_box_with_check: 
- Rust 型推論を学び、説明できるようになりました :ballot_box_with_check:

## 7. おすすめの教材
- [The Rust Programming Language 日本語版](https://doc.rust-jp.rs/book-ja/title-page.html)
- [RustCoder ―― AtCoder と Rust で始める競技プログラミング入門](https://zenn.dev/toga/books/rust-atcoder)
- [実践Rustプログラミング入門](https://www.amazon.co.jp/gp/product/B08PF27TRZ/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
- [手を動かして考えればよくわかる 高効率言語 Rust 書きかた・作りかた](https://www.amazon.co.jp/gp/product/4802613512/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
