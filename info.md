#2022-11-26 SAT @10전비 나래생활관 싸지방

## S-RIM 적정주가 계산법
- 기업가치 = 자기자본 + (초과이익/할인율)
    : 자기자본 = 지배기업소유주지분(지배주주지분)
    : 할인율 = BBB- 등급 회사채 5년 수익률 (매일 갱신) https://www.kisrating.com/ratingsStatistics/statics_spread.do
    : 초과이익 = 자기자본 * (가중평균 3년 ROE - 할인율)
- 적정주가 = 기업가치 / 유통주식수

## Open DART API
- API Key: b64695f3f2a79d07bde772ffa630f935e0d050c0


## 프로젝트 계획 (와꾸)
- 종목코드 DB 구성 (유통주식수 포함) (분기별? 월별? 업데이트)
- 할인율 매일 크롤링
- 가중평균 3년 ROE는 연초에 계산해서 종목 DB와 같이 저장
- 자기자본 분기별 업데이트
    => 매일 할인율에 따라 기업가치만 다시 계산하면 적정주가 계산 가능
- 현재가 API로 get
- (적정주가 - 현재가) 내림차순으로 정렬!

### 고민점
1. 종목 DB
    - 우선주 제외?
    - 리츠 주 제외?