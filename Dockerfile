FROM python:3.11

WORKDIR ./.

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "8000"]

ENTRYPOINT ["python3", "-m","http.setver"]
CMD ["5000"]