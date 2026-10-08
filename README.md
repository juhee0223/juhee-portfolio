# Park Juhee · Portfolio

[박주희 포트폴리오](https://juhee0223.github.io/modoodoc-portfolio/)

기획·풀스택 개발·실서비스 운영, AI 도구를 활용한 구현과 직접 확인 경험을 소개합니다.
단짠과 의료 AI 해커톤을 대표 사례로 구성했습니다.

## 수정 및 빌드

```sh
python3 build.py
python3 -m http.server 8765
```

- `content.json`: 공개용 프로젝트·연구·활동 내용
- `build.py`: 공통 레이아웃과 정적 HTML 생성
- `styles.css`, `site.js`: 반응형 스타일·프로젝트 필터·메뉴
- `assets/`: 공개 가능한 서비스 화면과 설명 자료

빌드한 HTML을 함께 커밋합니다. GitHub Pages는 `main` 브랜치의 루트를 게시합니다.
이 저장소는 독립 배포되며 기존 CJ 제출용 사이트를 변경하지 않습니다.
서비스 화면은 팀 공동 산출물입니다. 개인 기여와 팀 성과, 운영된 기능과 배포 예정 기능을 구분해 기재했습니다.
