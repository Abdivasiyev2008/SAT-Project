
// Canvas elementini va kerakli elementlarni olish
const canvas = document.getElementById('paintCanvas');
const ctx = canvas.getContext('2d');
const colorPicker = document.getElementById('colorPicker');
const brushSizeInput = document.getElementById('brushSize');
const clearCanvasButton = document.getElementById('clearCanvas');
const drawIcon = document.getElementById('drawIcon');

// Canvasning o'lchamlarini butun sahifaga moslashtirish
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let painting = false;
let drawEnabled = false; // Chizishni faollashtirish
let brushColor = colorPicker.value;
let brushSize = brushSizeInput.value;

// Chizish boshlanishi
function startPosition(e) {
    if (!drawEnabled) return; // Agar chizish faollashtirilmagan bo'lsa, chizish boshlanmasin
    painting = true;
    draw(e);
}

// Chizish tugatilishi
function endPosition() {
    painting = false;
    ctx.beginPath();
}

// Chizish jarayoni
function draw(e) {
    if (!painting) return;

    // Sahifa qaysi joyda aylantirilganini olish
    const scrollY = window.scrollY || document.documentElement.scrollTop;

    // Yangi kursor pozitsiyasini olish (scroll Yni qo'shish)
    const x = e.clientX;
    const y = e.clientY + scrollY;

    ctx.lineWidth = brushSize;
    ctx.lineCap = 'round';
    ctx.strokeStyle = brushColor;

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

// Rangni yangilash
colorPicker.addEventListener('input', (e) => {
    brushColor = e.target.value;
});

// Brush o'lchamini yangilash
brushSizeInput.addEventListener('input', (e) => {
    brushSize = e.target.value;
});

// Canvasni tozalash
clearCanvasButton.addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

// Canvasga rasm chizishni boshlash va to'xtatish
canvas.addEventListener('mousedown', startPosition);
canvas.addEventListener('mouseup', endPosition);
canvas.addEventListener('mousemove', draw);

// Chizish ikonkasi bosilganda faollashishi
drawIcon.addEventListener('click', () => {
    drawEnabled = !drawEnabled;
    if (drawEnabled) {
        canvas.style.display = 'block';
        document.querySelector('.controls').style.display = 'block';
        drawIcon.style.color = 'green';
        canvas.style.cursor = 'crosshair';
    } else {
        canvas.style.display = 'none';
        document.querySelector('.controls').style.display = 'none';
        drawIcon.style.color = '#333';
        canvas.style.cursor = 'default';
    }
});