mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"mk16ms028@iiserkol.ac.in\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml