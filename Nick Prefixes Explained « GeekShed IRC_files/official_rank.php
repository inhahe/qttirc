
<!DOCTYPE html>
<html>
<head>
<title>IRC Networks</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<style>

* {
	font-family: sans-serif;
}

#mainsearch {
	text-align: center;
	font-size: 19px;
	padding-top: 80px;
	padding-bottom: 80px;
}

.mibbutton {
    border: 2px solid #7B934C;
    background: #BEEC9D;
    padding: 5px;
	margin: 0px;
    color: #000;
	text-decoration: none;
    font-size: 15px;
	border-radius: 4px;
	-moz-border-radius: 4px;
	-webkit-border-radius: 4px;
}

.mibbutton:hover {
	text-decoration: none;
	color: #000;
	background: #93C145;
}

.mibinput {
	font-size: 15px;
	padding: 5px;
	border: 2px solid #666;
	margin-right: 5px;
	border-radius: 4px;
	-moz-border-radius: 4px;
	-webkit-border-radius: 4px;
}

</style>
</head>

<body onload="document.getElementById('qsearch').focus();">


<style>
#header {
	color: #222;
	font-family: sans-serif;
	font-size: 17px;
	text-align: left;
	padding: 16px;
	background: #eee;
	border: 2px solid #aaa;
	-moz-border-radius: 16px;
	-webkit-border-radius: 16px;
	border-radius: 16px;
}

#footer {
	color: #222;
	font-family: sans-serif;
	font-size: 15px;
	text-align: left;
	padding: 16px;
	background: #eee;
	border: 2px solid #aaa;
	-moz-border-radius: 16px;
	-webkit-border-radius: 16px;
	border-radius: 16px;
}
	
.menuitem {
	color: #444;
}

.menuitema {
	font-weight: bold;
	color: #008;
}
</style>

<div id=header>
<table width=100%><tr>
<td><a href="/"><img src="/mainlogo.png" border=0 width=300 height=185></a></td>
<td align=center>
<!--/*
  *
  * Revive Adserver iFrame Tag
  * - Generated with Revive Adserver v3.1.0
  *
  */-->

<iframe id='af8d2196' name='af8d2196' src='https://as.mibbit.com/www/delivery/afr.php?zoneid=4&amp;cb=1515029644' frameborder='0' scrolling='no' width='728' height='90'><a href='http://as.mibbit.com/www/delivery/ck.php?n=a205a12b&amp;cb=INSERT_RANDOM_NUMBER_HERE' target='_blank'><img src='http://as.mibbit.com/www/delivery/avw.php?zoneid=4&amp;cb=61313377&amp;n=a205a12b' border='0' alt='' /></a></iframe>
</td>
</tr>
</table>
<table width=100%>
	<tr>
		<td>
 <a href="/networks" class=menuitem>Browse networks</a></td>


</tr>
</table>
</div>
<br>

<style>
.helpdiv {
	text-align: center;
	font-family: sans-serif;
	font-color: #444;
	font-size: 17px;
	margin: 8px;
	padding: 8px;
	background: #eee;
}
</style>
<div class="helpdiv">
Find places to chat</div>

<div id=mainsearch>
<form action="/" method="get">
<input class=mibinput type=text placeholder="e.g. music trivia" name=q id=qsearch size=32><input type=submit class=mibbutton value="Search channels">
</form>
</div>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-109769140-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-109769140-1');
</script>

<div id=footer>
	<a class=menuitem href="/add_network.php">Get your IRC network listed</a>
</div>

</body>
</html>