/*
 * 站内搜索：提交前给关键词补 site: 限定，然后交给浏览器原生提交。
 * 引擎、参数名、action 全部由模板按 data/search.yaml 的 default 输出，
 * 这里不切换引擎、不记忆选择。
 */
(function () {
  var form = document.getElementById('siteSearchForm');
  if (!form) return;

  var input = document.getElementById('edtSearch');
  var prefix = form.getAttribute('data-site-prefix');
  if (!input || !prefix) return;

  form.addEventListener('submit', function () {
    var keyword = input.value.trim();
    if (!keyword || keyword.indexOf('site:') === 0) return;
    input.value = prefix + ' ' + keyword;
  });
})();
