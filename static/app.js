let candidates = [];
let askedAttributes = [];
let currentAttributeId = null;
let questionNumber = 0;
let gameType = 'all';
let totalCandidates = 0;
let currentGuessId = null;

function showScreen(screenId) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(screenId).classList.add('active');
}

async function startGame(type) {
  gameType = type;
  candidates = [];
  askedAttributes = [];
  questionNumber = 0;
  currentGuessId = null;
  showScreen('game-screen');

  const response = await fetch('/api/game/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type })
  });

  const data = await response.json();
  candidates = data.candidates;
  totalCandidates = data.candidates.length;
  updateStats();
  await nextQuestion();
}

function updateStats() {
  document.getElementById('candidates-count').textContent = candidates.length;
  document.getElementById('stat-questions').textContent = questionNumber;
  document.getElementById('stat-remaining').textContent = candidates.length;
  document.getElementById('stat-total').textContent = totalCandidates;
  const progress = Math.min((askedAttributes.length / 35) * 100, 95);
  document.getElementById('progress-fill').style.width = progress + '%';
}

async function nextQuestion() {
  if (candidates.length === 0) {
    giveUp();
    return;
  }

  if (candidates.length === 1) {
    await makeGuess(candidates[0]);
    return;
  }

  const thinkingTexts = [
    'Reading your mind...',
    'Checking the stats...',
    'Scanning the squad...',
    'Narrowing it down...',
    'Getting warmer...',
    'Almost got you...',
    'Final whistle soon...'
  ];
  const idx = Math.min(Math.floor(questionNumber / 3), thinkingTexts.length - 1);
  document.getElementById('thinking-text').textContent = thinkingTexts[idx];

  const response = await fetch('/api/game/question', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ candidates, asked: askedAttributes })
  });

  const data = await response.json();

  if (data.guess) {
    await makeGuess(data.candidate_id);
    return;
  }

  currentAttributeId = data.attribute_id;
  askedAttributes.push(data.attribute_id);
  questionNumber++;
  document.getElementById('q-number').textContent = questionNumber;
  document.getElementById('question-text').textContent = data.question;
  updateStats();
}

async function answer(ans) {
  document.querySelectorAll('.ans-btn').forEach(b => b.disabled = true);

  const response = await fetch('/api/game/answer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      candidates,
      attribute_id: currentAttributeId,
      answer: ans
    })
  });

  const data = await response.json();
  candidates = data.candidates;
  updateStats();
  document.querySelectorAll('.ans-btn').forEach(b => b.disabled = false);

  if (candidates.length === 0) {
    giveUp();
  } else if (candidates.length === 1) {
    await makeGuess(candidates[0]);
  } else {
    await nextQuestion();
  }
}

async function makeGuess(characterId) {
  const response = await fetch(`/api/character/${characterId}`);
  const character = await response.json();
  const guessName = document.getElementById('guess-name');
  guessName.textContent = character.name;
  guessName.dataset.id = characterId;
  currentGuessId = characterId;
  document.getElementById('guess-type').textContent = character.type.toUpperCase();
  showScreen('guess-screen');
}

function correct() {
  document.getElementById('result-emoji').textContent = '🏆';
  document.getElementById('result-title').textContent = 'GOAL!';
  document.getElementById('result-text').textContent = `I guessed it in ${questionNumber} questions. The Football Oracle strikes again! ⚡`;
  showScreen('result-screen');
}

function wrong() {
  if (currentGuessId) {
    candidates = candidates.filter(id => id !== currentGuessId);
  }
  currentGuessId = null;

  if (candidates.length === 0) {
    giveUp();
    return;
  }

  showScreen('game-screen');
  document.getElementById('thinking-text').textContent = 'Let me think again...';
  updateStats();
  nextQuestion();
}

function giveUp() {
  document.getElementById('result-emoji').textContent = '🤔';
  document.getElementById('result-title').textContent = 'YOU WIN!';
  document.getElementById('result-text').textContent = `I asked ${questionNumber} questions and couldn't figure it out. Respect! Are you sure they're in my database? 🧞`;
  showScreen('result-screen');
}

function resetGame() {
  candidates = [];
  askedAttributes = [];
  currentAttributeId = null;
  questionNumber = 0;
  totalCandidates = 0;
  currentGuessId = null;
  showScreen('home-screen');
}