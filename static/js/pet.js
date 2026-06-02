// ==================== MENU HAMBURGUER ====================
const hamburguer = document.getElementById("hamburguer");
const menu = document.getElementById("menu");

hamburguer.addEventListener("click", () => {
  menu.classList.toggle("active");
  
  if (menu.classList.contains("active")) {
    hamburguer.innerHTML = '<i class="fa fa-times"></i>';
  } else {
    hamburguer.innerHTML = '<i class="fa fa-bars"></i>';
  }
});

// ==================== CARROSSEL ====================
const slides = document.querySelectorAll('.slide');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const dotsContainer = document.getElementById('dots');
let currentIndex = 0;
let interval;

// Criar bolinhas
function createDots() {
  dotsContainer.innerHTML = '';
  slides.forEach((_, index) => {
    const dot = document.createElement('div');
    dot.classList.add('dot');
    if (index === 0) dot.classList.add('active');
    dot.addEventListener('click', () => goToSlide(index));
    dotsContainer.appendChild(dot);
  });
}

function goToSlide(index) {
  slides.forEach(slide => slide.classList.remove('active'));
  slides[index].classList.add('active');
  
  document.querySelectorAll('.dot').forEach((dot, i) => {
    dot.classList.toggle('active', i === index);
  });
  currentIndex = index;
}

function nextSlide() {
  let next = currentIndex + 1;
  if (next >= slides.length) next = 0;
  goToSlide(next);
}

function prevSlide() {
  let prev = currentIndex - 1;
  if (prev < 0) prev = slides.length - 1;
  goToSlide(prev);
}

function startAutoPlay() {
  interval = setInterval(nextSlide, 5000); // 5 segundos
}

function stopAutoPlay() {
  clearInterval(interval);
}

// Eventos do carrossel
prevBtn.addEventListener('click', () => { stopAutoPlay(); prevSlide(); startAutoPlay(); });
nextBtn.addEventListener('click', () => { stopAutoPlay(); nextSlide(); startAutoPlay(); });

// Pausar ao passar o mouse
document.querySelector('.carousel-section').addEventListener('mouseover', stopAutoPlay);
document.querySelector('.carousel-section').addEventListener('mouseout', startAutoPlay);

// ==================== FORMULÁRIO ====================
const form = document.getElementById("formContato");
const feedback = document.getElementById("feedback");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const nome = document.getElementById("nome").value.trim();
  const email = document.getElementById("email").value.trim();
  const mensagem = document.getElementById("mensagem").value.trim();

  if (!nome || !email || !mensagem) {
    feedback.innerText = "Preencha todos os campos!";
    feedback.style.color = "red";
    return;
  }

  feedback.innerText = "Mensagem enviada com sucesso! 🐶 Obrigado!";
  feedback.style.color = "green";
  form.reset();

  setTimeout(() => feedback.innerText = "", 4000);
});

// Inicializar
createDots();
startAutoPlay();