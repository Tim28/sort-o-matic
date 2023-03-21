ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
    apk add --no-cache python3 py3-pip


# Python 3 HTTP Server serves the current working dir
# So let's set it to our add-on persistent data directory.
WORKDIR /app

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY sort-o-matic/* /app

CMD [ "/run.sh" ]
