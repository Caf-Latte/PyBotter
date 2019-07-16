import pybotter
import datetime

##################
pybotter.fetch_timelines()
dt_now = datetime.datetime.now()
mont = dt_now.month
date = dt_now.day
hour = dt_now.hour
minu = dt_now.minute
##################


# ランダムでツイート
#pybotter.tweet_random("rnd_text.txt")

# テキストを順番にツイートさせる
#pybotter.tweet_order("ord_text.txt", "loop")
#pybotter.tweet_order("ord_text.txt", "once")

# リプライ返し
#pybotter.reply_mention("rep_ment.json")

# TLに反応リプ
#pybotter.reply_home("rep_home.json")


##################
pybotter.write_last_ids()
##################