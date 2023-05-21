window.onload = function() {

  document.getElementById("result_request").addEventListener("click", function() {
      let input = document.querySelector('#input_text');
      let label = $('input[name="btnradio"]:checked').attr('id');

      // создаем объект с данными для отправки
      let data = { text: input.value };

      let spinner = document.querySelector('.spinner-border');
  
      // показываем спиннер
      spinner.hidden = false;
      document.querySelector('#result_show').innerText = '';

      let spinnerTimeout = setTimeout(() => {
        spinner.hidden = true;
    
        // отправляем POST запрос на сервер
        fetch(`/${label}/process/`, {
          method: 'POST',
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response => response.json())
        .then(data => {
          // выводим результат на странице
          let result;
          if (data.result === 'attack') {
            result = 'Существует';
            document.querySelector('#result_show').classList.add('text-danger');
          } else if (data.result === 'neutral') {
            result = 'Не существует';
            document.querySelector('#result_show').classList.add('text-success');
          } else {
            result = 'Ошибка';
            document.querySelector('#result_show').classList.add('text-warning');
          }
          document.querySelector('#result_show').innerText = result;
        })
        .catch(error => console.error(error));
      }, 750);    
  });

const retreainButtons = document.querySelectorAll('.btn-group .btn');

retreainButtons.forEach((button) => {
  button.addEventListener('click', () => {
    let model_label = $('input[name="btnradio"]:checked').attr('id');
    let label = button.getAttribute('id');
    let input = document.querySelector('#input_text').value;
    let data = { text: input, label: label };

    fetch(`/${model_label}/retrain/ `, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        document.querySelector('.retrain_result').innerText = data.result;
      })
      .catch(error => console.error(error));
  });
});
};