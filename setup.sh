mkdir -p ~/.streamlit

echo "\
[server]\n\
port = $PORT\n
enableCORS = true\n\
headless = true\n\
\n\
" > ~/.streamlipit/config.toml