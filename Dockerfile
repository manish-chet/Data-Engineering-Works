FROM python:3.10-slim

WORKDIR /site

RUN pip install --no-cache-dir mkdocs-material
RUN pip install pymdown-extensions mkdocs-mermaid2-plugin

CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]
