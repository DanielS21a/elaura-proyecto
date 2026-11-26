// Filtra las habitaciones en el navegador por número, estado y orientación.
const filtros = document.getElementById('filtros');

if (filtros) {
  const numero = document.getElementById('filtro-numero');
  const estado = document.getElementById('filtro-estado');
  const orientacion = document.getElementById('filtro-orientacion');
  const fichas = document.querySelectorAll('#habitaciones > li');
  const sinResultados = document.getElementById('sin-resultados');

  const filtrar = () => {
    let visibles = 0;
    fichas.forEach((ficha) => {
      const coincide =
        ficha.dataset.numero.includes(numero.value.trim()) &&
        (!estado.value || ficha.dataset.estado === estado.value) &&
        (!orientacion.value || ficha.dataset.orientacion === orientacion.value);
      ficha.hidden = !coincide;
      if (coincide) visibles += 1;
    });
    sinResultados.hidden = visibles > 0;
  };

  filtros.addEventListener('input', filtrar);
  filtros.addEventListener('submit', (evento) => evento.preventDefault());
}
