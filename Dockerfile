FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get clean && apt-get update && apt-get install -y locales

RUN sed -i 's/^# *\(fa_IR.UTF-8\)/\1/' /etc/locale.gen
RUN locale-gen


COPY requirements/ ./requirements/
RUN pip install --upgrade pip && pip install -r requirements/dev.txt

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
