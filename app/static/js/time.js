// Função para fechar a mensagem
function closeMessage() {
    var flashMessage = document.getElementById('flash-message');
    flashMessage.style.display = 'none';
  }

  // Fecha automaticamente após 5 segundos
  setTimeout(function () {
    closeMessage();
  }, 5000); // 5000 milissegundos = 5 segundos

  // Associar função de fechar ao botão
  var closeButton = document.getElementById('close-button');
  closeButton.addEventListener('click', closeMessage);
