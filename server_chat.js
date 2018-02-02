// べゼリー設定Webアプリ 
// for Bezelie Edgar
// in Node-JS
// by Jun Toyoda (Team Bezelie)
// From  Aug 10th 2017
// ---------------------------------------------------------------------------------
// モジュールをロードして変数にオブジェクトとして読み込む
var http = require('http'); // httpアクセスのための機能を提供するモジュール
                            //   http.createServer(function);
var fs   = require('fs');   // ファイルおよびファイルシステムを操作するモジュール
                            //   fs.readFile('file name','utf-8',callback function)
                            //   fs.readFileSync('file name','utf-8')
var ejs  = require('ejs');  // JS用テンプレートエンジンejs(Embedded JavaScript Templates)
                            //    ejs.render(変数に代入されたejs, 置換データオブジェクト);
var url  = require('url');  // URL文字列をパースやフォーマットするモジュール
                            //    url.parse(request.url);
var qs   = require('querystring');
                            // クエリー文字列をパースしてオブジェクトに変換するモジュール
                            //    qs.parse();
var exec = require('child_process').exec; 
                            // 子プロセスの生成と管理をするモジュール。
                            //    exec(COMMAND, [options], callback(error, stdout, stderr) {}
                            //    option maxBuffer:バッファの最大容量(byte)
                            //    error :エラーオブジェクト
                            //    stdout:標準出力に出力されたデータ
                            //    stderr:標準エラー出力に出力されたデータ
var CSV  = require("comma-separated-values"); 
                            // CSVを配列変数やオブジェクトに変換する
var os   = require('os');
                            //    os.networkInterfaces();
var sleep = require('sleep');
                            // ウェイト処理用モジュール

// ejsファイルの読み込み
var template            = fs.readFileSync(__dirname + '/ejs/template.ejs', 'utf-8');
var top                 = fs.readFileSync(__dirname + '/ejs/top.ejs', 'utf-8');
var editBasic           = fs.readFileSync(__dirname + '/ejs/editBasic.ejs', 'utf-8');
var editChat            = fs.readFileSync(__dirname + '/ejs/editChat.ejs', 'utf-8');
var editTime            = fs.readFileSync(__dirname + '/ejs/editTime.ejs', 'utf-8');
var editServo           = fs.readFileSync(__dirname + '/ejs/editServo.ejs', 'utf-8');
var setBasic            = fs.readFileSync(__dirname + '/ejs/setBasic.ejs', 'utf-8');
var setTime             = fs.readFileSync(__dirname + '/ejs/setTime.ejs', 'utf-8');
var setServo            = fs.readFileSync(__dirname + '/ejs/setServo.ejs', 'utf-8');
var editIntent          = fs.readFileSync(__dirname + '/ejs/editIntent.ejs', 'utf-8');
var selectIntent4entity = fs.readFileSync(__dirname + '/ejs/selectIntent4entity.ejs', 'utf-8');
var editEntity          = fs.readFileSync(__dirname + '/ejs/editEntity.ejs', 'utf-8');
var selectIntent4dialog = fs.readFileSync(__dirname + '/ejs/selectIntent4dialog.ejs', 'utf-8');
var editDialog          = fs.readFileSync(__dirname + '/ejs/editDialog.ejs', 'utf-8');
var starting_pythonApp  = fs.readFileSync(__dirname + '/ejs/starting_pythonApp.ejs', 'utf-8');
var reboot              = fs.readFileSync(__dirname + '/ejs/reboot.ejs', 'utf-8');
var disableServer       = fs.readFileSync(__dirname + '/ejs/disableServer.ejs', 'utf-8');
var test                = fs.readFileSync(__dirname + '/ejs/test.ejs', 'utf-8');

// 変数宣言
var routes = { // パスごとの表示内容を連想配列に格納
    "/":{
        "title":"BEZELIE",
        "message":"べゼリー設定データの編集ができます",
        "content":top}, // テンプレート
    "/editBasic":{
        "title":"基本設定",
        "message":"べゼリーの基本的な設定を行います",
        "content":editBasic},
    "/editChat":{
        "title":"対話設定",
        "message":"３種類のデータを編集することで、対話を作ることができます",
        "content":editChat},
    "/editTime":{
        "title":"時間設定",
        "message":"アラームと活動時間の設定をします",
        "content":editTime},
    "/editServo":{
        "title":"サーボ調整",
        "message":"サーボの初期位置（角度）を調整します。単位は度です。サーボを上から見て時計回りが正の値になります",
        "content":editServo},
    "/disableServer":{
        "title":"再起動",
        "message":"プログラムを停止し、アクセスポイント化を無効にして再起動します",
        "content":disableServer},
    "/editIntent":{
        "title":"【質問内容】の編集",
        "message":"質問内容の追加や削除ができます。質問内容とはべゼリーに聞きたい内容のことです。この文字が音声認識されるわけではないので、わかりやすい名称をつけてください",
        "content":editIntent},
    "/selectIntent4entity":{
        "title":"【言い回し】の編集",
        "message":"リストから質問内容を選んでください。リストの中に望みの質問内容が無い場合は、いったん対話編集画面に戻り、質問内容の追加をしてください",
        "content":selectIntent4entity},
    "/editEntity":{
        "title":"【言い回し】の編集",
        "message":"質問の色々な言い回しの追加や削除ができます。質問の言い回しとはべゼリーに質問する際の、さまざまな言いかたのことです。ひらがなで入力してください",
        "content":editEntity},
    "/selectIntent4dialog":{
        "title":"【返答候補】の編集",
        "message":"リストから質問内容を選んでください。リストの中に好みの質問内容が無い場合は、いったん対話編集画面に戻り、質問内容データの追加をしてください。",
        "content":selectIntent4dialog},
    "/editDialog":{
        "title":"【返答候補】の編集",
        "message":"返答候補の追加や削除ができます。返答候補とはユーザーからの質問に対するべゼリーからの返答の候補です。複数の返答を設定した場合はランダムで選ばれます。",
        "content":editDialog},
    "/reboot":{
        "title":"再起動",
        "message":"システムを再起動します",
        "content":reboot},
    "/starting_pythonApp":{
        "title":"プログラムの再起動",
        "message":"プログラムを再起動します",
        "content":starting_pythonApp},
    "/setBasic":{
        "title":"設定完了",
        "message":"設定を更新しました",
        "content":setBasic},
    "/setTime":{
        "title":"設定完了",
        "message":"設定を更新しました",
        "content":setTime},
    "/setServo":{
        "title":"設定完了",
        "message":"設定を更新しました",
        "content":setServo},
    "/test":{
        "title":"テスト",
        "message":"これはテスト用のページです",
        "content":test}
};
// 変数宣言
var file_chatIntent            = __dirname+"/chatIntent.csv";
var file_chatEntity            = __dirname+"/chatEntity.csv";
var file_chatDialog            = __dirname+"/chatDialog.csv";
var file_chatEntity_tsv        = __dirname+"/chatEntity.tsv";
var file_chatEntity_dic        = __dirname+"/chatEntity.dic";
var file_restart_app           = __dirname+"/restart_app.sh";
var file_exec_talk             = __dirname+"/exec_openJTalk.sh"
var file_setting_disableServer = __dirname+"/setting_disableServer.sh";
var file_data_chat             = __dirname+"/data_chat.json"
var file_debug                 = __dirname+"/debug.txt"
var errorMsg = ""; // これが空欄のときはエラー無し
var posts = "";    // ブラウザからPOSTで送られてきたデータ
var intent = "";   // 今回選択されたintent（単数）

// 関数定義
function getLocalAddress() {                    // IPアドレスの取得
    var ifacesObj = {}
    ifacesObj.ipv4 = [];
    ifacesObj.ipv6 = [];
    var interfaces = os.networkInterfaces();

    for (var dev in interfaces) {
        interfaces[dev].forEach(function(details){
            if (!details.internal){
                switch(details.family){
                    case "IPv4":
                        ifacesObj.ipv4.push({name:dev, address:details.address});
                    break;
                    case "IPv6":
                        ifacesObj.ipv6.push({name:dev, address:details.address})
                    break;
                }
            }
        });
    }
    return ifacesObj;
};

function pageWrite (res){                      // ページ描画
    content = ejs.render( template, {
        title: routes[url_parts.pathname].title,
        errorMsg: errorMsg,
        content: ejs.render( routes[url_parts.pathname].content, {
            message: routes[url_parts.pathname].message,  // pathnameに応じたメッセージを指定
            posts: posts,  // ブラウザからPOSTされてきたデータ
            intent: intent // 今回選ばれたインテント
        })
    });
    res.writeHead(200, {'Content-Type': 'text/html; charset=UTF-8'}); // ステイタスコードやhttpヘッダーをクライアントに送信する。
    res.write(content);
    res.end();
}

function delChk (query, posts, intent){       // 削除しようとしている番号が、選択中のインテントのものかを調べる
    errorMsg = "番号が違います";
    for (var i=0;i < posts.length; i++ ) {
        if (posts[i][0]==intent && i==query.delNum){
            errorMsg = "";
        }
    }
    return errorMsg;
}

function readPosts(file){                     // 
    var text = fs.readFileSync(file, 'utf8'); // 同期でファイルを読む
    //var text = fs.readFileSync(__dirname + "/" + file, 'utf8'); // 同期でファイルを読む
    posts = new CSV(text, {header:false}).parse(); //  TEXTをCSVを仲介してリスト変数に変換する
    return posts;
}

function obj2csv(posts){                     // 
    text = '';
    for (var i=0;i < posts.length; i++ ) {
        text = text+posts[i]+'\n';
        }
    return text;
}

function debug(text){                        // 
    fs.appendFileSync(file_debug, text, 'utf8'); // 同期でファイルを読む
}

//-------------------------------------------------------------------------------------------------------
// ルーティング
function routing(req, res){ // requestイベントが発生したら実行される関数
    url_parts = url.parse(req.url); // URL情報をパース処理
    errorMsg = "";
    // 想定していないページに飛ぼうとした場合の処理
    if (routes[url_parts.pathname] == null){ // パスが変数routesに登録されていない場合はエラーを表示する
        content = "<h1>NOT FOUND PAGE:" + req.url + "</h1>"
        res.writeHead(200, {'Content-Type': 'text/html; charset=UTF-8'}); // ステイタスコードやhttpヘッダーをクライアントに送信する。
        res.write(content);
        res.end();
        return;
    }
    // GETリクエストの処理  -------------------------------------------------------------------------------
    if (req.method === "GET"){
        if (url_parts.pathname === "/editIntent" || url_parts.pathname === "/selectIntent4entity" || url_parts.pathname === "/selectIntent4dialog"){ 
            posts = readPosts(file_chatIntent);
            pageWrite(res);
            return;
        } else if (url_parts.pathname === "/editBasic" || url_parts.pathname === "/editTime" || url_parts.pathname === "/editServo"){ //
            var json = fs.readFileSync(file_data_chat, "utf-8");  // 同期でファイルを読む
            obj_config = JSON.parse(json); // JSONをオブジェクトに変換する。ejsからも読めるようにグローバルで定義する
            pageWrite(res)
        } else if (url_parts.pathname == "/starting_pythonApp"){ // Juliusとpythonプログラムの再起動
            pageWrite(res);
            debug('restart function start \n');
            var COMMAND = "sh "+file_exec_talk+" "+"プログラムを再起動します";
            exec(COMMAND, function(error, stdout, stderr) {
              var COMMAND = "bash "+file_restart_app;
              exec(COMMAND, function(error, stdout, stderr) {
                debug('app done \n');
                debug('stdout: '+stdout+'\n');
                debug('stderr: '+stderr+'\n');
              }); // end of exec
            }); // end of exec
            debug('restart function end \n');
        } else if (url_parts.pathname == "/reboot"){ // 再起動
            pageWrite(res);
            var COMMAND = "sh "+file_exec_talk+" "+"システムを再起動します";
            exec(COMMAND, function(error, stdout, stderr) {
              var COMMAND = 'sudo reboot';
              exec(COMMAND, function(error, stdout, stderr) {
              }); // end of exec
            }); // end of exec
        } else if (url_parts.pathname === "/disableServer"){ // サーバーを無効化して再起動
            pageWrite(res);
            var COMMAND = "sh "+file_exec_talk+" "+"プログラムを終了し、アクセスポイント化を無効化して再起動します";
            exec(COMMAND, function(error, stdout, stderr) {
              var COMMAND = "sh "+file_setting_disableServer;
              exec(COMMAND, function(error, stdout, stderr) {
                var COMMAND = 'sudo reboot';
                exec(COMMAND, function(error, stdout, stderr) {
                }); // end of exec
              }); // end of exec
            }); // end of exec
        } else {
            pageWrite(res);
        }// end of if
    } // end of get request
    // POSTリクエストの処理 -------------------------------------------------------------------------------
    if (req.method === 'POST') {
        req.data = "";
        req.on("data", function(data) {
            req.data += data;
        });
        req.on("end", function() {
            var query = qs.parse(req.data); // 全受信データをquerry stringでパースする。
        // ----------------------------------------------------------------------------------------------
            if (url_parts.pathname == "/editIntent"){ // インテントの編集
                posts = readPosts(file_chatIntent);
                if (query.newItem){ // 新規追加
                    for (var i=0;i < posts.length; i++ ) {
                        if (posts[i][1] == query.newItem){
                            errorMsg = "すでに登録されています";
                        }
                    }
                    if (errorMsg == ""){ 
                        posts.push(['common',query.newItem]); // newItemをpostの配列に入れる。
                    }
                } else if (query.delNum){ // 削除
                    if(isNaN(query.delNum)){
                        errorMsg = "数字(半角)を入力してください";
                    } else if(query.delNum >= posts.length) {
                        errorMsg = "数字が大きすぎます";
                    } else {
                        intent = posts[query.delNum][1];
                        posts = readPosts(file_chatEntity);
                        for (var i=0;i < posts.length; i++ ) {
                            if (posts[i][0] == intent){
                                errorMsg = "この質問内容に対応している言い回しデータが存在します。先に削除してください。";
                            }
                        }
                        posts = readPosts(file_chatDialog);
                        for (var i=0;i < posts.length; i++ ) {
                            if (posts[i][0] == intent){
                                errorMsg = "この質問内容に対応している返答候補データが存在します。先に削除してください。";
                            }
                        }
                        posts = readPosts(file_chatIntent);
                    }
                    if (errorMsg == ""){ // エラーがなかったのでアイテム削除
                        posts.splice(query.delNum, 1); // postsからdelNum行を削除
                    }
                } else { // 必要ないが念のため。
                }
                if (errorMsg == ""){
                    text = obj2csv(posts);
                    fs.writeFileSync(file_chatIntent, text , 'utf8', function (err) { // ファイルに書込
                    });
                }
                pageWrite(res);
            } else if (url_parts.pathname == "/editEntity"){ // エンティティの編集
                posts = readPosts(file_chatEntity);
                if (query.intent){ // selectIntentから来た場合
                    intent = query.intent; // グローバル変数intentに代入。
                    errorMsg = " ";
                } else if (query.newItem){ // 新規追加
                    for (i=0;i<query.newItem.length;i++){ // ひらがなかチェック
                        var unicode = query.newItem.charCodeAt(i);
                        if ( unicode<0x3040 || unicode>0x309f ){
                            if ( unicode != 0x30fc ){ // chou-on
                                errorMsg = "言い回しデータはひらがな(全角)で入力してください";
                            }
                        }
                    }
                    for (var i=0;i < posts.length; i++ ) { // 重複チェック
                        if (posts [i][0] == intent && posts[i][1] == query.newItem){
                            errorMsg = "すでに登録されています";
                        }
                    }
                    if (errorMsg == ""){ // エラーがなかったのでアイテム追加
                        posts.push([intent,query.newItem]); // newItemをpostの配列に入れる。
                    }
                } else if (query.delNum){ // 削除
                    if(isNaN(query.delNum)){ // 数値かチェック
                        errorMsg = "数字(半角)を入力してください";
                    }else{ // 選択中のインテントにひもづくエンティティかどうかチェック
                        errorMsg = delChk(query, posts, intent);
                    }
                    if (errorMsg == ""){ // エラーがなかったのでアイテム削除
                        posts.splice(query.delNum, 1); // postsからdelNum行を削除
                    }
                } else { // 必要ないが念の為
                }
                if (errorMsg == ""){ // エラーがなかったらファイルに書き込み
                   text = obj2csv(posts);
                   fs.writeFile(file_chatEntity, text , 'utf8', function (err) {
                      var COMMAND = 'sudo sed -E "s/,/    /g" '+file_chatEntity+' > '+file_chatEntity_tsv; // csvをtsvに変換
                      exec(COMMAND, function(error, stdout, stderr) { // tsvファイルをjuliusのdic形式に変換
                           var COMMAND = 'iconv -f utf8 -t eucjp '+file_chatEntity_tsv+' | /home/pi/dictation-kit-v4.4/src/julius-4.4.2/gramtools/yomi2voca/yomi2voca.pl > '+file_chatEntity_dic; // tsvをdicに変換
                           // var COMMAND = 'iconv -f utf8 -t eucjp chatEntity.tsv | /home/pi/dictation-kit-v4.4/src/julius-4.4.2/gramtools/yomi2voca/yomi2voca.pl > chatEntity.dic'; // tsvをdicに変換
                           exec(COMMAND, function(error, stdout, stderr) {
                           });
                       }); //end of exec
                   }); // end of fs
                } // end of if
                pageWrite(res);
            } else if (url_parts.pathname == "/editDialog"){ // ダイアログの編集
                posts = readPosts(file_chatDialog);
                if (query.intent){ // intentを選択した場合の処理。
                    intent = query.intent; // グローバル変数intentに代入。
                    errorMsg = " ";
                } else if (query.newItem){ // 新規追加の場合。重複をチェックする。
                    for (var i=0;i < posts.length; i++ ) {
                        if (posts [i][0] == intent && posts[i][1] == query.newItem){
                            errorMsg = "すでに登録されています";
                        }
                    }
                    if (errorMsg == ""){ // 重複がなかった場合。追加する。
                        posts.push([intent,query.newItem]); // newItemをpostの配列に入れる。
                    }
                } else if (query.delNum){ // 削除
                    if(isNaN(query.delNum)){ // 数字じゃない場合
                        errorMsg = "数字(半角)を入力してください";
                    }else{
                        errorMsg = delChk(query, posts, intent);
                    }
                    if (errorMsg == ""){ // エラーがなかったので削除
                        posts.splice(query.delNum, 1); // postsからdelNum行を削除
                    }
                } else { //必要ないが念の為
                }
                if (errorMsg == ""){ // エラーがなかったらファイルに書き込み
                    text = obj2csv(posts);
                    fs.writeFileSync(file_chatDialog, text , 'utf8', function (err) { // ファイルに書込
                    });
                }
                pageWrite(res);
            } else if (url_parts.pathname == "/setBasic"){ // 基本設定の保存
                obj_config.data0[0] = qs.parse(req.data);
                fs.writeFile(file_data_chat, JSON.stringify(obj_config), function (err) {
                });
                pageWrite(res);
            } else if (url_parts.pathname == "/setTime"){ // 時間設定の保存
                obj_config.data1[0] = qs.parse(req.data);
                fs.writeFile(file_data_chat, JSON.stringify(obj_config), function (err) {
                });
                pageWrite(res);
                yearNow=obj_config.data1[0].nowYear;
                timeNow=obj_config.data1[0].nowTime;
                console.log(yearNow);
                console.log(timeNow);
                var COMMAND = "sudo date -s '"+yearNow+" "+timeNow+"'";
                exec(COMMAND, function(error, stdout, stderr) {
                });
            } else if (url_parts.pathname == "/setServo"){ // サーボ調整の保存
                obj_config.data2[0] = qs.parse(req.data);
                fs.writeFile(file_data_chat, JSON.stringify(obj_config), function (err) {
                });
                pageWrite(res);
                var COMMAND = "python bezelie.py";
                exec(COMMAND, function(error, stdout, stderr) {
                });
            } else { // 該当せず
                res.writeHead(200, {'Content-Type': 'text/html; charset=UTF-8'});
                res.write("NO-POST!!");
                res.end();
                return;
            } // end of if
        }); // end of req on
    } // end of POST request
} // end of doRequest

// ---------------------------------------------------------------------------------------------------------
// IPアドレスの設定
var host = getLocalAddress().ipv4[0].address; // 現在のIPアドレスを取得する。
// var host = 'localhost'         //
// var host = '10.0.0.1'          // 
debug('server_editChat.js start \n');
debug(host+'\n');

// サーバーの起動
console.log ("starting node server");
var server = http.createServer(); // http.serverクラスのインスタンスを作る。戻値はhttp.server型のオブジェクト。
server.on('request', routing);    // serverでrequestイベントが発生した場合のコールバック関数を登録
var port = 3000;                  // portは1024以上の数字なら何でもよい。
server.listen(port, host)         // サーバーを待ち受け状態にする。
// var COMMAND = "sh "+file_exec_talk+" "+host;
// exec(COMMAND, function(error, stdout, stderr) {
//   sleep.sleep(6);
//   server.listen(port, host)         // サーバーを待ち受け状態にする。
// });
console.log ("server is listening at "+host+":"+port);
