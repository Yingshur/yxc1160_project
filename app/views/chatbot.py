import os

from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory,session, jsonify
from app.mixed.emails import verification_email, confirmation_email, approval_email, new_confirmation_email, rejection_email
import folium
from app.models import User, Emperor, \
    Verification, Invitation, Image, TemporaryEmperor, TemporaryImage, War, TemporaryWar, Architecture, TemporaryArchitecture, Literature, TemporaryLiterature, Artifact, TemporaryArtifact, LogBook, Deletion, Version, CurrentVersion, NewVersion
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, ChangeEmailForm, RegisterForm, RegisterEmail, \
    AdminCodeForm, InvitationCodeForm, AllEmperorForm, WarForm, ArchitectureForm, ImageEditForm, ImageUploadForm, LiteratureForm, ArtifactForm, DeleteForm, ChatForm
import re
from huggingface_hub import InferenceClient
from flask import Blueprint

chatbot_bp = Blueprint("chatbot_bp", __name__)

token_ = os.getenv("HUGGINGFACE_API_KEY")
model_ready = False
client = None

def client_setting(ai_client):
    global client, model_ready
    client = ai_client
    model_ready = True


def readiness_test():
    return model_ready and client is not None

def background_chatbot():
    global client, model_ready
    try:
        print("Initialization starts!")
        client = InferenceClient(
            provider="groq",
            api_key=token_,
        )
        client.chat.completions.create(model="meta-llama/Meta-Llama-3-8B-Instruct",
                                                messages=[{"role": "user", "content": "Hello World!"}], max_tokens=5)
        client_setting(client)
        print("Success!")
    except Exception as exception_:
        print(f"Not working, Error: {exception_}")


@chatbot_bp.route('/chatbot', methods = ["GET", "POST"], endpoint = "chatbot")
def chatbot():
    global client, model_ready
    form = ChatForm()
    text_ = None
    if not model_ready:
        flash("AI chatbot is still loading, please wait for a few seconds.")
        return render_template("chatbot.html", text_=None, title="Chatbot", form=form)

    if form.validate_on_submit():
        user_input = form.chat_content.data
        if user_input:
            result = client.chat.completions.create(model="meta-llama/Meta-Llama-3-8B-Instruct", messages=[
                {"role": "system",
                 "content": "Keep the answer concise please, 15 sentences should be the maximum! It is preferable to keep the answer between ten and fifteen sentences! Also, complete sentences only!"},
                {
                    "role": "system",
                    "content": (
                        "Only answer topics related to the Roman Empire and Eastern Roman Empire.\n"
                        "Place a strong focus on the Macedonian dynasty, Doukas dynasty, Komnenos dynasty, Angelos dynasty, and Palaiologos dynasty.\n"
                        "Topics related to other dynasties and periods can still be answered.\n"
                        "Good topics include Eastern Roman Emperors, wars (battles), domestic political struggles, literature, architecture, and artifacts.\n"
                        "Also answer questions about the Byzantine Empire's allies and enemies, such as the Bulgars, Cumans, Pechenegs, and Ottoman Turks.\n"
                        "Other topics include foreign relations of the Empire, even with distant lands as far as East Asia and Africa.\n"
                        "Please do answer regular greeting questions such as 'Hello', 'Good morning' and 'Good evening'\n"
                        "For irrelevant topics, please just reply 'Irrelevant topic, please ask a Byzantine/Roman related question!'."
                    )
                },
                {"role": "system",
                 "content": "I only want answers, not the process of thinking! !Important! Only direct answers! I do not want anything related to <think>! For example, when I ask about Roman Empire just tell me about relevant information!" },
                {"role": "user", "content": user_input}], max_tokens=300)
            text_ = result.choices[0].message.content.strip()
            all_sentences = re.split(r"(?<=[.!?]) +", text_)
            if len(all_sentences) > 15:
                text_ = " ".join(all_sentences[:15]).strip()

    return render_template("chatbot.html", text_ = text_, title = "Chatbot", form = form)

