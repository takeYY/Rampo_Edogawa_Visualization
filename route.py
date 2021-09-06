from flask import Flask
from controllers.index import index_page
from controllers.information import information_page
from controllers.text_preprocessing import preprocessing_page
from controllers.morphological_analysis import morph_analysis_page
# from controllers.co_oc_network_2d import network2d__page
from controllers.khcoder import khcoder_page
from controllers.others import others_page

app = Flask(__name__)
app.register_blueprint(index_page)
app.register_blueprint(information_page)
app.register_blueprint(preprocessing_page)
app.register_blueprint(morph_analysis_page)
# app.register_blueprint(network2d__page)
app.register_blueprint(khcoder_page)
app.register_blueprint(others_page)
