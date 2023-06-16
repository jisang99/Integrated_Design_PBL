import pandas as pd
import numpy as np
import random
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.metrics.pairwise import cosine_similarity

# from domain.product.product_schema import ProductRecommendResponse

PRODUCT_RESULT_SIZE = 10
random.seed(42)

df = pd.read_csv('./products.csv')
viewed_id = [1, 2]

def make_doc2vec_models(tagged_data, tok, vector_size=128, window=3, epochs=40, min_count=0, workers=4):
    model = Doc2Vec(tagged_data, vector_size=vector_size, window=window, epochs=epochs, min_count=min_count,
                    workers=workers, seed=42)
    model.save(f'./{tok}_laptop_spec_model.doc2vec')


def make_doc2vec_data(data, column, t_document=False):
    data_doc = []
    for tag, doc in zip(data.index, data[column]):
        doc = doc.split(" ")
        data_doc.append(([tag], doc))
    if t_document:
        data = [TaggedDocument(words=text, tags=tag) for tag, text in data_doc]
        return data
    else:
        return data_doc


def get_recommend_contents(user, data_doc, model):
    scores = []

    for tags, text in data_doc:
        trained_doc_vec = model.docvecs[tags[0]]
        scores.append(cosine_similarity(user.reshape(-1, 128), trained_doc_vec.reshape(-1, 128)))

    scores = np.array(scores).reshape(-1)
    # 코사인 유사도를 통해 TOP 10 보여줌
    scores_index = np.argsort(-scores)[:PRODUCT_RESULT_SIZE]

    # 추천 노트북, 추천 노트북의 인덱스, 코사인점수 출력
    return scores_index, scores


def make_user_embedding(index_list, data_doc, model):
    user = []
    user_embedding = []
    for i in index_list:
        user.append(data_doc[i][0][0])
    for i in user:
        user_embedding.append(model.docvecs[i])
    user_embedding = np.array(user_embedding)
    user = np.mean(user_embedding, axis=0)
    return user


def view_user_history(data):
    print(data[['노트북 이름', '가격', 'category', '스펙']])


def product_recommend(df, viewed_id):
    battery_values = [999999.0, 9999.0]  # 원하는 배터리 값 리스트

    filtered_ids = df[df['배터리'].isin(battery_values)].index.tolist()
    df = df[df['배터리'] != 999999.0]
    df = df[df['배터리'] != 9999.0]

    df['스펙'] = df.apply(lambda row: f"{row['제조사']} {row['배터리']} {row['cpu']} {row['램 용량']} \
    {row['램 상세']} {row['화면크기']} {row['화면상세']} {row['그래픽']} {row['저장용량']} {row['저장용량 상세']} {row['무게']} {row['가격']} ",
                        axis=1)

    new_df = df[['id', '이름', '가격', '스펙']]

    data = new_df
    data_spec_tag = make_doc2vec_data(data, '스펙', t_document=True)
    data_sepc_content = make_doc2vec_data(data, '스펙')

    make_doc2vec_models(data_spec_tag, tok=False)
    model = Doc2Vec.load('./False_laptop_spec_model.doc2vec')

    user_category_1 = data.loc[df['id'].isin(viewed_id), :]

    user_1 = make_user_embedding(user_category_1.index.values.tolist(), data_sepc_content, model)

    result_index, cos = get_recommend_contents(user_1, data_sepc_content, model)

    filtered_ids_set = set(filtered_ids)
    result_index = np.array([idx for idx in result_index if idx not in filtered_ids_set])

    result_data = df.loc[result_index]

    cos_similarity = cos[result_index]
    cos_similarity_rounded = cos_similarity * 100
    print(cos_similarity_rounded)
    result_data['유사도'] = cos_similarity_rounded

    # data_list = result_data.to_dict('records')

    # result = []
    # for product_result in data_list:
    #     result.append(ProductRecommendResponse(
    #         product_id=product_result["id"],
    #         product_image=product_result["이미지"],
    #         product_name=product_result["이름"],
    #         similarity=round(product_result["유사도"], 2)
    #     ))

    # return result


print(product_recommend(df, viewed_id))

