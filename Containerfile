# vim: set filetype=dockerfile
FROM registry.access.redhat.com/ubi9/ubi-minimal

ARG APP_ROOT=/app-root

RUN microdnf install -y --nodocs --setopt=keepcache=0 --setopt=tsflags=nodocs \
    python3.11 python3.11-devel python3.11-pip

# PYTHONDONTWRITEBYTECODE 1 : disable the generation of .pyc
# PYTHONUNBUFFERED 1 : force the stdout and stderr streams to be unbuffered
# PYTHONCOERCECLOCALE 0, PYTHONUTF8 1 : skip legacy locales and use UTF-8 mode
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONCOERCECLOCALE=0 \
    PYTHONUTF8=1 \
    PYTHONIOENCODING=UTF-8 \
    LANG=en_US.UTF-8 \
    PIP_NO_CACHE_DIR=off

WORKDIR /app-root

# Add explicit files and directories
# (avoid accidental inclusion of local directories or env files or credentials)
COPY pyproject.toml LICENSE README.md ./

COPY src ./src

RUN pip3.11 install --no-cache-dir .

# this directory is checked by ecosystem-cert-preflight-checks task in Konflux
COPY LICENSE /licenses/

# Run the application
EXPOSE 8080
CMD ["python3.11", "src/lightspeed_stack.py"]

LABEL vendor="Red Hat, Inc."


# no-root user is checked in Konflux
USER 1001
