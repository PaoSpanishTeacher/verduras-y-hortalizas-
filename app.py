import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Huerto de Palabras Mágico", layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 0rem; }
    iframe { border: none; }
    </style>
    """, unsafe_allow_html=True)

html_huerto_premium_random = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Quicksand:wght@500;700&family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {
            --farm-green: #2d6a4f;
            --farm-light: #d8f3dc;
            --carrot-orange: #fb8500;
            --tomato-red: #e63946;
            --accent-purple: #7209b7;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }

        body {
            font-family: 'Quicksand', sans-serif;
            min-height: 100vh;
            background: #fdfae5;
            background-image: radial-gradient(#2d6a4f11 2px, transparent 2px);
            background-size: 30px 30px;
            display: flex; flex-direction: column; align-items: center;
            padding-top: 60px;
        }

        header { text-align: center; padding-bottom: 20px; width: 100%; }
        h1 { font-family: 'Fredoka', sans-serif; font-size: 3rem; color: var(--farm-green); text-shadow: 3px 3px 0px white; }
        .brand-name { font-family: 'Dancing Script', cursive; font-size: 1.8rem; color: var(--accent-purple); }

        .main-layout {
            display: grid; grid-template-columns: 280px 1fr;
            gap: 30px; width: 95%; max-width: 1200px; margin-top: 20px;
        }

        /* LISTA LATERAL */
        .sidebar {
            background: white; padding: 25px; border-radius: 25px;
            border: 4px solid var(--farm-light); box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            height: fit-content;
        }
        .sidebar h3 { font-family: 'Fredoka', sans-serif; color: var(--farm-green); margin-bottom: 15px; text-align: center; }
        
        .word-item {
            padding: 12px; margin-bottom: 10px; background: #f8fcf8;
            border-radius: 15px; font-weight: 700; color: #444;
            display: flex; justify-content: space-between; align-items: center;
            border: 2px solid transparent; transition: 0.3s;
        }
        .word-item.done { background: #e8f5e9; color: #2e7d32; border-color: #c8e6c9; opacity: 0.7; }

        /* JUEGO */
        .game-zone { display: flex; flex-direction: column; gap: 25px; }
        
        .progress-container {
            width: 100%; background: white; height: 20px;
            border-radius: 20px; border: 3px solid var(--farm-light); overflow: hidden;
        }
        #progress-fill {
            height: 100%; width: 0%; background: linear-gradient(90deg, var(--carrot-orange), var(--tomato-red));
            transition: width 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .drop-zone {
            background: white; border: 4px dashed var(--farm-green);
            border-radius: 30px; min-height: 150px; display: flex;
            justify-content: center; align-items: center; gap: 15px;
            padding: 30px; position: relative; box-shadow: inset 0 5px 15px rgba(0,0,0,0.05);
        }
        .drop-zone::before { content: "¡Arrastra las sílabas aquí!"; color: #bbb; font-style: italic; font-size: 1.2rem; }
        .drop-zone.has-content::before { display: none; }

        .pool {
            background: rgba(255,255,255,0.4); border: 3px solid var(--farm-light);
            border-radius: 30px; padding: 30px; display: flex; flex-wrap: wrap;
            justify-content: center; gap: 15px; min-height: 250px; backdrop-filter: blur(5px);
        }

        .piece {
            background: white; border: 3px solid var(--farm-green);
            border-radius: 18px; padding: 15px 25px;
            font-family: 'Fredoka', sans-serif; font-size: 1.5rem;
            color: var(--farm-green); cursor: grab;
            box-shadow: 0 6px 0px var(--farm-green);
            transition: 0.2s; text-transform: lowercase;
        }
        .piece:active { transform: translateY(3px); box-shadow: 0 2px 0px var(--farm-green); }
        .piece.dragging { opacity: 0.3; }
        .piece.is-correct { background: #4caf50; color: white; border-color: #2e7d32; box-shadow: 0 4px 0px #2e7d32; }

        /* ALERTAS */
        #alert-box {
            position: fixed; top: 15%; left: 50%; transform: translateX(-50%) scale(0);
            padding: 15px 45px; border-radius: 50px; color: white; font-weight: bold;
            font-size: 1.8rem; z-index: 500; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #alert-box.show { transform: translateX(-50%) scale(1); }
        .bg-win { background: #4caf50; box-shadow: 0 10px 20px rgba(76,175,80,0.3); }

        /* PROFESOR */
        #professor-pop {
            position: fixed; bottom: -400px; left: 50%; transform: translateX(-50%);
            z-index: 1000; transition: 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            text-align: center;
        }
        #professor-pop.active { bottom: 30px; }
        .prof-bubble {
            background: white; padding: 20px 40px; border-radius: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2); font-size: 1.8rem;
            font-weight: bold; color: var(--accent-purple); margin-bottom: 15px;
        }

        /* FINAL */
        #final-screen {
            position: fixed; inset: 0; background: rgba(255,255,255,0.98);
            display: none; flex-direction: column; align-items: center;
            justify-content: center; z-index: 2000; text-align: center;
        }
        #final-screen.active { display: flex; }

        .btn-restart {
            background: var(--carrot-orange); color: white; border: none;
            padding: 20px 50px; font-size: 1.8rem; border-radius: 60px;
            cursor: pointer; margin-top: 30px; box-shadow: 0 8px 0px #d35400;
            font-family: 'Fredoka', sans-serif;
        }
        
        .balloon { position: fixed; bottom: -100px; animation: floatUp 6s linear forwards; font-size: 3rem; }
        @keyframes floatUp { to { transform: translateY(-120vh) rotate(20deg); } }
    </style>
</head>
<body>

    <header>
        <h1>Huerto de Palabras</h1>
        <div class="brand-name">Pau Spanish Teacher</div>
    </header>

    <div class="main-layout">
        <div class="sidebar">
            <h3 id="round-title">Ronda: 10 Palabras</h3>
            <div id="list-container"></div>
        </div>
        <div class="game-zone">
            <div class="progress-container"><div id="progress-fill"></div></div>
            <div class="drop-zone" id="drop-zone"></div>
            <div style="text-align:center"><button onclick="clearWord()" style="background:#eee; border:none; padding:8px 20px; border-radius:15px; cursor:pointer; font-weight:bold;">Limpiar Palabra</button></div>
            <div class="pool" id="pool"></div>
        </div>
    </div>

    <div id="alert-box"></div>

    <div id="professor-pop">
        <div class="prof-bubble">¡Excelente trabajo! ¡Eres un genio!</div>
        <span style="font-size: 8rem;">👨‍🏫</span>
    </div>

    <div id="final-screen">
        <span style="font-size: 8rem;">🥕</span>
        <h1>¡Felicidades, terminaste!</h1>
        <p style="font-size: 1.5rem; color: var(--accent-purple); font-weight: bold;">Juego creado por Pau Spanish Teacher</p>
        <button class="btn-restart" onclick="location.reload()">Jugar con palabras nuevas</button>
    </div>

    <script>
        const MASTER_BANK = [
            { w: "zanahoria", p: ["za", "na", "ho", "ria"] },
            { w: "tomate", p: ["to", "ma", "te"] },
            { w: "lechuga", p: ["le", "chu", "ga"] },
            { w: "cebolla", p: ["ce", "bo", "lla"] },
            { w: "pepino", p: ["pe", "pi", "no"] },
            { w: "brócoli", p: ["bró", "co", "li"] },
            { w: "ajo", p: ["a", "jo"] },
            { w: "pimiento", p: ["pi", "mien", "to"] },
            { w: "calabaza", p: ["ca", "la", "ba", "za"] },
            { w: "espinaca", p: ["es", "pi", "na", "ca"] },
            { w: "papa", p: ["pa", "pa"] },
            { w: "elote", p: ["e", "lo", "te"] },
            { w: "berenjena", p: ["be", "ren", "je", "na"] },
            { w: "rábano", p: ["rá", "ba", "no"] },
            { w: "apio", p: ["a", "pio"] },
            { w: "coliflor", p: ["co", "li", "flor"] },
            { w: "betabel", p: ["be", "ta", "bel"] },
            { w: "hongo", p: ["hon", "go"] },
            { w: "espárrago", p: ["es", "pá", "rra", "go"] },
            { w: "ejote", p: ["e", "jo", "te"] }
        ];

        let selectedWords = [];
        let score = 0;
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function playSound(f, d) {
            const osc = audioCtx.createOscillator();
            const g = audioCtx.createGain();
            osc.frequency.value = f;
            g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + d);
            osc.connect(g); g.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + d);
        }

        function init() {
            // Seleccionar 10 al azar
            selectedWords = [...MASTER_BANK].sort(() => Math.random() - 0.5).slice(0, 10);
            
            const list = document.getElementById('list-container');
            const pool = document.getElementById('pool');
            
            selectedWords.forEach(item => {
                list.innerHTML += `<div class="word-item" id="li-${item.w}">${item.w} <span>❓</span></div>`;
            });

            let allSyllables = [];
            selectedWords.forEach(item => {
                item.p.forEach(s => allSyllables.push({t: s, w: item.w}));
            });
            allSyllables.sort(() => Math.random() - 0.5);

            allSyllables.forEach((s, i) => {
                const div = document.createElement('div');
                div.className = 'piece';
                div.textContent = s.t;
                div.dataset.owner = s.w;
                div.draggable = true;
                div.id = 's-' + i;
                div.ondragstart = (e) => { e.dataTransfer.setData('text', div.id); div.classList.add('dragging'); };
                div.ondragend = () => div.classList.remove('dragging');
                pool.appendChild(div);
            });
        }

        const dz = document.getElementById('drop-zone');
        dz.ondragover = (e) => e.preventDefault();
        dz.ondrop = (e) => {
            const id = e.dataTransfer.getData('text');
            const el = document.getElementById(id);
            if(el) {
                dz.appendChild(el);
                dz.classList.add('has-content');
                check();
            }
        };

        function check() {
            const items = Array.from(dz.children);
            const current = items.map(i => i.textContent).join('');
            const target = selectedWords.find(w => w.w === current);

            if (target) {
                items.forEach(i => i.classList.add('is-correct'));
                playSound(523, 0.5);
                confetti({ particleCount: 60, spread: 70, origin: { y: 0.7 } });
                
                const ab = document.getElementById('alert-box');
                ab.textContent = "¡Muy bien!"; ab.className = "bg-win show";
                setTimeout(() => ab.classList.remove('show'), 1000);

                setTimeout(() => {
                    dz.innerHTML = '';
                    dz.classList.remove('has-content');
                    document.getElementById(`li-${target.w}`).classList.add('done');
                    document.getElementById(`li-${target.w}`).querySelector('span').textContent = '✅';
                    score++;
                    document.getElementById('progress-fill').style.width = (score * 10) + '%';
                    
                    if (score === 5) { // Aparece el profesor a mitad de camino
                        document.getElementById('professor-pop').classList.add('active');
                        setTimeout(() => document.getElementById('professor-pop').classList.remove('active'), 3000);
                    }
                    
                    if (score === 10) win();
                }, 800);
            }
        }

        function clearWord() {
            Array.from(dz.children).forEach(i => document.getElementById('pool').appendChild(i));
            dz.classList.remove('has-content');
        }

        function win() {
            confetti({ particleCount: 200, spread: 100, origin: { y: 0.6 } });
            setTimeout(() => {
                document.getElementById('final-screen').classList.add('active');
                if ('speechSynthesis' in window) {
                    const u = new SpeechSynthesisUtterance("Te felicito, eres un experto en verduras.");
                    u.lang = 'es-ES'; window.speechSynthesis.speak(u);
                }
            }, 1000);
        }

        init();
    </script>
</body>
</html>
"""

components.html(html_huerto_premium_random, height=950, scrolling=False)
