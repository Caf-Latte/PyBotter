import twitter
import datetime, random, re, json, os
import config, text_ord, text_rand, re_pat_home, re_pat_ment

# 認証の情報
t = twitter.Twitter(auth=config.APIKEY)

###便利ツール###
# 特定の文字列を置換
def replace_ch(text, s_name=""):
    dt_now = datetime.datetime.now()
    mont = dt_now.strftime("%m")
    date = dt_now.strftime("%d")
    hour = dt_now.strftime("%H")
    minu = dt_now.strftime("%M")

    re_text = text.replace("{screen_name}", s_name).replace("{month}", mont).replace("{date}", date).replace("{hour}", hour).replace("{minute}", minu)

    return re_text

# データ書き込み用
def write_data(w_data):
    data_path = os.path.join(os.path.dirname(__file__), "data.json")

    with open(data_path, "w") as f:
        json.dump(w_data, f)

# データ読み込み用
def read_data():
    data_path = os.path.join(os.path.dirname(__file__), "data.json")

    with open(data_path, "r") as f:
        return_data = json.load(f)
    
    return return_data
######


###ツイート機能に必要な関数###
# テキストをランダムにツイートさせる
def tweet_rand():
    # ツイート生成
    text = random.choice(text_rand.tweet_data)

    # 文字列置換
    tweet = replace_ch(text)

    # ポスト
    t.statuses.update(status=tweet)

# テキストを順番にツイートさせる
def tweet_ord():
    # どこまでツイートしたか復元
    data_dict = read_data()

    # 最終行だったなら0に戻す
    if data_dict["tweet_order"] == (len(text_ord.tweet_data)):
        print("最終行です。最初に戻ります")
        data_dict["tweet_order"] = 0
    else:
        pass

    # 取り出すデータを選ぶ
    text = text_ord.tweet_data[data_dict["tweet_order"]]

    # 文字列置換
    tweet = replace_ch(text)

    # ポスト
    t.statuses.update(status=tweet)

    # 数値を1増やす。
    data_dict["tweet_order"] += 1

    # データに書き込み
    write_data(data_dict)

# リプライ返し
def reply_mention():
    # Mentionのデータリスト取得
    res = t.statuses.mentions_timeline(count=50)

    # どこまで読み込みしたか復元
    data_dict = read_data()
    last_rep_twi_id = data_dict["rep_mention"]

    # リスト初期化
    list_rep_make = []

    # リプライ対象のツイートか判別し、対象ならばリスト格納。対象外ならリストに入れない。
    for m_num in res:
        if m_num["id"] > last_rep_twi_id:
            list_temp = []
            list_temp.append(m_num["id"])
            list_temp.append(m_num["user"]["screen_name"])
            list_temp.append(repr(m_num["text"]))
            list_rep_make.append(list_temp)

    # リプライ対象のツイートが1つ以上ならリプライ作成。0なら何もしない。
    if len(list_rep_make) > 0:
        # 一致検索
        for rep in list_rep_make:
            content = rep[2]

            for rep_2 in re_pat_ment.re_pat_ment:
                pattern = rep_2[0]
                resulut = re.search(pattern, re.escape(content))

                if resulut is None:      
                    pass
                else:
                    # ツイート作成(パターン一致時)
                    twi_id = rep[0]
                    sc_nam = rep[1]
                    text = ("@" + sc_nam + " " + random.choice(rep_2[1]))
                    
                    # 文字列置換
                    tweet = replace_ch(text, sc_nam)
                    
                    # ポスト
                    t.statuses.update(status=tweet,in_reply_to_status_id=twi_id)
                    break
            else:
                # ツイート作成(全パターン不一致時)            
                twi_id = rep[0]
                sc_nam = rep[1]
                text = ("@" + sc_nam + " " + random.choice(re_pat_ment.rep_rand_m))  

                # 文字列置換
                tweet = replace_ch(text)

                # ポスト
                t.statuses.update(status=tweet,in_reply_to_status_id=twi_id)
    else:
        pass

    #読み込んだ最新ツイートIDの記録
    last_rep_twi_id = res[0]["id"]
    data_dict["rep_mention"] = last_rep_twi_id
    write_data(data_dict)

# TLに反応リプ
def reply_home():
    # TLのデータリスト取得
    res = t.statuses.home_timeline(count=200)

    # どこまで読み込みしたか復元
    data_dict = read_data()
    last_home_twi_id = data_dict["rep_home_tl"]

    # リスト初期化
    list_rep_make = []

    # リプライ対象のツイートか判別し、対象ならばリスト格納。対象外ならリストに入れない。
    for m_num in res:
        # 調べたIDの比較
        if m_num["id"] > last_home_twi_id:

            # RTを除外
            del_rt = re.search(r"RT @(.+)", repr(m_num["text"]))
            if del_rt is None:

                # 自身のツイートを除外
                if m_num["user"]["screen_name"] != config.MY_ID:
                    list_temp = []
                    list_temp.append(m_num["id"])
                    list_temp.append(m_num["user"]["screen_name"])
                    list_temp.append(repr(m_num["text"]))
                    list_rep_make.append(list_temp)
                else:
                    pass
            else:
                pass

    # リプライ対象のツイートが1つ以上ならリプライ作成。0なら何もしない。
    if len(list_rep_make) > 0:
        # 一致検索
        for rep in list_rep_make:
            content = rep[2]

            for rep_2 in re_pat_home.re_pat_home:
                pattern = rep_2[0]
                resulut = re.search(pattern, re.escape(content))

                if resulut is None:      
                    pass
                else:
                    # ツイート作成(パターン一致時)
                    twi_id = rep[0]
                    sc_nam = rep[1]
                    text = ("@" + sc_nam + " " + random.choice(rep_2[1]))
                    
                    # 文字列置換
                    tweet = replace_ch(text, sc_nam)
                    
                    # ポスト
                    t.statuses.update(status=tweet,in_reply_to_status_id=twi_id)
                    break
            else:
                pass

    #読み込んだ最新ツイートIDの記録
    last_home_twi_id = res[0]["id"]
    data_dict["rep_home_tl"] = last_home_twi_id
    write_data(data_dict)
