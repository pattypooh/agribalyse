FROM python:3.8

RUN mkdir -p /agribalyse

WORKDIR /agribalyse

COPY . /agribalyse

EXPOSE 8889

RUN echo "Files copied to agribalyse "
RUN pip install -r requirements.txt

#CMD jupyter lab --ip=* --port=8889 --allow-root --no-browser

