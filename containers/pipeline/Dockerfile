FROM python:3.8

# Install gcloud sdk
RUN apt-get update -y && apt-get install --no-install-recommends -y -q ca-certificates wget unzip git

RUN pip install google-api-python-client

RUN cd / && \
    wget -nv https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.zip && \
    unzip -qq google-cloud-sdk.zip -d tools && \
    rm google-cloud-sdk.zip && \
    tools/google-cloud-sdk/install.sh --usage-reporting=false \
        --path-update=false --bash-completion=false \
        --disable-installation-options && \
    tools/google-cloud-sdk/bin/gcloud -q components update \
        gcloud core gsutil && \
    tools/google-cloud-sdk/bin/gcloud config set component_manager/disable_update_check true && \
    touch /tools/google-cloud-sdk/lib/third_party/google.py

ENV PATH $PATH:/tools/node/bin:/tools/google-cloud-sdk/bin


# Copy application dependency manifests to the container image.
# Copying this separately prevents re-running pip install on every code change.
COPY requirements.txt ./

# Install production dependencies.
RUN pip install -r requirements.txt

COPY . ./

ENTRYPOINT ["python","main.py"]
