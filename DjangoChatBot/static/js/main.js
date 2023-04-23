document.addEventListener("DOMContentLoaded", function () {
    const micButton = document.getElementById("micButton");
    const questionInput = document.getElementById("questionInput");
    const submitQuestion = document.getElementById("submitQuestion");
    const answerDiv = document.getElementById("answer");
    const headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("X-CSRFToken", csrf_token);
  
    function textToSpeech(text) {
      const speech = new SpeechSynthesisUtterance(text);
      speech.lang = "es-ES";
      window.speechSynthesis.speak(speech);
    }
  
    function autoResize(element) {
      element.style.height = "auto";
      element.style.height = element.scrollHeight + "px";
    }
  
    document.getElementById("questionInput").addEventListener("input", function () {
      autoResize(this);
    });

  
    function getAnswer(question) {
      fetch("/chatbot/", {
        method: "POST",
        headers: headers,
        body: JSON.stringify({ question: question }),
      })
        .then((response) => response.json())
        .then((data) => {
          const questionElement = document.createElement("div");
          questionElement.className = "user-question";
          questionElement.textContent = "Usuario: " + question;
          answerDiv.appendChild(questionElement);
  
          const answerElement = document.createElement("div");
          answerElement.className = "bot-answer";
          answerElement.textContent = "Chatbot: " + data.answer;
          answerDiv.appendChild(answerElement);
  
          textToSpeech(data.answer);
        });
    }
  
    micButton.addEventListener("click", () => {
      const recognition = new webkitSpeechRecognition();
      recognition.lang = "es-ES";
      recognition.start();
  
      micButton.classList.add("listening");
  
      recognition.onresult = function (event) {
        const question = event.results[0][0].transcript;
        questionInput.value = question;
        getAnswer(question);
  
        micButton.classList.remove("listening");
      };
      recognition.onerror = function () {
        micButton.classList.remove("listening");
      };
    });
  
    submitQuestion.addEventListener("click", (e) => {
      e.preventDefault();
      const question = questionInput.value;
      getAnswer(question);
    });
  });