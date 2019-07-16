import datetime
import random
import re
import json
import os
import twitter
import config


# 認証の情報
t = twitter.Twitter(auth=config.APIKEY)


### 便利ツール ###
# 特定の文字列を置換
def replace_string(text, screen_name=""):
    dt_now = datetime.datetime.now()
    month = dt_now.strftime("%m")
    date = dt_now.strftime("%d") 
    hour = dt_now.strftime("%H")
    minute = dt_now.strftime("%M")

    replaced_text = (text\
    .replace("\\n","\n")\
    .replace("{screen_name}", screen_name)\
    .replace("{month}", month)\
    .replace("{date}", date)\
    .replace("{hour}", hour)\
    .replace("{minute}", minute))

    return replaced_text

# データ読み込み
def read_data(data_name):
    data_path = os.path.join(os.path.dirname(__file__), "data.json")

    with open(data_path, "r", encoding="utf-8") as f:
        return_data = json.load(f)[str(data_name)]
    
    return return_data

# データ書き込み
def write_data(data_name, value):
    data_path = os.path.join(os.path.dirname(__file__), "data.json")

    with open(data_path, "r", encoding="utf-8") as f:
        writing_data = json.load(f)

    writing_data[str(data_name)] = int(value)

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(writing_data, f)

# パターンファイル読み込み
def read_pattern(mode, pattern_file_name):
    data_path = os.path.join(os.path.dirname(__file__), str(pattern_file_name))

    if mode == "txt":
        with open(data_path, "r", encoding="utf-8") as f:
            pattern = f.readlines()
    
    elif mode == "json":
        with open(data_path, "r", encoding="utf-8") as f:
            pattern = json.load(f)   

    else:
        print("要モード指定")
        os.exit()

    return pattern


### データ取得・記録 ###
def fetch_timelines():
    global home_tl
    home_tl = t.statuses.home_timeline(count=200)

    global mention_tl
    mention_tl = t.statuses.mentions_timeline(count=200)

def write_last_ids():
    if len(home_tl) != 0:
        write_data("home_tl", home_tl[0]["id"])

    if len(mention_tl) != 0:
        write_data("mention_tl", mention_tl[0]["id"])


###ツイートに必要な関数###
# テキストをランダムにツイートする
def tweet_random(file_name):
    # パターン読み込み
    text_list = read_pattern(mode="txt", pattern_file_name=file_name)

    # ツイート生成
    text = random.choice(text_list)

    # 文字列置換
    tweet = replace_string(text)

    # ツイート送信
    t.statuses.update(status=str(tweet))


# テキストを順番にツイートする(デフォルトではループ)
def tweet_order(file_name, mode="loop"):
    # パターン読み込み
    text_list = read_pattern(mode="txt", pattern_file_name=file_name)

    # どこまでツイートしたか復元
    ord_num = read_data(file_name)

    # ループモードかつ最終行なら最初に戻す
    if (mode == "loop" and ord_num == len(text_list)):
            ord_num = 0       
    else:
        pass
    
    # 一回のみのモードかつ最終行ならツイートしない
    if (mode == "once" and ord_num == len(text_list)):
        return 0
    else:
        pass

    # ツイート生成
    text = text_list[ord_num]
    # 文字列置換
    tweet = replace_string(text)
    # ツイート
    t.statuses.update(status=str(tweet))

    # どこまでツイートしたか記録
    ord_num += 1
    write_data(file_name, ord_num)


# リプライへの返信
def reply_mention(file_name):
    # リプライが1個以上なら返信作成開始
    if len(mention_tl) != 0:
            
        # パターンファイル展開
        reply_pattern = read_pattern(mode="json", pattern_file_name=file_name)

        # 最後に返信したIDの復元
        last_id = read_data("mention_tl")

        # パターンと照合
        for i in mention_tl:
            
            # 対象のツイートIDが最後に記録したIDより大きければ、処理開始
            if i["id"] > last_id:

                for j in reply_pattern:
                    result = re.search(j, repr(re.escape(i["text"])))

                    # 合致するパターンを見つけるかパターンファイルの最後までループ
                    if result is None:
                        pass

                    else:
                        # 一致した場合ツイート生成
                        text = random.choice(reply_pattern[j])

                        # リプライを返さないパターンの判別
                        if text != config.END_PATTERN:
                            # リプライに必要な情報収集
                            tweet_id = i["id"]
                            screen_name = i["user"]["screen_name"]

                            # 文頭にScreen_Name付加および、文字列置換
                            sc_text = ("@" + screen_name + " " + text)
                            tweet = replace_string(sc_text, str(screen_name))

                            # ポスト
                            t.statuses.update(status=tweet,in_reply_to_status_id=tweet_id)
                            break
                        else:
                            # リプライに必要な情報収集
                            break
                else:
                    # 全パターン不一致時のツイート生成
                        text = random.choice(reply_pattern["(?!.*)"])

                        # リプライを返さないパターンの判別
                        if text != config.END_PATTERN:
                            # リプライに必要な情報収集
                            tweet_id = i["id"]
                            screen_name = i["user"]["screen_name"]

                            # 文頭にScreen_Name付加および、文字列置換
                            sc_text = ("@" + screen_name + " " + text)
                            tweet = replace_string(sc_text, str(screen_name))

                            # ポスト
                            t.statuses.update(status=tweet,in_reply_to_status_id=tweet_id)
                        else:
                            pass
            
            else:
                break


# TLへの反応リプライ
def reply_home(file_name):
    # リプライ対象が1個以上なら返信作成開始
    if len(home_tl) != 0:
        
        # パターン読み込み
        reply_pattern = read_pattern(mode="json", pattern_file_name=file_name)

        # 最後に返信したIDの復元
        last_id = read_data("home_tl")

        # ツイートへの処理開始
        for i in home_tl:
            # 対象のツイートIDが最後に記録したIDより大きければ、処理開始
            if i["id"] > last_id:
                # 自身のツイート及びRT、他ユーザーへのMentionを除外
                if (i["user"]["screen_name"]).lower() == config.MY_ID.lower():
                    pass
                
                elif re.search(r"RT @(.+)|@\w+|＠\w+", repr(i["text"])) is None:
                    # パターンと照合
                    for j in reply_pattern:
                        result = re.search(j, repr(re.escape(i["text"])))

                        # 合致するパターンを見つけるかパターンファイルの最後までループ
                        if result is None:
                            pass
                        
                        else:
                            # 一致した場合ツイート生成
                            text = random.choice(reply_pattern[j])
                            # リプライに必要な情報収集
                            tweet_id = i["id"]
                            screen_name = i["user"]["screen_name"]

                            # 文頭にScreen_Name付加および、文字列置換
                            sc_text = ("@" + screen_name + " " + text)
                            tweet = replace_string(sc_text, str(screen_name))

                            # ポスト
                            t.statuses.update(status=tweet,in_reply_to_status_id=tweet_id)
                            break

                else:
                    pass

            else:
                break

