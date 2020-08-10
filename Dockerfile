FROM python:3.6
WORKDIR /app
RUN export PYTHONIOENCODING=utf8
# install pip
RUN pip3 install --upgrade pip -i https://pypi.douban.com/simple
COPY requirements.txt /app
RUN pip3 install --no-cache-dir  -r requirements.txt -i https://pypi.douban.com/simple
ENV LANG=C.UTF-8 C_FORCE_ROOT=true
COPY . /app
CMD python3 manage.py runserver -h 0.0.0.0 -p 5000
