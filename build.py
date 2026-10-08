#!/usr/bin/env python3
"""Build a dependency-free, public portfolio from reviewed content."""
from pathlib import Path
from html import escape
import json
import re
from hashlib import sha256

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / 'content.json').read_text())
BASE = 'https://juhee0223.github.io/juhee-portfolio'
STYLE_VERSION = sha256((ROOT / 'styles.css').read_bytes()).hexdigest()[:10]
SCRIPT_VERSION = sha256((ROOT / 'site.js').read_bytes()).hexdigest()[:10]
CATS = {'service':'서비스 개발·운영','ai':'AI 응용','systems':'시스템 연구'}
def e(s): return escape(str(s), quote=True)
def tags(items): return ''.join(f'<span>{e(x)}</span>' for x in items)
def links(items):
    result = []
    for item in items:
        external = item['url'].startswith(('https://', 'http://'))
        attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
        arrow = '↗' if external else '→'
        result.append(f'<a class="text-link" href="{e(item["url"])}"{attrs}>{e(item["label"])} <span aria-hidden="true">{arrow}</span></a>')
    return ''.join(result)

# Exact phrases already present in the reviewed copy; emphasis adds no claims.
DETAIL_HIGHLIGHTS = {
    'danzzan': ['6,063명', '3,500장', '정책을 수정', '테스트 계정을 직접 탈퇴', '업무에 필요한 범위만', '배포·시연할 예정', '10,000 VU', '중복 발급 0건', '발급 순번 갭 0건', '필수 동의 판정', '총학생회·학교·협력사와 요구사항을 조율', '현장 팔찌 배부', 'SMS 딥링크', 'required 속성과 체크 상태', '저장 트랜잭션을 행별로 분리', '미번역 데이터 0건', 'Lua 원자 처리'],
    'conquer-health': ['46.51점', '14팀 중 1위', '벤치마크상', 'HealthBench 평가 기준', 'ANSWER_INSTRUCTION', '별도 LLM 호출을 추가하지 않음', '회귀 테스트'],
    'olly': ['5개 시나리오', '각 10회', 'request_id와 trace_id', '로컬 SLM', '오류 상태를 유지한 추적', '단일 요청을 기준'],
    'sketch-to-spec': ['SRS 요구사항 명세', 'ASCII 화면 흐름', '계획 수정 루프', 'Self-Healing(Plan Revision)', '멀티모달 입력 결합'],
    'sun-date': ['봉사활동이라는 공동 경험', 'EASYTHON 2025 해커톤 우수상'],
    'gamegc': ['Greedy와 Cost-Benefit', 'Pipeline 기반 GameGC', '스파이크와 점진적 회수 패턴'],
    'dacon': ['F1 Score', '상위 10%', 'Feature engineering', '모델별 성능을 비교'],
    'bird-repeller': ['KHUTHON 2025 해커톤 우수상', '기피음을 자동 재생', 'YOLOv5 기반 조류 인식', 'Threading'],
    'rocksdb': ['제1저자', '1천만 건', '4,096B', 'Write Amplification Factor', '조회 성공 횟수', '84,097 ops/s', '64,667 ops/s', 'Hit 5,797회'],
}
def highlighted(text, slug):
    pattern = '|'.join(re.escape(e(term)) for term in sorted(DETAIL_HIGHLIGHTS.get(slug, []), key=len, reverse=True))
    if not pattern: return e(text)
    return re.sub(pattern, lambda match: f'<strong class="detail-highlight">{match.group()}</strong>', e(text))

def shell(title, body, depth='', description='서비스 기획과 개발, 배포·운영 경험부터 AI 응용과 시스템 연구까지. 박주희의 프로젝트와 문제 해결 과정을 소개하는 포트폴리오.', canonical=''):
    home = depth+'index.html' if depth else ''
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · 박주희</title><meta name="description" content="{e(description)}">
<meta name="theme-color" content="#ffffff"><meta property="og:title" content="{e(title)} · 박주희"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}/{canonical}">
<link rel="canonical" href="{BASE}/{canonical}"><link rel="icon" href="{depth}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{depth}styles.css?v={STYLE_VERSION}"><script src="{depth}site.js?v={SCRIPT_VERSION}" defer></script></head>
<body><a class="skip-link" href="#main">본문으로 바로가기</a>
<header class="site-header"><div class="nav-wrap"><a class="brand" href="{depth}index.html" aria-label="박주희 포트폴리오 홈"><span>박주희</span><small>Portfolio</small></a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">메뉴 <span aria-hidden="true">☰</span></button>
<nav id="site-nav" aria-label="주요 메뉴"><a href="{home}#projects">프로젝트</a><a href="{home}#research">논문·출판</a><a href="{home}#awards">수상</a><a href="{home}#activities">활동</a><a href="{home}#credentials">자격증·어학</a><a class="nav-contact" href="{home}#contact">연락처</a></nav></div></header>
{body}
<footer class="site-footer"><div class="container footer-inner"><p>박주희 | 포트폴리오<br><span>© 2026 Park Juhee</span></p><a href="https://github.com/juhee0223" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="#main">맨 위로 ↑</a></div></footer>
</body></html>'''

def project_image(v, depth=''):
    return f'<img src="{depth}{e(v["src"])}" alt="{e(v["alt"])}" width="{v["width"]}" height="{v["height"]}" loading="lazy" decoding="async">'

def project_visual(p):
    v = p.get('visual')
    if not v:
        return ''
    source = f'<a class="text-link" href="{e(v["source_url"])}" target="_blank" rel="noopener noreferrer">자료 출처 ↗</a>' if v.get('source_url') else ''
    return f'''<figure id="visual" class="case-visual"><a class="visual-open" href="../{e(v['src'])}" target="_blank" rel="noopener" aria-label="{e(p['title'])} 대표 자료 크게 보기">{project_image(v, '../')}</a><figcaption><strong>{e(v['label'])}</strong><p>{e(v['caption'])}</p><div class="visual-links"><a class="text-link" href="../{e(v['src'])}" target="_blank" rel="noopener">크게 보기 ↗</a>{source}</div></figcaption></figure>'''

def card(p, i):
    v = p.get('visual')
    media = f'<div class="card-media {e(v.get("preview_layout", ""))}">{project_image(v.get("preview", v))}</div><p class="card-media-label">{e(v.get("preview_label", v["label"]))}</p>' if v else ''
    return f'''<article class="project-card {"featured-card" if i < 2 else "supporting-card"}" data-category="{e(p['category'])}"><a class="card-body" href="projects/{e(p['slug'])}.html" aria-labelledby="project-{e(p['slug'])}">{media}<div class="card-meta"><span>{e(p['kind'])}</span><span>{e(p['period'])}</span></div><h3 id="project-{e(p['slug'])}">{e(p['title'])}<span aria-hidden="true">↗</span></h3><p class="card-subtitle">{e(p['subtitle'])}</p><p class="card-description">{e(p['summary'])}</p><div class="tech-tags">{tags(p['tech'][:5])}</div><div class="card-result">{e(p['outcome'])}</div><span class="card-cta">프로젝트 읽기 <span aria-hidden="true">→</span></span></a></article>'''

def home():
    featured_html=''.join(card(p,i) for i,p in enumerate(DATA['projects'][:2]))
    supporting_html=''.join(card(p,i) for i,p in enumerate(DATA['projects'][2:], start=2))
    pubs=''
    for p in DATA['publications']:
        abstract = '<dl class="pub-abstract">'+''.join(f'<div><dt>{e(row["label"])}</dt><dd>{e(row["text"])}</dd></div>' for row in p['abstract'])+'</dl>' if p.get('abstract') else ''
        pubs+=f'''<article class="publication" id="{e(p['id'])}"><div class="pub-main"><div class="eyebrow">{e(p['venue'])} / {e(p['year'])}</div><h3>{e(p['title'])}</h3><p>{e(p['description'])}</p>{abstract}<p class="pub-authors">{e(p['authors'])}</p><div class="pub-links">{links(p['links'])}</div></div><span class="pub-distinction">{e(p['distinction'])}</span></article>'''
    awards=''.join(f'''<article class="award"><time>{e(a['date'])}</time><div><h3>{e(a['title'])}</h3><p class="award-summary">{e(a['summary'])}</p><p class="award-host">주최: {e(a['organization'])}</p></div><a class="award-project" href="{e(a['url'])}"><span>{e(a['project'])}</span><span class="award-cta">{e(a['link_label'])} <span aria-hidden="true">→</span></span></a></article>''' for a in DATA['awards'])
    activities=''
    for a in DATA['activities']:
        role = f'<span class="activity-role">{e(a["role"])}</span> · ' if a.get('role') else ''
        focus = f'<p class="activity-focus">{e(a["focus"])}</p>' if a.get('focus') else ''
        related = '<div class="activity-links">'+''.join(f'<a class="text-link" href="{e(link["url"])}">{e(link["label"])} →</a>' for link in a['links'])+'</div>' if a.get('links') else ''
        activities+=f'''<article class="activity"><div class="eyebrow">{role}{e(a['period'])}</div><h3>{e(a['title'])}</h3>{focus}<ul>{''.join(f'<li>{e(b)}</li>' for b in a['bullets'])}</ul>{related}</article>'''
    credentials=''.join(f'''<article class="credential"><p class="eyebrow">{e(c["category"])}</p><h3>{e(c["title"])}</h3><p class="credential-detail">{e(c["detail"])} · <time>{e(c["date"])}</time></p></article>''' for c in DATA["credentials"])
    return f'''<main id="main">
<section class="hero container"><img class="hero-portrait" src="assets/juhee-portrait.jpg" alt="박주희 프로필 사진" width="1169" height="1712" fetchpriority="high"><p class="eyebrow">박주희 포트폴리오</p><h1>만든 서비스가<br><span class="accent-text">실제로 쓰일 때까지.</span></h1><p class="hero-description">사용자와 운영자의 요구를 정리하고,<br>AI를 활용한 화면·서버 구현부터 배포와 운영 후 개선까지 이어갑니다.</p><div class="hero-actions"><a class="text-link" href="#projects">프로젝트 살펴보기 ↓</a><a class="text-link" href="https://github.com/juhee0223" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div></section>
<section id="projects" class="section container"><div class="section-heading"><div><h2>프로젝트 <span class="section-count">9</span></h2></div><p>서비스를 완성한 경험과 근거를 바탕으로 판단한 경험.<br>단짠과 의료 AI 해커톤을 대표 사례로 소개합니다.</p></div><div class="filter-row"><div class="filters" role="group" aria-label="프로젝트 분야 필터"><button type="button" data-filter="all" class="active" aria-pressed="true">전체 <span>9</span></button><button type="button" data-filter="service" aria-pressed="false">서비스</button><button type="button" data-filter="ai" aria-pressed="false">AI 응용</button><button type="button" data-filter="systems" aria-pressed="false">시스템 연구</button></div><p class="project-count" role="status" aria-live="polite">9개의 프로젝트</p></div><div class="project-group"><h3 class="project-group-title">대표 프로젝트 <span>서비스 완성과 문제 해결</span></h3><div class="project-grid featured-grid">{featured_html}</div></div><div class="project-group"><h3 class="project-group-title">더 살펴볼 경험 <span>관측성 · AI 응용 · 시스템 실험</span></h3><div class="project-grid supporting-grid">{supporting_html}</div></div></section>
<section id="research" class="section research-section"><div class="container"><div class="section-heading"><div><h2>논문 · 출판 <span class="section-count">{len(DATA["publications"])}</span></h2></div><p>스토리지 성능 분석과 텍스트 임베딩 연구,<br>그리고 운영체제 교재 기반 RAG 저서.</p></div><div class="publication-list">{pubs}</div></div></section>
<section id="awards" class="section container"><div class="section-heading"><div><h2>수상 <span class="section-count">4</span></h2></div><p>해커톤에서의 실행과 연구의 성과.</p></div><div class="award-list">{awards}</div></section>
<section id="activities" class="section activities-section"><div class="container"><div class="section-heading"><div><h2>활동 <span class="section-count">{len(DATA["activities"])}</span></h2></div><p>현장의 반복 업무 개선부터 연구·정보 전달까지,<br>개발 밖에서 문제를 보고 실행한 경험입니다.</p></div><div class="activity-grid">{activities}</div><div class="skills-panel"><div><h3>사용 기술</h3></div><div class="skill-groups"><p><strong>Development</strong><span>Java · Spring Boot · React · TypeScript · Python · C / C++</span></p><p><strong>AI & Data</strong><span>Codex · LLM / RAG · LangGraph · PyTorch · OpenCV · scikit-learn</span></p><p><strong>Systems & Operations</strong><span>NHN Cloud · Docker · Kubernetes · Redis · Kafka · MySQL · Linux · Git</span></p></div></div></div></section>
<section id="credentials" class="section container"><div class="section-heading"><h2>자격증 · 어학</h2></div><div class="credential-grid">{credentials}</div></section>
<section id="contact" class="section container contact-section"><div><h2>연락처</h2><p>단국대학교 소프트웨어학과 4학년</p></div><div class="contact-links"><a class="contact-email" href="mailto:pjuhee23@dankook.ac.kr">pjuhee23@dankook.ac.kr <span>↗</span></a><div><a class="text-link" href="https://github.com/juhee0223" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div></div></section></main>'''

def detail(p,i):
    project_awards = [a for a in DATA['awards'] if a['url'] == f"projects/{p['slug']}.html"]
    award_summary = ''.join(f'<p class="case-award"><span class="award-label">수상</span><strong>{e(a["title"])}</strong><time datetime="{e(a["date"])}">{e(a["date"])}</time></p>' for a in project_awards)
    body_sections=''
    for j,s in enumerate(p['sections']):
        paragraphs=''.join(f'<p>{highlighted(t,p["slug"])}</p>' for t in s.get('paragraphs',[]))
        bullets='<ul>'+''.join(f'<li>{highlighted(t,p["slug"])}</li>' for t in s.get('bullets',[]))+'</ul>' if s.get('bullets') else ''
        status = f'<p class="case-status">{e(s["status"])}</p>' if s.get('status') else ''
        flow = '<div class="decision-flow" aria-label="과정 설명">'+''.join(f'<div><span class="flow-index">{k+1:02d}</span><h3>{e(step["title"])}</h3><p>{e(step["text"])}</p></div>' for k,step in enumerate(s['steps']))+'</div>' if s.get('steps') else ''
        metrics = '<dl class="result-metrics">'+''.join(f'<div><dt>{e(m["label"])}</dt><dd>{e(m["value"])}</dd></div>' for m in s['metrics'])+'</dl>' if s.get('metrics') else ''
        body_sections+=f'<section class="case-section" id="section-{j}"><div><h2>{e(s["title"])}</h2>{status}{paragraphs}{bullets}{flow}{metrics}</div></section>'
    gallery=''
    if p['slug']=='danzzan':
        gallery='''<section class="case-gallery"><div class="eyebrow">서비스 화면</div><h2>예매 안내와 동의 확인</h2><div class="phone-gallery"><figure><a href="../assets/danzzan-consent.png" target="_blank" rel="noopener"><img src="../assets/danzzan-consent.png" alt="단짠 예매 안내와 필수 동의 확인 화면" loading="lazy" width="941" height="1672"></a><figcaption>예매 안내와 필수 동의 확인 · 팀 공동 산출물</figcaption></figure></div></section>'''
    elif p['slug']=='olly':
        gallery='''<section class="case-gallery"><div class="eyebrow">로컬 MVP 데모</div><h2>오류 요청도 추적할 수 있도록</h2><figure><a href="../assets/olly-error.png" target="_blank" rel="noopener"><img class="wide-image" src="../assets/olly-error.png" alt="의도적으로 오류를 발생시킨 OLLY 데모에서 요청 ID, trace ID, 오류 상태가 함께 표시된 화면" width="1336" height="676" loading="lazy"></a><figcaption>실패 요청의 ID와 오류 상태를 유지하는 데모 화면 · 팀 공동 산출물</figcaption></figure></section>'''
    nav=('<a href="#visual">대표 자료</a>' if p.get('visual') else '') + ''.join(f'<a href="#section-{j}">{e(s["title"])}</a>' for j,s in enumerate(p['sections']))
    status = f'<p class="case-status">{e(p["status"])}</p>' if p.get('status') else ''
    nxt=DATA['projects'][(i+1)%len(DATA['projects'])]
    return f'''<main id="main"><div class="container"><a class="back-link" href="../index.html#projects">← 전체 프로젝트</a><section class="case-hero"><div><p class="eyebrow">{e(CATS[p['category']])}</p><h1>{e(p['title'])}</h1><p class="case-subtitle">{e(p['subtitle'])}</p><div class="case-meta"><span>{e(p['period'])}</span><span>{e(p['kind'])}</span></div>{award_summary}<p class="case-summary">{e(p['summary'])}</p>{status}<div class="pub-links">{links(p.get('primary_links', p['links']))}</div></div></section><div class="case-overview"><div><span class="eyebrow">기여와 역할</span><p>{e(p['role'])}</p></div><div><span class="eyebrow">결과</span><p>{highlighted(p['outcome'],p['slug'])}</p></div><div><span class="eyebrow">사용 기술</span><div class="tech-tags">{tags(p['tech'])}</div></div></div><div class="case-layout"><aside class="case-toc"><span class="eyebrow">목차</span>{nav}<a href="#evidence">관련 자료</a></aside><div class="case-body">{project_visual(p)}{body_sections}{gallery}<section id="evidence" class="case-evidence"><p class="eyebrow">관련 자료</p><h2>프로젝트 자료 및 구현 근거</h2><div class="evidence-links">{links(p['links'])}</div></section></div></div><nav class="project-pagination" aria-label="프로젝트 이동"><a href="../index.html#projects">← 프로젝트 목록</a><a href="{e(nxt['slug'])}.html"><small>다음 프로젝트</small><strong>{e(nxt['title'])} →</strong></a></nav></div></main>'''

(ROOT/'index.html').write_text(shell('포트폴리오', home()))
(ROOT/'projects').mkdir(exist_ok=True)
for i,p in enumerate(DATA['projects']):
    (ROOT/'projects'/f'{p["slug"]}.html').write_text(shell(p['title'],detail(p,i),'../',p['summary'],f'projects/{p["slug"]}.html'))
(ROOT/'.nojekyll').touch()
(ROOT/'404.html').write_text(shell('페이지를 찾을 수 없습니다',f'<main id="main" class="container not-found"><p class="eyebrow">404 / NOT FOUND</p><h1>여기는 아직 빈 페이지예요.</h1><p>프로젝트 목록에서 다시 시작해 주세요.</p><a class="button primary" href="{BASE}/">포트폴리오 홈으로 →</a></main>',depth=BASE+'/'))
urls=['']+[f'projects/{p["slug"]}.html' for p in DATA['projects']]
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}/{u}</loc></url>' for u in urls)+'</urlset>')
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
print(f'Built homepage, {len(DATA["projects"])} project pages, 404, sitemap.')
