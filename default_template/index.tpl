{% include 'header.tpl' %}
    {% for repo in repos %}
        <a href="repos/{{repos[repo].name}}">{{repos[repo].name}}</a><br />
        {{repos[repo].description}}<br />
        <br />
    {% endfor %}
{% include 'footer.tpl' %}