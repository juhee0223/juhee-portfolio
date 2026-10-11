(() => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  function closeMenu() {
    toggle?.setAttribute('aria-expanded', 'false');
    nav?.classList.remove('is-open');
  }
  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  });
  nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') {
      closeMenu(); toggle.focus();
    }
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.nav-wrap')) closeMenu();
  });
  const contents = [...document.querySelectorAll('.case-toc a[href^="#"]')]
    .map(link => ({ link, section: document.getElementById(link.hash.slice(1)) }))
    .filter(item => item.section);
  if (contents.length) {
    const caseToc = document.querySelector('.case-toc');
    const siteHeader = document.querySelector('.site-header');
    let scheduled = false;
    let activeContent = null;
    function caseNavigationOffset() {
      const headerHeight = siteHeader?.offsetHeight || 0;
      const tocHeight = caseToc?.offsetHeight || 0;
      document.documentElement.style.setProperty('--site-header-height', `${headerHeight}px`);
      document.documentElement.style.setProperty('--case-toc-height', `${tocHeight}px`);
      return headerHeight + tocHeight + 24;
    }
    function updateContents() {
      const offset = caseNavigationOffset();
      let current = contents[0];
      contents.forEach(item => {
        if (item.section.getBoundingClientRect().top <= offset) current = item;
      });
      if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2) {
        current = contents[contents.length - 1];
      }
      contents.forEach(item => {
        if (item === current) item.link.setAttribute('aria-current', 'location');
        else item.link.removeAttribute('aria-current');
      });
      if (current !== activeContent && caseToc && caseToc.scrollWidth > caseToc.clientWidth) {
        const tocRect = caseToc.getBoundingClientRect();
        const linkRect = current.link.getBoundingClientRect();
        if (linkRect.left < tocRect.left || linkRect.right > tocRect.right) {
          const left = caseToc.scrollLeft + linkRect.left - tocRect.left - (tocRect.width - linkRect.width) / 2;
          caseToc.scrollTo({ left: Math.max(0, left), behavior: 'smooth' });
        }
      }
      activeContent = current;
      scheduled = false;
    }
    function scheduleContents() {
      if (!scheduled) {
        scheduled = true;
        requestAnimationFrame(updateContents);
      }
    }
    window.addEventListener('scroll', scheduleContents, { passive: true });
    window.addEventListener('resize', scheduleContents);
    window.addEventListener('load', scheduleContents);
    window.addEventListener('hashchange', () => {
      scheduleContents();
      requestAnimationFrame(scheduleContents);
    });
    updateContents();
  }
  let scheduleHeaderNavigation = () => {};
  const header = document.querySelector('.site-header');
  const headerLinks = [...document.querySelectorAll('#site-nav a')]
    .filter(link => link.hash)
    .map(link => ({ link, section: document.getElementById(link.hash.slice(1)) }));
  if (headerLinks.length) {
    let headerScheduled = false;
    const clearHeaderCurrent = () => headerLinks.forEach(item => item.link.removeAttribute('aria-current'));
    function updateHeaderCurrent() {
      if (document.querySelector('.case-hero')) {
        headerLinks.forEach(item => {
          if (item.link.hash === '#projects') item.link.setAttribute('aria-current', 'page');
          else item.link.removeAttribute('aria-current');
        });
      } else {
        const sectionLinks = headerLinks.filter(item => item.section);
        if (!sectionLinks.length) {
          headerScheduled = false;
          return;
        }
        const offset = (header?.offsetHeight || 0) + 24;
        let current = null;
        sectionLinks.forEach(item => {
          if (item.section.getBoundingClientRect().top <= offset) current = item;
        });
        if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2) {
          current = sectionLinks[sectionLinks.length - 1];
        }
        clearHeaderCurrent();
        current?.link.setAttribute('aria-current', 'location');
      }
      headerScheduled = false;
    }
    function scheduleHeaderCurrent() {
      if (!headerScheduled) {
        headerScheduled = true;
        requestAnimationFrame(updateHeaderCurrent);
      }
    }
    window.addEventListener('scroll', scheduleHeaderCurrent, { passive: true });
    window.addEventListener('resize', scheduleHeaderCurrent);
    window.addEventListener('hashchange', scheduleHeaderCurrent);
    window.addEventListener('load', scheduleHeaderCurrent);
    updateHeaderCurrent();
    scheduleHeaderNavigation = scheduleHeaderCurrent;
  }
  const buttons = document.querySelectorAll('[data-filter]');
  const cards = document.querySelectorAll('.project-card');
  buttons.forEach(button => button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    buttons.forEach(item => {
      item.classList.toggle('active', item === button);
      item.setAttribute('aria-pressed', String(item === button));
    });
    let visible = 0;
    cards.forEach(card => {
      const show = filter === 'all' || card.dataset.category === filter;
      card.hidden = !show;
      if (show) visible++;
    });
    document.querySelectorAll('.project-group').forEach(group => {
      group.hidden = ![...group.querySelectorAll('.project-card')].some(card => !card.hidden);
    });
    const count = document.querySelector('.project-count');
    if (count) count.textContent = `${visible}개의 프로젝트`;
    scheduleHeaderNavigation();
  }));
})();
