from flask import Blueprint, render_template, request, flash
from get_data import get_basic_data, dict_in_list2csv
from morphological import mrph_analysis, get_morphological_analysis_description_dict

morph_analysis_page = Blueprint(
    'morph_analysis', __name__, url_prefix='/morphological-analysis')


@morph_analysis_page.route('', methods=['GET', 'POST'])
def show():
    """
    形態素解析

    """
    # 基本情報
    basic_data = get_basic_data(title='形態素解析', active_url='morph_analysis')
    # 形態素解析器の説明文
    description = get_morphological_analysis_description_dict()
    # リクエストがGETならば
    if request.method == 'GET':
        return render_template('morphological.html', basic_data=basic_data, mrph_type='None', description=description)

    # 送信されたデータの取得と形態素解析器の種類
    text = request.form.get('words')
    mrph_type = request.form.get('mrph')
    # テキストが入力されなかった場合
    if not text:
        flash('テキストが入力されていません。', 'error')
        return render_template('morphological.html', basic_data=basic_data, mrph_type='None', description=description)
    # 形態素解析
    mrph_result, divide_dict = mrph_analysis(mrph_type, text)
    # 形態素解析の結果が返ってこなかった場合
    if not mrph_result:
        flash('解析に失敗しました。テキストデータが大きすぎます。', 'error')
        return render_template('morphological.html', basic_data=basic_data, mrph_type=mrph_type, description=description, mrph_data=dict(words=text))

    # mrph_resultをcsvとして保存し、df, csv_nameを取得
    result_df, csv_name = dict_in_list2csv(mrph_result, divide_dict)
    # 形態素解析結果をまとめるデータ群
    mrph_data = dict(words=text, result_df=result_df[:50], csv_name=csv_name,
                     over50=50 < len(result_df), columns_num=len(result_df.columns))

    return render_template('morphological.html', basic_data=basic_data, mrph_type=mrph_type, description=description, mrph_data=mrph_data)