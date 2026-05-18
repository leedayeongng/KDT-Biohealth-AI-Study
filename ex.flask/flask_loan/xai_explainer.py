# 의사결정나무가 ‘승인/거절’을 왜 그렇게 판단했는지, 사람이 읽을 수 있는 문장으로 뽑아내는기능

import pandas as pd
import joblib


def explain_decision(model, input_df):
    """ tree 구조 파악 규칠 추출 """
    # <<1>>
    node_indicator = model.decision_path(input_df)  # 데이터가 어떤 노드를 거쳐갔는지 반환
    leaf_id = model.apply(input_df)                 # apply 메서드는 데이터가 최종적으로 도착한 리프 id 반환
    # print(node_indicator, leaf_id)
    #트리의 내부 속성에 접근
    feature = model.tree_.feature
    threshold = model.tree_.threshold
    sample_id = 0
    #데이터 노드들의 id 목록을 추출
    node_index = node_indicator.indices[node_indicator.indptr[sample_id]: node_indicator.indptr[sample_id+1]]
    reasons = []
    #데이터가 지나간 노드 목록을 처음부터 역추적하며 규칙 이유를 읽어옴
    feature_names = input_df.columns
    for node_id in node_index:
        #더 이상 조건 분기가 없으면 건너뛴다.
        if leaf_id[sample_id] == node_id:
            continue
        #현재 노드에서 어던 조건으로 분기가 이루어졌는지 체크
        if(input_df.iloc[sample_id, feature[node_id]] <= threshold[node_id]):
            threshold_sign = "<=" #작거나 같다 (트리의 왼쪽 가지로 감)
        else:
            threshold_sign =">"
        # print(threshold_sign)

        #노드의 변수
        feat_name = feature_names[feature[node_id]]
        #사용자 입력값
        val = input_df.iloc[sample_id, feature[node_id]]
        #임계값
        thresh = threshold[node_id]
        # print(feat_name, val, thresh)

        kr_names = {
            'ApplicantIncome' : '본인 연 소득'
            , 'CoapplicantIncome' : '공동신청자 소득'
            , 'LoanAmount' : '대출요청액'
            , 'Married' : '결혼여부( 1.0:기혼, 0.0:미혼 )'
        }
        kr_feat = kr_names.get(feat_name, feat_name)
        if threshold_sign == "<=" :
            reasons.append(f'사유 {kr_feat}이 기준치 ({thresh:.1f}) 이하임 (현재 입력값 : {val:.1f})')
        else :
            reasons.append(f'사유 {kr_feat}이 기준치 ({thresh:.1f}) 이하임 (현재 입력값 : {val:.1f})')
    print(reasons)
    return reasons

if __name__ == '__main__' :
    model = joblib.load('loan_model.pkl')
    # 가동여부를 확인하기 위해 임시로 넣은 데이터
    # 대출요건 만족 시 맨 앞에 0으로 출력, ['사유 공동신청자 소득이 기준치 (9974.0) 이하임 (현재 입력값 : 10000.0)']
    # 대출요건 불만족 시 맨 앞에 1로 출력, ['사유 공동신청자 소득이 기준치 (9974.0) 이하임 (현재 입력값 : 1000.0)', '사유 결혼여부( 1.0:기혼, 0.0:미혼 )이 기준치 (0.5) 이하임 (현재 입력값 : 0.0)', '사유 대출요청액이 기준치 (61.0) 이하임 (현재 입력값 : 300.0)']
    sample_data = pd.DataFrame([{
        'ApplicantIncome' : 100.0
        , 'CoapplicantIncome' : 100.0
        , 'LoanAmount' : 300000.0
        , 'Married' : 1
    }])
    pred = model.predict(sample_data)[0]
    result_text = "승인" if pred == 1 else "거절"
    print(f'심사결과 : {result_text}')
    reasons = explain_decision (model, sample_data) # <- model sample을 가져오기 <<1>>
    print('결과 사유')
    for i, reason in enumerate(reasons, 1):
        print(f' {i}. {reason}')