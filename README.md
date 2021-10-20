# Random Stat

e-stat から取得した統計データをランダムで表示するサービスです｡

# サービス概要

サービスのコンセプト

1. 無作為にデータを表示することで新たな発見･気づきを得られる｡
2. 統計表同士の比較表示が簡単に行える

# サービスを作った経緯

既存のサービスでは､ある仮説ないし目的をもって比較する統計対象を選択する必要があり,
目的もなくただ統計データを眺め､興味を持った統計データを深堀りするといった使い方に適していませんでした｡
そのため､無作為に抽出したデータを表示することで､新たな発見や気付きを得ることができるサービスを作ってみたいと考え開発に至りました｡

# 苦労した点

ほとんどのライブラリの選定にあたり､日本語ドキュメントが存在せず､また､日本語の有用な技術ブログ等も得られなかった点です｡

そのため､開発の途中から GoogleChrome の検索言語を英語に変更し､英語で書かれたドキュメント･技術ブログ等を参考にしました｡

この結果､開発以前は日本語で書かれた公式ドキュメントを読むことにすら忌避感がありましたが､それが解消されました｡
今後､日本語化されていないライブラリを解説するブログ等を作成してみたいと考えております｡

# 機能一覧

- メイン機能

  - 統計表セットをランダムに表示
  - 統計表をランダムに取得
  - 統計表の種類を固定してランダムに取得
  - カテゴリー検索
  - 地域･カテゴリーを指定して統計表を取得
  - 統計表詳細情報
  - 統計データ表示
  - お気に入り登録･削除
  - 統計表示履歴
  - 統計表データを csv で取得(実装中)

- アカウント機能

  - アカウント登録機能

    - Google アカウントで登録
    - GitHub アカウントで登録
    - Facebook アカウントで登録
    - Email で登録
    - アカウント登録後､アクティベーションメール送信機能
    - アクティベーションメールを再送信機能

  - ログイン機能

    - Google アカウントでログイン
    - GitHub アカウントでログイン
    - Facebook アカウントでログイン
    - Email でログイン
    - ゲストログイン
    - パスワードリセット機能(パスワードをお忘れの場合)
    - 前回のログイン情報 表示機能
    - 前回のログイン情報 リセット機能

  - アカウント管理

    - アバターアップロード機能
    - ユーザー名変更
    - Email アドレス変更
    - パスワード変更
    - パスワード設定(ソーシャルアカウントで登録し､パスワードが設定されていない場合に使用)
    - アカウント削除

  - ログイン履歴

    - 接続元 IP アドレスを表示
    - ログイン･ログアウト時刻を表示

  - アカウント連携

    - Google 連携･連携解除
    - GitHub 連携･連携解除
    - Facebook 連携･連携解除

# 使用技術一覧

## Backend

- Python 3.7.3
- Django 3.2.8
- Django REST framework 3.12.4

## Frontend

- Vue.js 2.6.12

## Infrastructure

- AWS
  - ECR
  - ECS on Fargate
  - Route53
  - S3
  - ELB
  - KMS
  - ACM
  - RDS(PostgreSQL 11.9)
- Terraform
- Docker
- Nginx
- GitHub Actions

# 使用ライブラリ抜粋

## Backend

- boto3==1.18.64
- Django==3.2.8
- django-cleanup==5.2.0
- django-cors-headers==3.10.0
- django-csp==3.7
- django-environ==0.8.0
- django-filter==21.1
- django-imagekit==4.0.2
- django-storages==1.12.2
- djangorestframework==3.12.4
- djangorestframework-simplejwt==4.8.0
- djoser==2.1.0
- gunicorn==20.1.0
- psycopg2==2.9.1
- social-auth-app-django==4.0.0

## Frontend

- axios
- BootstrapVue
- Vuex
- Vue Router

# セキュリティ

- HTTP headers

  - Content-Security-Policy
  - Referrer-Policy
  - Permissions-Policy
  - HTTP Strict-Transport-Security
  - X-Frame-Options
  - X-XSS-Protection
  - X-Content-Type-Options

- Cookies

  - http-only
  - secure
  - samesite Strict

- File Upload
  - magic number 検査
  - 拡張子検査
  - Exif 削除
  - upload イメージ縮小

## File upload

- max_length(Model)
- extension(FileExtensionValidator)
- change file name(UUID)
- magic number
- remove Exif
- limit image size

