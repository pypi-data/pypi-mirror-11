/*
 *  /MathJax/jax/output/HTML-CSS/autoload/maction.js
 *
 *  Copyright (c) 2009-2013 The MathJax Consortium
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

MathJax.Hub.Register.StartupHook("HTML-CSS Jax Ready",function(){var g="2.3";var c=MathJax.ElementJax.mml,e=MathJax.OutputJax["HTML-CSS"];var d,f,b;var a=e.config.tooltip=MathJax.Hub.Insert({delayPost:600,delayClear:600,offsetX:10,offsetY:5},e.config.tooltip||{});c.maction.Augment({HTMLtooltip:e.addElement(document.body,"div",{id:"MathJax_Tooltip"}),toHTML:function(j,h,l){var i=this.selected();if(i.type=="null"){j=this.HTMLcreateSpan(j);j.bbox=this.HTMLzeroBBox();return j}j=this.HTMLhandleSize(this.HTMLcreateSpan(j));j.bbox=null;var k=i.toHTML(j);if(l!=null){e.Remeasured(i.HTMLstretchV(j,h,l),j)}else{if(h!=null){e.Remeasured(i.HTMLstretchH(j,h),j)}else{e.Measured(k,j)}}this.HTMLhandleHitBox(j);this.HTMLhandleSpace(j);this.HTMLhandleColor(j);return j},HTMLhandleHitBox:function(i,l){var k;if(e.msieHitBoxBug){var j=e.addElement(i,"span",{isMathJax:true});k=e.createFrame(j,i.bbox.h,i.bbox.d,i.bbox.w,0,"none");i.insertBefore(j,i.firstChild);j.style.marginRight=e.Em(-i.bbox.w);if(e.msieInlineBlockAlignBug){k.style.verticalAlign=e.Em(e.getHD(i).d-i.bbox.d)}}else{k=e.createFrame(i,i.bbox.h,i.bbox.d,i.bbox.w,0,"none");i.insertBefore(k,i.firstChild);k.style.marginRight=e.Em(-i.bbox.w)}k.className="MathJax_HitBox";k.id="MathJax-HitBox-"+this.spanID+(l||"")+e.idPostfix;var h=this.Get("actiontype");if(this.HTMLaction[h]){this.HTMLaction[h].call(this,i,k,this.Get("selection"))}},HTMLstretchH:c.mbase.HTMLstretchH,HTMLstretchV:c.mbase.HTMLstretchV,HTMLaction:{toggle:function(i,j,h){this.selection=h;j.onclick=i.childNodes[1].onclick=MathJax.Callback(["HTMLclick",this]);j.style.cursor=i.childNodes[1].style.cursor="pointer"},statusline:function(i,j,h){j.onmouseover=i.childNodes[1].onmouseover=MathJax.Callback(["HTMLsetStatus",this]);j.onmouseout=i.childNodes[1].onmouseout=MathJax.Callback(["HTMLclearStatus",this]);j.onmouseover.autoReset=j.onmouseout.autoReset=true},tooltip:function(i,j,h){if(this.data[1]&&this.data[1].isToken){j.title=j.alt=i.childNodes[1].title=i.childNodes[1].alt=this.data[1].data.join("")}else{j.onmouseover=i.childNodes[1].onmouseover=MathJax.Callback(["HTMLtooltipOver",this]);j.onmouseout=i.childNodes[1].onmouseout=MathJax.Callback(["HTMLtooltipOut",this]);j.onmouseover.autoReset=j.onmouseout.autoReset=true}}},HTMLclick:function(l){this.selection++;if(this.selection>this.data.length){this.selection=1}var k=this;while(k.type!=="math"){k=k.inherit}var h=MathJax.Hub.getJaxFor(k.inputID),j=!!h.hover;h.Update();if(j){var i=document.getElementById(h.inputID+"-Span");MathJax.Extension.MathEvents.Hover.Hover(h,i)}return MathJax.Extension.MathEvents.Event.False(l)},HTMLsetStatus:function(h){this.messageID=MathJax.Message.Set((this.data[1]&&this.data[1].isToken)?this.data[1].data.join(""):this.data[1].toString())},HTMLclearStatus:function(h){if(this.messageID){MathJax.Message.Clear(this.messageID,0)}delete this.messageID},HTMLtooltipOver:function(i){if(!i){i=window.event}if(b){clearTimeout(b);b=null}if(f){clearTimeout(f)}var h=i.pageX;var k=i.pageY;if(h==null){h=i.clientX+document.body.scrollLeft+document.documentElement.scrollLeft;k=i.clientY+document.body.scrollTop+document.documentElement.scrollTop}var j=MathJax.Callback(["HTMLtooltipPost",this,h+a.offsetX,k+a.offsetY]);f=setTimeout(j,a.delayPost)},HTMLtooltipOut:function(h){if(f){clearTimeout(f);f=null}if(b){clearTimeout(b)}var i=MathJax.Callback(["HTMLtooltipClear",this,80]);b=setTimeout(i,a.delayClear)},HTMLtooltipPost:function(o,m){f=null;if(b){clearTimeout(b);b=null}var p=this.HTMLtooltip;p.style.display="block";p.style.opacity="";p.style.filter=e.config.styles["#MathJax_Tooltip"].filter;if(this===d){return}p.style.left=o+"px";p.style.top=m+"px";p.innerHTML='<span class="MathJax"><nobr></nobr></span>';var q=p.insertBefore(e.EmExSpan.cloneNode(true),p.firstChild);var l=q.firstChild.offsetHeight/60,h=q.lastChild.firstChild.offsetHeight/60;e.em=e.outerEm=c.mbase.prototype.em=h;var i=Math.floor(Math.max(e.config.minScaleAdjust/100,(l/e.TeX.x_height)/h)*e.config.scale);p.firstChild.style.fontSize=i+"%";q.parentNode.removeChild(q);var n=e.createStack(p.firstChild.firstChild);var k=e.createBox(n);try{e.Measured(this.data[1].toHTML(k),k)}catch(j){if(!j.restart){throw j}p.style.display="none";MathJax.Callback.After(["HTMLtooltipPost",this,o,m],j.restart);return}e.placeBox(k,0,0);e.createRule(p.firstChild.firstChild,k.bbox.h,k.bbox.d,0);d=this},HTMLtooltipClear:function(i){var h=this.HTMLtooltip;if(i<=0){h.style.display="none";h.style.opacity=h.style.filter="";b=null}else{h.style.opacity=i/100;h.style.filter="alpha(opacity="+i+")";b=setTimeout(MathJax.Callback(["HTMLtooltipClear",this,i-20]),50)}}});MathJax.Hub.Browser.Select({MSIE:function(h){e.msieHitBoxBug=true}});MathJax.Hub.Startup.signal.Post("HTML-CSS maction Ready");MathJax.Ajax.loadComplete(e.autoloadDir+"/maction.js")});
