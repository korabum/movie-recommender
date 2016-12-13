<?php

if (isset($_GET['title'])) {
	$url = './get_plot_summary/' . $_GET["title"];
	$content = file_get_contents($url);
	$json = json_decode($content, true);

	// $content = file_get_contents('./status0');
	// $json = json_decode($content, true);
	if ($json["status"] == 0) {
		$plot = $json["plot"];
		$title = $json["title"];
	} else if ($json["status"] == 1) {
		$movies = $json["movies"];
	} else if ($json["status"] == 404) {
		print_r("Not Found");
	}

}

if (isset($_POST['similar_title'])) {
	$url = './get_similar_movies/' . $_POST["title"];
	$content = file_get_contents($url);
	$json = json_decode($content, true);

	// $content = file_get_contents('./output');
	// $json = json_decode($content, true);
	if ($json["status"] == 0) {
		$similar_movies = $json["movies"];
	} else if ($json["status"] == 404) {
		print_r("Not Found");
	}
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
	if (isset($title)) {
		echo "Title: ".$title."<br>";
		echo "Plot summary:<br>".$plot;
		echo '<form action="" method="post">
			<input type="hidden" value="'.$title.'" name="similar_title">
			<input type="submit" value="Get Similar Movies">
			</form>';

	}

	if (isset($movies)) {
		echo "<ul>";
		foreach ($movies as $movie) {
			echo '<li>
			<a href="./?title='.$movie["title"].'">'.$movie["title"].'</a>
			</li>';
		}
		echo "</ul>";
	}

	if (isset($similar_movies)) {
		echo "<ul>";
		foreach ($similar_movies as $movie) {
			echo '<li>Title: '.$movie["title"].'<br>
			Plot summary: '.$movie["plot"].'</li>';
		}
		echo "</ul>";
	}
?>
</body>
</html> 