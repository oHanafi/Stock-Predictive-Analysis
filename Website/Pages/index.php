<html>
	<link rel="stylesheet" type="text/css" href="style/style.css">
	<title>SPAnalytics.nl</title>
<head>

<?php

    $serverName = "85.214.62.99";
    $connectionOptions = array(
        "Database" => "ProjectSPA",
        "Uid" => "Excel",
        "PWD" => "ibbeltje"
    );
    //Establishes the connection
    $conn = sqlsrv_connect($serverName, $connectionOptions);
		
?>
</head>
<body>
	<header>
		<h1>SPAnalytics<span>.nl</span></h1>
		<div class="menu">
			<ul>
				<li><a href="#">HOME</a></li>
				<li><a href="#">STOCKS</a></li>
				<li><a href="#">NEWS</a></li>
				<li><a href="#">CONTACT</a></li>
			</ul>
		</div>
	</header>
	<div class="content">
		<div class="stock-overview">
<?php
$totaal = 0;
	$sql = "SELECT DISTINCT s.short ,d.closing FROM Stock s, StockData D WHERE s.Stock_ID = d.Stock_ID and stock_time IN (SELECT  MAX(stock_time) FROM StockData GROUP BY Stock_ID)";
	$stmt = sqlsrv_query( $conn, $sql );
		if( $stmt === false) {
		die( print_r( sqlsrv_errors(), true) );
		}

	while( $row = sqlsrv_fetch_array( $stmt, SQLSRV_FETCH_ASSOC) ){
		$str = strtolower($row['short']);
			$sql2 = "SELECT TOP(10) closing FROM StockData D, Stock s where s.stock_ID = d.Stock_ID and s.short = '".$str."' ORDER BY d.Stock_Time DESC";
			$stmt2 = sqlsrv_query( $conn, $sql2 );
				if( $stmt2 === false) {
				die( print_r( sqlsrv_errors(), true) );
				}
				$totaal = 0;
				while( $row2 = sqlsrv_fetch_array( $stmt2, SQLSRV_FETCH_ASSOC) ){
					$totaal = $totaal + $row2['closing'];
				
				}
				$avg = $totaal/10;
			
				$sql3 = "SELECT DISTINCT Title, n.Stock_ID, s.Short, Post_Time, Author, Polarity, Subjectivity, Link FROM NewsArticle n, Stock s WHERE n.Stock_ID = s.Stock_ID AND s.short = '".$str."' and Post_Time BETWEEN (SELECT dateadd(day,datediff(day,1,GETDATE()),0)) and (SELECT dateadd(day,datediff(day,0,GETDATE()),0)) ORDER BY Stock_ID";
				$stmt3 = sqlsrv_query( $conn, $sql3 );
				if( $stmt3 === false) {
				die( print_r( sqlsrv_errors(), true) );
				}
				$tel = 0;
				$betrouwbaar = 0;
				while( $row3 = sqlsrv_fetch_array( $stmt3, SQLSRV_FETCH_ASSOC) ){
					$betrouwbaar = $betrouwbaar + ($row3['Polarity'] * (1 - $row3['Subjectivity']));
					$tel = $tel +1;
				}
				$nieuws = $betrouwbaar/$tel;
				
				
				$sql4 = "SELECT DISTINCT d.closing FROM Stock s, StockData D WHERE s.Stock_ID = d.Stock_ID and short = '".$str."' and stock_time IN (SELECT  MAX(stock_time) FROM StockData GROUP BY Stock_ID)";$stmt4 = sqlsrv_query( $conn, $sql4 );
				if( $stmt4 === false) {
				die( print_r( sqlsrv_errors(), true) );
				}
				$huidig = 0;
				while( $row4 = sqlsrv_fetch_array( $stmt4, SQLSRV_FETCH_ASSOC) ){
					$huidig = $row4['closing'];
				}
				
				if (is_nan($nieuws)){
				$advies = (0.6 * $avg + 0.4 * $huidig);
				}else{
				$advies = ((0.4 * $nieuws) * $avg + ((1-(0.4*$nieuws)) * $huidig));
				}
			
				
		echo '<article class="stock-advise">';
		if ($advies < $huidig){
		echo '<img src="PijlNeg.png"height="36" width="36" id="pijl">'."<br />";
		}else{
		echo '<img src="PijlNeg.png"height="36" width="36" id="pijl">'."<br />";
		}
		echo "<p>".$row['short']."</p>"."<br />";
		echo "<p>".$row['closing']."</p>"."<br />";
		echo '</article>';
			
          
	}

sqlsrv_free_stmt( $stmt);
sqlsrv_free_stmt( $stmt2);
?>
		</div>
	
		<div class="specific">
			<div class="chart-area">
			</div>
			<div class="newsarticles">
				<article></article>
				<article></article>
				<article></article>
			</div>
		</div>
	</div>
</body>
</html>