document.addEventListener('DOMContentLoaded', () => {

    const petSelect = document.getElementById('petSelect');
    const dataInput = document.getElementById('agendamentoData');
    const horaInput = document.getElementById('agendamentoHora');

    const summaryPet = document.getElementById('summaryPet');
    const summaryDate = document.getElementById('summaryDate');
    const summaryHour = document.getElementById('summaryHour');

    const summaryServices = document.getElementById('summaryServices');
    const summaryTotal = document.getElementById('summaryTotal');

    const checkboxes = document.querySelectorAll(
        '.service-checkbox'
    );

    function atualizarResumo() {

        summaryPet.textContent =
            petSelect.options[
                petSelect.selectedIndex
            ]?.text || '---';

        summaryDate.textContent =
            dataInput.value || '---';

        summaryHour.textContent =
            horaInput.value || '---';

        summaryServices.innerHTML = '';

        let total = 0;

        checkboxes.forEach((checkbox) => {

            if (checkbox.checked) {

                const nome =
                    checkbox.dataset.name;

                const preco =
                    parseFloat(
                        checkbox.dataset.price
                    );

                total += preco;

                const li =
                    document.createElement('li');

                li.textContent =
                    `${nome} - R$ ${preco.toFixed(2)}`;

                summaryServices.appendChild(li);

            }

        });

        if (summaryServices.innerHTML === '') {

            summaryServices.innerHTML =
                '<li>Nenhum serviço selecionado</li>';
        }

        summaryTotal.textContent =
            `R$ ${total.toFixed(2).replace('.', ',')}`;
    }

    petSelect.addEventListener(
        'change',
        atualizarResumo
    );

    dataInput.addEventListener(
        'change',
        atualizarResumo
    );

    horaInput.addEventListener(
        'change',
        atualizarResumo
    );

    checkboxes.forEach((checkbox) => {

        checkbox.addEventListener(
            'change',
            atualizarResumo
        );

    });

});