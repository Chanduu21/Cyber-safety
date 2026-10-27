const searchInput = document.getElementById('scamSearch');
const scamCards = [...document.querySelectorAll('.scam-card')];
const resultCount = document.getElementById('resultCount');
const noResults = document.getElementById('noResults');
searchInput.addEventListener('input', () => {
  const term = searchInput.value.trim().toLowerCase(); let visible = 0;
  scamCards.forEach(card => { const match = card.dataset.search.includes(term); card.hidden = !match; if (match) visible++; });
  resultCount.textContent = `${visible} topic${visible === 1 ? '' : 's'}`; noResults.hidden = visible !== 0;
});
const checks = [...document.querySelectorAll('.check-item input')];
function updateChecks(){const done=checks.filter(c=>c.checked).length;document.getElementById('progressText').textContent=`${done} of ${checks.length} complete`;document.getElementById('progressBar').style.width=`${done/checks.length*100}%`;}
checks.forEach(c=>c.addEventListener('change',updateChecks));
let questions=[],answers=[],current=0,chosen=null;
const questionText=document.getElementById('questionText'), optionsEl=document.getElementById('answerOptions'), nextBtn=document.getElementById('nextQuestion');
async function loadQuiz(){try{const res=await fetch('/api/quiz');questions=await res.json();startQuiz();}catch(e){questionText.textContent='Could not load the quiz. Please refresh the page.';}}
function startQuiz(){answers=[];current=0;chosen=null;document.getElementById('quizContent').hidden=false;document.getElementById('quizResult').hidden=true;renderQuestion();}
function renderQuestion(){const q=questions[current];chosen=null;document.getElementById('quizProgress').textContent=`QUESTION ${current+1} OF ${questions.length}`;document.getElementById('quizBar').style.width=`${current/questions.length*100}%`;questionText.textContent=q.question;optionsEl.innerHTML='';q.options.forEach((option,i)=>{const el=document.createElement('button');el.type='button';el.className='answer-option';el.innerHTML=`<span class="option-letter">${String.fromCharCode(65+i)}</span><span></span>`;el.querySelector('span:last-child').textContent=option;el.addEventListener('click',()=>{chosen=i;optionsEl.querySelectorAll('.answer-option').forEach(b=>b.classList.remove('selected'));el.classList.add('selected');nextBtn.disabled=false;nextBtn.textContent=current===questions.length-1?'See my result →':'Next question →';});optionsEl.appendChild(el);});nextBtn.disabled=true;nextBtn.textContent='Choose an answer';}
nextBtn.addEventListener('click',async()=>{if(chosen===null)return;answers.push(chosen);if(current<questions.length-1){current++;renderQuestion();return;}nextBtn.disabled=true;try{const res=await fetch('/api/quiz',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({answers})});const result=await res.json();document.getElementById('quizContent').hidden=true;document.getElementById('quizResult').hidden=false;document.getElementById('quizBar').style.width='100%';document.getElementById('quizProgress').textContent='QUIZ COMPLETE';document.getElementById('resultScore').textContent=`You scored ${result.score} / ${result.total}`;document.getElementById('resultMessage').textContent=result.message;const expl=document.getElementById('explanations');expl.innerHTML='';result.explanations.forEach((e,i)=>{const p=document.createElement('div');p.className='explanation';const b=document.createElement('b');b.textContent=`${i+1}. ${answers[i]===questions[i].answer?'Correct':'Remember'}`;p.append(b,document.createTextNode(e));expl.appendChild(p);});}catch(e){nextBtn.disabled=false;nextBtn.textContent='Something went wrong — try again';}});
document.getElementById('retryQuiz').addEventListener('click',startQuiz);loadQuiz();
