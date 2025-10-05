from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from database import db
import os
import hashlib
import filetype

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER