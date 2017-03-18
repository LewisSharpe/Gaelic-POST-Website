% rebase("base.tpl", title="PoS Tagger", menu_type="home", page_name = "Tagger Demo")

<p>
    In order to do some statistics on the usage of the API, we would like to archive your IP address.<br>
    You can choose to opt out of this by unchecking the checkbox.<br>
    Please note that this is only for demonstration  purposes. If you want to use this service for your research project or in your own apps, please <a href="{{base_url}}contact">contact us</a>.
</p>

<h2>Tagger</h2>
<div class="row">
    <h3>Default tagger</h3>
    <div class="col-md-12">
	<form action="{{base_url}}tag/default/file" method="POST" enctype="multipart/form-data">
	    <h3>File</h3>
	    <div class="checkbox">
		<label>
		    <input type="checkbox" name="ip" value="1" checked> <em>Yes, you can collect my IP</em>
		</label>
	    </div>
	    <input type="hidden" name="application" value="Web form">
	    <div class="form-group">
		<label>
		    Choose a file on your drive:
		    <input type="file" name="file" />
		</label>
	    </div>
	    <div class="form-group">
		<input type="submit" value="Send"/>
	    </div>
	</form>
    </div>

    <div class="col-md-12">
	<form action="{{base_url}}tag/default/string" method="POST">
	    <h3>String</h3>
	    <div class="checkbox">
		<label>
		    <input type="checkbox" name="ip" value="1" checked> <em>Yes, you can collect my IP</em>
		</label>
	    </div>
	    <input type="hidden" name="application" value="Web form">
	    <div class="form-group">
		<label>
		    Input the text to tokenise:
		    <input type="text" name="text" class="form-control"/>
		</label>
	    </div>
	    <div class="form-group">
		<input type="submit" value="Send"/>
	    </div>
	</form>
    </div>

    <h3>Simplified tagger</h3>
    <div class="col-md-12">
	<form action="{{base_url}}tag/simplified/file" method="POST" enctype="multipart/form-data">
	    <h3>File</h3>
	    <div class="checkbox">
		<label>
		    <input type="checkbox" name="ip" value="1" checked> <em>Yes, you can collect my IP</em>
		</label>
	    </div>
	    <input type="hidden" name="application" value="Web form">
	    <div class="form-group">
		<label>
		    Choose a file on your drive:
		    <input type="file" name="file" />
		</label>
	    </div>
	    <div class="form-group">
		<input type="submit" value="Send"/>
	    </div>
	</form>
    </div>

    <div class="col-md-12">
	<form action="{{base_url}}tag/simplified/string" method="POST">
	    <h3>String</h3>
	    <div class="checkbox">
		<label>
		    <input type="checkbox" name="ip" value="1" checked> <em>Yes, you can collect my IP</em>
		</label>
	    </div>
	    <input type="hidden" name="application" value="Web form">
	    <div class="form-group">
		<label>
		    Input the text to tokenise:
		    <input type="text" name="text" class="form-control"/>
		</label>
	    </div>
	    <div class="form-group">
		<input type="submit" value="Send"/>
	    </div>
	</form>
    </div>
</div>
