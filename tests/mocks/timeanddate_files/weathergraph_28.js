//Copyright timeanddate.com 2021, do not use without permission
var $jscomp=$jscomp||{};$jscomp.scope={};$jscomp.ASSUME_ES5=!1;$jscomp.ASSUME_NO_NATIVE_MAP=!1;$jscomp.ASSUME_NO_NATIVE_SET=!1;$jscomp.SIMPLE_FROUND_POLYFILL=!1;$jscomp.defineProperty=$jscomp.ASSUME_ES5||"function"==typeof Object.defineProperties?Object.defineProperty:function(d,k,f){d!=Array.prototype&&d!=Object.prototype&&(d[k]=f.value)};$jscomp.getGlobal=function(d){return"undefined"!=typeof window&&window===d?d:"undefined"!=typeof global&&null!=global?global:d};$jscomp.global=$jscomp.getGlobal(this);
$jscomp.polyfill=function(d,k,f,g){if(k){f=$jscomp.global;d=d.split(".");for(g=0;g<d.length-1;g++){var m=d[g];m in f||(f[m]={});f=f[m]}d=d[d.length-1];g=f[d];k=k(g);k!=g&&null!=k&&$jscomp.defineProperty(f,d,{configurable:!0,writable:!0,value:k})}};$jscomp.polyfill("Array.prototype.fill",function(d){return d?d:function(d,f,g){var k=this.length||0;0>f&&(f=Math.max(0,k+f));if(null==g||g>k)g=k;g=Number(g);0>g&&(g=Math.max(0,k+g));for(f=Number(f||0);f<g;f++)this[f]=d;return this}},"es6","es3");
$jscomp.polyfill("Object.is",function(d){return d?d:function(d,f){return d===f?0!==d||1/d===1/f:d!==d&&f!==f}},"es6","es3");$jscomp.polyfill("Array.prototype.includes",function(d){return d?d:function(d,f){var g=this;g instanceof String&&(g=String(g));var k=g.length;f=f||0;for(0>f&&(f=Math.max(f+k,0));f<k;f++){var q=g[f];if(q===d||Object.is(q,d))return!0}return!1}},"es7","es3");
$jscomp.checkStringArgs=function(d,k,f){if(null==d)throw new TypeError("The 'this' value for String.prototype."+f+" must not be null or undefined");if(k instanceof RegExp)throw new TypeError("First argument to String.prototype."+f+" must not be a regular expression");return d+""};$jscomp.polyfill("String.prototype.includes",function(d){return d?d:function(d,f){return-1!==$jscomp.checkStringArgs(this,d,"includes").indexOf(d,f||0)}},"es6","es3");
(function(){function d(a){return a.targetTouches&&1<=a.targetTouches.length?a.targetTouches[0].clientX:a.clientX}function k(a,b,c,h,e,d,f){var n=Math.sqrt(Math.pow(c-a,2)+Math.pow(h-b,2));n=f*n/(n+Math.sqrt(Math.pow(e-c,2)+Math.pow(d-h,2)));f-=n;return[c+n*(a-e),h+n*(b-d),c-f*(a-e),h-f*(b-d)]}function f(a,b,c){var h=[],e,d=b.length;for(e=0;e<d-4;e+=2)h=h.concat(k(b[e],b[e+1],b[e+2],b[e+3],b[e+4],b[e+5],c));a.lineTo(b[0],b[1]);a.quadraticCurveTo(h[0],h[1],b[2],b[3]);for(e=2;e<b.length-5;e+=2)a.bezierCurveTo(h[2*
e-2],h[2*e-1],h[2*e],h[2*e+1],b[e+2],b[e+3]);a.lineTo(b[d-2],b[d-1])}function g(a,b){b=b.split(" ");a.beginPath();for(var c=0,h=b.length;c<h;c++){var e=b[c].charAt(0),d=b[c].substr(1).split(",");switch(e){case "M":a.moveTo(d[0],d[1]);break;case "L":a.lineTo(d[0],d[1]);break;case "S":a.stroke();break;case "F":a.fill()}}a.closePath()}function m(a,b,c,d){if(p){var e=a.getContext("2d"),h=.6*a.width,f=.17*h;a.width=a.width;e.strokeStyle=d||"black";e.fillStyle=d||"black";if(1<=b){e.translate(.2*a.width+
.5,.5*a.width+.5);a.style[UA.trans]="rotate("+(parseFloat(c)+90)+"deg)";g(e,"M0,0 L"+h+",0 L"+(h-f)+","+f+" M"+h+",0 L"+(h-f)+","+(0-f)+" S");a=Mf((b+2)/5);for(c=2;10<=a;)e.save(),e.translate(c,0),g(e,"M0,0 L0,"+2*-f+" L"+.8*f+",0 F"),a-=10,c+=f,e.restore();for(b=0;b<a;b++)e.save(),e.translate(c,b%2?-f:0),g(e,"M0,0 L0,"+-f+" S"),c+=0==b%2?0:.8*f,e.restore()}else e.translate(a.width/2,a.width/2),e.arc(0,0,h/2,0,2*Math.PI),e.stroke()}else e=cE("img"),e.src="//c.tadst.com/gfx/comp/sa0.png",a.className=
"static",aCh(a,e),e.style.filter=UA.mat(c+180),e.style.marginTop=(14-e.offsetHeight)/2+"px",e.style.marginLeft=(14-e.offsetWidth)/2+"px"}function q(a){this.w=a;this.l="temp";this.u=1195;this.h=360;this.b=90;this.t=85;this.g=this.w.grid[this.l];--this.g.low;this.g.range+=1;10>this.g.range&&(a=10-this.g.range,this.g.high+=Mf(a/2),this.g.low-=Math.ceil(a/2),this.g.range=10);this.j=this.h-this.b-this.t;this.s=this.j/this.g.range;this.m=Math.max(this.v(this.w.grid.prec.high,"prec"),Math.max(this.w.grid.time/
36E5/2*20,20));this.e=this.w.grid.sections;this.q=this.u/this.e}function r(a,b,c,d,e,f){var h=document.createDocumentFragment();this.a=b;this.b=c;this.c=d;this.w=this.b.w.detail[this.c];this.e=e;this.f=this.b.p(b);this.g=cE("div",{id:"ws_"+b,"class":"section"+(e?" divide":"")},h);esa(this.g,{w:this.b.q});if(e){c=len=this.b.w.detail.length;for(b=this.c+1;b<len;b++)if(this.b.w.detail[b].hl){c=b;break}b=(c-this.c)*this.b.q;this.h=cE("div",{"class":"date"},this.g);esa(this.h,{w:b})}if(this.w.rain||this.w.snow)this.i=
cE("div",{"class":"prec"},this.g),this.w.snow&&(this.k=cE("div",{"class":"snow"},this.i),this.l=cE("div",{"class":"text"},this.i)),this.w.rain&&(this.m=cE("div",{"class":"rain"},this.i),this.n=cE("div",{"class":"text"},this.i));void 0!=this.w.templow&&(void 0===this.b.w.temp&&(this.o=cE("div",{"class":"tempBox"},this.g)),this.p=cE("div",{"class":"tempLow"},this.g));this.q=cE("div",{"class":"time"},this.g);this.r=cE("div",{"class":"wicon"},this.g);this.s=cE("div",{"class":"temp"},this.g);this.t=cE("div",
{"class":"wind"},this.g);this.u=cE(p?"canvas":"div",{"class":"wsicon",width:40,height:40},this.t);this.v=cE("div",{"class":"wstext"},this.t);f&&this.setData();aCh(a,h)}function t(a,b){var c=this;c.a=a;c.b=a.parentNode;c.c=new q(b);c.d=!p;c.e=16;c.f=-1;c.s=0;c.t=0;c.g=[];c.h();c.i();c.j();c.k();c.l();c.b.parentNode.style.position="relative";c.b.onmousemove=function(a){a=a||event;c.showTooltip(a.pageX||a.clientX,"mousemove")};ael(c.b,"mousedown",function(a){c.showTooltip(d(a),"mousedown")});ael(c.b,
"touchstart",function(a){c.showTooltip(d(a),"touchstart")});p?(c.m=cE("canvas",{width:c.g.length*c.c.q,height:c.a.offsetHeight,"class":"linegraph"}),aCh(c.a,c.m)):(document.namespaces.add("v","urn:schemas-microsoft-com:vml"),c.n=cE("v:polyline",{coordorigin:"0,0",coordsize:c.a.scrollWidth+" "+c.a.offsetHeight,width:c.a.scrollWidth+"px",height:c.a.offsetHeight+"px",filled:"FALSE",strokecolor:"#fedb77",strokeweight:"1pt","class":"linegraph"}),aCh(c.a,c.n));c.r()}function u(a,b){this.a=gf(a);this.b=
gf(b);this.c=0;this.d=!1;this.e=0;this.f=45;this.g=200;this.h=!1;this.i=0;this.j();this.k=this.b.offsetWidth;this.l=this.a.scrollWidth}var l=document,v="N NNE NE ENE E ESE SE SSE S SSW SW WSW W WNW NW NNW".split(" "),p=void 0!==cE("canvas").getContext;q.prototype={p:function(a){return this.q*a},r:function(a){var b;var c=0;for(b=this.w.detail.length;c<b;c++){var d=this.w.detail[c].date;if(a>=d&&a<d+this.w.grid.time)return c*this.q+(a-d)/this.w.grid.time*this.q}return a<this.w.detail[0].date?0:(b+1)*
this.q},z:function(a){return(this.g.range-(this.w.detail[a][this.l]-this.g.low))*this.s+this.t},x:function(a){return(this.g.range-a+this.g.low)*this.s+this.t},c:function(a){a=this.w.detail[a];var b=this.v(a.rain,"prec")||0,c=this.v(a.snow,"prec")||0;return{rain:a.rain?(this.h-this.b-10)/this.m*b:0,snow:a.snow?(this.h-this.b-10)/this.m*c:0,intensity:Math.min(10,b+c),ratio:b/(b+c)}},v:function(a,b){return"pc"===b||"hum"===b?a:"cf"===b?(parseFloat(a)+this.w.conv.temp.offset)*this.w.conv.temp.scale:(parseFloat(a)+
this.w.conv[b].offset)*this.w.conv[b].scale},n:function(a,b){return"pc"===b||"hum"===b?a:"cf"===b?parseFloat(a)/this.w.conv.temp.scale-this.w.conv.temp.offset:parseFloat(a)/this.w.conv[b].scale-this.w.conv[b].offset},o:function(a){this.l=a;this.g=this.w.grid[this.l];this.s=this.j/this.g.range}};r.prototype={onmouseover:function(a){},setData:function(){var a=this,b=a.b.z(a.c)||150;a.g.tempPos=b;a.g.pos=a.c*a.b.sectionWidth;void 0!=a.w.templow?(ih(a.s,"Hi:"+Math.round(a.w[a.b.l])),ac(a.s,"low",1),esa(a.s,
{y:b-15}),ih(a.p,"Lo:"+Math.round(a.w.templow)),ac(a.p,"low",1),esa(a.p,{y:a.b.x(a.w.templow)})):(ih(a.s,void 0!==a.w[a.b.l]?Math.round(a.w[a.b.l]):"N/A"),a.s.style.transform="translateY("+(b-30)+"px)");sA(a.r,"data-icon",a.w.icon);a.r.style.transform="translateY("+(b-70)+"px)";if(a.w.rain||a.w.snow){var c=a.b.c(a.c);a.w.rain&&(esa(a.m,{h:c.rain}),a.m.style.opacity=a.w.pc/100,a.n.style.bottom=Math.max(0,c.rain/2-6)+"px",ih(a.n,0<c.rain?a.w.rain:""));a.w.snow&&(esa(a.k,{h:c.snow}),a.k.style.opacity=
a.w.pc/100,a.k.style.bottom=c.rain+"px",a.l.style.bottom=Math.max(c.rain?c.rain/2+8:0,c.rain+(c.snow-c.rain)/2-6)+"px",ih(a.l,0<c.snow?a.w.snow:""))}void 0!==a.w.wind&&(m(a.u,a.b.v(a.w.wind,"wind"),a.w.wd),ih(a.v,Math.round(a.w.wind)));a.e&&ih(a.h,a.w.hls);void 0!==a.w.templow&&void 0===a.b.w.temp&&esa(a.o,{h:(a.w.temp-a.w.templow)*a.b.s,y:b});ih(a.q,a.w.ts);a.g.onmouseover=function(){a.onmouseover(a.c,a.g.pos+a.b.sectionWidth/2)}},setHighlight:function(a){ac(this.g,"highlight",a)}};t.prototype={h:function(){this.o=
cE("div",{"class":"weatherTooltip"});aCh(this.a.parentNode.parentNode,this.o)},i:function(){var a=this.c.w.sunrise,b=0;if(a)for(var c=this.c.w.detail.length*this.c.q;b<a.length;b++){var d=a[b],e=Mf(this.c.r(d.date));if(e>c)break;var f=(b===a.length-1?c:Mf(this.c.r(a[b+1].date)))-e;d=cE("div",{"class":"s"===d.type?"night":"day"});d.style.width=f+"px";d.style.marginLeft=e+"px";aCh(this.a,d)}},k:function(){var a=document.createDocumentFragment(),b,c=this;for(b=0;b<c.c.w.detail.length;b++){var d=new r(a,
b,c.c,b,c.c.w.detail[b].hl,c.d);c.g.push(d)}aCh(c.a,a);c.d||setTimeout(function(){for(b=0;b<c.g.length;b++)c.g[b].setData()},1)},j:function(){this.q=cE("div",{"class":"weatherGrid"});this.a.parentNode.parentNode.insertBefore(this.q,this.a.parentNode);var a=cE("div",null,this.q);ih(a,"Time");a.style.top=0;a=cE("div",null,this.q);ih(a,sprintf("Wind<br> (%s)",this.c.w.units.wind));a.style.bottom=0;0<this.c.w.grid.prec.high&&(a=cE("div",null,this.q),ih(a,sprintf("Rain/Snow<br>(%s)",this.c.w.units.prec)),
a.style.bottom="60px");a=cE("div",null,this.q);ih(a,sprintf("Temp<br> (%s)",this.c.w.units.temp));a.style.bottom="85%";a=Math.ceil(this.c.g.range/12);for(var b=this.c.g.low;b<=this.c.g.high+1;b+=a){var c=this.c.x(b),d=cE("div",{"class":"gridline"},this.a);esa(d,{y:c,w:this.c.w.detail.length*this.c.q});d=cE("div",{"class":"gridtext"},this.q);ih(d,b);esa(d,{y:c})}0>=Mf(this.c.v(this.c.g.low,"temp"))&&0<=Math.ceil(this.c.v(this.c.g.high,"temp"))&&(c=this.c.x(Math.round(this.c.n(0,"temp"))),d=cE("div",
{"class":"gridline zero"},this.a),esa(d,{y:c,w:this.c.w.detail.length*this.c.q}))},l:function(){var a=this,b=0;a.p=cE("div",{"class":"weatherLinks"},a.a.parentNode.parentNode);for(var c=0;c<a.c.w.detail.length;c++)a.c.w.detail[c].hl&&(b=cE("a",{href:"#"},a.p),ih(b,a.c.w.detail[c].hls),b.to=linkTo=gf("ws_"+c),b.onclick=function(){a.s=parseInt(this.to.id.match(/\d+/)[0]);sc.jumpToElement(this.to);return!1},b=b.to.offsetLeft);b<a.a.parentNode.offsetWidth&&sd(a.p,0)},r:function(){var a=this;if(p){var b=
a.m.getContext("2d");a.m.width=a.m.width;b.strokeStyle="#fedb77";b.lineWidth=2;b.setLineDash&&b.setLineDash([5,2])}var c=function(c,d){var e,h=[],g=[];for(e=0;e<c.length;e++){var k=c[e];h.push(a.c.r(k.date)+(d?a.c.q/2:0));h.push(a.c.x(k[a.c.l]));e<c.length-1&&72E5<c[e+1].date-c[e].date&&g.push(e)}p?(b.beginPath(),f(b,h,.25,g),b.stroke(),g.forEach(function(c){var d=h[2*c];c=b.getImageData(d,0,(void 0!==h[2*(c+1)]?h[2*(c+1)]:a.m.width)-d,a.m.height);for(var e=c.data,f=0,g=e.length;f<g;f+=4)e[f]=0<e[f]?
220:e[f],e[f+1]=220,e[f+2]=220;b.putImageData(c,d,0)})):a.n.points.value=h.join(" ")};a.c.w.temp?a.c.w.temp[0][a.c.l]&&c(a.c.w.temp):void 0===a.c.w.detail[0].templow&&a.c.w.detail[0][a.c.l]&&c(a.c.w.detail,!0)},showTooltip:function(a,b){if(a-=this.b.getBoundingClientRect().left)this.e=Math.max(16,Math.min(1195,a));["mousedown","mousemove","touchstart"].includes(b)?(a=Mf((this.b.scrollLeft+this.e)/this.c.q),this.t=(a%4-1+4)%4):a=0==this.s?this.s:this.s+this.t;if(this.f!==a){b=this.c.w.detail[a];if(!b)return;
var c=v[Mf((b.wd+11.25)/22.5%16)],d=this.c.w.units,e="Rain: "+(b.rain||0)+d.prec+" Snow: "+(b.snow||0)+d.prec;ih(this.o,"           <div class=date>"+b.ds+"</div><div class=hr></div><div class=\"inner__block\"><div class=left__block><div class='wicon-large' data-icon='"+b.icon+"'></div><div class=tempblock><div class=temp>"+("undefined"!=typeof b.temp?Math.round(b.temp):"N/A")+(void 0!==b.templow?" / "+Math.round(b.templow):"")+" "+d.temp+"</div>"+(void 0!==b.desc?"<div class=wdesc>"+b.desc+"</div>":
"")+"</div></div><div class='mid__block'>"+(void 0!==b.cf?"<div><span class=indent>Feels Like: </span>"+Math.round(b.cf)+" "+d.temp+"</div>":"")+(void 0!==b.hum?"<div><span class=indent>Humidity: </span>"+b.hum+"%</div>":"")+(void 0!==b.baro?"<div><span class=indent>Barometer: </span>"+b.baro+" "+d.baro+"</div>":"")+(void 0!==b.pc?"<div>Precipitation: "+e+"</div>":"")+(void 0!==b.pc?"<div>Precipitation Chance: "+b.pc+"%</div>":"")+"</div><div class='right__block'>"+(void 0!==b.wind?'<canvas id="tt-wind" class=wind width=40 height=40></canvas>':
"")+(void 0!==b.wind?"<div class=windDirection>"+c+"</div>":"")+(void 0!==b.wind?"<div><span class=indent>Wind: </span>"+b.wind+" "+d.wind+"</div>":"")+'</div></div><div id="tt-arrow" class=arrow></div>');void 0!==b.wind&&(c=gf("tt-wind"),m(c,this.c.v(b.wind,"wind"),b.wd,"white"));this.g[a]&&this.g[a].setHighlight(!0);this.g[this.f]&&this.g[this.f].setHighlight(!1);this.f=a}gf("tt-arrow").style.left=this.e+"px"},setBgType:function(a){var b;for(b=0;b<this._sections.length;b++)this.g[b].setBgType(a)},
setLineType:function(a){this.c.o(a);var b;for(b=0;b<this.g.length;b++)this.g[b].setLineType(a);this.r()}};u.prototype={j:function(){var a=this;"undefined"!==typeof window.ontouchstart&&ael(a.a,"touchstart",function(b){a.u(b)});ael(a.a,"mousedown",function(b){a.u(b)})},n:function(){var a=+new Date;var b=a-this.o;this.o=a;a=this.c-this.p;this.p=this.c;this.q=1E3*a/(1+b)*.8+.2*this.q},r:function(){var a=this;if(a.s){var b=+new Date-a.o;b=-a.s*Math.exp(-b/325);.5<b||-.5>b?(a.jumpTo(a.t+b),raf(function(){a.r()})):
(a.jumpTo(a.t),a.a.scrolling=!1)}else a.a.scrolling=!1},u:function(a){a=a||event;var b=this;l.onmousemove=function(a){b.w(a)};l.onmouseup=function(a){b.x(a)};l.ontouchmove=function(a){b.w(a)};l.ontouchend=function(a){b.x(a)};b.h=!0;b.a.scrolling=!0;b.i=d(a);b.q=b.s=0;b.p=b.c;b.o=+new Date;clearInterval(b.v);b.v=setInterval(function(){b.n()},100);a.preventDefault?a.preventDefault():a.returnValue=!1;return!1},w:function(a){a=a||event;if(this.h){var b=d(a);var c=this.i-b;if(2<c||-2>c)this.i=b,this.jumpTo(this.c+
c)}this.a.scrolling=!0;a.preventDefault?a.preventDefault():a.returnValue=!1;a.stopPropagation?a.stopPropagation():a.cancelBubble=!0;return!1},x:function(a){a=a||event;var b=this;l.onmousemove="";l.onmouseup="";l.ontouchmove="";l.ontouchend="";b.h=!1;clearInterval(b.v);10<b.q||-10>b.q?(b.s=.8*b.q,b.t=Math.round(b.c+b.s),b.o=+new Date,raf(function(){b.r()})):b.a.scrolling=!1;a.preventDefault?a.preventDefault():a.returnValue=!1;a.stopPropagation?a.stopPropagation():a.cancelBubble=!0;return!1},y:function(a,
b){var c=this;b=b>c.g?c.g:b;c.jumpTo(c.c+a*b);c.d&&(c.e=setTimeout(function(){c.y(a,b+5)},100))},z:function(a){var b=this;b.d=!0;b.a.scrolling=!0;b.y(a,b.f);l.onmouseup=function(){b.d=!1;clearTimeout(b.e);b.a.scrolling=!1;l.onmouseup=""}},onScroll:function(a){},bindScrollLeftTo:function(a){var b=this;b.aa=a;ael(a,"mousedown",function(){b.z(-1)})},bindScrollRightTo:function(a){var b=this;b.bb=a;ael(a,"mousedown",function(){b.z(1)})},jumpTo:function(a){this.l=this.a.scrollWidth;this.c=a=0>=a?0:this.l-
a<this.k?this.l-this.k:a;this.b.scrollLeft=a;ac(this.aa,"hidden",4>=a);ac(this.bb,"hidden",a>=this.l-this.k-4);this.onScroll(a)},jumpToElement:function(a){var b=this;b.s=a.offsetLeft-b.c;b.t=a.offsetLeft;b.o=+new Date;raf(function(){b.r()})},getBounds:function(){return{x1:this.c,x2:this.c+this.k}}};ael(window,"load",function(){var a=gf("weather");window.wg=new t(a,data);window.sc=new u("weather","weatherContainer");sc.bindScrollLeftTo(gf("navLeft"));sc.bindScrollRightTo(gf("navRight"));sc.onScroll=
function(){wg.showTooltip()};setTimeout(function(){sc.jumpTo(void 0!==window.wgsp?wgsp:0)},100)})})();