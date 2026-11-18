/* Testes de lógica com DOM simulado: não substituem inspeção visual no navegador. */
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const root=__dirname,read=name=>fs.readFileSync(path.join(root,'web',name),'utf8');
const E=require('./web/engine.js');
const dataContext={window:{}};vm.createContext(dataContext);vm.runInContext(read('datasets.js'),dataContext);const data=dataContext.window.APS_DATA;
for(const [scenario,rows] of Object.entries(data.scenarios)){
 const original=rows.map(([id,score])=>({id,score})),before=JSON.stringify(original);
 for(const kind of ['quick','heap']){const sorted=E.sortedCopy(original,kind);assert(E.valid(original,sorted),scenario+' '+kind);assert.equal(JSON.stringify(original),before)}
}
for(const values of [[],[1],[4,4,4],[5,2,-3,0],Array.from({length:100},(_,i)=>100-i)])for(const kind of ['quick','heap']){const a=values.map((score,id)=>({id,score}));assert(E.valid(a,E.sortedCopy(a,kind)))}
const elements=new Map();
const context2d=new Proxy({measureText:text=>({width:text.length*6}),createLinearGradient:()=>({addColorStop(){}}),createRadialGradient:()=>({addColorStop(){}})},{get:(o,k)=>k in o?o[k]:(()=>{}),set:(o,k,v)=>(o[k]=v,true)});
function el(id){if(!elements.has(id))elements.set(id,{value:'',checked:false,disabled:false,style:{},innerHTML:'',textContent:'',dataset:{},classList:{toggle(){}},addEventListener(){},querySelectorAll:()=>[],focus(){},click(){},setPointerCapture(){},getContext:()=>context2d,getBoundingClientRect:()=>({width:1000,height:540})});return elements.get(id)}
for(const [id,value] of Object.entries({pilot:'race-0','duel-source':'race','duel-n':'24','duel-speed':'3','league-scenario':'aleatoria','league-algorithm':'quick'}))el(id).value=value;
const storage=new Map();const sandbox={ArenaEngine:E,APS_DATA:data,console,URLSearchParams,URL,Blob,Math,Number,JSON,Set,Map,Event:class{},setTimeout,clearTimeout,requestAnimationFrame(){},location:{protocol:'file:'},window:{devicePixelRatio:1,addEventListener(){},dispatchEvent(){}},document:{getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:()=>el('download')},localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)}};
vm.createContext(sandbox);vm.runInContext(read('render.js'),sandbox);sandbox.ArenaRender=sandbox.window.ArenaRender;vm.runInContext(read('app.js'),sandbox);
const run=code=>vm.runInContext(code,sandbox);
(async()=>{
 assert.equal(run('race.racers.length'),12);assert.equal(run('race.racers.filter(p=>p.team).length'),7);
 run('startRace();');assert(run('race.playing'));
 run("race.objects=[{lane:race.racers[0].lane,z:5,type:'energy',hits:new Set()}];tickRace(.01)");assert.equal(run('race.racers[0].energy'),1);
 run('pauseRace()');const elapsed=run('race.elapsed');run('tickRace(1)');assert.equal(run('race.elapsed'),elapsed);run('pauseRace()');
 run('for(let i=0;i<2700&&race.playing;i++)tickRace(1/60);');assert(!run('race.playing'));assert.equal(run('lastRace.length'),12);assert(run('lastRace.every(p=>p.score>=0&&Number.isSafeInteger(p.score))'));
 run('resetDuel();for(let i=0;i<10000&&!(duels.quick.done&&duels.heap.done);i++)stepDuel();');assert(run('duels.quick.done&&duels.heap.done'));
 assert(run('E.valid(duels.original,duels.quick.a)&&E.valid(duels.original,duels.heap.a)'));
 await run('buildLeague()');assert.equal(run('ranking.length'),20000);
 el('include-race').checked=true;await run('buildLeague()');assert.equal(run('ranking.length'),20012);assert.equal(run('ranking.filter(p=>p.team).length'),7);
 el('league-algorithm').value='heap';await run('buildLeague()');assert.equal(run('ranking.length'),20012);assert(run('ranking.every((p,i)=>i===0||ranking[i-1].score>=p.score)'));
 el('only-team').checked=true;run('renderLeague()');assert.equal(run('filtered.length'),7);
 el('league-search').value='luis';run('renderLeague()');assert.equal(run('filtered[0].name'),'Luís Gustavo');
 run("R.race($('track'),race,1000);R.algorithm($('quick-canvas'),duels.quick,'quick');R.algorithm($('heap-canvas'),duels.heap,'heap')");
 const fixture={tamanhos:[20000],resultados:['Quick Sort','Heap Sort'].map((algoritmo,i)=>({cenario:'Aleatório',algoritmo,n:20000,obrigatorio:true,mediana_s:.01+i/100,min_s:.009,max_s:.07,pico_memoria_bytes:200+i*100,tempos_s:[.01,.02,.03],validado:true}))};
 sandbox.labFixture=fixture;
 run('showBenchmark(labFixture)');assert(el('lab-results').innerHTML.includes('Quick Sort'));assert(el('lab-results').innerHTML.includes('PICO (bytes)'));assert(!el('export-csv').disabled);
 sandbox.fetch=async()=>({ok:true,json:async()=>({estado:'concluido',dados:fixture})});
 await run('followBenchmark()');assert(!run('benchBusy'));assert(el('cancel-benchmark').disabled);
 console.log('OK: 4 CSVs × 2 algoritmos, casos-limite, 12 naves/7 colegas, coleta, pausa, corrida, duelo, liga 20000/20012, busca e renderizador simulado.');
})().catch(e=>{console.error(e);process.exitCode=1});
