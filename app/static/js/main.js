/* Conteúdo do arquivo main.js */
/*
document.getElementById("search-form").addEventListener("submit", function(event) {
    event.preventDefault();
    var searchInput = document.getElementById("search-input").value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/search", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            var resultado = response.resultado;
            document.getElementById("search-result").textContent = resultado;
        }
    };
    var data = "search=" + encodeURIComponent(searchInput);
    xhr.send(data);
});
document.getElementById('clear-button').addEventListener('click', function() {
    document.getElementById('search-input').value = '';
});

document.addEventListener('DOMContentLoaded', function() {
    var menuButton = document.querySelector('.menu-button');
    var menuItems = document.querySelector('.menu-items');

    menuButton.addEventListener('click', function() {
        menuItems.classList.toggle('show');
    });

});
*/
$(document).ready(function(){
    $("#filtro").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#tabela-corpo tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
    
    // Function to handle the "Cadastrar" button click event
    $('#btnCadastrar').on('click', function() {
      // Show the modal when the button is clicked
      $('#cadastroModal').modal('show');
    });
  
    // Handle the "Salvar" button click event in the modal
    $('#btnSalvar').on('click', function() {
      var nomeArquivo = $('#nomeArquivo').val();
      // Here you can handle the saving of the data, such as adding it to the 'dados' array.
      // For now, let's just print the entered data.
      console.log("Nome do Arquivo:", nomeArquivo);
      
      // Close the modal after saving
     // $('#cadastroModal').modal('hide');
    });
});
      $(document).ready(function () {
        document
          .getElementById("clear-button")
          .addEventListener("click", function () {
            document.getElementById("search-input").value = "";
          });

        $("#search-form").submit(function (event) {
          event.preventDefault();

          let pesquisa = $("#search-input").val();
          // Impedir o envio padrão do formulário
          if (pesquisa == "") {
            alert("Informe o tipo de pesquisa.");
          } else {
            let dados = {
              pesquisa: pesquisa,
            };

            $("#loading").removeClass("d-none");
            // Enviar uma requisição AJAX
            $.ajax({
              type: "POST",
              url: "http://127.0.0.1:5000/pesquisar",
              contentType: "application/json",
              data: JSON.stringify(dados),
              success: function (response) {
                $("#loading").addClass("d-none");

                // Manipular a resposta do servidor
                let html = "";
                
                html += '<div class="card mt-3">';
                  html += `<div class="card-header">${pesquisa}</div>`
                  html += '<div class="card-body">';
                    html += response;
                  html += '</div>';
                html += '</div>';
                $("#historico").prepend(html);
                $("#search-input").val("");
                pesquisa = "";
              },
              error: function () {
                $("#historico").html("Ocorreu um erro na requisição.");
              },
            });
          }
        });
      });