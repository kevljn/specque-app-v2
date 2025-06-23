// Gestion des votes
document.addEventListener('DOMContentLoaded', function() {
    const votingForms = document.querySelectorAll('.voting form');
    
    votingForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const button = this.querySelector('button[type="submit"]');
            const originalText = button.textContent;
            
            try {
                button.disabled = true;
                button.textContent = 'Vote en cours...';
                
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.status === 'success') {
                        // Mettre à jour l'interface utilisateur
                        const allButtons = this.querySelectorAll('button');
                        allButtons.forEach(btn => {
                            btn.classList.remove('active');
                            if (btn === button) {
                                btn.classList.add('active');
                            }
                        });
                    }
                }
            } catch (error) {
                console.error('Erreur lors du vote:', error);
            } finally {
                button.disabled = false;
                button.textContent = originalText;
            }
        });
    });
});

// Gestion de l'éditeur de texte
document.addEventListener('DOMContentLoaded', function() {
    const textEditor = document.getElementById('content');
    if (textEditor) {
        // Ajouter des raccourcis Markdown
        textEditor.addEventListener('keydown', function(e) {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 'b':
                        e.preventDefault();
                        wrapSelection('**', '**');
                        break;
                    case 'i':
                        e.preventDefault();
                        wrapSelection('*', '*');
                        break;
                }
            }
        });
    }
});

// Fonction utilitaire pour envelopper la sélection
function wrapSelection(prefix, suffix) {
    const textarea = document.getElementById('content');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = textarea.value.substring(start, end);
    const replacement = prefix + selectedText + suffix;
    
    textarea.value = textarea.value.substring(0, start) + replacement + textarea.value.substring(end);
    textarea.selectionStart = start + prefix.length;
    textarea.selectionEnd = end + prefix.length;
    textarea.focus();
} 