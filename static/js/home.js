/* ==========================================================================
   INTERAÇÕES EXCLUSIVAS DA HOME (CARROSSEL AUTOMÁTICO & FORMULÁRIO)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
    const slides = document.querySelectorAll(".slide");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const dotsContainer = document.getElementById("dots");
    
    let currentSlide = 0;
    let slideInterval;

    // Criar as bolinhas indicadoras dinamicamente baseada na quantidade de slides
    slides.forEach((_, index) => {
        const dot = document.createElement("div");
        dot.classList.add("dot");
        if (index === 0) dot.classList.add("active");
        dot.addEventListener("click", () => goToSlide(index));
        dotsContainer.appendChild(dot);
    });

    const dots = document.querySelectorAll(".dot");

    function updateCounters(index) {
        slides.forEach(slide => slide.classList.remove("active"));
        dots.forEach(dot => dot.classList.remove("active"));
        
        slides[index].classList.add("active");
        dots[index].classList.add("active");
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        updateCounters(currentSlide);
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        updateCounters(currentSlide);
    }

    function goToSlide(index) {
        currentSlide = index;
        updateCounters(currentSlide);
        resetTimer();
    }

    // Configura o temporizador automático de 5 segundos
    function startTimer() {
        slideInterval = setInterval(nextSlide, 5000);
    }

    function resetTimer() {
        clearInterval(slideInterval);
        startTimer();
    }

    // Ouvintes dos botões físicos de seta
    if(nextBtn && prevBtn) {
        nextBtn.addEventListener("click", () => { nextSlide(); resetTimer(); });
        prevBtn.addEventListener("click", () => { prevSlide(); resetTimer(); });
    }

    startTimer();

    // --- INTERAÇÃO DO FORMULÁRIO DE CONTATO CONTATO ---
    const formContato = document.getElementById("formContato");
    const feedback = document.getElementById("feedback");

    if (formContato) {
        formContato.addEventListener("submit", function (e) {
            e.preventDefault();
            
            // Simula o processamento do envio da mensagem
            feedback.style.color = "#2ecc71";
            feedback.textContent = "Obrigado! Sua mensagem foi enviada. Entraremos em contato em breve. 🐾";
            
            formContato.reset();
            
            // Remove o texto de feedback após 6 segundos
            setTimeout(() => {
                feedback.textContent = "";
            }, 6000);
        });
    }
});