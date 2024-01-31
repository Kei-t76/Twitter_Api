# Twitter_Api

Twitter api v2がリリースされ, v1と仕様が変更されている点が多かったのでテンプレートとして残します

## 注意点

### 仕様
v2は大きく分けて一般利用者向けサービスと学術利用を目的とした研究者向けサービスの2つがあります.<br>
一般向けでは直近1週間分のツイートが取得でき、研究者向けでは期間無制限にツイートを取得できます.<br>
一般向けと研究者向けでコード内のエンドポイントの指定が変わります.

- 一般利用者向けエンドポイント: https://api.twitter.com/2/tweets/search/recent
- 学術研究者向けエンドポイント: https://api.twitter.com/2/tweets/search/all

### APIキーの取得
Twitter APIを利用するには一般利用か学術利用かにかかわらずAPIの利用申請をしてキーを取得する必要があります.<br>
研究者向けのキー申請は申請者が学術機関か研究機関に在籍していることが条件.

### 公式リファレンス
そのほか一般向けサービスと研究者向けサービスではパラメータの指定が異なる部分があるため、公式のリファレンスを参照してください<br>

一般利用者向けリファレンス<br>
- https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent <br>


研究者向けリファレンス<br>
- https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
