import datetime
import glob
import json
import os
import re
from pprint import pprint
import twitter
import config

# 認証の情報
t = twitter.Twitter(auth=config.APIKEY)


# データ初期化
data_dict = {"home_tl": 0, "mention_tl": 0}

# エラーメッセージ格納用のリスト
warning_list = []

### 開始メッセージ ###
print("セットアップを開始します。")


### rnd_*.txt関係のセットアップ ###
# 同ディレクトリ内のrnd_*.txtの条件に当てはまるファイルのリストを作成
rnd_data_list = [os.path.basename(p) for p in glob.glob(os.path.dirname(__file__) + os.sep + "rnd_*.txt") if os.path.isfile(p)]

# rnd_*.txtじゃないものが0じゃないなら
if len(rnd_data_list) != 0: 
    # セットアップ開始のメッセージ
    print("\n\n*-*-*-*-*-*-*-*-*-*-*")
    print("ランダムにツイートさせる機能のセットアップを開始します。")

    # ファイル巡回開始
    for i in rnd_data_list:
        rnd_data_path = os.path.join(os.path.dirname(__file__), i)

        # 巡回対象のファイルを表示
        print("\nチェック対象: " + str(i))

        # ファイル展開
        with open(rnd_data_path, "r", encoding="utf-8") as f:
            text_list = f.readlines()

        # 空白のファイルではないかを判断
        if len(text_list) == 0:
            print("**" + str(i) + " は空白のファイルです！データを入力してからもう一度セットアップを開始してください。**")
            input("何かキーを押して終了。")
            os._exit(1)

        # 文字数チェック
        for j in text_list:
            if len(j) >= 141:
                warning_list.append(str(i) + "の「 " + str(j) + " 」\nが141字以上の可能性があります。")
        else:
            print(str(i) + " のチェック完了。")
    
    else:
        # チェック終了のメッセージ
        print("\nセットアップ完了。")


### ord_*.txt関係のセットアップ ###
# 同ディレクトリ内のord_*.txtの条件に当てはまるファイルのリストを作成
ord_data_list = [os.path.basename(p) for p in glob.glob(os.path.dirname(__file__) + os.sep + "ord_*.txt") if os.path.isfile(p)]

# ord_*.txtが0じゃないなら
if len(ord_data_list) != 0: 
    # セットアップ開始のメッセージとゼロオリジンじゃないことの注意書き
    print("\n\n*-*-*-*-*-*-*-*-*-*-*")
    print("順番にツイートさせる機能のセットアップを開始します。\n" +
        "注意:" "\t最初の行は1行目として指定してください。" +
        "\n\t空白の場合は先頭から開始されます。")

    # 何行目から始めるか聞く
    for i in ord_data_list:
        # データの行数を取得
        ord_data_path = os.path.join(os.path.dirname(__file__), i)
        with open(ord_data_path, "r", encoding="utf-8") as f:
            text_list = f.readlines()

        # 空白のファイルではないかを判断
        if len(text_list) == 0:
            print("\n**" + str(i) + " は空白のファイルです！データを入力してからもう一度セットアップを開始してください。**")
            input("何かキーを押して終了。")
            os._exit(1)

        # 正常な値が入るまで無限ループ(神奈川県警と兵庫県警には通報しないでください。)
        while True:
            print("\n" + str(i) + " のデータは何行目から始めますか？")
            ord_num = input(">> ")

            # 空白ならば1に変換
            if not ord_num:
                ord_num = "1"

            # 正常な値かを判別
            if ord_num.isdecimal():
                if 1 <= int(ord_num)  <= len(text_list):
                    data_dict[i] = int(ord_num)
                    data_dict[i] -= 1

                    # 文字数チェック
                    for j in text_list:
                        if len(j) >= 141:
                            warning_list.append(str(i) + "の「 " + str(j) + " 」\nが141字以上の可能性があります。")
                    
                    break

                else:
                    print("**指定された行数がファイルの行数の範囲を超えています。**")
            else:
                print("**数字を入力して下さい。**")
        
        print(str(i) + " のチェック完了。")

    print("\nセットアップ完了。")


### rep_*.json関係のセットアップ ###
# 同ディレクトリ内のrep_*.jsonの条件に当てはまるファイルのリストを作成
rep_data_list = [os.path.basename(p) for p in glob.glob(os.path.dirname(__file__) + os.sep + "rep_*.json") if os.path.isfile(p)]

# rep_*.jsonじゃないものが0じゃないなら
if len(rep_data_list) != 0: 
    # セットアップ開始のメッセージ
    print("\n\n*-*-*-*-*-*-*-*-*-*-*")
    print("リプライ機能のセットアップを行います。")

    # ファイル巡回開始
    for i in rep_data_list:
        rep_data_path = os.path.join(os.path.dirname(__file__), i)

        # 巡回対象のファイルを表示
        print("\nチェック対象: " + str(i))

        # ファイル展開と同時に空ではないかを確認
        try:
            with open(rep_data_path, "r", encoding="utf-8") as f:
                text_dic = json.load(f)
        except json.JSONDecodeError as e:
            print(str(e) + " 展開中にエラー発生。")
            print("**" + str(i) + " は入力に不備がある可能性があります。データを確認してからもう一度セットアップを開始してください。**")
            input("何かキーを押して終了。")
            os._exit(1)

        # 文字数チェック
        for j in text_dic:
            try:
                test_pattern = re.compile(repr(j))
            except re.error:
                warning_list.append(str(i) + "の「 " + str(j) + "  」\nは正規表現の記法に不備がある可能性があります。データを確認してからもう一度セットアップを開始してください。")

            for k in text_dic[j]:
                if len(k) >= 124:
                    warning_list.append(str(i) + "の「 " + str(k) + " 」\nが124字以上の可能性があります。\nさらに、{{screen_name}}が含まれる場合は相手のIDの長さによっては送信できない場合があります。")
        else:
            print(str(i) + " のチェック完了。")
    
    else:
        # チェック終了のメッセージ
        print("\nセットアップ完了。")


### Tweet_ID関係のセットアップ ###
print("\n\n*-*-*-*-*-*-*-*-*-*-*")
print("各種Tweet_IDの取得開始。")

# TLの最新IDのデータ取得
get_home = t.statuses.home_timeline(count=5)
data_dict["home_tl"] = get_home[0]["id"]

# mentionの最新IDのデータ取得
get_mention = t.statuses.mentions_timeline(count=5)
data_dict["mention_tl"] = get_mention[0]["id"]

print("各種Tweet_IDの取得完了。")


### 各種取得したデータの書き込み ###
print("\n\n*-*-*-*-*-*-*-*-*-*-*")
print("データ記録開始")

data_path = os.path.join(os.path.dirname(__file__), "data.json")
with open(data_path, "w", encoding="utf-8") as f:
    json.dump(data_dict, f)

print("全データ記録完了。")





### 終了メッセージ  ###
dt_now = datetime.datetime.now()
print("\n\n*-*-*-*-*-*-*-*-*-*-*")
print("==全セットアップ終了==")

if len(warning_list) != 0 :
    with open (os.path.dirname(__file__) + os.sep + "warning_log.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(warning_list))
    print("-*-警告を warning_log.txt に出力しました。-*-")

print(str(dt_now + datetime.timedelta(minutes=1)) + "以降に起動して下さい")
input("何かキーを押して終了")
