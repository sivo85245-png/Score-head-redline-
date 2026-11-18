/* Algoritmos sobre registros completos. Usados no duelo e ranking demonstrativo. */
(function(root){
'use strict';
function* quick(a){
 const stack=[[0,a.length-1]];
 while(stack.length){const [lo,hi]=stack.pop();if(lo>=hi)continue;
  const pivot=a[(lo+hi)>>1].score;let lt=lo,i=lo,gt=hi;
  yield {type:'pivot',a:(lo+hi)>>1,b:hi,pivot,lo,hi};
  while(i<=gt){yield {type:'compare',a:i,b:gt,pivot,lo,hi};
   if(a[i].score<pivot){if(i!==lt){[a[i],a[lt]]=[a[lt],a[i]];yield {type:'swap',a:i,b:lt,pivot,lo,hi}}i++;lt++}
   else{yield {type:'compare',a:i,b:gt,pivot,lo,hi};if(a[i].score>pivot){if(i!==gt){[a[i],a[gt]]=[a[gt],a[i]];yield {type:'swap',a:i,b:gt,pivot,lo,hi}}gt--}else i++}
  }
  const l=[lo,lt-1],r=[gt+1,hi];if(l[1]-l[0]>r[1]-r[0])stack.push(l,r);else stack.push(r,l);
 }
}
function* heap(a){
 function* down(i,n){while(i*2+1<n){let c=i*2+1;if(c+1<n){yield {type:'compare',a:c,b:c+1,heap:n};if(a[c+1].score>a[c].score)c++}yield {type:'compare',a:i,b:c,heap:n};if(a[i].score>=a[c].score)break;[a[i],a[c]]=[a[c],a[i]];yield {type:'swap',a:i,b:c,heap:n};i=c}}
 for(let i=(a.length>>1)-1;i>=0;i--)yield* down(i,a.length);
 for(let end=a.length-1;end>0;end--){[a[0],a[end]]=[a[end],a[0]];yield {type:'swap',a:0,b:end,heap:end};yield* down(0,end)}
}
function sortedCopy(a,kind='quick'){const b=a.slice();for(const e of (kind==='heap'?heap:quick)(b)){}return b}
function valid(original,a){if(original.length!==a.length)return false;const m=new Map(original.map(p=>[p.id,p.score]));return a.every((p,i)=>{if((i&&a[i-1].score>p.score)||m.get(p.id)!==p.score)return false;return m.delete(p.id)})&&m.size===0}
const team=['Vitor Silva de Oliveira','Samuel Pedro','Luís Gustavo','Mateus','Gabriel','Juliano','João'];
const pilots=[...team,'Helena Duarte','Rafael Monteiro','Camila Torres','Bruno Azevedo','Isabela Costa'].map((name,i)=>({id:'race-'+i,name,team:i<7,score:0,color:i<7?['#ff334b','#fff3f3','#ff7688','#ffadad','#d6dce7','#b92146','#ff496b'][i]:'#8196b0'}));
const api={quick,heap,sortedCopy,valid,team,pilots};root.ArenaEngine=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
