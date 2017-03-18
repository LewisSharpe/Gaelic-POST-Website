% rebase("base.tpl", title="API Call no. " + str(api_call[0]), menu_type="infos", page_name="API Calls")

<h1>API call no. {{api_call[0]}}</h1>

<p><strong>IP which issued the call:</strong>
    % if api_call[2] is not None:
    <a href="{{base_url}}infos/ip/{{api_call[2]}}">{{api_call[2]}}</a> (<a href="{{base_url}}infos/api_calls/by_ip/{{api_call[2]}}">see all requests by this IP</a>)
    % else:
    -
    % end
</p>
<p><strong>Method used:</strong> {{api_call[1]}}</p>
<p><strong>Application used:</strong> {{api_call[3]}}</p>
<p><strong>Duration:</strong> {{api_call[7]}} seconds</p>
<p><strong>Date:</strong> {{api_call[4].strftime("%d/%m/%Y - %H:%M")}}</p>
<table class="table">
    <tr>
	<th>Text</th>
	<th>Tokenised output</th>
    </tr>
    <tr>
	<td width="50%">{{api_call[5].replace("\n", "<br>")}}</td>
	<td width="50%">{{api_call[6]}}</td>
    </tr>
</table>
