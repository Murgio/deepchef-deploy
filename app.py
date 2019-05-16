# coding=utf-8
from utils_food import get_corresponding_recipes
from chefkoch_parser import ChefkochParser
from predict_food import PredictFood
from werkzeug.utils import secure_filename
from flask import Flask, redirect, url_for, request, render_template, stream_with_context, Response, send_from_directory, jsonify
import os
from google_drive_downloader import GoogleDriveDownloader as gd
import pathlib
import json
from datetime import datetime
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


#from log_food import LogFood
#from gevent.wsgi import WSGIServer

# Define a flask app
app = Flask(__name__)
#app.config['MEDIA_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '/Extracting-food-preferences-master/notebooks/input')

def check_models_exist():
    # Download main csv file first
    gd.download_file_from_google_drive(file_id='1FfifIKiBKy5nfTewrovsq8lzsSVrr6F_', dest_path='./meta/chefkoch.csv')
    files_id = ['1LlIKnuQka6uNyalozbuTlSSCEuRmyRam', '19nvL3R2WpLlqIrh2KFoooWl4aQ48vWL2', '1SIp3bkGiRCQks9HTEqkqZXYTEO05IniR', '1qGqMfRuI1rsuUPH6vxPigy0yT9YL1ime']
    files_name = ['inceptionv3_4_new_ohne_dpot_2.97270.hdf5', 'sklearn_ipca_object.p', 'image_features_pca_nmslib_index.bin', 'image_paths.hdf5']
    def download_all_models():
        for file_id, file_name in zip(files_id, files_name):
            gd.download_file_from_google_drive(file_id=file_id, dest_path='./models/' + file_name)
    d = pathlib.Path('./models')
    if not d.exists():
        d.mkdir(parents=True, exist_ok=True)
        download_all_models()
    else:
        for file_id, file_name in zip(files_id, files_name):
            m = pathlib.Path('./models/' + file_name)
            if not m.exists():
                gd.download_file_from_google_drive(file_id=file_id, dest_path='./models/' + file_name)


def result_as_json(result_list, chefkoch_rezepte_csv):
    # JSON as String
    result_as_json_string = get_corresponding_recipes(result_list, chefkoch_rezepte_csv).drop(['Unnamed: 0', 'link'], 1,
                                                                                              inplace=False).to_json(force_ascii=False)
    return json.loads(result_as_json_string)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# @app.route('/images/<path:filename>')
# def custom_static(filename):
#    print(filename)
#    return send_from_directory(app.config['MEDIA_FOLDER'], filename)


@app.route('/predict', methods=['GET', 'POST'])
def streamed_response():
    if request.method == 'POST':
        # logger.new_request()
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath,
                                 'uploads',
                                 secure_filename(f.filename))
        upload_path = pathlib.Path('./uploads')
        if not upload_path.exists():
            upload_path.mkdir(parents=True, exist_ok=True)
        f.save(file_path)

        # [['category', incep_confidence, recipe_id, image_index, image_path], [], ...]
        start = datetime.now()
        result_list, inc_result, ann_result = predict_food_result.model_predict(
            file_path)
        #TODO: Don't include the same recipe more than once.
        result_json = result_as_json(
            result_list, predict_food_result.chefkoch_rezepte)
        end = datetime.now()
        food_time = end-start
        # logger.new_calc_time(food_time.microseconds*(1/1000000)) # seconds

        parser.update_result_list(result_list)

        # Log result food ids
        food_ids = [food_id[2] for food_id in result_list]
        # logger.new_food_ids(food_ids)

        # Log result food image indexes
        image_indexes = [food_id[3] for food_id in result_list]
        # logger.new_image_indexes(image_indexes)

        # Log inception result and ann results
        #inc_result = dict((pred[0], float(pred[1])) for pred in inc_result)
        # logger.new_inc_result(inc_result)
        # logger.new_ann_result(ann_result)

        food = parser.food_list_html()
        # logger.flush()
        # return jsonify(result_json)
        return ''.join(map(str, food))
    # def upload():
    #        for i, id in enumerate(ids):
    #            yield food_list_html(id_food=id, i=i)
    # return Response(stream_with_context(upload()))
    return None


if __name__ == '__main__':
    check_models_exist()
    parser = ChefkochParser()
    predict_food_result = PredictFood(k=20)
    #logger = LogFood(path='meta/log_food.json')
    app.run(host='0.0.0.0', port=5042, debug=False)

    # Serve the app with gevent
    #http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
