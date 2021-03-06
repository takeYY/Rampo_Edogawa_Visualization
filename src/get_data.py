import pandas as pd
import datetime
import random
import string


def get_hinshi_dict():
    return dict(meishi='名詞', doushi='動詞', keiyoushi='形容詞', fukushi='副詞', kandoushi='感動詞')


def get_co_oc_strength_dict():
    return dict(jaccard='Jaccard係数（0.0〜1.0）', dice='Dice係数（0.0〜1.0）', simpson='Simpson係数（0.0〜1.0）',
                frequency='共起頻度（0〜∞）', pmi='相互情報量（-∞〜∞）')


def get_edogawa_df():
    return pd.read_csv('csv/edogawa.csv')


def get_edogawa_detail_df():
    return pd.read_csv('csv/edogawa_detail.csv')


def get_original_text_df():
    return pd.read_csv('csv/original_text.csv')


def get_edogawa_merge_df(drop_duplicates=False):
    edogawa = get_edogawa_df()
    edogawa_detail = get_edogawa_detail_df()
    original_text = get_original_text_df()
    edogawa_merge = pd.merge(edogawa, edogawa_detail, on='reader_id')
    edogawa_merge = pd.merge(edogawa_merge, original_text, on='reader_id')
    if drop_duplicates:
        edogawa_merge = edogawa_merge.drop_duplicates(subset='name')

    return edogawa_merge


def get_edogawa_merge_with_rows_df():
    edogawa_merge = get_edogawa_merge_df()
    rows_list = []
    edogawa = get_edogawa_df()
    for idx, rows in edogawa.iterrows():
        row_name = rows['name']
        df = edogawa_merge.query(' name == @row_name ')
        rows_list.append(len(df))
    edogawa_detail = get_edogawa_detail_df()
    original_text = get_original_text_df()
    edogawa['rows_num'] = rows_list
    edogawa_merge = pd.merge(edogawa, edogawa_detail, on='reader_id')
    edogawa_merge = pd.merge(edogawa_merge, original_text, on='reader_id')
    return edogawa_merge


def get_khcoder_df(file_name):
    return pd.read_csv(f'csv/khcoder/{file_name}.csv')


def get_jumanpp_df(file_name):
    return pd.read_csv(f'csv/jumanpp/{file_name}.csv')


def get_mecab_df(file_name):
    return pd.read_csv(f'csv/mecab/{file_name}.csv')


def get_basic_data(title='ホーム', active_url='home'):
    return dict(title=title, active_url=active_url)


def get_novels_tuple(novels=get_edogawa_df(), col1='name', col2='file_name'):
    novels_col1 = list(novels[col1])
    novels_col2 = list(novels[col2])
    return list(zip(novels_col1, novels_col2))


def mecab_divide_dict():
    return {'surface': '表層形', 'hinshi': '品詞', 'hinshi_detail_1': '品詞細分類(1)', 'hinshi_detail_2': '品詞細分類(2)',
            'hinshi_detail_3': '品詞細分類(3)', 'katsuyou_type': '活用型', 'katsuyou_form': '活用形', 'genkei': '原形',
            'yomi': '読み', 'hatsuon': '発音'}


def juman_divide_dict():
    return {'midashi': '見出し', 'yomi': '読み', 'genkei': '原形', 'hinshi': '品詞', 'bunrui': '品詞細分類',
            'katsuyou1': '活用型', 'katsuyou2': '活用形', 'imis': '意味情報', 'repname': '代表表記'}


def get_plotly_symbols():
    return ['circle', 'square', 'diamond', 'cross', 'x', 'star', 'hexagram',
            'star-triangle-up', 'star-triangle-down', 'star-square', 'star-diamond',
            'circle-open', 'square-open', 'diamond-open', 'cross-open', 'x-open', 'star-open', 'hexagram-open',
            'star-triangle-up-open', 'star-triangle-down-open', 'star-square-open', 'star-diamond-open',
            'circle-dot', 'square-dot', 'diamond-dot', 'cross-dot', 'x-dot', 'star-dot', 'hexagram-dot',
            'star-triangle-up-dot', 'star-triangle-down-dot', 'star-square-dot', 'star-diamond-dot',
            'circle-open-dot', 'square-open-dot', 'diamond-open-dot', 'cross-open-dot', 'x-open-dot', 'star-open-dot', 'hexagram-open-dot',
            'star-triangle-up-open-dot', 'star-triangle-down-open-dot', 'star-square-open-dot', 'star-diamond-open-dot']


def get_plotly_text_positions():
    return ['top center', 'top right', 'middle right', 'bottom center', 'bottom right']


def get_datetime_now(hours: int = 9):
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=hours)))\
                   .strftime('%Y_%m_%d_%H_%M_%S%f')


def create_category_df(df: pd.DataFrame):
    try:
        big_captions = [big if big == big else ''
                        for big in df['大見出し'].tolist()]
        middle_captions = [middle if middle == middle else ''
                           for middle in df['中見出し'].tolist()]
        small_captions = [small if small == small else ''
                          for small in df['小見出し'].tolist()]
        categories = []
        for big, middle, small in zip(big_captions, middle_captions, small_captions):
            category = ''
            if big:
                category += big
            if middle:
                category += f'_{middle}' if category else middle
            if small:
                category += f'_{small}' if category else small
            categories.append(category)
        df['カテゴリー'] = categories
    except:
        print('カテゴリーは作成できませんでした。')

    return df


def get_category_list(csv_filename):
    csv_path = 'csv/mecab'
    df = create_category_df(pd.read_csv(f'{csv_path}/{csv_filename}.csv'))
    return df['カテゴリー'].unique().tolist()


def create_random_string(n):
    rand_str_list = [random.choice(string.ascii_letters + string.digits)
                     for i in range(n)]
    return ''.join(rand_str_list)


def save_df(df):
    csv_name = f'{get_datetime_now()}_mrph'
    df.to_csv(f'tmp/{csv_name}.csv', index=False, encoding='utf_8_sig')
    return csv_name
