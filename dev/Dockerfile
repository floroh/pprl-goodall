FROM python:3.13-slim-trixie AS base
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends git \
 && apt-get autoremove -y \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*.deb
RUN pip install poetry
WORKDIR /opt/pprl-goodall

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY api api
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    --mount=type=cache,target=/root/.cache/pip \
    poetry config virtualenvs.in-project true && \
    poetry install --without dev --no-root --no-interaction --no-ansi

COPY dev/docker.env .env
# Export all variables in the file, skipping empty or commented lines
RUN export $(grep -v '^\s*#' .env | grep -v '^\s*$' | xargs)

COPY dev/run_goodall.sh /usr/local/bin/run_goodall.sh
RUN chmod +x /usr/local/bin/run_goodall.sh

# Ensure Poetry virtual environment is activated in every shell session
RUN echo 'export PATH="/opt/pprl-goodall/.venv/bin:$PATH"' >> ~/.bashrc

FROM base AS pprl-goodall-ui
COPY goodall/api_helper goodall/api_helper
COPY goodall/models goodall/models
COPY goodall/modifier goodall/modifier
COPY goodall/plotting goodall/plotting
COPY goodall/protocol goodall/protocol
COPY goodall/result_analysis goodall/result_analysis
COPY goodall/tracking goodall/tracking
COPY goodall/ui goodall/ui
COPY goodall/utils goodall/utils
COPY data/configs data/configs
ENV PYTHONPATH=/opt/pprl-goodall
CMD ["run_goodall.sh", "poetry", "run", "streamlit", "run", "goodall/ui/PPRL_Services_UI.py", "--server.headless", "true"]

FROM base AS pprl-goodall-cli
COPY goodall/api_helper goodall/api_helper
COPY goodall/models goodall/models
COPY goodall/modifier goodall/modifier
COPY goodall/plotting goodall/plotting
COPY goodall/protocol goodall/protocol
COPY goodall/result_analysis goodall/result_analysis
COPY goodall/tracking goodall/tracking
COPY goodall/utils goodall/utils
COPY data/configs data/configs
ENV PYTHONPATH=/opt/pprl-goodall
ENTRYPOINT ["run_goodall.sh", "poetry", "run", "python", "-m", "goodall.tracking.experiment_manager_cli"]
CMD ["status"]