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

?>



<html>
<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>	
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>

<div class="container">

	<div class="row">
        <div class="col-md-6">
    		<h2>Cibyl</h2>
            <div id="custom-search-input">
                <div class="input-group col-md-12">

                <form class="form-inline" action="" method="get">
	                    <input type="text" class="form-control input-lg" placeholder="Insert movie title" name="title"/>
                </form>

                </div>
            </div>
        </div>
	</div>

<?php
	if (isset($main_title)) {
		echo '<div class="list-group">';
			echo '<div class="list-group-item">';
			echo '<h4 class="list-group-item-heading">'.$main_title.'</h4>';
			echo '<p class="list-group-item-text">'.$main_plot.'</p>';
			echo '</div>';
		echo '</div>';

		echo '<h3>Similar Movies</h3>';
		echo '<div class="list-group">';
		foreach (array_reverse($similar_movies) as $movie) {
			echo '<div class="list-group-item">';
			echo '<h4 class="list-group-item-heading">'.$movie["title"].'</h4>';
			echo '<p class="list-group-item-text">'.$movie["plot"].'</p>';
			echo '<p class="list-group-item-text">Genre: '.$movie["genre"].'</p>';
			echo '<p class="list-group-item-text">Rating: '.$movie["rating"].'</p>';
			echo '</div>';
		}
		echo '</div>';
	}

	if (isset($movies)) {
		echo '<div class="row"';
		echo '<div class="list-group">';
		foreach ($movies as $movie) {
			echo '<a href="./?title='.urlencode($movie["title"]).'" class="list-group-item">'.$movie["title"].'</button>';
		}
		echo "</div>";
		echo "</div>";
	}
?>
</div>
</body>
</html> 