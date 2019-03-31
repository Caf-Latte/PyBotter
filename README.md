# PyBotter
PythonでTwitterのbot

Pythonでなるべく簡単に(欲を言うならPythonが書けない人でもできるように？)
Twitterのbotを作ることができるもの。

任意で機能を拡張できるように、ツイートとリプライのbotを運用するうえで最低限の機能のみを搭載。

--------

注意点
  使用前にpipでtwiteerをインストールしておいてください。
  ↓これ
  https://github.com/sixohsix/twitter
  
--------

開発環境
  WIndows 10 home 64bit
  Python 3.7.2 64bit

動作確認済み環境
  Raspberry Pi3 modelB
  Raspbian Stretch
  Python 3.7.2

--------

今後の改善案
  home_TL及びmentions_TLの取得にscinceパラメータを指定し、処理の軽減を図る
  API制限対策のために各TLのデータを1度の取得で何度も使用できるようにする。
