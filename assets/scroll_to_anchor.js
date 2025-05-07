function scrollToAnchorFromHash() {
    if (window.location.hash) {
        var anchor = window.location.hash.substring(1);
        // Tenta encontrar o elemento repetidamente por até 2 segundos
        var attempts = 0;
        var maxAttempts = 40; // 40 tentativas (2 segundos se intervalo = 50ms)
        var interval = setInterval(function() {
            var el = document.getElementById(anchor);
            if (el) {
                el.scrollIntoView({behavior: "smooth", block: "center"});
                clearInterval(interval);
            }
            attempts += 1;
            if (attempts > maxAttempts) {
                clearInterval(interval);
            }
        }, 50);
    }
}

// Ao trocar de página no Dash, o evento 'hashchange' pode não ser disparado.
// Por isso, escutamos mudanças no pathname e hash.
window.addEventListener('hashchange', scrollToAnchorFromHash);
window.addEventListener('popstate', scrollToAnchorFromHash);

// Também tenta ao carregar a página
window.addEventListener('DOMContentLoaded', scrollToAnchorFromHash);

// E tenta novamente após cada atualização do layout do Dash
document.addEventListener('DOMContentLoaded', function() {
    // Dash dispara 'plotly_afterplot' após renderizar gráficos
    document.body.addEventListener('plotly_afterplot', scrollToAnchorFromHash);
});