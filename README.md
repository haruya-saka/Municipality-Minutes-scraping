# Municipality-Minutes-scraping
全国自治体の会議録を北海道を中心にホームページよりスクレイピングし、収集します。  
掲載しているコードは自力で書き、かつ許可を得たものです。

・全国自治体各市町村のホームページに掲載されている会議路録のうち、検索システムを導入しておらず、かつpdfファイルで公開しているものを中心にスクレイピングを行う。  

・自治体により掲載方法が異なるため、それぞれ別のスクリプトを書く。  

・pdfだけを取ってくるのでなく、年度、会議のナンバー・種類まで取ってくる  

## 例（北海道新篠津村）
"元号　第n回　会の種類　内容".pdf　という形式で取ってこなければいけない。（pdfファイルを取るだけでなく、どの会議のどの情報なのかを見てわかるようにネームしなければいけない）

<img width="500" alt="スクリーンショット 2023-11-15 1 23 06" src="https://github.com/haruya-saka/Municipality-Minutes-scraping/assets/127200853/1dec9325-6b1d-45a2-8bfd-9cf200a5e3c5">

会議録を掲載しているページのURLをBeautifulSoupを用いてパースし、.pdfを持つaタグを取得する。ページネーションされていない場合や、年度毎にリンク分割されていない場合は数行で済む。

<img width="500" alt="スクリーンショット 2023-11-15 1 28 43" src="https://github.com/haruya-saka/Municipality-Minutes-scraping/assets/127200853/76f52902-c1af-4c6a-97ba-45a6f2ec7aa2">

新篠津町の会議録掲載ページは上記のようになっている。
例えば令和5年　第3回　定例会（9月6日～9月15日）の議決結果、一般質問を取得したい場合、htmlから関連するテキストを取ってきて紐づけることを考える。
<img width="500" alt="スクリーンショット 2023-11-15 1 37 03" src="https://github.com/haruya-saka/Municipality-Minutes-scraping/assets/127200853/316ea29f-1162-47e4-9093-18035aab5e4f">

デベロッパーで令和5年度第3回　定例会の議決結果を見る。（https://www.vill.shinshinotsu.hokkaido.jp/hotnews/detail/00000288.html）

まず「令和5年度」を取得したい場合だが、令和5年度のh2タグと令和4年度のh2タグ、さらにpdfファイルの存在するaタグの親divタグは同じ階層に並んでおり、h2タグから元号を取ってくるのは難しい。
よって今回は、pdfファイルネームから作成年度（西暦）を取得し、和暦に変換する関数を用いている(24行)。

次に「第3回　定例会」を取得したい場合。これも「会の情報」と「議決結果」、「一般質問」が同じ階層に並んでいるため取得が難しい。よって、linksからfor文で取り出したaタグ(link)の親に当たるtr要素を取得し(53行)、その配下に存在するspanタグの0番目のテキストを指定して取ってきている(56行)。

さらに「議決結果」、「一般質問」は、一般質問がある場合とない場合で条件分岐して取得している(60行)。
<img width="500" alt="スクリーンショット 2023-11-15 1 27 29" src="https://github.com/haruya-saka/Municipality-Minutes-scraping/assets/127200853/909e77b6-aced-4cb2-aa96-cfd1da2a3b4e">
