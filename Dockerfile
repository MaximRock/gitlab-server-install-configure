# Отдельный "сборочный" образ
FROM python:3.12-slim-bullseye AS compile-image
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt


# Образ, который будет непосредственно превращаться в контейнер
FROM python:3.12-slim-bullseye AS run-image
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY bot /app/bot
CMD [ "python", "bot/main.py" ]
