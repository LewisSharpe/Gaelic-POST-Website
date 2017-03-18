% rebase("base.tpl", title="Token infos", menu_type="infos", page_name="Tokens")
<h2>Token: {{token}}</h2>
<p>Has been associated to the following tags:</p>
<ul>
    % for t in tags:
    <li>{{t[0]}} - <a href="{{base_url}}infos/api_calls/{{t[1]}}">API Call</a></li>
    % end
</ul>
