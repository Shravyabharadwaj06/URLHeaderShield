/**
 * CyberTheme Engine
 * Handles particle backgrounds, typewriter effects, and professional security sounds.
 */

const CyberTheme = {
    // 1. Particle Background
    initBackground: function() {
        const canvas = document.createElement('canvas');
        canvas.id = 'cyber-bg';
        document.body.prepend(canvas);

        const style = document.createElement('style');
        style.innerHTML = `
            #cyber-bg {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
                background: #050505;
                pointer-events: none;
            }
        `;
        document.head.appendChild(style);

        const ctx = canvas.getContext('2d');
        let particles = [];
        const particleCount = 60;
        const connectionDist = 150;

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        window.addEventListener('resize', resize);
        resize();

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 0.5;
                this.vy = (Math.random() - 0.5) * 0.5;
                this.radius = Math.random() * 2;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;

                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(0, 191, 255, 0.5)';
                ctx.fill();
            }
        }

        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                particles[i].draw();

                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < connectionDist) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(0, 191, 255, ${1 - dist / connectionDist})`;
                        ctx.lineWidth = 0.5;
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(animate);
        }
        animate();
    },

    // 2. Typewriter Effect
    typeWriter: function(elementId, text, speed = 40) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        element.innerHTML = "";
        let i = 0;
        
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        type();
    },

    // 3. Synthetic Sound Effects (Web Audio API)
    audioCtx: null,
    
    initAudio: function() {
        if (!this.audioCtx) {
            this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
    },

    playDigitalBeep: function(freq = 800, duration = 0.1, type = 'sine') {
        this.initAudio();
        const osc = this.audioCtx.createOscillator();
        const gain = this.audioCtx.createGain();

        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);
        
        gain.gain.setValueAtTime(0.1, this.audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, this.audioCtx.currentTime + duration);

        osc.connect(gain);
        gain.connect(this.audioCtx.destination);

        osc.start();
        osc.stop(this.audioCtx.currentTime + duration);
    },

    playSystemReady: function() {
        this.playDigitalBeep(600, 0.05);
        setTimeout(() => this.playDigitalBeep(900, 0.05), 100);
    },

    playInterfaceClick: function() {
        this.playDigitalBeep(1200, 0.03, 'square');
    }
};

// Auto-initialize on link
document.addEventListener('DOMContentLoaded', () => {
    CyberTheme.initBackground();
    CyberTheme.playSystemReady();
    
    // Auto-bind sound to all buttons
    document.querySelectorAll('button, .analyze-btn, .continue-btn').forEach(btn => {
        btn.addEventListener('mouseenter', () => CyberTheme.playInterfaceClick());
    });
});
