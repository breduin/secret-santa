/* Скрипт скрывает/показывает поля в форме создания/редактирования игры
*/
window.addEventListener("load", () => {            

   
    let costsLimitField = document.getElementById("id_your_gift_cost_limit");
    let placeField = document.getElementById("id_place");
     
    function setDisplayField(param, field) {
        if (param == 'none') {
            /* Устанавливается display: none; для родителя исключаемого поля, 
            т.е. для p-обёртки */
            field.parentNode.style.setProperty(
                    "display", "none", "important");
        }                    
        else
        {
            field.parentNode.style.removeProperty(
                    "display"
                    );
        }
        }

    /* проверка после загрузки формы */
    let costsChoiceField = document.getElementById("id_gift_cost_limit");
    let currentValue = costsChoiceField.value;
    if (currentValue != 'YOUR') {
        setDisplayField('none', costsLimitField);
    }

    let isOnlineField = document.getElementById("id_is_online");
    currentValue = isOnlineField.checked;
    if (currentValue) {
        setDisplayField('none', placeField);
    }

    /* показать/скрыть поле id_your_gift_cost_limit, если выбран/не выбран 
    "Указать свой лимит стоимости подарка" в поле id_gift_cost_limit*/
    costsChoiceField.addEventListener("change", (event) => {                
        choiceValue = event.target.value;

        if (choiceValue != 'YOUR' ) {                                       
            setDisplayField('none', costsLimitField);
        }
        else {
            setDisplayField('block', costsLimitField);
        }
    });

    /* показать/скрыть поле id_place, если выбран/не выбран 
    "Будет онлайн?" в поле id_is_online */
    isOnlineField.addEventListener("change", (event) => {                
        choiceValue = event.target.checked;
        if (choiceValue) {                                       
            setDisplayField('none', placeField);
        }
        else {
            setDisplayField('block', placeField);
        }
    });    

});
