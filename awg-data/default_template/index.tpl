{% include 'header.tpl' %}
    {% for repo in repos %}
        <a href="repos/{{repos[repo].name}}.html">{{repos[repo].name}}</a><br />
        {{repos[repo].description}}<br />
        <br />
    {% endfor %}
{% include 'footer.tpl' %}