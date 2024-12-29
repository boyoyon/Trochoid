<html lang="ja">
    <head>
        <meta charset="utf-8" />
    </head>
    <body>
        <h1><center>Trochoid</center></h1>
        <h2>なにものか？</h2>
        <p>
            トロコイド(trochoid)を表示するだけのプログラムです。<br>
            <table border="1">
                <tr><th>用語</th><th>説明</th></tr>
                <tr><td>トロコイド(trochoid)</td><td>円をある軌道に沿ってすべらないように転がしたとき、その円の内部または外部の定点が描く曲線</td></tr>
                <tr><td>サイクロイド(cycloid)</td><td>軌道が直線、定点が円周上の場合のトロコイド</td></tr>
                <tr><td>カーディオイド(cardioid)</td><td>軌道が円、定点が円周上の場合のトロコイド</td></tr>
            </table>
            <h3>軌道が直線</h3>
            <h4>定点が円の外部</h4>
            <img src="images/trochoid.gif"><br>
            <h4>定点が円周上：cycloid</h4>
            <img src="images/cycloid.gif"><br>
            <h4>定点が円の内部</h4>
            <img src="images/trochoid_05.gif"><br>
            <h3>軌道が円:円の外を転がる(epitrochoid))</h3>
            <h4>定点が円の外部</h4>
            <img src="images/epitrochoid_2.gif"><br>
            <h4>定点が円周上：cardioid</h4>
            <img src="images/cardioid.gif"><br>
            <h4>定点が円周上：cardioid。円の半径比 4 vs 5</h4>
            層が4段、葉っぱが5枚になる<br>
            <img src="images/cardioid_4_5.gif"><br>
            <h4>定点が円の内部</h4>
            <img src="images/epitrochoid_075.gif"><br>
            <h3>軌道が円:円の中を転がる(intratrochoid, spirograph)</h3>
            <img src="images/intratrochoid.gif"><br>
        </p>
        <h2>環境構築方法</h2>
        <p>
            pip install opencv-python<br>
        </p>
        <h2>使い方</h2>
        <h3>軌道が直線</h3>
        <p>
            python trochoid.py [(回転円の半径に対する定点の倍率)]<br>
        </p>
        <h3>軌道が円：円の外部を転がる</h3>
        <p>
            python epitrochoid.py [(回転円の半径に対する定点の倍率) (回転円の半径) (固定円の半径)]<br>
        </p>
        <h3>軌道が円：円の内部を転がる(spirograph)</h3>
        <p>
            python intratrochoid.py<br>
        </p>
        <h3>おまけ：サイクロイドを円周に貼り付けるとカーディオイドになる</h3>
        <p>
            python cycloid_cardioid.py<br>
            軌道に沿った円の回転(1回転) ＋ 軌道の回転(1回転) ＝ 2回転<br>
        </p>
            <img src="images/cycloid_cardioid.gif"><br>
        <h3>おまけ：定点が円の外、直線軌道のトロコイドを丸い軌道に貼り付けるとNTTロゴが出来上がる</h3>
        <p>
            python ntt.py<br>
        </p>
            <img src="images/ntt.gif"><br>
    </body>
</html>
