% rebase("base.tpl", title="Tokens", menu_type="infos", page_name="Tokens")

<p><strong>Number of unique tokens:</strong> {{len(tokens)}}</p>
<table class="table">
    <tr>
	<th>Token</th>
	<th>Number of uses</th>
	<th>Frequency</th>
    </tr>
    % for t in tokens:
    <tr>
	<td><a href="{{base_url}}infos/token?{{urlencode({"token" : t[0]})}}">{{t[0]}}</a></td>
	<td>{{t[1]}}</td>
	<td>{{"%.2f" % (t[1] / total * 100)}}%</td>
    </tr>
    % end
</table>
