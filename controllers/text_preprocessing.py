from flask import Blueprint, render_template, request, flash
from src.description import preprocessing_other_options_description
from src.get_data import get_basic_data
from src.preprocessing import texts_preprocessing, get_other_option_dict

preprocessing_page = Blueprint(
    'text_preprocessing', __name__, url_prefix='/rikkyo-edogawa/text-preprocessing')


@preprocessing_page.route('', methods=['GET', 'POST'])
def show():
    """
    テキストの前処理

    """
    # 基本情報
    basic_data = get_basic_data(title='テキストの前処理',
                                active_url='preprocessing')
    # その他設定の項目取得
    other_option = get_other_option_dict()
    # 詳細説明追加
    description = dict(other_options=preprocessing_other_options_description())
    if request.method == 'GET':
        return render_template('preprocessing.html',
                               basic_data=basic_data,
                               other_option=other_option,
                               description=description)

    # 利用者から送られてきた情報を取得
    texts = request.form.get('texts')
    # textsがない場合
    if not texts:
        flash('テキストが入力されていません。', 'error')
        return render_template('preprocessing.html',
                               basic_data=basic_data,
                               ther_option=other_option,
                               description=description)

    remove_words = request.form['remove-texts']
    remove_word_in_texts = request.form['remove-text-in-texts']
    replace_words = request.form['replace-texts']
    other_options = request.form.getlist('other-option')
    # 選択されたその他設定を取得
    selected_option = [other_option.get(k) for k in other_options]
    # 送られてきた情報を基にテキストを前処理
    preprocessed_text, errors = texts_preprocessing(texts,
                                                    remove_words,
                                                    remove_word_in_texts,
                                                    replace_words,
                                                    other_options)
    # 送るデータの辞書
    sent_data_dict = dict(texts=texts, remove_texts=remove_words, remove_text_in_texts=remove_word_in_texts,
                          other_option=selected_option, replace_texts=replace_words)
    # エラーがある場合
    if errors:
        for error in errors:
            flash(error, 'error')
        return render_template('preprocessing.html',
                               basic_data=basic_data,
                               sent_data=sent_data_dict,
                               other_option=other_option,
                               description=description)
    # 送るデータをまとめる
    sent_data_dict['preprocessed_texts'] = preprocessed_text
    return render_template('preprocessing.html',
                           basic_data=basic_data,
                           sent_data=sent_data_dict,
                           other_option=other_option,
                           description=description)
