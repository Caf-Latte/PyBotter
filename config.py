import twitter

APIKEY = twitter.OAuth(
    #Consumer_Keyをここに入れる
    consumer_key="XXXXXXXXXX",

    #Consumer_Secretをここに入れる
    consumer_secret="XXXXXXXXXX",
    
    #Access_Tokenをここに入れる
    token="XXXXXXXXXX",
    
    #Access_Token_Secretをここに入れる
    token_secret="XXXXXXXXXX"
)

# アカウントのスクリーンネーム(@より後の英数字と_のみ)
MY_ID = ("XXXXXXXXX")

# 会話を終了させる(リプライを返さない)パターン
END_PATTERN = ("{{END}}")