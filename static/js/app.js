const episodeData = document.querySelector('.episode-data');
const questionCard = document.getElementById('question-card');
const questionCounters = document.querySelectorAll('.question-counter');
const remainingCounters = document.querySelectorAll('.question-remaining');
const fullscreenSection = document.getElementById('fs-section');
const questionList = document.getElementById('question-list');
const prevBtn = document.getElementById('prev-question');
const nextBtn = document.getElementById('next-question');
const questionItems = document.querySelectorAll('.question-item');
const fullscreenBtn = document.getElementById('questions-fullscreen');
const questionViewer = document.getElementById('question-viewer');
const fullscreenExit = document.getElementById('fullscreen-exit');

const videoScript = document.getElementById('video-script');
const videoLength = document.getElementById('video-length');

let questions = [];
let currentIndex = -1;
const checked = new Set();

function renderQuestions() {
  if (!questionCard) return;
  if (questions.length === 0) {
    questionCard.innerHTML = '<span class="muted">مفيش اسئلة لسه. ابدأ بكتابة اول سؤال.</span>';
    if (questionCounters.length) {
      questionCounters.forEach((counter) => {
        counter.textContent = '0 / 0';
      });
    }
    if (remainingCounters.length) {
      remainingCounters.forEach((counter) => {
        counter.textContent = 'متبقي 0';
      });
    }
    if (fullscreenSection) {
      fullscreenSection.textContent = 'عام';
    }
    if (prevBtn) prevBtn.disabled = true;
    if (nextBtn) nextBtn.disabled = true;
    if (questionList) questionList.innerHTML = '';
    currentIndex = -1;
    return;
  }

  if (currentIndex < 0) currentIndex = 0;
  if (currentIndex >= questions.length) currentIndex = questions.length - 1;

  const currentQuestion = questions[currentIndex];
  questionCard.textContent = currentQuestion.text;
  if (fullscreenSection) {
    fullscreenSection.textContent = currentQuestion.section || 'عام';
  }
  questionCard.classList.toggle('completed', checked.has(currentIndex));
  if (questionCounters.length) {
    questionCounters.forEach((counter) => {
      counter.textContent = `${currentIndex + 1} / ${questions.length}`;
    });
  }
  if (remainingCounters.length) {
    const remaining = Math.max(questions.length - checked.size, 0);
    remainingCounters.forEach((counter) => {
      counter.textContent = `متبقي ${remaining}`;
    });
  }
  if (prevBtn) prevBtn.disabled = currentIndex === 0;
  if (nextBtn) nextBtn.disabled = currentIndex === questions.length - 1;

  if (questionItems.length) {
    questionItems.forEach((item) => {
      const idx = Number(item.dataset.index);
      item.classList.toggle('active', idx === currentIndex);
      item.classList.toggle('checked', checked.has(idx));
    });
  }
}

if (episodeData) {
  try {
    questions = JSON.parse(episodeData.dataset.questions || '[]');
  } catch (err) {
    questions = [];
  }

  if (questionItems.length) {
    questionItems.forEach((item) => {
      const idx = Number(item.dataset.index);
      item.addEventListener('click', () => {
        currentIndex = idx;
        if (checked.has(idx)) {
          checked.delete(idx);
        } else {
          checked.add(idx);
        }
        renderQuestions();
      });
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (currentIndex > 0) {
        currentIndex -= 1;
        renderQuestions();
      }
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (currentIndex < questions.length - 1) {
        currentIndex += 1;
        renderQuestions();
      }
    });
  }

  renderQuestions();
}

if (fullscreenBtn && questionViewer) {
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      questionViewer.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  };

  fullscreenBtn.addEventListener('click', toggleFullscreen);
  if (fullscreenExit) {
    fullscreenExit.addEventListener('click', () => {
      if (document.fullscreenElement) {
        document.exitFullscreen().catch(() => {});
      }
    });
  }

  document.addEventListener('fullscreenchange', () => {
    const isFullscreen = document.fullscreenElement === questionViewer;
    fullscreenBtn.textContent = isFullscreen ? '⤡' : '⤢';
    questionViewer.classList.toggle('is-fullscreen', isFullscreen);
  });
}

if (questionCard) {
  questionCard.addEventListener('click', () => {
    if (currentIndex < 0) return;
    if (checked.has(currentIndex)) {
      checked.delete(currentIndex);
    } else {
      checked.add(currentIndex);
    }
    renderQuestions();
  });
}

if (videoScript && videoLength) {
  const updateCount = () => {
    const words = videoScript.value.trim().split(/\s+/).filter(Boolean);
    videoLength.textContent = `${words.length} كلمة`;
  };
  videoScript.addEventListener('input', updateCount);
  updateCount();
}
