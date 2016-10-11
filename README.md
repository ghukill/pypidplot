# pypidplot
Graph CPU and Memory Usage of Linux PID with Python / Plotly

## Prep and Configure

pypidplot requires a [Plotly](https://plot.ly/) account.  It is free for limited usage, and quite great.

**Install dependencies**
<pre><code>pip install -r requirements.txt
</code></pre>

**Init Plotly API configuration file with API token**
* generate API token here: [https://plot.ly/settings/api](https://plot.ly/settings/api)
* then...
<pre><code>import plotly
plotly.tools.set_credentials_file(username='YOUR_USERNAME', api_key='YOUR_API_KEY')</code></pre>

**Add streaming ID token**
* create streaming token here: [https://plot.ly/settings/api](https://plot.ly/settings/api)
* edit plotly config file (should exist from init above), `~/.plotly/.credentials`:
<pre><code>{
        "username": "YOUR_USERNAME",
        "stream_ids": [ADD_STREAMING_TOKEN_HERE],
        "api_key": "YOUR_API_KEY"
}</code></pre>


