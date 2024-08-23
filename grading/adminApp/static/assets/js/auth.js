document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            if (this.checked) {
                checkboxes.forEach(function (cb) {
                    if (cb !== this) {
                        cb.checked = false;
                    }
                }, this);
            }
        });
    });




    var page = 0
    var nextButton = document.getElementById('button_next_step');
    nextButton.addEventListener('click', function () {
        page++
        console.log(page);
        if (page == 1) {

            sendAjaxRequestPageSelect();

        }

        if (page == 2) {
            var checkboxes = document.querySelectorAll('input[name="role"]');
            var selectedValues = [];

            checkboxes.forEach(function (checkbox) {
                if (checkbox.checked) {
                    selectedValues.push(checkbox.value);

                    sendAjaxRequestPagePricing(selectedValues);

                }
            });
        }

        if (page == 3) {
            var checkboxes = document.querySelectorAll('input[name="pricing"]');
            var selectedValues = [];

            checkboxes.forEach(function (checkbox) {
                if (checkbox.checked) {
                    selectedValues.push(checkbox.value);

                    sendAjaxRequestPageRegister(selectedValues);

                }
            });
        }

    });

    var previousButton = document.getElementById('button_previous_step');
    previousButton.addEventListener('click', function () {
        page--
        console.log(page);
        if (page == 1 || 2 || 3) {

            sendAjaxRequestPageSelect();

        }

    });



    var formData = new FormData();
    function sendAjaxRequestPageSelect() {
        var formData = new FormData();

        fetch("/dashboard/registration/select", {
            method: 'POST',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        })
            .then(response => response.text())
            .then(data => {
                document.getElementById('contant').innerHTML = data;
                document.getElementById('button_previous_step').style.display = 'none';
                document.getElementById('button_next_step').style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }


    function sendAjaxRequestPagePricing(selectedValue) {
        formData.append("role_id", selectedValue);

        fetch("/dashboard/registration/pricing/" + selectedValue, {
            method: 'POST',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        })
            .then(response => response.text())
            .then(data => {
                document.getElementById('contant').innerHTML = data;
                document.getElementById('button_previous_step').style.display = 'block';
                document.getElementById('button_next_step').style.display = 'block';
                
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function sendAjaxRequestPageRegister(selectedValue) {
        
        formData.append("subscriptionInfo_id", selectedValue)
        fetch(`/dashboard/register?subscriptionInfo_id=${selectedValue}`, {
            method: 'GET',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById('contant').innerHTML = data;
            document.getElementById('button_previous_step').style.display = 'none';
            document.getElementById('button_next_step').style.display = 'none';
            document.getElementById('form_role_id').value = formData.get('role_id');
            document.getElementById('form_subscriptionInfo_id').value = formData.get('subscriptionInfo_id');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});