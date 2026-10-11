#!/usr/bin/env python3
"""Build a dependency-free, public portfolio from reviewed content."""
from pathlib import Path
from html import escape
import json
import re
from hashlib import sha256
from decimal import Decimal

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
    images = ''.join(f'<figure>{project_image(item, "../")}<figcaption>{e(item["label"])}</figcaption></figure>' for item in v['images']) if v.get('images') else project_image(v, '../')
    layout = ' screen-strip' if v.get('images') else ''
    return f'''<figure id="visual" class="case-visual"><div class="visual-frame{layout}">{images}</div><figcaption><strong>{e(v['label'])}</strong><p>{e(v['caption'])}</p><div class="visual-links">{source}</div></figcaption></figure>'''

def project_diagram(p):
    diagram = p.get('diagram')
    if not diagram:
        return ''
    labels = {'danzzan':'서비스 연계', 'conquer-health':'응답·평가 흐름', 'olly':'관측 경로'}
    nodes = ''
    for step in diagram['steps']:
        branches = '<ul class="system-branches">'+''.join(f'<li>{e(branch)}</li>' for branch in step['branches'])+'</ul>' if step.get('branches') else ''
        nodes += f'<li class="system-node"><h3>{e(step["title"])}</h3><p>{e(step["text"])}</p>{branches}</li>'
    label = diagram.get('label', labels.get(p['slug'], '시스템 흐름'))
    feedback = f'<p class="system-feedback"><span aria-hidden="true">↶</span>{e(diagram["feedback"])}</p>' if diagram.get('feedback') else ''
    return f'<figure id="flow" class="system-diagram"><figcaption><span class="flow-label">{e(label)}</span><div><h2>{e(diagram["title"])}</h2><p>{e(diagram["description"])}</p></div></figcaption><ol class="system-graph system-graph-{len(diagram["steps"])}" aria-label="{e(diagram["title"])}">{nodes}</ol>{feedback}<div class="flow-attribution"><span>참여 범위</span><p>{e(diagram["note"])}</p></div></figure>'

def phrase_list(items, slug=None):
    render = (lambda value: highlighted(value, slug)) if slug else e
    return '<ul class="phrase-list">'+''.join(f'<li>{render(item)}</li>' for item in items)+'</ul>'

def info_row(label, value):
    return f'<div class="info-row"><dt>{e(label)}</dt><dd>{value}</dd></div>'

def evidence_table(table):
    """Render a compact, source-backed comparison table for a case-study section."""
    if not table:
        return ''
    columns = ''.join(f'<th scope="col">{e(column)}</th>' for column in table['columns'])
    rows = ''.join(
        '<tr>'+''.join(
            f'<th scope="row">{e(value)}</th>' if index == 0 else f'<td>{e(value)}</td>'
            for index, value in enumerate(row)
        )+'</tr>'
        for row in table['rows']
    )
    note = f'<p class="evidence-table-note">{e(table["note"])}</p>' if table.get('note') else ''
    return f'<div class="evidence-table-wrap" tabindex="0" role="region" aria-label="{e(table["caption"])}"><table class="evidence-table"><caption>{e(table["caption"])}</caption><thead><tr>{columns}</tr></thead><tbody>{rows}</tbody></table>{note}</div>'

def project_facts(p, detail=False):
    role = phrase_list(p['role_items'], p['slug']) if detail and p.get('role_items') else highlighted(p['role'], p['slug']) if detail else e(p['card_role'])
    rows = info_row('담당', role)
    if detail:
        rows += info_row('기간·구성', e(p['period']+' · '+p['kind']))
    for metric in p.get('card_metrics', []):
        rows += info_row(metric['label'], f'<strong class="metric-value">{e(metric["value"])}</strong>')
    # Numeric results appear in their own rows; the outcome row retains team context.
    outcome = p.get('card_outcome', p['outcome']) if not detail or p.get('card_metrics') else p['outcome']
    result = phrase_list(p['outcome_items'], p['slug']) if detail and p.get('outcome_items') and not p.get('card_metrics') else highlighted(outcome, p['slug'])
    rows += info_row('성과', result)
    status = p.get('status') if detail else p.get('card_status')
    if status:
        rows += info_row('운영 상태', e(status))
    if detail and p.get('metrics_source'):
        rows += info_row('성과 근거', links([p['metrics_source']]))
    rows += info_row('사용 기술', '<div class="tech-tags">'+tags(p['tech'] if detail else p['tech'][:5])+'</div>')
    if detail:
        for key, label in [('collaboration', '협업 도구'), ('collaboration_method', '협업 방식'), ('branch_strategy', '브랜치 전략')]:
            if p.get(key): rows += info_row(label, e(p[key]))
    return f'<dl class="info-list {"case-overview" if detail else "card-facts"}">{rows}</dl>'

def card(p, i):
    v = p.get('visual')
    preview = (''.join(project_image(item) for item in v["images"]) if v.get("images") else project_image(v.get("preview", v))) if v else ''
    layout = "screen-strip" if v and v.get("images") else v.get("preview_layout", "") if v else ""
    media = f'<div class="card-media-wrap"><div class="card-media {e(layout)}">{preview}</div><p class="card-media-label">{e(v.get("preview_label", v["label"]))}</p></div>' if v else ''
    return f'''<article class="project-card {"featured-card" if i < 2 else "supporting-card"}" data-category="{e(p['category'])}"><a class="card-body" href="projects/{e(p['slug'])}.html" aria-labelledby="project-{e(p['slug'])}">{media}<div class="card-copy"><div class="card-meta"><span>{e(p['kind'])}</span><span>{e(p['period'])}</span></div><h3 id="project-{e(p['slug'])}">{e(p['title'])}<span aria-hidden="true">↗</span></h3><p class="card-subtitle">{e(p.get('card_intro',p['subtitle']))}</p>{project_facts(p)}<span class="card-cta">프로젝트 읽기 <span aria-hidden="true">→</span></span></div></a></article>'''

def publication_abstract(p):
    rows = p.get('phrase_abstract', p.get('display_abstract', p.get('abstract', [])))
    if not rows:
        return f'<p>{e(p["description"])}</p>'
    table = ''
    if p.get('comparison'):
        c = p['comparison']
        head = ''.join(f'<th scope="col">{e(value)}</th>' for value in c['columns'])
        body = ''.join('<tr>'+''.join(f'<th scope="row">{e(value)}</th>' if i == 0 else f'<td>{e(value)}</td>' for i,value in enumerate(row))+'</tr>' for row in c['rows'])
        table = f'<div class="research-table-wrap" tabindex="0" role="region" aria-label="{e(c["caption"])}"><table class="research-table"><caption>{e(c["caption"])}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
    result = ''
    for i,row in enumerate(rows):
        contents = phrase_list(row['items']) if 'items' in row else f'<p>{e(row["text"])}</p>'
        result += f'<div class="pub-abstract-row"><h4>{e(row["label"])}</h4>{contents}</div>'
        if i == 1: result += table
    return '<div class="pub-abstract">'+result+'</div>'

def skills_section():
    groups = ''.join(f'<article class="skill-group"><h3>{e(g["title"])}</h3><div class="tech-tags">{tags(g["tech"])}</div><p>{e(g["context"])}</p><div class="skill-links">{links(g["links"])}</div></article>' for g in DATA['skills'])
    return f'<section id="skills" class="skills-section container" aria-labelledby="skills-title"><div class="section-heading"><h2 id="skills-title">사용 기술</h2><p>프로젝트에서 활용한 기술과 경험</p></div><div class="skill-grid">{groups}</div><div class="skills-collaboration"><strong>협업 도구·방식</strong><div class="tech-tags">{tags(["Jira", "Agile / Scrum", "스프린트·데일리 스크럼", "GitHub Flow"])}</div></div></section>'

def home():
    featured_html=''.join(card(p,i) for i,p in enumerate(DATA['projects'][:2]))
    supporting_html=''.join(card(p,i) for i,p in enumerate(DATA['projects'][2:], start=2))
    pubs=''
    for p in DATA['publications']:
        metadata = info_row('게재·발행', e(p['venue']+' / '+p['year']))+info_row('저자·역할', e(p['authors']))+info_row('구분', e(p['distinction']))
        pubs+=f'''<article class="publication" id="{e(p['id'])}"><div class="pub-main"><h3>{e(p['title'])}</h3><dl class="info-list publication-meta">{metadata}</dl>{publication_abstract(p)}<div class="pub-links">{links(p['links'])}</div></div></article>'''
    awards=''.join(f'''<article class="award"><time>{e(a['date'])}</time><div><h3>{e(a['title'])}</h3><p class="award-summary">{e(a['summary'])}</p><p class="award-host">주최: {e(a['organization'])}</p></div><a class="award-project" href="{e(a['url'])}"><span>{e(a['project'])}</span><span class="award-cta">{e(a['link_label'])} <span aria-hidden="true">→</span></span></a></article>''' for a in DATA['awards'])
    activities=''
    for a in DATA['activities']:
        role = f'<span class="activity-role">{e(a["role"])}</span> · ' if a.get('role') else ''
        focus = f'<p class="activity-focus">{e(a["focus"])}</p>' if a.get('focus') else ''
        related = '<div class="activity-links">'+''.join(f'<a class="text-link" href="{e(link["url"])}">{e(link["label"])} →</a>' for link in a['links'])+'</div>' if a.get('links') else ''
        activity_rows = a.get('phrase_rows', [{'label':'활동 내용', 'items':a['bullets']}])
        details = ''.join(info_row(row['label'], phrase_list(row['items'])) for row in activity_rows)
        activities+=f'''<article class="activity"><div class="eyebrow">{role}{e(a['period'])}</div><h3>{e(a['title'])}</h3>{focus}<dl class="info-list activity-facts">{details}</dl>{related}</article>'''
    credentials=''.join(f'''<article class="credential"><p class="eyebrow">{e(c["category"])}</p><h3>{e(c["title"])}</h3><p class="credential-detail">{e(c["detail"])} · <time>{e(c["date"])}</time></p></article>''' for c in DATA["credentials"])
    return f'''<main id="main">
<section class="hero container"><img class="hero-portrait" src="assets/juhee-portrait.jpg" alt="박주희 프로필 사진" width="1169" height="1712" fetchpriority="high"><h1>만든 서비스가<br><span class="accent-text">실제로 쓰일 때까지.</span></h1><p class="hero-description">사용자와 운영자의 요구를 정리하고,<br>AI를 활용한 화면·서버 구현부터 배포와 운영 후 개선까지 이어갑니다.</p><div class="hero-actions"><a class="text-link" href="#projects">프로젝트 살펴보기 ↓</a><a class="text-link" href="https://github.com/juhee0223" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div></section>
{skills_section()}
<section id="projects" class="section container"><div class="section-heading"><div><h2>프로젝트 <span class="section-count">9</span></h2></div><p>서비스를 완성한 경험과 근거를 바탕으로 판단한 경험.<br>단짠과 의료 AI 해커톤을 대표 사례로 소개합니다.</p></div><div class="filter-row"><div class="filters" role="group" aria-label="프로젝트 분야 필터"><button type="button" data-filter="all" class="active" aria-pressed="true">전체 <span>9</span></button><button type="button" data-filter="service" aria-pressed="false">서비스</button><button type="button" data-filter="ai" aria-pressed="false">AI 응용</button><button type="button" data-filter="systems" aria-pressed="false">시스템 연구</button></div><p class="project-count" role="status" aria-live="polite">9개의 프로젝트</p></div><div class="project-group"><h3 class="project-group-title">대표 프로젝트 <span>서비스 완성과 문제 해결</span></h3><div class="project-grid featured-grid">{featured_html}</div></div><div class="project-group"><h3 class="project-group-title">더 살펴볼 경험 <span>관측성 · AI 응용 · 시스템 실험</span></h3><div class="project-grid supporting-grid">{supporting_html}</div></div></section>
<section id="research" class="section research-section"><div class="container"><div class="section-heading"><div><h2>논문 · 출판 <span class="section-count">{len(DATA["publications"])}</span></h2></div><p>스토리지 성능 분석과 텍스트 임베딩 연구,<br>그리고 운영체제 교재 기반 RAG 저서.</p></div><div class="publication-list">{pubs}</div></div></section>
<section id="awards" class="section container"><div class="section-heading"><div><h2>수상 <span class="section-count">4</span></h2></div><p>해커톤에서의 실행과 연구의 성과.</p></div><div class="award-list">{awards}</div></section>
<section id="activities" class="section activities-section"><div class="container"><div class="section-heading"><div><h2>활동 <span class="section-count">{len(DATA["activities"])}</span></h2></div><p>현장의 반복 업무 개선부터 연구·정보 전달까지,<br>개발 밖에서 문제를 보고 실행한 경험입니다.</p></div><div class="activity-grid">{activities}</div></div></section>
<section id="credentials" class="section container"><div class="section-heading"><h2>자격증 · 어학</h2></div><div class="credential-grid">{credentials}</div></section>
<section id="contact" class="section container contact-section"><div class="section-heading"><h2>연락처</h2></div><div><p>단국대학교 소프트웨어학과 4학년</p></div><div class="contact-links"><a class="contact-email" href="mailto:pjuhee23@dankook.ac.kr">pjuhee23@dankook.ac.kr <span>↗</span></a><div><a class="text-link" href="https://github.com/juhee0223" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div></div></section></main>'''

def section_extras(p, s):
    bullets = phrase_list(s.get('display_bullets', s.get('bullets', [])), p['slug']) if s.get('display_bullets', s.get('bullets')) else ''
    status = f'<p class="case-status">{e(s["status"])}</p>' if s.get('status') else ''
    metrics = '<dl class="info-list result-metrics">'+''.join(info_row(m['label'], f'<strong class="metric-value">{e(m["value"])}</strong>') for m in s['metrics'])+'</dl>' if s.get('metrics') else ''
    comparison = ''
    if s.get('score_comparison'):
        rows = ''.join(f'<tr><th scope="row">{e(row["round"])}</th><td class="aim-score">{e(row["aim"])}</td><td>{e(row["runner_up"])}</td><td>{Decimal(row["aim"]) - Decimal(row["runner_up"]):+.2f}</td></tr>' for row in s['score_comparison'])
        comparison = f'<div class="score-comparison"><table><caption>최종 상위 2팀의 라운드별 점수 (점)</caption><thead><tr><th scope="col">평가</th><th scope="col">AIM · 1위</th><th scope="col">2위 팀</th><th scope="col">차이</th></tr></thead><tbody>{rows}</tbody></table><p class="score-note">{e(s["score_note"])}</p></div>'
    sources='<div class="contribution-sources">'+links(s['links'])+'</div>' if s.get('links') else ''
    return status, bullets+metrics+comparison+evidence_table(s.get('evidence_table'))+sources

def case_band(label, title, body, anchor):
    number, rail_title = label.split(' / ', 1)
    rail = f'<span class="case-rail-index">{e(number)}</span><span class="case-rail-title">{e(rail_title)}</span>'
    return f'<section class="case-band" id="{e(anchor)}"><div class="case-rail">{rail}</div><div class="case-content"><h2 class="case-band-title">{e(title)}</h2>{body}</div></section>'

def case_gallery_item(item):
    return f'<figure class="case-inline-image"><div class="visual-frame">{project_image(item, "../")}</div><figcaption><strong>{e(item["label"])}</strong><p>{e(item["caption"])}</p>{links([{"label":"자료 출처", "url":item["source_url"]}])}</figcaption></figure>'

def case_section(p, index, story=None):
    s=p['sections'][index]
    status, extras=section_extras(p,s)
    groups=story['groups'] if story else [{'label':r['label'],'row_indices':[i]} for i,r in enumerate(s['phrase_rows'])]
    rows=''
    for group in groups:
        items=[item for i in group['row_indices'] for item in s['phrase_rows'][i]['items']]
        rows+=f'<div class="story-row"><h4>{e(group["label"])}</h4>{phrase_list(items,p["slug"])}</div>'
    title=story['title'] if story else s.get('display_title',s['title'])
    media=''
    if p['slug']=='danzzan' and index==1:
        partner=p.get('partnership')
        if partner:
            media=f'<div class="partner-feature">{project_image(partner,"../")}<p class="partner-kicker">네이버페이 페이스사인 협업 · 봄축제 입장 연계</p><p>단짠 예매 유지 → 날짜별 예매자 명단 전달 → 페이스사인 현장 입장</p><small>개인 참여: 협업 범위·명단 전달 기준 조율 및 가입 흐름 반영 · 얼굴 인증은 협력사 담당</small></div>'
        media+=project_diagram(p)
        extras+=''.join(case_gallery_item(item) for item in p.get('gallery',[]))
        extras+='<figure class="case-inline-image consent-image"><div class="visual-frame"><img src="../assets/danzzan-consent.png" alt="단짠 예매 안내와 필수 동의 확인 화면" loading="lazy" width="941" height="1672"></div><figcaption>예매 안내와 필수 동의 확인 · 팀 공동 산출물</figcaption></figure>'
    if p['slug']=='danzzan' and index==6 and p.get('translation_screens'):
        shots=''.join(f'<figure>{project_image(item,"../")}<figcaption>{e(item["label"])}</figcaption></figure>' for item in p['translation_screens'])
        extras+=f'<div class="recovery-result"><span>복구 검증</span><strong>미번역 대상 0건</strong><p>실제 번역 대상 조건의 SQL 조회로 확인 · 새 공지의 번역·저장·영어 화면 표시 검증</p></div><div class="translation-gallery" id="translation-screens">{shots}</div><p class="media-note">가을축제 번역 화면 · 팀 공동 산출물. 개인 기여는 운영 중 번역 누락의 원인 분석·복구 및 저장·화면 검증.</p><div class="visual-links">{links([{"label":"팀 공개 화면 자료","url":"https://github.com/DKU-Dan-Zzan"}])}</div>'
    return f'<article class="case-story" id="section-{index}"><h3>{e(title)}</h3>{status}{media}<div class="story-rows">{rows}</div>{extras}</article>'

def detail(p,i):
    plan=p['contribution_story']
    awards=[a for a in DATA['awards'] if a['url']==f"projects/{p['slug']}.html"]
    award_label='팀 수상' if plan.get('team_scope_items') else '수상'
    award_summary=''.join(f'<p class="case-award"><span class="award-label">{award_label}</span><strong>{e(a["title"])}</strong></p>' for a in awards)
    scope_label='직접 담당' if plan['contribution_sections'] else '참여 범위'
    overview=info_row(scope_label,phrase_list(plan['scope_items'],p['slug']))
    if plan.get('team_scope_items'):
        overview+=info_row('팀·협업 범위',phrase_list(plan['team_scope_items'],p['slug']))
    overview+=info_row('프로젝트',e(p['intro_phrase']))
    overview+=info_row('기간·구성',e(p['period']+' · '+p['kind']))
    if p.get('operation_history'):
        operations=''.join(f'<li><strong>{e(item["period"])} · {e(item["title"])}:</strong> {e(item["detail"])}</li>' for item in p['operation_history'])
        overview+=info_row('실제 운영',f'<ul class="operation-history">{operations}</ul>')
    if p.get('context_items'): overview+=info_row('연구 범위',phrase_list(p['context_items']))
    if p.get('status'): overview+=info_row('현재 상태',e(p['status']))
    overview=case_band('01 / 담당 범위','담당 범위와 프로젝트 맥락','<dl class="case-info contribution-scope">'+overview+'</dl>','overview')
    contributions='<span id="problem-solving" class="anchor-alias" aria-hidden="true"></span>'
    if p['slug'] in ('sketch-to-spec', 'dacon'): contributions+=project_diagram(p)
    contributions+=''.join(case_section(p,story['section'],story) for story in plan['contribution_sections'])
    contributions=case_band('02 / 핵심 기여','판단·구현·검증으로 이어진 기여',contributions,'contributions') if plan['contribution_sections'] else ''
    results=''
    if plan.get('personal_results'):
        results+='<div class="contribution-result"><h3>개인 작업 결과</h3>'+phrase_list(plan['personal_results'],p['slug'])+'</div>'
    if plan.get('team_results'):
        results+='<div class="contribution-result team-result"><h3>팀 공동 성과</h3>'+phrase_list(plan['team_results'],p['slug'])+'</div>'
    results+=''.join(case_section(p,story['section'],story) for story in plan['result_sections'])
    if p.get('metrics_source'): results+='<div class="visual-links">'+links([p['metrics_source']])+'</div>'
    if p['slug']=='olly': results+='<figure class="case-inline-image"><img src="../assets/olly-error.png" alt="OLLY 오류 요청 ID와 trace ID, 오류 상태를 함께 확인하는 데모 화면" width="1336" height="676" loading="lazy"><figcaption>팀 공동 산출물 · 실패 요청의 ID와 오류 상태를 유지하는 로컬 MVP 데모</figcaption></figure>'
    result_title='개인 작업의 결과' if not plan.get('team_scope_items') else '개인 결과와 공동 성과'
    results=case_band('03 / 결과',result_title,results,'results')
    context='<span id="stack" class="anchor-alias" aria-hidden="true"></span><h3 class="context-stack-title">사용 기술</h3><div class="tech-tags">'+tags(p['tech'])+'</div>'
    collaboration=''
    for key,label in [('collaboration','협업 도구'),('collaboration_method','협업 방식'),('branch_strategy','브랜치 전략')]:
        if p.get(key): collaboration+=info_row(label,e(p[key]))
    if collaboration: context+='<dl class="case-info collaboration-info">'+collaboration+'</dl>'
    if p['slug'] not in ('danzzan', 'sketch-to-spec', 'dacon'): context+=project_diagram(p)
    context+=project_visual(p)
    context+=''.join(case_section(p,index) for index in plan['context_sections'])
    if p['slug']!='danzzan': context+=''.join(case_gallery_item(item) for item in p.get('gallery',[]))
    if not plan['contribution_sections']: context='<span id="problem-solving" class="anchor-alias" aria-hidden="true"></span>'+context
    context=case_band('04 / 기술 맥락','기여를 이해하기 위한 구조와 자료',context,'implementation')
    evidence=case_band('05 / 근거','작업 및 프로젝트 근거','<div class="evidence-links">'+links(p['links'])+'</div>','evidence')
    nav='<a href="#overview">담당 범위</a>'
    if plan['contribution_sections']: nav+='<a href="#contributions">핵심 기여</a>'
    nav+='<a href="#results">결과</a><a href="#implementation">기술 맥락</a><a href="#evidence">근거</a>'
    nxt=DATA['projects'][(i+1)%len(DATA['projects'])]
    return f'''<main id="main" class="case-study"><div class="container"><a class="back-link" href="../index.html#projects">← 전체 프로젝트</a><section class="case-hero"><p class="eyebrow">{e(CATS[p['category']])}</p><h1>{e(p['title'])}</h1><p class="case-subtitle">{e(plan['headline'])}</p>{award_summary}<div class="pub-links">{links(p.get('primary_links',p['links'])[:2])}</div></section><nav class="case-toc" aria-label="프로젝트 상세 목차">{nav}</nav>{overview}{contributions}{results}{context}{evidence}<nav class="project-pagination" aria-label="프로젝트 이동"><a href="../index.html#projects">← 프로젝트 목록</a><a href="{e(nxt['slug'])}.html"><small>다음 프로젝트</small><strong>{e(nxt['title'])} →</strong></a></nav></div></main>'''

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
