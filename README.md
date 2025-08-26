This is a user contribution-based website documenting the history of middle to late Byzantine Empire:


Features: 
Content display: Information of each category is shown in a table, which provides links to relevant articles.
Adding and editing articles: External users are allowed to contribute to the website, normal registered users’ requests are accepted, subjected to approval by administrators. 
Version control: Administrators can decide to roll back/forward to an older/newer version if deemed necessary.
AI Chatbot: LLM-powered AI Chatbot, tailored to provide answers to Byzantine/Roman related questions. 
Privacy policy: Terms and conditions are published on the registration page, no data is collected from unregistered (anonymous users).
Feedback form: Users can submit feedback by filling the form. 


Technical details:
Frontend: Predominantly HTML & CSS (under jinja2 and bootstrap framework), with minor JavaScript support
Backend: Python under Flask framework
AI Chatbot: Meta-Llama-3-8B-Instruct (free API obtained via Hugging Face)
Database: Aiven MySQL free database server


Requirements:
pip install -r requirements.txt
(important libraries including Flask, flask_login, SQLAlchemy, Folium etc.)


Run locally:


python run.py


On deployment (currently use railway.com):


gunicorn -w 4 -b 0.0.0.0:5086 app:app

Privacy: Full compliance with the GDPR.


License:
Apache 2.0 License









