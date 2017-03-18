% if menu_type == "home":
% menu = [ ("GPOST API", base_url), ("About", base_url+"about"), ("Demos", base_url+"demos"), ("Documentation", base_url+"doc"), ("Contact", base_url+"contact")]
% else:
% menu = [ ("Infos", base_url+"infos"), ("API Calls", base_url+"infos/api_calls"), ("Tokens", base_url+"infos/tokens") ]
% end

<!doctype html>
<html>
    <head>
	<meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <title>{{title or 'Gaelic Tokeniser API'}}</title>
        <meta charset="utf-8"/>

	<!--<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">-->
	<link href="{{base_url}}static/bootstrap.min.css" rel="stylesheet"/>
	<link href="{{base_url}}static/bootstrap-theme.min.css" rel="stylesheet"/>
	<link href="{{base_url}}static/code.css" rel="stylesheet"/>
	
	<style>

	img.logo {
	    margin-left: 0px;
	    margin-top:0px;
	    margin-bottom:0px;
	    margin-right: 40px;
	}

	.right {
	    float:right; 
	}
	</style>
    </head>
    <body>
	<a href="http://www.iidi.napier.ac.uk"><img src="{{base_url}}static/newbanner.png" width="1000px" class="logo visible-lg-inline"/></a>
	<a href="http://www.napier.ac.uk"><img src="{{base_url}}static/logo_napier.gif" width="600px" class="logo right visible-lg-inline" /></a>
	<nav class="navbar navbar-default">
	    <div class="container">
		<div class="navbar-header">
		    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar">
			<span class="sr-only">Toggle navigation</span>
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
		    </button>
		</div>
		<div id="navbar" class="collapse navbar-collapse">
		    <a href="http://www.iidi.napier.ac.uk"><img src="{{base_url}}static/logo_iidi.png" width="200px" class="logo visible-xs-inline"/></a>
		    <a href="http://www.napier.ac.uk"><img src="{{base_url}}static/logo_napier.gif" class="logo visible-xs-inline" /></a>
		    <ul class="nav navbar-nav">
			% for item in menu:
			% menu_names = [ x[0] for x in menu]
			% if item[0] == page_name:
			% classe = "active"
			% else:
			% classe = ""
			% end
			<li class="{{classe}}"><a href="{{item[1]}}">{{item[0]}}</a></li>
			% end
		    </ul>
		</div><!--/.nav-collapse -->
	    </div>
	</nav>

	<div class="container" id="main">
	    {{!base}}

	    <br>
	    <footer>
		<p>&copy; Edinburgh Napier University</p>
	    </footer>
	</div><!-- /.container -->

	<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
    </body>
</html>
