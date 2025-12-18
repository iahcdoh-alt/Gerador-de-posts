// ========================================
// Instagram Post Generator - JavaScript
// Integrius Automações - 2025
// ========================================

// ===== THEME TOGGLE =====
const themeToggle = document.getElementById('themeToggle');
const body = document.body;
const themeIcon = document.querySelector('.theme-icon');
const themeText = document.querySelector('.theme-text');

// Carregar tema salvo
const savedTheme = localStorage.getItem('theme') || 'dark';
if (savedTheme === 'light') {
    body.classList.remove('dark-mode');
    themeIcon.textContent = '🌙';
    themeText.textContent = 'Modo Escuro';
} else {
    body.classList.add('dark-mode');
    themeIcon.textContent = '☀️';
    themeText.textContent = 'Modo Claro';
}

themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');

    if (body.classList.contains('dark-mode')) {
        themeIcon.textContent = '☀️';
        themeText.textContent = 'Modo Claro';
        localStorage.setItem('theme', 'dark');
    } else {
        themeIcon.textContent = '🌙';
        themeText.textContent = 'Modo Escuro';
        localStorage.setItem('theme', 'light');
    }
});

// ===== TABS =====
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const targetTab = button.dataset.tab;

        // Remove active class from all
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));

        // Add active to clicked
        button.classList.add('active');
        document.getElementById(targetTab).classList.add('active');
    });
});

// ===== FORM SUBMISSION - POST NORMAL =====
const formPostNormal = document.getElementById('formPostNormal');
const progressNormal = document.getElementById('progressNormal');
const imagePreviewNormal = document.getElementById('imagePreviewNormal');
const textResultNormal = document.getElementById('textResultNormal');

formPostNormal.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(formPostNormal);
    const data = {
        tipo_post: formData.get('tipo_post'),
        nicho: formData.get('nicho'),
        tema: formData.get('tema'),
        tom: formData.get('tom'),
        cta: formData.get('cta')
    };

    // Show progress
    progressNormal.style.display = 'block';
    formPostNormal.querySelector('button[type="submit"]').disabled = true;

    try {
        const response = await fetch('/api/gerar-post-normal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            // Exibir imagem
            imagePreviewNormal.innerHTML = `<img src="${result.imagem_url}" alt="Post gerado">`;

            // Exibir texto
            const textoCompleto = `${result.legenda}\n\n${result.hashtags.join(' ')}`;
            textResultNormal.value = textoCompleto;

            // Salvar URL da imagem para download
            imagePreviewNormal.dataset.imageUrl = result.imagem_url;

            alert('✅ Post gerado com sucesso!');
        } else {
            alert(`❌ Erro: ${result.erro}`);
        }
    } catch (error) {
        alert(`❌ Erro ao gerar post: ${error.message}`);
        console.error('Erro:', error);
    } finally {
        progressNormal.style.display = 'none';
        formPostNormal.querySelector('button[type="submit"]').disabled = false;
    }
});

// ===== FORM SUBMISSION - BOM DIA =====
const formBomDia = document.getElementById('formBomDia');
const progressBomDia = document.getElementById('progressBomDia');
const imagePreviewBomDia = document.getElementById('imagePreviewBomDia');
const textResultBomDia = document.getElementById('textResultBomDia');

formBomDia.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(formBomDia);
    const data = {
        categoria: formData.get('categoria'),
        subtema: formData.get('subtema') || ''
    };

    // Show progress
    progressBomDia.style.display = 'block';
    formBomDia.querySelector('button[type="submit"]').disabled = true;

    try {
        const response = await fetch('/api/gerar-bom-dia', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            // Exibir imagem
            imagePreviewBomDia.innerHTML = `<img src="${result.imagem_url}" alt="Bom dia gerado">`;

            // Exibir texto
            const textoCompleto = `${result.legenda}\n\n${result.hashtags.join(' ')}`;
            textResultBomDia.value = textoCompleto;

            // Salvar URL da imagem para download
            imagePreviewBomDia.dataset.imageUrl = result.imagem_url;

            alert('✅ Bom Dia Motivacional gerado com sucesso!');
        } else {
            alert(`❌ Erro: ${result.erro}`);
        }
    } catch (error) {
        alert(`❌ Erro ao gerar post: ${error.message}`);
        console.error('Erro:', error);
    } finally {
        progressBomDia.style.display = 'none';
        formBomDia.querySelector('button[type="submit"]').disabled = false;
    }
});

// ===== FORM SUBMISSION - POST DIVERSO =====
const formPostDiverso = document.getElementById('formPostDiverso');
const progressDiverso = document.getElementById('progressDiverso');
const imagePreviewDiverso = document.getElementById('imagePreviewDiverso');
const textResultDiverso = document.getElementById('textResultDiverso');

formPostDiverso.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(formPostDiverso);
    const data = {
        motivo: formData.get('motivo'),
        genero: formData.get('genero'),
        idade: parseInt(formData.get('idade')),
        personalidade: formData.get('personalidade'),
        mensagem_extra: formData.get('mensagem_extra') || ''
    };

    // Validação do motivo
    if (!data.motivo) {
        alert('⚠️ Por favor, selecione o motivo da comemoração!');
        return;
    }

    // Show progress
    progressDiverso.style.display = 'block';
    formPostDiverso.querySelector('button[type="submit"]').disabled = true;

    try {
        const response = await fetch('/api/gerar-post-diverso', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            // Exibir imagem
            imagePreviewDiverso.innerHTML = `<img src="${result.imagem_url}" alt="Card comemorativo">`;

            // Exibir mensagem
            textResultDiverso.value = result.legenda;

            // Salvar URL da imagem para download
            imagePreviewDiverso.dataset.imageUrl = result.imagem_url;

            alert('✅ Card comemorativo gerado com sucesso!');
        } else {
            alert(`❌ Erro: ${result.erro}`);
        }
    } catch (error) {
        alert(`❌ Erro ao gerar card: ${error.message}`);
        console.error('Erro:', error);
    } finally {
        progressDiverso.style.display = 'none';
        formPostDiverso.querySelector('button[type="submit"]').disabled = false;
    }
});

// ===== UTILITY FUNCTIONS =====
function copiarTexto(textareaId) {
    const textarea = document.getElementById(textareaId);

    if (!textarea.value || textarea.value === 'Aguardando geração...') {
        alert('⚠️ Nenhum texto para copiar!');
        return;
    }

    textarea.select();
    document.execCommand('copy');

    alert('📋 Texto copiado para área de transferência!');
}

function baixarImagem(previewId) {
    const preview = document.getElementById(previewId);
    const imageUrl = preview.dataset.imageUrl;

    if (!imageUrl) {
        alert('⚠️ Nenhuma imagem para baixar!');
        return;
    }

    // Criar link temporário e clicar
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = `instagram_post_${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    alert('💾 Download iniciado!');
}

// ===== VERIFICAR STATUS AO CARREGAR =====
window.addEventListener('load', async () => {
    try {
        const response = await fetch('/api/status');
        const status = await response.json();

        if (!status.openai_configurado) {
            alert('⚠️ AVISO: APIs não estão configuradas corretamente!');
        }
    } catch (error) {
        console.error('Erro ao verificar status:', error);
    }
});
