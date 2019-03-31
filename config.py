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

# アカウントのスクリーンネーム(@以降、大文字小文字正確に)
MY_ID = ("XXXXXXX")