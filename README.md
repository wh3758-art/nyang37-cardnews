# nyang37 카드뉴스 자동 게시

인스타그램 [@nyang37_](https://www.instagram.com/nyang37_/) 의 뉴스 카드뉴스를 만들고 게시하는 저장소입니다.

## 흐름

1. **카드 만들기 (Claude 예약 작업, 평일 오전 7:37):** 뉴닉 레터로 주제를 고르고 원 기사·공식 발표를 조사해 `cards/<날짜>/01.html ~ 06.html` 과 `caption.txt` 를 올립니다.
2. **이미지 만들기 (GitHub Actions `카드 이미지 만들기`):** 카드가 올라오면 자동으로 1080×1350 JPG 로 바꿔 `images/<날짜>/` 에 저장합니다.
3. **게시**
   - 검토 후 게시 (기본): GitHub 앱 → 이 저장소 → Actions → `인스타그램 게시` → **Run workflow**
   - 완전 자동: 저장소 변수 `AUTO_POST` 를 `true` 로 바꾸면 2번이 끝나자마자 바로 게시됩니다.

> 저장소는 **공개(Public)** 여야 합니다. 인스타그램이 raw.githubusercontent.com 주소에서 이미지를 직접 가져가기 때문이에요.

## 처음 한 번만 하는 설정

### 1. 인스타그램 계정
- 인스타그램을 프로페셔널(크리에이터 또는 비즈니스) 계정으로 전환
- 페이스북 페이지를 만들고 인스타그램 계정과 연결

### 2. Meta 개발자 앱과 토큰 (모두 무료)
1. https://developers.facebook.com 에 페이스북 계정으로 로그인 → **내 앱 → 앱 만들기** (용도: 인스타그램 콘텐츠 관리 / 유형: 비즈니스)
2. **Graph API 탐색기** (https://developers.facebook.com/tools/explorer) 에서 방금 만든 앱을 선택하고 권한 추가:
   `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`, `business_management`
   → **Generate Access Token** → 로그인하고 페이지·인스타 계정 모두 허용
3. **액세스 토큰 디버거** (https://developers.facebook.com/tools/debug/accesstoken) 에 토큰을 넣고 **액세스 토큰 연장** → 장기 토큰(60일)이 나옵니다.
4. 다시 Graph API 탐색기에서 장기 토큰으로 `me/accounts` 를 조회 → 내 페이지의 `access_token` 이 **만료 없는 페이지 토큰**입니다. → 이것이 `IG_ACCESS_TOKEN`
5. 같은 곳에서 `<페이지 id>?fields=instagram_business_account` 조회 → 나오는 `id` 가 `IG_USER_ID`

앱은 '개발 모드'인 채로 두어도 됩니다. 앱 관리자 본인의 계정에는 앱 검수 없이 게시할 수 있습니다.

### 3. GitHub 저장소 설정
저장소 → **Settings → Secrets and variables → Actions**
- **Secrets** 탭: `IG_USER_ID`, `IG_ACCESS_TOKEN` 추가
- **Variables** 탭: `AUTO_POST` = `false` (검토 후 게시) 또는 `true` (완전 자동)

토큰은 채팅이나 코드에 붙여넣지 말고 여기에만 넣으세요.

## 직접 실행해 보기
- 이미지 다시 만들기: Actions → `카드 이미지 만들기` → Run workflow (날짜 입력)
- 게시: Actions → `인스타그램 게시` → Run workflow
