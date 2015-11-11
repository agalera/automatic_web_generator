<html>
    <head>
        <!-- load css -->
        <link rel="stylesheet" type="text/css" href="/main.css">
    </head>
    <body>
        <div id="header">
            <div id="avatar_url">
                <img src="{{ info.avatar_url }}" width="100%"/>
            </div>
            <div id="header_text">
                <h1><div id="name">{{ info.name }}</div></h1>
                GitHub: <a href="{{ info.html_url }}">{{ info.html_url }}</a><br />
                Public Repos: {{ info.public_repos }}<br />
                Public Gists: {{ info.public_gists }}<br />
                From: {{ info.location }}<br />
                Email: {{ info.email }}
            </div>
        </div>
    <div id="body">