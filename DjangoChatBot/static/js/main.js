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

  
    function getAnswer(question, user_rating_choice = null, evaluation_id = null) {
      fetch("/chatbot/", {
        method: "POST",
        headers: headers,
        body: JSON.stringify({
          question: question,
          user_rating_choice: user_rating_choice,
          evaluation_id: evaluation_id,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          const evaluation_id = data.evaluation_id; // Obtiene el evaluation_id de la respuesta JSON
    
          const questionElement = document.createElement("div");
          questionElement.className = "user-question";
          questionElement.textContent = "Usuario: " + question;
          answerDiv.appendChild(questionElement);
    
          const answerElement = document.createElement("div");
          answerElement.className = "bot-answer";
          answerElement.textContent = "Chatbot: " + data.answer;
          answerDiv.appendChild(answerElement);
    
          // Crea y agrega los botones de valoración para cada respuesta
          const ratingButtonsContainer = document.createElement("div");
          ratingButtonsContainer.className = "mt-3 d-flex justify-content-center";
    
          const usefulButton = document.createElement("button");
          usefulButton.className = "btn btn-success btn-yes me-2";
          usefulButton.innerHTML = '<i class="fas fa-thumbs-up"></i> Útil';
          usefulButton.addEventListener("click", () => {
            sendUserRating(evaluation_id, question, data.answer, "U"); // Incluye el evaluation_id
            usefulButton.disabled = true;
            notUsefulButton.disabled = true;
          });
          ratingButtonsContainer.appendChild(usefulButton);
    
          const notUsefulButton = document.createElement("button");
          notUsefulButton.className = "btn btn-danger btn-no";
          notUsefulButton.innerHTML = '<i class="fas fa-thumbs-down"></i> No útil';
          notUsefulButton.addEventListener("click", () => {
            sendUserRating(evaluation_id, question, data.answer, "N"); // Incluye el evaluation_id
            usefulButton.disabled = true;
            notUsefulButton.disabled = true;
          });
          ratingButtonsContainer.appendChild(notUsefulButton);
    
          answerDiv.appendChild(ratingButtonsContainer);
    
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

    // Función para enviar la valoración del usuario al backend
    function sendUserRating(evaluation_id, question, answer, ratingChoice) {
      updateUserRating(evaluation_id, ratingChoice); // Envía 'U' o 'N' en lugar de 1 o -1
    }
    function updateUserRating(evaluation_id, ratingChoice) {
      fetch("/evaluation/update_rating/", {
        method: "POST",
        headers: headers, 
        body: JSON.stringify({
          evaluation_id: evaluation_id,
          user_rating_choice: ratingChoice,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            console.log("Valoración actualizada con éxito");
          } else {
            console.log("Error al actualizar la valoración");
          }
        });
    }
  });