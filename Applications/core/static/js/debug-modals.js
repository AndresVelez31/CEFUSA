console.log('🔍 DEBUG: Verificando estado inicial de modales');

document.addEventListener('DOMContentLoaded', () => {
    const modals = [
        'usernameModal',
        'emailModal', 
        'resetPasswordModal',
        'successResetModal'
    ];
    
    console.log('='.repeat(60));
    console.log('Estado de modales al cargar la página:');
    console.log('='.repeat(60));
    
    modals.forEach(modalId => {
        const modal = document.getElementById(modalId);
        if (modal) {
            const styles = window.getComputedStyle(modal);
            console.log(`\n${modalId}:`);
            console.log(`  - display: ${styles.display}`);
            console.log(`  - visibility: ${styles.visibility}`);
            console.log(`  - opacity: ${styles.opacity}`);
            console.log(`  - tiene clase 'show': ${modal.classList.contains('show')}`);
        } else {
            console.error(`❌ Modal ${modalId} no encontrado`);
        }
    });
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ Si todos los modales tienen display: none, está correcto');
    console.log('❌ Si alguno tiene display: flex, hay un problema');
    console.log('='.repeat(60));
});
