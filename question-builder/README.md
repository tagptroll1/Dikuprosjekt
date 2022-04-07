# Question builder console application

---

## Installing with pipenv

```
pip install pipenv
pipenv install
pipenv run start
```

---

## Installing with pip

```
pip install -r requirements.txt
python submit_question.py
```

---

## Requirements

A `.env` file or system environment variables for `API_KEY` and `API_URL`

`question_template.json` is a template of what the questions look like for manual creation.  
The only way to manually write them and send them is to spin up a session, press 1 to create
a questions save, press ctrl+c to abort that and go back to menu. Now manually copy paste
the manually created list into the created save, then press send on the menu. It reads the json
on selection so changes should send.  
You will be promped with a message saying cache does not match save, just tell it to send the save.

---

For normal use use the terminal, select options, create questions, confirm them with the print options
and press send when finished.
