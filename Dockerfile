FROM python:3.8
WORKDIR /agribalyse

COPY . .

EXPOSE 8889

RUN echo "Files copiedto agribalyse "
RUN pip install -r requirements.txt

#CMD jupyter lab --ip=* --port=8889 --allow-root --no-browser

