<?php

function curl_get_contents($url)
{
  $ch = curl_init($url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
  curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
  curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
  $data = curl_exec($ch);
  curl_close($ch);
  return $data;
}

if (isset($_GET['title'])) {
	$base_url = 'http://localhost:5000/';
	$url = $base_url . 'get-plot-summary/' . $_GET["title"];
	$url = str_replace(" ","%20",$url);
	$content = curl_get_contents($url);
	$json = json_decode($content, true);

	// $content = file_get_contents('./status0');
	// $json = json_decode($content, true);

	if ($json["status"] == 0) {
		$main_title = $json["title"];
		$main_plot = $json["plot"];

		$url = $base_url . 'get-similar-movies/' . $json["title"];
		$url = str_replace(" ","%20",$url);
		$content = curl_get_contents($url);
		$json = json_decode($content, true);

		// $content = file_get_contents('./output');
		// $json = json_decode($content, true);

		if ($json["status"] == 0) {
			$similar_movies = $json["movies"];
		} else if ($json["status"] == 404) {
			print_r("Not Found");
		}

	} else if ($json["status"] == 1) {
		$movies = $json["movies"];
	} else if ($json["status"] == 404) {
		print_r("Not Found");
	}

}

if (isset($_POST['similar_title'])) {
	
}

?>

<html>
<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">	
</head>
<body>
<div class="row">
	<div class="col-md-12">
		<div class="input-group">
		<form action="" method="get">
			<input type="text" class="form-control" placeholder="insert movie title" name="title"><br>
			<button type="submit" class="btn btn-primary">Submit</button>

		</form>
		</div>
	</div>
</div>

<?php
	if (isset($main_title)) {
		echo "Title: ".$main_title."<br>";
		echo "Plot summary:<br>".$main_plot."<br>";
		echo "Similar Movies:<br>";

		echo "<ul>";
		foreach ($similar_movies as $movie) {
			echo '<li>Title: '.$movie["title"].'<br>
			Plot summary: '.$movie["plot"].'</li>';
		}
		echo "</ul>";
	}

	if (isset($movies)) {
		echo "<ul>";
		foreach ($movies as $movie) {
			echo '<li>
			<a href="./?title='.urlencode($movie["title"]).'">'.$movie["title"].'</a>
			</li>';
		}
		echo "</ul>";
	}
?>
</body>
</html> 