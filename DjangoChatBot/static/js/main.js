document.addEventListener("DOMContentLoaded", function() {
    const micButton = document.getElementById('micButton');
    const questionInput = document.getElementById('questionInput');
    const submitQuestion = document.getElementById('submitQuestion');
    const answerDiv = document.getElementById('answer');

    function textToSpeech(text) {
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'es-ES';
        window.speechSynthesis.speak(speech);
    }

    function getAnswer(question) {
        fetch('/api/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        })
        .then(response => response.json())
        .then(data => {
            const answerElement = document.createElement('div');
            answerElement.textContent = data.answer;
            answerDiv.appendChild(answerElement);
            textToSpeech(data.answer);
        });
    }

    micButton.addEventListener('click', () => {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.start();

        recognition.onresult = function(event) {
            const question = event.results[0][0].transcript;
            questionInput.value = question;
            getAnswer(question);
        };
    });

    submitQuestion.addEventListener('click', (e) => {
        e.preventDefault(); // Añade esta línea para evitar que se refresque la página al enviar el formulario
        const question = questionInput.value;
        getAnswer(question);
    });
});