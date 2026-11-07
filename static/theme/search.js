/*
 * 站内搜索：按 data/search.yaml 的配置在多个搜索引擎间切换。
 * 配置由模板写入 window.SITE_SEARCH，这里只负责交互，不需要改模板。
 */
(function () {
  var cfg = window.SITE_SEARCH;
  if (!cfg || !cfg.engines || !cfg.engines.length) return;

  var form = document.getElementById('siteSearchForm');
  var input = document.getElementById('edtSearch');
  var select = document.getElementById('searchEngine');
  if (!form || !input || !select) return;

  var STORAGE_KEY = 'site-search-engine';

  function findEngine(id) {
    for (var i = 0; i < cfg.engines.length; i++) {
      if (cfg.engines[i].id === id) return cfg.engines[i];
    }
    return null;
  }

  function currentEngine() {
    return findEngine(select.value) || findEngine(cfg.default) || cfg.engines[0];
  }

  // 同步表单的 action 和参数名，保证禁用 JS 时也能按当前引擎搜索
  function syncForm() {
    var engine = currentEngine();
    form.setAttribute('action', engine.url.split('?')[0]);
    input.setAttribute('name', engine.param || 'q');
  }

  function saveEngine(id) {
    try {
      window.localStorage.setItem(STORAGE_KEY, id);
    } catch (e) {
      /* 隐私模式下忽略 */
    }
  }

  function restoreEngine() {
    var saved = null;
    try {
      saved = window.localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      saved = null;
    }
    if (saved && findEngine(saved)) {
      select.value = saved;
    }
  }

  select.addEventListener('change', function () {
    saveEngine(select.value);
    syncForm();
  });

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    var keyword = input.value.trim();
    if (!keyword) {
      input.focus();
      return;
    }
    var engine = currentEngine();
    var query = engine.site && cfg.site ? 'site:' + cfg.site + ' ' + keyword : keyword;
    window.location.href = engine.url.replace('{q}', encodeURIComponent(query));
  });

  restoreEngine();
  syncForm();
})();
