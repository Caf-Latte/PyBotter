import twitter
import datetime, json, os
import config

# データ初期化
data_dict = {"tweet_order":0, "rep_mention":0, "rep_home_tl":0}

# 認証情報
t = twitter.Twitter(auth=config.APIKEY)

# mentionの最新IDのデータ取得
res_m = t.statuses.mentions_timeline(count=5)
data_dict["rep_mention"] = res_m[0]["id"]

# TLの最新IDのデータ取得
res_h = t.statuses.home_timeline(count=5)
data_dict["rep_home_tl"] = res_h[0]["id"]

# 書き込み
data_path = os.path.join(os.path.dirname(__file__), "data.json")
with open(data_path, "w") as f:
    json.dump(data_dict, f)

dt_now = datetime.datetime.now()

print(str(dt_now + datetime.timedelta(minutes=1)) + "以降に起動して下さい")
input("何かキーを押して終了")
