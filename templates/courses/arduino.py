{% extends "base.html" %}
{% block content %}
<form method="post" action="/courses/arduino/send_code/">
<textarea name="code"></textarea>
<input type="submit" value="Send Code" />
</form>
{% endblock %}