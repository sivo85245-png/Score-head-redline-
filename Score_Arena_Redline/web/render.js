/* Renderizador de perspectiva 3D em Canvas, sem bibliotecas remotas. */
(function(root){
'use strict';
const F=(n)=>Math.round(n).toLocaleString('pt-BR');
function setup(canvas){const r=canvas.getBoundingClientRect();if(!r.width||!r.height)return null;const d=window.devicePixelRatio||1,w=Math.round(r.width*d),h=Math.round(r.height*d);if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h}const c=canvas.getContext('2d');c.setTransform(d,0,0,d,0,0);return [c,r.width,r.height]}
function poly(c,points,fill,stroke){c.beginPath();points.forEach((p,i)=>i?c.lineTo(p.x,p.y):c.moveTo(p.x,p.y));c.closePath();if(fill){c.fillStyle=fill;c.fill()}if(stroke){c.strokeStyle=stroke;c.lineWidth=1;c.stroke()}}
function line(c,a,b,color,width=1){c.beginPath();c.moveTo(a.x,a.y);c.lineTo(b.x,b.y);c.strokeStyle=color;c.lineWidth=width;c.stroke()}
function ship(c,project,x,y,z,color,t,scale=1,boost=false){
 const p=(a,b,d)=>project(x+a*scale,y+b*scale,z+d*scale);
 // A nave é composta por faces tridimensionais: asas, fuselagem, cockpit e motores.
 c.save();c.shadowBlur=12;c.shadowColor=color;
 poly(c,[p(-1.05,0,-.42),p(-.22,.12,1.3),p(-.18,-.16,-.8)],'#7b4e61',color);
 poly(c,[p(1.05,0,-.42),p(.22,.12,1.3),p(.18,-.16,-.8)],'#bea4b0',color);
 poly(c,[p(-1.05,0,-.42),p(-.25,.18,.35),p(-.2,.05,-.8)],color,'#fff5');
 poly(c,[p(1.05,0,-.42),p(.25,.18,.35),p(.2,.05,-.8)],'#f8e9ef',color);
 poly(c,[p(0,.15,1.6),p(-.3,.15,.1),p(-.25,-.15,-.88),p(.25,-.15,-.88),p(.3,.15,.1)],'#fceff3',color);
 poly(c,[p(0,.38,.66),p(-.2,.17,.06),p(0,.18,-.45),p(.2,.17,.06)],'#231a32','#ffd9e5');
 line(c,p(0,.39,.66),p(0,.19,-.45),color,2);
 for(const side of [-1,1]){poly(c,[p(side*.35,0,-.55),p(side*.53,.02,-.65),p(side*.44,.03,-1.2-(boost?1.3:.5)*(1+Math.sin(t/45)*.18))],'#ff244480');line(c,p(side*.43,.02,-.55),p(side*.43,.02,-1.15-(boost?.9:0)),'#fff4ee',2)}c.restore();
}
function race(canvas,state,t){const data=setup(canvas);if(!data)return;const[c,w,h]=data;const horizon=h*.32;const focal=Math.min(w*.9,h*1.4);const project=(x,y,z)=>{const depth=Math.max(1,z+7);return {x:w*.5+x*focal/depth,y:horizon+(5.2-y)*focal/depth,s:focal/depth}};
 const sky=c.createLinearGradient(0,0,0,h);sky.addColorStop(0,'#180d20');sky.addColorStop(.5,'#72213e');sky.addColorStop(1,'#140e1d');c.fillStyle=sky;c.fillRect(0,0,w,h);
 // Planète et halo.
 const planetX=w*.77,planetY=h*.2,r=h*.15;const halo=c.createRadialGradient(planetX,planetY,r*.4,planetX,planetY,r*2.4);halo.addColorStop(0,'#fb567848');halo.addColorStop(1,'#fb567800');c.fillStyle=halo;c.fillRect(0,0,w,h*.65);
 const planet=c.createRadialGradient(planetX-r*.4,planetY-r*.3,2,planetX,planetY,r);planet.addColorStop(0,'#ffb9bd');planet.addColorStop(.5,'#d95770');planet.addColorStop(1,'#51263b');c.beginPath();c.arc(planetX,planetY,r,0,Math.PI*2);c.fillStyle=planet;c.fill();c.save();c.translate(planetX,planetY);c.rotate(-.25);c.beginPath();c.ellipse(0,0,r*1.65,r*.18,0,0,Math.PI*2);c.strokeStyle='#ffb3c450';c.lineWidth=3;c.stroke();c.restore();
 for(let i=0;i<80;i++){c.fillStyle=i%9?'#ffe7f066':'#fff';c.fillRect((Math.sin(i*72.15)*.5+.5)*w,(Math.cos(i*83.4)*.5+.5)*h*.4,i%9?1:2,1)}
 for(let layer=0;layer<3;layer++){const pts=[{x:0,y:h*.65}];for(let i=0;i<=20;i++)pts.push({x:i*w/20,y:horizon+layer*26-Math.abs(Math.sin(i*3.4+layer*8))*h*(.13-layer*.02)});pts.push({x:w,y:h*.65});poly(c,pts,['#3f2038','#301a2e','#211827'][layer])}
 const ground=c.createLinearGradient(0,horizon,0,h);ground.addColorStop(0,'#301b2c');ground.addColorStop(1,'#0c0c17');c.fillStyle=ground;c.fillRect(0,horizon+h*.07,w,h);
 poly(c,[project(-7,0,180),project(7,0,180),project(7,0,0),project(-7,0,0)],'#171420');
 for(let lane=0;lane<=4;lane++){const x=-6+lane*3;line(c,project(x,.01,160),project(x,.01,0),lane===0||lane===4?'#ff4058':'#f4dce923',lane===0||lane===4?3:1)}
 const motion=(state.playing&&!state.paused?state.elapsed:0)*27;
 for(let i=16;i>=0;i--){const z=(i*12-motion%12)+2;if(z>0){line(c,project(-6,0,z),project(6,0,z),'#ff759528');for(const side of [-1,1]){const x=side*7.1;poly(c,[project(x-.15,0,z),project(x+.15,0,z),project(x+.15,2.2,z),project(x-.15,2.2,z)],'#eec5d5');line(c,project(x,2.2,z),project(x,2.2,z+4),'#ff4058',2)}}}
 // Portiques de départ et structures lumineuses.
 for(const z of [130-motion%24,78-motion%24,40-motion%24]){for(const side of [-1,1]){const x=side*7.4;line(c,project(x,0,z),project(x,7,z),'#9a4564',5);line(c,project(x,7,z),project(side*4.9,9,z),'#e9b0c7',4)}line(c,project(-4.9,9,z),project(4.9,9,z),'#ff657c',4)}
 const objects=state.objects||[];
 const faces=[],labels=[];for(const o of objects){if(o.z<1||o.z>145)continue;faces.push({z:o.z,draw(){const x=(o.lane-1.5)*3,y=.7;if(o.type==='energy'){const a=project(x,y+.9,o.z),b=project(x+.55,y,o.z),d=project(x-.55,y,o.z),e=project(x,y-.6,o.z);c.save();c.shadowBlur=18;c.shadowColor='#fff';poly(c,[a,b,e,d],'#fff7f0','#ffb6c8');c.restore()}else{poly(c,[project(x-.9,0,o.z),project(x+.9,0,o.z),project(x+.9,1.4,o.z),project(x-.9,1.4,o.z)],'#932039','#ff566f');poly(c,[project(x-.9,1.4,o.z),project(x+.9,1.4,o.z),project(x+.9,1.4,o.z+1),project(x-.9,1.4,o.z+1)],'#e94a63');line(c,project(x-.6,.2,o.z),project(x+.6,1.2,o.z),'#fff1eb',2)}}})}
 const roster=state.racers||[];const player=roster.find(p=>p.id===state.playerId);const playerDistance=player?player.distance:0;
 for(let i=0;i<roster.length;i++){const p=roster[i];const me=p.id===state.playerId;const z=me?5:Math.max(10,Math.min(115,22+(i%3)*14+(p.distance-playerDistance)*.22));const x=(p.visualLane-1.5)*3+(me?0:Math.sin(i*4)*.28);faces.push({z,draw(){const y=1.05+Math.sin(t/650+i)*.05;const color=p.team?p.color:'#9facbf';ship(c,project,x,y,z,color,t,me?.85:.7,me&&state.boosting&&state.boost>0);const label=project(x,y+1.1,z);labels.push({point:label,name:p.name+(me?' / VOCE':''),me,team:p.team});}})}
 faces.sort((a,b)=>b.z-a.z);for(const f of faces)f.draw();
 const placed=[];labels.sort((a,b)=>a.point.y-b.point.y);
 for(const label of labels){c.font=(label.me?'11':'10')+'px Segoe UI';const width=c.measureText(label.name).width+16;let x=Math.max(width/2+10,Math.min(w-width/2-10,label.point.x)),y=label.point.y-4;
  for(let attempt=0;attempt<24;attempt++){const overlap=placed.some(b=>Math.abs(x-b.x)<(width+b.width)/2+5&&Math.abs(y-b.y)<19);if(!overlap)break;y-=20;if(y<75){y=label.point.y+20;x=Math.max(width/2+10,Math.min(w-width/2-10,x+(x<w/2?-90:90)))}}
  placed.push({x,y,width});line(c,label.point,{x,y:y+4},label.team?'#ff889c60':'#a69bb54a');c.fillStyle='#140e1edf';c.fillRect(x-width/2,y-12,width,18);c.fillStyle=label.team?'#ff4058':'#9a89a4';c.fillRect(x-width/2,y-12,2,18);c.fillStyle=label.team?'#fff1f4':'#c9bbc9';c.textAlign='center';c.fillText(label.name,x,y);
 }
 // Ombre périphérique et flash de collision.
 const vignette=c.createRadialGradient(w/2,h/2,h*.2,w/2,h/2,w*.7);vignette.addColorStop(0,'#0000');vignette.addColorStop(1,'#0906119c');c.fillStyle=vignette;c.fillRect(0,0,w,h);if(state.flash>0){c.fillStyle='#ff234335';c.fillRect(0,0,w,h)}
}
function algorithm(canvas,model,kind){const data=setup(canvas);if(!data)return;const[c,w,h]=data;c.clearRect(0,0,w,h);if(!model){c.fillStyle='#b69bac';c.font='12px Segoe UI';c.fillText('Termine uma corrida ou escolha uma amostra CSV.',18,h/2);return}const a=model.a,event=model.event;const max=Math.max(1,...a.map(x=>x.score));const active=i=>event&&(event.a===i||event.b===i);if(kind==='quick'){const gap=(w-30)/a.length;for(let i=0;i<a.length;i++){const x=15+i*gap,bar=(a[i].score/max)*(h-72),y=h-36-bar;const color=model.done?'#f3dce4':active(i)?'#fff1f5':'#e94361';const grad=c.createLinearGradient(x,y,x,h-36);grad.addColorStop(0,color);grad.addColorStop(1,'#77233c');c.fillStyle=grad;c.fillRect(x,y,Math.max(2,gap-4),bar);c.fillStyle='#a7899a';c.font='8px Consolas';c.textAlign='center';c.fillText(i,x+gap/2,h-18);if(a.length<=24){c.save();c.translate(x+gap/2,y-6);c.rotate(-.7);c.fillStyle=color;c.fillText(F(a[i].score),0,0);c.restore()}}if(event&&event.pivot!==undefined){const y=h-36-event.pivot/max*(h-72);c.setLineDash([4,5]);line(c,{x:12,y},{x:w-10,y},'#fff8',1);c.setLineDash([]);c.textAlign='left';c.fillStyle='#fff';c.font='10px Segoe UI';c.fillText('PIVÔ '+F(event.pivot),15,16)}}else{const visible=Math.min(a.length,31),levels=Math.floor(Math.log2(Math.max(visible,1)))+1;const coords=[];for(let i=0;i<visible;i++){const level=Math.floor(Math.log2(i+1)),start=2**level-1,count=2**level;coords.push({x:(i-start+.5)/count*(w-12)+6,y:30+level*(h-74)/Math.max(1,levels-1)})}for(let i=1;i<visible;i++)line(c,coords[(i-1)>>1],coords[i],'#684354');for(let i=0;i<visible;i++){const p=coords[i],r=a.length<=12?21:15;const extracted=event&&event.heap!==undefined&&i>=event.heap;c.beginPath();c.arc(p.x,p.y,r,0,Math.PI*2);c.fillStyle=active(i)?'#f8e5ed':extracted?'#483c49':'#672b42';c.fill();c.strokeStyle=extracted?'#8d7a89':'#ff6982';c.stroke();c.fillStyle=active(i)?'#391c2b':'#fff';c.font=`${a.length<=12?9:8}px Consolas`;c.textAlign='center';c.fillText(a[i].score>=10000?Math.round(a[i].score/1000)+'k':a[i].score,p.x,p.y+3)}c.fillStyle='#ad91a1';c.textAlign='left';c.font='9px Segoe UI';c.fillText(visible<a.length?'Árvore: primeiros 31 nós. Vetor completo na lista abaixo.':'Raiz = índice 0 · Valores abreviados; exatos na lista abaixo.',12,h-12)}}
root.ArenaRender={setup,race,algorithm};
})(window);
