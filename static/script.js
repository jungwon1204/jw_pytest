document.getElementById('checkBtn').addEventListener('click', async function () {
  const userInput = document.getElementById('userAnswer').value.trim();
  const correctAnswer = document.getElementById('correctAnswer').value.trim();
  const resultBox = document.getElementById('result');
  const nextBtn = document.getElementById('nextBtn');

  resultBox.innerHTML = '';

  try {
    const response = await fetch('/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_answer: userInput,
        correct_answer: correctAnswer
      })
    });

    const data = await response.json();

    const resultTitle = document.createElement('h3');
    const resultText = document.createElement('pre');

    resultText.style.backgroundColor = '#fff';
    resultText.style.border = '1px solid #ffb3d9';
    resultText.style.padding = '10px';
    resultText.style.borderRadius = '8px';
    resultText.style.whiteSpace = 'pre-wrap';

    if (data.result) {
      resultTitle.textContent = '🎉 정답입니다!';
      resultTitle.style.color = '#d63384';
      resultText.textContent = `당신의 답:\n${userInput}`;

      // ✅ 개념 설명 추가
      if (data.concept) {
        const conceptDiv = document.createElement('div');
        conceptDiv.style.marginTop = '15px';
        conceptDiv.style.padding = '10px';
        conceptDiv.style.backgroundColor = '#ffeaf5';
        conceptDiv.style.border = '1px solid #ffa6c1';
        conceptDiv.style.borderRadius = '8px';
        conceptDiv.textContent = `📘 관련 개념: ${data.concept}`;
        resultBox.appendChild(conceptDiv);
      }

    } else {
      resultTitle.textContent = '❌ 틀렸어요!';
      resultTitle.style.color = '#ff3366';
      resultText.textContent = `당신의 답:\n${userInput}\n\n정답:\n${correctAnswer}`;
    }

    resultBox.appendChild(resultTitle);
    resultBox.appendChild(resultText);
    nextBtn.style.display = 'inline-block';

  } catch (error) {
    resultBox.textContent = '⚠️ 서버 오류 발생';
    resultBox.style.color = 'red';
  }
});

document.getElementById('nextBtn').addEventListener('click', function () {
  window.location.reload();
});
