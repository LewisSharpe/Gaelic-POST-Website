<!doctype html>
<html>
    <head>
        <title>Gaelic POST</title>
	<meta charset="utf-8"/>
	<link href="static/style.css" rel="stylesheet"/>

    </head>

    <body>
	<div id="page">
	    <h1 id="top">Gaelic Tagger API</h1>

	    <div id="content">
		<p>
		    In order to do some statistics on the usage of the API, we would like to archive your IP address.<br>
		    You can choose to opt out of this by unchecking the checkbox.
		</p>

		<h2>Tokenise</h2>
		<form action="/tokenise/file" method="POST" enctype="multipart/form-data">
		    <h3>A file</h3>
		    <label>
			<input type="checkbox" name="ip" value="1" checked> <em>Yes, you can collect my IP</em>
		    </label>
		    <br>
		    <input type="hidden" name="application" value="Web form">
		    <label>
			Choose a file on your drive:
			<input type="file" name="file" />
		    </label>
		    <br>
		    <input type="submit" value="Send" class="form-control"/>
		</form>

		<form action="/tokenise/string" method="POST">
		    <h3>A string</h3>
		    <label>
			<input type="checkbox" name="ip" value="1" checked> <em>Yes, you can collect my IP</em>
		    </label>
		    <br>
		    <input type="hidden" name="application" value="Web form">
		    <label>
			Input the text to tokenise:
			<input type="text" name="text" class="form-control" />
		    </label>
		    <br>
		    <input type="submit" value="Send" class="form-control"/>
		</form>

		<h2>Tag</h2>
	    	<form action="/tag/default/file" method="POST" enctype="multipart/form-data">
		    <h3>A file</h3>
		    <label>
			<input type="checkbox" name="ip" value="1" checked> <em>Yes, you can collect my IP</em>
		    </label>
		    <br>
		    <input type="hidden" name="application" value="Web form">
		    <label>
			Choose a file on your drive:
			<input type="file" name="file" />
		    </label>
		    <br>
		    <input type="submit" value="Send" class="form-control"/>
		</form>
		<form action="/tag/default/string" method="POST">
		    <h3>A string</h3>
		    <label>
			<input type="checkbox" name="ip" value="1" checked> <em>Yes, you can collect my IP</em>
		    </label>
		    <br>
		    <input type="hidden" name="application" value="Web form">
		    <label>
			Input the text to tokenise:
			<input type="text" name="text" class="form-control"/>
		    </label>
		    <br>
		    <input type="submit" value="Send" class="form-control"/> 
		</form>
	    </div>
	</div>
    </body>
</html>
