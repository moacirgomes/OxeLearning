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