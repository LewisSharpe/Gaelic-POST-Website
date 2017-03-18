% rebase("base.tpl", title="API Calls", menu_type="infos", page_name="API Calls")

<p>You can click on an IP adress to know more about it.<br/>
    Otherwise click on the green arrow to access details about a particular API call.</p>
<p><a href="{{base_url}}infos/map">See on a map</a></p>

<table class="table">
    <tr>
	<th>Date</th>
	<th>IP address</th>
	<th>Application</th>
	<th>Method</th>
	<th>Details</th>
    </tr>

    % for api_call in api_calls:
    <tr>
	<td>{{api_call[4].strftime("%d/%m/%Y - %H:%M")}}</td>
	<td>
	    % if api_call[2] is not None:
	    <a href="{{base_url}}infos/ip/{{api_call[2]}}">{{api_call[2]}}</a>
	    % else:
	    -
	    % end
	</td>
	<td>{{ api_call[3] }}</td>
	<td>{{ api_call[1] }}</td>
	<td><a href="{{base_url}}infos/api_calls/{{api_call[0]}}"><img src="{{base_url}}static/go.png" width="24px"></a></td>
    </tr>
    % end
</table>
