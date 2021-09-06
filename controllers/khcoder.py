from flask import Blueprint, render_template, request
from get_data import get_basic_data, get_novels_tuple, get_khcoder_df

khcoder_page = Blueprint(
    'khcoder', __name__, url_prefix='/khcoder')


@khcoder_page.route('', methods=['GET', 'POST'])
def show():
    """
    KH Coder

    """
    # 基本情報
    basic_data = get_basic_data(title='KH Coder', active_url='KH-coder')
    # 江戸川乱歩作品関連の情報
    novels_data = get_novels_tuple(col1='name', col2='file_name')

    if request.method == 'GET':
        return render_template('khcoder.html', basic_data=basic_data, novels_data=novels_data)

    # 利用者から送られてきた情報を基にデータ整理
    name, file_name = request.form['name'].split('-')
    sent_data = dict(name=name, file_name=file_name,
                     text_chapter=get_novels_tuple(novels=get_khcoder_df(file_name), col1='テキスト', col2='章'))

    return render_template('khcoder.html', basic_data=basic_data, novels_data=novels_data, sent_data=sent_data)
