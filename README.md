# MM.C.P.E.
_The Streamlit Mattermost Channel Post Exporter_ 

## Introduction

The MM.C.P.E. is a little program that connects to your mattermost database 
directly. It reads the channels and presents them as a dropdown box. Selecting 
a channel allows you to export all messages in that channel together with the 
name of the poster. Exports can also be downloaded in CSV format.


## Installation
- Create database.yaml 
  - _see below: Configuration_
- Create virtual environment 
  - _python3 -m venv venv_
- Activate the virtual environment 
  - _source venv/bin/activate_
- Install dependencies 
  - _pip install -r requirements.txt_
- Run the program 
  - _streamlit run main.py_

Open your web-browser http://localhost:8501 
or over the network: http://xxx.xxx.xxx.xxx:8501


## Configuration

database.yaml should contain:

```
database: 
  host: <hostname or ip> 
  user: <database_username>
  password: <database_password> 
  database: <database_name, ie mattermost> 
```


