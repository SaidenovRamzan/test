$(document).ready(function() {
    const $loginButton = $(".btn-default");

    if ($loginButton.length) {
        $loginButton.on("click", async function(event) {
            const username = $("#id_username").val();
            const password = $("#id_password").val();

            const userData = {
                username: username,
                password: password,
            };

            try {
                const response = await $.ajax({
                    url: '/api/login',
                    method: 'POST',
                    data: JSON.stringify(userData),
                    contentType: 'application/json',
                });

                if (response.token.length > 0) {
                    localStorage.setItem('Token', response.token)
                    console.log('Authentication successful:', response);
                } else {
                    console.log(userData)
                    event
                    console.error('Authentication failed:', response.statusText);
                }
            } catch (error) {
                console.error('Network error:', error);
            }
        });
    }
});