Financial Modeling Prep (FMP) のAPIサンプルコード
==

Install
--

1. [FMP](https://site.financialmodelingprep.com/) にサインアップ/サインインします．
1. "Dashboard" から APIKEY をコピーし、sample.envに貼り付けます.
1. ファイル名を sample.env から .env にします．
1. ターミナル(WindowsはUbuntu推奨)でこのディレクトリを開き，以下のコマンドで仮想環境を作成します．
    ```bash
    python3 -m venv .venv
    ```
1. 以下のコマンドで仮想環境に入ります．
    ```bash
    source .venv/bin/activate
    ```
1. コマンドラインに(.venv)とついていることを確認し，以下のコマンドで必要なPythonパッケージをダウンロードします．
    ```bash
    pip install -r requirements.txt
    ```

以上で準備は完了です．

References
--

src/main.py 
--
**FMPから各セクタの，過去2年分の株価変化率（日次リターン）を取得しCSVに保存します．**

注）APIは無料枠だと 250 call/day です．
1セクタ 1call なので，実行毎に 11call 消費します．

実験では再現性が重要です．
csvの末尾に時間のラベルを付けることで，誤ってファイルを上書きしないようにしています．

scripts/plot.py
--
**csvをプロットします．**

注）実行前に main.py で取得したcsvのファイル名を CSV_PATH の適切な箇所にコピペしましょう．


Notes
--
セクタは世界産業分類基準（Global Industry Classification Standard，GICS）に基づくらしいですが，完全準拠ではないそうです（ChatGPTが言うには）．

色々いじってみて下さい．