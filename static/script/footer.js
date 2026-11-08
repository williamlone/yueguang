//版权信息
var blogBase = document.currentScript.src.replace(/\/script\/footer\.js(\?.*)?$/, '');
document.currentScript.insertAdjacentHTML('afterEnd','<a href="' + blogBase + '/archives/1.html">联系我们</a> ┊ <a href="' + blogBase + '/archives/2414.html">投放广告</a> ┊ 版权所有：深圳市南山区月光博客信息咨询部 ┊ 备案号：<a href="http://beian.miit.gov.cn/" rel="nofollow">粤ICP备16102788号-1</a>┊ Powered by：Hugo ');

// google analytics
/*
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-272027-5']);
_gaq.push(['_trackPageview']);
(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
*/

// google analytics
// Global site tag (gtag.js) - Google Analytics

var imported = document.createElement('script');
imported.src = 'https://www.googletagmanager.com/gtag/js?id=UA-272027-5';
document.head.appendChild(imported);
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'UA-272027-5');


// baidu tongji
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "//hm.baidu.com/hm.js?4c883bb3fd82099c8817b0063a78be5f";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();

// cloudflare tongji
(function() {
var js = document.createElement('script');
js.setAttribute('data-cf-beacon', '{"token": "f792c3d32f584d7790561b2c23e80f17"}');
js.setAttribute('defer', true);
js.setAttribute('src', 'https://static.cloudflareinsights.com/beacon.min.js');
document.body.appendChild(js);
})();


//通栏广告
//  $(".content.alpha").prepend("<center><a rel='nofollow' href='https://ngmov.me/?channelCode=ngyg93' target='_blank'><img src='/images/ads.jpg' alt='add 2020-1-7'></a></center>");
//  $(".divSearchPanel").append("<center><a rel='nofollow' href='https://www.ivacykodi.com/best-deal-offer-cn/?aff=91574' target='_blank'><img src='/images/300X250.png' border='0' alt='add 2020-1-7'></a></center>");
