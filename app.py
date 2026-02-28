import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Huerto de Palabras", layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 0rem; }
    iframe { border: none; }
    </style>
    """, unsafe_allow_html=True)

html_huerto_aleatorio = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --farm-green: #2d6a4f;
            --farm-light: #d8f3dc;
            --carrot-orange: #fb8500;
            --accent: #7209b7;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body {
            font-family: 'Quicksand', sans-serif;
            background: #fdfae5;
            display: flex; flex-direction: column; align-items: center;
            padding-top: 60px; min-height: 100vh;
        }
        header { text-align: center; margin-bottom: 20px; }
        h1 { font-family: 'Fredoka', sans-serif; color: var(--farm-green); font-size: 2.5rem; }
        
        .main-layout {
            display: grid; grid-template-columns: 260px 1fr;
            gap: 20px; width: 95%; max-width: 1100px;
        }
        
        .sidebar {
            background: white; padding: 20px; border-radius: 20px;
            border: 3px solid var(--farm-light); height: fit-content;
        }
        .word-item {
            padding: 8px; margin: 5px 0; border-radius: 10px;
            background: #f9fbf9; font-weight: bold; color: #444;
            display: flex; justify-content: space-between;
        }
        .word-item.done { background: #e8f5e9; color: #2e7d32; text-decoration: line-through; }

        .game-zone { display: flex; flex-direction: column; gap: 20px; }
        .drop-box {
            background: white; border: 4px dashed var(--farm-green);
            border-radius: 20px; min-height: 120px; display: flex;
            justify-content: center; align-items: center; gap: 10px; padding: 20px;
        }
        .pool {
            background: rgba(255,255,255,0.5); border-radius: 20px;
            padding: 20px; display: flex; flex-wrap: wrap; gap: 10px;
            justify-content: center; min-height: 200px;
        }
        .piece {
            background: white; border: 2px solid #ddd; border-bottom: 5px solid #ccc;
            border-radius: 12px; padding: 10px 20px; font-size: 1.2rem;
            cursor: grab; font-family: 'Fredoka', sans-serif;
        }
        .piece.dragging { opacity: 0.3; }
        .piece.correct { background: #4caf50; color: white; border-color: #2e7d32; }

        #win-modal {
            position: fixed; inset: 0; background: white;
            display: none; flex-direction: column; align-items: center;
            justify-content: center; z-index: 100; text-align: center;
        }
        #win-modal.active { display: flex; }
        .btn {
            background: var(--carrot-orange); color: white; border: none;
            padding: 15px 30px; border-radius: 50px; font-size: 1.5rem;
            cursor: pointer; margin-top: 20px; font-family: 'Fredoka', sans-serif;
        }
    </style>
</head>
<body>

    <header>
        <h1>Juego del Huerto</h1>
        <p style="color: var(--accent); font-weight: bold;">Pau Spanish Teacher</p>
    </header>

    <div class="main-layout">
        <div class="sidebar">
            <h3 style="margin-bottom:10px; color: var(--farm-green)">Lista de hoy:</h3>
            <div id="list-container"></div>
        </div>
        <div class="game-zone">
            <div class="drop-box" id="drop-zone"></div>
            <div style="text-align:center"><button onclick="clearDrop()" style="cursor:pointer; padding:5px 15px; border-radius:10px; border:1px solid #ccc;">Reiniciar palabra</button></div>
            <div class="pool" id="pool"></div>
        </div>
    </div>

    <div id="win-modal">
        <h1 style="font-size: 4rem;">🥕🥦🍅</h1>
        <h1>¡Fantástico!</h1>
        <p>Has completado las verduras de esta ronda.</p>
        <button class="btn" onclick="location.reload()">Jugar con palabras nuevas</button>
    </div>

    <script>
        // BANCO GRANDE DE PALABRAS (25 verduras)
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
            { w: "rápano", p: ["rá", "ba", "no"] },
            { w: "apio", p: ["a", "pio"] },
            { w: "coliflor", p: ["co", "li", "flor"] },
            { w: "betabel", p: ["be", "ta", "bel"] },
            { w: "hongo", p: ["hon", "go"] },
            { w: "espárrago", p: ["es", "pá", "rra", "go"] },
            { w: "ejote", p: ["e", "jo", "te"] },
            { w: "alcachofa", p: ["al", "ca", "cho", "fa"] },
            { w: "calabacín", p: ["ca", "la", "ba", "cín"] },
            { w: "perejil", p: ["pe", "re", "jil"] },
            { w: "puerro", p: ["pue", "rro"] },
            { w: "camote", p: ["ca", "mo", "te"] }
        ];

        let currentRoundWords = [];
        let completedCount = 0;

        function initRound() {
            // 1. Elegir 10 palabras al azar del banco de 25
            currentRoundWords = [...MASTER_BANK]
                .sort(() => Math.random() - 0.5)
                .slice(0, 10);

            const listCont = document.getElementById('list-container');
            const poolCont = document.getElementById('pool');
            
            // 2. Renderizar lista lateral
            currentRoundWords.forEach(item => {
                listCont.innerHTML += `<div class="word-item" id="li-${item.w}">${item.w} <span>❓</span></div>`;
            });

            // 3. Mezclar todas las sílabas de las 10 elegidas
            let syllables = [];
            currentRoundWords.forEach(item => {
                item.p.forEach(s => syllables.push({t: s, owner: item.w}));
            });
            syllables.sort(() => Math.random() - 0.5);

            syllables.forEach((s, i) => {
                const div = document.createElement('div');
                div.className = 'piece';
                div.textContent = s.t;
                div.dataset.owner = s.owner;
                div.draggable = true;
                div.id = 's-' + i;
                div.ondragstart = (e) => { e.dataTransfer.setData('text', div.id); div.classList.add('dragging'); };
                div.ondragend = () => div.classList.remove('dragging');
                poolCont.appendChild(div);
            });
        }

        const dz = document.getElementById('drop-zone');
        dz.ondragover = (e) => e.preventDefault();
        dz.ondrop = (e) => {
            const id = e.dataTransfer.getData('text');
            const el = document.getElementById(id);
            if(el) {
                dz.appendChild(el);
                checkWord();
            }
        };

        function checkWord() {
            const items = Array.from(dz.children);
            const str = items.map(i => i.textContent).join('');
            const target = currentRoundWords.find(w => w.w === str);

            if (target) {
                items.forEach(i => i.classList.add('correct'));
                confetti({ particleCount: 30, spread: 50, origin: { y: 0.8 } });
                
                setTimeout(() => {
                    dz.innerHTML = '';
                    document.getElementById(`li-${target.w}`).classList.add('done');
                    document.getElementById(`li-${target.w}`).querySelector('span').textContent = '✅';
                    completedCount++;
                    if(completedCount === 10) document.getElementById('win-modal').classList.add('active');
                }, 700);
            }
        }

        function clearDrop() {
            const items = Array.from(dz.children);
            items.forEach(i => document.getElementById('pool').appendChild(i));
        }

        initRound();
    </script>
</body>
</html>
"""

components.html(html_huerto_aleatorio, height=950, scrolling=False)
