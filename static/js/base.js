// Avisa cuando se pulsa un enlace de un módulo todavía no implementado.
const toastPendiente = document.getElementById('toast-pendiente');

document.querySelectorAll('[data-pendiente]').forEach((enlace) => {
  enlace.addEventListener('click', (evento) => {
    evento.preventDefault();
    toastPendiente.querySelector('.toast-body').textContent =
      `${enlace.dataset.pendiente}: esta sección estará disponible próximamente.`;
    bootstrap.Toast.getOrCreateInstance(toastPendiente).show();
  });
});
