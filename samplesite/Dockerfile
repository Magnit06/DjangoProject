FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .
COPY entrypoint.sh .

RUN python -m pip install --upgrade pip
RUN pip list --outdated && pip install --upgrade wheel && pip install --upgrade setuptools && pip install psycopg2
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]